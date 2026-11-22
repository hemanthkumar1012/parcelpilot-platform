"""Pickup SLA and service-credit rules, decided in code.

Before this module the support agent received raw timestamps and fault flags and
decided on a breach by itself. That could not be tested and could change from one
model answer to the next. These functions make the decision; the agent only explains it.

Rules (from the policy documents the knowledge base quotes):
- Standard: a pickup qualifies for a service credit when it is more than 2 hours past
  the end of the pickup window, it is the carrier's fault and the customer is not at fault.
  The credit is the lower of INR 500 or 10% of the shipment fee.
- Northstar Logistics contract: more than 4 hours late, carrier fault, fixed INR 300 credit.
"""
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from decimal import ROUND_HALF_UP, Decimal

STANDARD_GRACE = timedelta(hours=2)
STANDARD_CREDIT_CAP = Decimal("500")
STANDARD_CREDIT_RATE = Decimal("0.10")
NORTHSTAR_GRACE = timedelta(hours=4)
NORTHSTAR_CREDIT = Decimal("300")


@dataclass(frozen=True)
class PickupAssessment:
    status: str                  # unknown, pending, on_time, late, breached
    picked_up: bool
    delay_minutes: int | None
    credit_eligible: bool
    credit_inr: str | None       # string so it serialises cleanly to JSON
    rule: str
    reason: str

    def to_dict(self) -> dict:
        return asdict(self)


def _as_utc(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    # SQLite returns naive datetimes; the app stores UTC.
    return value if value.tzinfo else value.replace(tzinfo=timezone.utc)


def _is_northstar(contract_file: str | None) -> bool:
    return bool(contract_file) and "northstar" in contract_file.lower()


def standard_credit(fee: Decimal | float | int | None) -> Decimal | None:
    if fee is None:
        return None
    ten_percent = (Decimal(str(fee)) * STANDARD_CREDIT_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return min(STANDARD_CREDIT_CAP, ten_percent)


def assess_pickup(
    window_end: datetime | None,
    picked_up_at: datetime | None,
    *,
    carrier_fault: bool,
    customer_fault: bool,
    fee: Decimal | float | int | None,
    contract_file: str | None = None,
    now: datetime | None = None,
) -> PickupAssessment:
    """Decide whether a pickup breached its SLA and whether a credit applies.

    A pickup exactly at the limit (for example exactly 2 hours late) is not a breach:
    the policy says "more than".
    """
    northstar = _is_northstar(contract_file)
    grace = NORTHSTAR_GRACE if northstar else STANDARD_GRACE
    rule = "northstar_contract" if northstar else "standard_policy"

    window_end = _as_utc(window_end)
    picked_up_at = _as_utc(picked_up_at)
    if window_end is None:
        return PickupAssessment("unknown", picked_up_at is not None, None, False, None, rule,
                                "No pickup window is recorded, so the SLA cannot be checked.")

    picked_up = picked_up_at is not None
    reference = picked_up_at if picked_up else (_as_utc(now) or datetime.now(timezone.utc))
    delay = reference - window_end

    if not picked_up and delay <= timedelta(0):
        return PickupAssessment("pending", False, None, False, None, rule,
                                "The pickup window has not ended yet.")

    delay_minutes = max(0, int(delay.total_seconds() // 60))
    if delay <= timedelta(0):
        return PickupAssessment("on_time", picked_up, 0, False, None, rule, "Picked up within the window.")
    if delay <= grace:
        return PickupAssessment("late", picked_up, delay_minutes, False, None, rule,
                                f"Late, but within the {int(grace.total_seconds() // 3600)}-hour limit.")

    # Breached from here on.
    if customer_fault:
        return PickupAssessment("breached", picked_up, delay_minutes, False, None, rule,
                                "The customer was at fault, so no credit applies.")
    if not carrier_fault:
        return PickupAssessment("breached", picked_up, delay_minutes, False, None, rule,
                                "The delay was not the carrier's fault, so no credit applies.")

    if northstar:
        credit = NORTHSTAR_CREDIT
    else:
        credit = standard_credit(fee)
        if credit is None:
            return PickupAssessment("breached", picked_up, delay_minutes, True, None, rule,
                                    "Credit applies, but the shipment fee is missing, so the amount needs a manual check.")
    return PickupAssessment("breached", picked_up, delay_minutes, True, f"{credit:.2f}", rule,
                            "Carrier fault beyond the limit, so a service credit applies.")
