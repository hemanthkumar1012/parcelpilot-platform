import json
from sqlalchemy.orm import Session
from app.db.models import User, Shipment, Order, SupportTicket, ShipmentTrackingEvent, AgentAction, CustomerAccount
from datetime import datetime, timezone
import uuid

def lookup_shipment(db: Session, tracking_id: str, current_user: User):
    shipment = db.query(Shipment).filter(Shipment.tracking_id == tracking_id).first()
    if not shipment:
        return {"error": "Shipment not found."}
    if current_user.role.value != "ADMIN" and shipment.account_id != current_user.account_id:
        return {"error": "Shipment not found or unauthorized."}
    
    return {
        "tracking_id": shipment.tracking_id,
        "status": shipment.current_status.value,
        "origin": shipment.origin,
        "destination": shipment.destination,
        "carrier": shipment.carrier,
        "estimated_delivery": str(shipment.estimated_delivery) if shipment.estimated_delivery else None
    }

def lookup_order(db: Session, order_id: str, current_user: User):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        return {"error": "Order not found."}
    if current_user.role.value != "ADMIN" and order.account_id != current_user.account_id:
        return {"error": "Order not found or unauthorized."}
    
    shipments = [{"tracking_id": s.tracking_id, "status": s.current_status.value} for s in order.shipments]
    return {
        "order_id": order.order_id,
        "shipments": shipments,
        "created_at": str(order.created_at)
    }

def get_tracking_history(db: Session, tracking_id: str, current_user: User):
    shipment = db.query(Shipment).filter(Shipment.tracking_id == tracking_id).first()
    if not shipment or (current_user.role.value != "ADMIN" and shipment.account_id != current_user.account_id):
        return {"error": "Shipment not found or unauthorized."}
    
    events = []
    for e in shipment.tracking_events:
        events.append({
            "status": e.status.value,
            "location": e.location,
            "description": e.description,
            "timestamp": str(e.created_at)
        })
    return {"tracking_id": tracking_id, "events": events}

def lookup_support_ticket(db: Session, ticket_id: str, current_user: User):
    ticket = db.query(SupportTicket).filter(SupportTicket.ticket_id == ticket_id).first()
    if not ticket:
        return {"error": "Ticket not found."}
    if current_user.role.value != "ADMIN" and ticket.account_id != current_user.account_id:
        return {"error": "Ticket not found or unauthorized."}
    
    return {
        "ticket_id": ticket.ticket_id,
        "status": ticket.status,
        "subject": ticket.subject,
        "priority": ticket.priority,
        "description": ticket.description,
        "created_at": str(ticket.created_at)
    }

