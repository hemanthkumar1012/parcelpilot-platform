from app.db import models
from app.tools import agent_tools


def make_user(db, name, email, account):
    user = models.User(
        name=name,
        email=email,
        hashed_password="not-used-in-tool-test",
        role=models.Role.CUSTOMER,
        account_id=account.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_agent_tools_enforce_tenant_isolation(db_session):
    account1 = models.CustomerAccount(name="Account One", plan="Standard")
    account2 = models.CustomerAccount(name="Account Two", plan="Standard")
    db_session.add_all([account1, account2])
    db_session.commit()

    user1 = make_user(db_session, "U1", "u1@tools.test", account1)
    user2 = make_user(db_session, "U2", "u2@tools.test", account2)

    shipment = models.Shipment(
        tracking_id="PP-TOOLS-1",
        customer_id=user1.id,
        account_id=account1.id,
        sender_name="A",
        receiver_name="B",
        origin="HYD",
        destination="BLR",
    )
    db_session.add(shipment)
    db_session.commit()

    own = agent_tools.lookup_shipment(db_session, "PP-TOOLS-1", user1)
    other = agent_tools.lookup_shipment(db_session, "PP-TOOLS-1", user2)

    assert own["tracking_id"] == "PP-TOOLS-1"
    assert "error" in other


def test_prepare_and_confirm_action_requires_authorization(db_session):
    account = models.CustomerAccount(name="Action Account", plan="Standard")
    db_session.add(account)
    db_session.commit()

    user = make_user(db_session, "Action User", "action@tools.test", account)

    ticket = models.SupportTicket(
        ticket_id="TKT-TOOLS1",
        account_id=account.id,
        requester_id=user.id,
        subject="Late shipment",
        description="Shipment is late",
        priority="P2",
    )
    db_session.add(ticket)
    db_session.commit()

    prepared = agent_tools.prepare_escalation(
        db_session,
        "TKT-TOOLS1",
        "SLA breach",
        user,
    )
    assert prepared["action_id"].startswith("ACT-")

    confirmed = agent_tools.confirm_action(
        db_session,
        prepared["action_id"],
        True,
        user,
    )
    assert "executed successfully" in confirmed["message"]

    action = (
        db_session.query(models.AgentAction)
        .filter_by(action_id=prepared["action_id"])
        .first()
    )
    assert action.status == "executed"
    assert action.executed_at is not None


def test_guest_cannot_create_or_confirm_actions(db_session):
    account = models.CustomerAccount(name="Guest Account", plan="Standard")
    db_session.add(account)
    db_session.commit()

    guest = models.User(
        name="Guest",
        email="guest@tools.test",
        hashed_password="unused",
        role=models.Role.GUEST,
        account_id=account.id,
    )
    db_session.add(guest)
    db_session.commit()

    ticket_result = agent_tools.create_support_ticket(
        db_session,
        "Subject",
        "Description",
        "P2",
        guest,
    )
    assert "error" in ticket_result

    action_result = agent_tools.confirm_action(
        db_session,
        "ACT-NOT-FOUND",
        True,
        guest,
    )
    assert "error" in action_result
