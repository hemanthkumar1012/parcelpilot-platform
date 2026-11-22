"""Unsupported answers, failed dependencies and the SLA tool, with the LLM mocked."""
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from types import SimpleNamespace

from app.db import models
from app.services import ai
from app.tools import agent_tools


def make_account_user(db, plan="Standard", contract=None):
    account = models.CustomerAccount(name="Acme", plan=plan, contract_file=contract)
    db.add(account)
    db.commit()
    db.refresh(account)
    user = models.User(name="Asha", email=f"asha{account.id}@example.com", hashed_password="x",
                       role=models.Role.CUSTOMER, account_id=account.id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return account, user


# ---- unsupported answers ----------------------------------------------------------

def test_knowledge_search_says_unsupported_when_no_policy_matches(db_session):
    _, user = make_account_user(db_session)
    result = agent_tools.knowledge_search(db_session, "refund for a lost laptop charger", user)
    assert result["supported"] is False
    assert result["results"] == []
    assert "do not have" in result["message"]


def test_knowledge_search_marks_matching_policy_as_supported(db_session):
    _, user = make_account_user(db_session)
    result = agent_tools.knowledge_search(db_session, "late pickup credit", user)
    assert result["supported"] is True
    assert result["results"]


def test_contract_policy_is_hidden_from_other_accounts(db_session):
    _, user = make_account_user(db_session, contract=None)
    result = agent_tools.knowledge_search(db_session, "northstar credit", user)
    sources = [r["source"] for r in result["results"]]
    assert not any("Northstar" in s for s in sources)


# ---- SLA tool uses the deterministic calculator -----------------------------------

def test_sla_tool_returns_computed_assessment(db_session):
    account, user = make_account_user(db_session)
    end = datetime(2026, 11, 20, 12, 0, tzinfo=timezone.utc)
    shipment = models.Shipment(
        tracking_id="PP-SLA-1", customer_id=user.id, account_id=account.id,
        sender_name="A", receiver_name="B", origin="Hyderabad", destination="Chennai",
        pickup_window_end=end, pickup_actual_at=end + timedelta(minutes=125),
        shipment_fee=Decimal("1500"), carrier_fault=True, customer_fault=False,
    )
    db_session.add(shipment)
    db_session.commit()

    result = agent_tools.shipment_sla_status(db_session, "PP-SLA-1", user)
    assert result["assessment"]["status"] == "breached"
    assert result["assessment"]["credit_inr"] == "150.00"


# ---- failed dependencies ------------------------------------------------------------

class _FailingCompletions:
    def create(self, **kwargs):
        raise TimeoutError("upstream timed out")


class _FailingClient:
    api_key = "real-looking-key"
    chat = SimpleNamespace(completions=_FailingCompletions())


def test_llm_timeout_returns_safe_message(db_session, monkeypatch):
    _, user = make_account_user(db_session)
    monkeypatch.setattr(ai, "get_openai_client", lambda: _FailingClient())

    reply, conv_id = ai.process_chat(db_session, user, None, "Where is my parcel?")

    assert reply == ai.AI_UNAVAILABLE_MESSAGE
    assert "timed out" not in reply          # provider error text is not shown to the user
    saved = db_session.query(models.ConversationMessage).filter_by(conversation_id=conv_id, role="assistant").all()
    assert saved and saved[-1].content == ai.AI_UNAVAILABLE_MESSAGE


def _tool_call(name, arguments):
    return SimpleNamespace(
        id="call_1",
        function=SimpleNamespace(name=name, arguments=arguments),
        model_dump=lambda: {"id": "call_1", "type": "function",
                            "function": {"name": name, "arguments": arguments}},
    )


class _ToolThenAnswerCompletions:
    def __init__(self):
        self.calls = 0
        self.seen_messages = None

    def create(self, **kwargs):
        self.calls += 1
        if self.calls == 1:
            message = SimpleNamespace(content="", tool_calls=[_tool_call("lookup_shipment", '{"tracking_id": "PP-1"}')])
        else:
            self.seen_messages = kwargs["messages"]
            message = SimpleNamespace(content="Sorry, I cannot check that right now.", tool_calls=None)
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])


def test_failed_tool_lookup_does_not_crash_chat(db_session, monkeypatch):
    _, user = make_account_user(db_session)
    completions = _ToolThenAnswerCompletions()
    client = SimpleNamespace(api_key="real-looking-key", chat=SimpleNamespace(completions=completions))
    monkeypatch.setattr(ai, "get_openai_client", lambda: client)

    def broken_lookup(*args, **kwargs):
        raise RuntimeError("database connection lost")

    monkeypatch.setattr(agent_tools, "lookup_shipment", broken_lookup)

    reply, _ = ai.process_chat(db_session, user, None, "Where is PP-1?")

    assert reply == "Sorry, I cannot check that right now."
    tool_messages = [m for m in completions.seen_messages if isinstance(m, dict) and m.get("role") == "tool"]
    assert "unavailable" in tool_messages[0]["content"]
    assert "database connection lost" not in tool_messages[0]["content"]


def test_readiness_returns_503_when_database_fails(client, db_session, monkeypatch):
    def broken_execute(*args, **kwargs):
        raise RuntimeError("database down")

    monkeypatch.setattr(db_session, "execute", broken_execute)
    response = client.get("/ready")
    assert response.status_code == 503