def create_support_ticket(db: Session, subject: str, description: str, priority: str, current_user: User):
    if current_user.role.value == "GUEST":
        return {"error": "Guests cannot create support tickets."}
    if not current_user.account_id:
        return {"error": "User does not have an active account."}

    ticket_id = f"TKT-{uuid.uuid4().hex[:6].upper()}"
    ticket = SupportTicket(
        ticket_id=ticket_id,
        account_id=current_user.account_id,
        requester_id=current_user.id,
        subject=subject,
        description=description,
        priority=priority,
        status="open"
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return {"message": "Support ticket created successfully.", "ticket_id": ticket_id}

def shipment_sla_status(db: Session, tracking_id: str, current_user: User):
    shipment = db.query(Shipment).filter(Shipment.tracking_id == tracking_id).first()
    if not shipment or (current_user.role.value != "ADMIN" and shipment.account_id != current_user.account_id):
        return {"error": "Shipment not found or unauthorized."}
    
    account = db.query(CustomerAccount).filter(CustomerAccount.id == shipment.account_id).first()
    
    return {
        "tracking_id": shipment.tracking_id,
        "carrier": shipment.carrier,
        "pickup_window_end": str(shipment.pickup_window_end) if shipment.pickup_window_end else None,
        "pickup_actual_at": str(shipment.pickup_actual_at) if shipment.pickup_actual_at else None,
        "carrier_fault": shipment.carrier_fault,
        "customer_fault": shipment.customer_fault,
        "cancellation_requested_at": str(shipment.cancellation_requested_at) if shipment.cancellation_requested_at else None,
        "account_plan": account.plan if account else "Unknown",
        "contract_file": account.contract_file if account else "Unknown"
    }

def prepare_escalation(db: Session, ticket_id: str, reason: str, current_user: User):
    if current_user.role.value == "GUEST":
        return {"error": "Guests cannot prepare escalations."}
    
    ticket = db.query(SupportTicket).filter(SupportTicket.ticket_id == ticket_id).first()
    if not ticket or (current_user.role.value != "ADMIN" and ticket.account_id != current_user.account_id):
        return {"error": "Ticket not found or unauthorized."}

    action_id = f"ACT-{uuid.uuid4().hex[:6].upper()}"
    action = AgentAction(
        action_id=action_id,
        account_id=ticket.account_id,
        user_id=current_user.id,
        action_type="ESCALATION",
        reference_entity="SupportTicket",
        reference_id=ticket_id,
        status="pending",
        details=json.dumps({"reason": reason})
    )
    db.add(action)
    db.commit()
    return {"message": f"Escalation prepared. Please confirm action {action_id} to proceed.", "action_id": action_id}

def confirm_action(db: Session, action_id: str, confirmed: bool, current_user: User):
    if current_user.role.value == "GUEST":
        return {"error": "Guests cannot confirm actions."}
    
    action = db.query(AgentAction).filter(AgentAction.action_id == action_id, AgentAction.status == "pending").first()
    if not action or (current_user.role.value != "ADMIN" and action.account_id != current_user.account_id):
        return {"error": "Pending action not found or unauthorized."}

    if confirmed:
        action.status = "executed"
        action.executed_at = datetime.now(timezone.utc)
        msg = f"Action {action_id} executed successfully."
    else:
        action.status = "cancelled"
        msg = f"Action {action_id} cancelled."
    
    db.commit()
    return {"message": msg}

def knowledge_search(db: Session, query: str, current_user: User):
    query_lower = query.lower()
    results = []
    
    if "escalation" in query_lower or "severity" in query_lower or "sla" in query_lower:
        results.append({
            "source": "01_Support_Policy_v3_CURRENT.pdf",
            "content": "Enterprise Plan targets: P1 - 30 minutes, 24x7. P2 - 2 hours. P3 - 1 business day. Growth Plan targets: P1 - 2 business hours, P2 - 4 business hours. Standard Plan targets: P1 - 4 business hours, P2 - 1 business day, P3 - 2 business days. If target is breached, escalate immediately."
        })
    if "credit" in query_lower or "late" in query_lower or "pickup" in query_lower:
        results.append({
            "source": "03_Cancellation_and_Service_Credit_SOP_v4.pdf",
            "content": "A shipment qualifies for a service credit if the pickup is delayed by more than 2 hours past the window end, it is carrier fault, and there is no customer fault. Credit is the lower of INR 500 or 10% of the shipment fee."
        })
    if current_user.account and current_user.account.contract_file:
        if "northstar" in query_lower and "Northstar" in current_user.account.contract_file:
            results.append({
                "source": "05_Northstar_Logistics_Enterprise_Agreement.pdf",
                "content": "Northstar Logistics custom agreement: If delayed > 4 hours due to carrier fault, fixed INR 300 credit applies."
            })
        if "lumenworks" in query_lower and "LumenWorks" in current_user.account.contract_file:
            results.append({
                "source": "06_LumenWorks_Service_Agreement.pdf",
                "content": "LumenWorks custom agreement: Apply standard SLA but expedite P1."
            })
            
    if "swiftship" in query_lower or "webhook" in query_lower:
        results.append({
            "source": "04_Product_Operations_Guide_and_Known_Issues.pdf",
            "content": "SwiftShip pickup confirmation webhooks can arrive up to 20 minutes late. Verify carrier status or wait through the delay window before telling the customer the pickup failed."
        })
        
    if not results:
        results.append({
            "source": "General Knowledge Base",
            "content": "No specific SLA clauses found for this query. Refer to standard terms."
        })
        
    return {"results": results}
