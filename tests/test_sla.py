"""Boundary tests for the pickup SLA and service-credit rules (app/services/sla.py)."""
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from app.services.sla import assess_pickup, standard_credit

WINDOW_END = datetime(2026, 11, 20, 12, 0, tzinfo=timezone.utc)


def at(minutes_late: int) -> datetime:
    return WINDOW_END + timedelta(minutes=minutes_late)


def assess(minutes_late, carrier_fault=True, customer_fault=False, fee=Decimal("2000"), contract=None, now=None):
    picked = at(minutes_late) if minutes_late is not None else None
    return assess_pickup(WINDOW_END, picked, carrier_fault=carrier_fault, customer_fault=customer_fault,
                         fee=fee, contract_file=contract, now=now)


def test_exactly_two_hours_late_is_not_a_breach():
    result = assess(120)
    assert result.status == "late"
    assert result.credit_eligible is False


def test_one_minute_past_two_hours_is_a_breach_with_credit():
    result = assess(121)
    assert result.status == "breached"
    assert result.credit_eligible is True
    assert result.credit_inr == "200.00"   # 10% of 2000


def test_on_time_and_early_pickups():
    assert assess(0).status == "on_time"
    assert assess(-15).status == "on_time"


def test_credit_is_capped_at_500():
    assert assess(180, fee=Decimal("9000")).credit_inr == "500.00"


def test_customer_fault_blocks_credit():
    result = assess(300, customer_fault=True)
    assert result.status == "breached"
    assert result.credit_eligible is False


def test_no_carrier_fault_means_no_credit():
    result = assess(300, carrier_fault=False)
    assert result.status == "breached"
    assert result.credit_eligible is False


def test_missing_fee_needs_manual_check():
    result = assess(300, fee=None)
    assert result.credit_eligible is True
    assert result.credit_inr is None


def test_northstar_contract_uses_four_hours_and_fixed_credit():
    contract = "05_Northstar_Logistics_Enterprise_Agreement.pdf"
    assert assess(240, contract=contract).status == "late"        # exactly 4 hours
    result = assess(241, contract=contract)
    assert result.status == "breached"
    assert result.credit_inr == "300.00"
    assert result.rule == "northstar_contract"


def test_not_picked_up_yet_inside_window_is_pending():
    result = assess(None, now=at(-30))
    assert result.status == "pending"


def test_not_picked_up_and_overdue_counts_from_now():
    result = assess(None, now=at(150))
    assert result.status == "breached"
    assert result.picked_up is False
    assert result.delay_minutes == 150


def test_missing_window_is_unknown():
    result = assess_pickup(None, at(10), carrier_fault=True, customer_fault=False, fee=100)
    assert result.status == "unknown"


def test_naive_datetimes_from_sqlite_are_treated_as_utc():
    naive_end = WINDOW_END.replace(tzinfo=None)
    naive_pick = at(121).replace(tzinfo=None)
    result = assess_pickup(naive_end, naive_pick, carrier_fault=True, customer_fault=False, fee=1000)
    assert result.status == "breached"


@pytest.mark.parametrize("fee, expected", [(0, Decimal("0.00")), (1234.5, Decimal("123.45")), (5000, Decimal("500"))])
def test_standard_credit_rounding(fee, expected):
    assert standard_credit(fee) == expected
