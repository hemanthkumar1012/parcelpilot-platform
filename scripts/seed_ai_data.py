from app.db.database import SessionLocal, Base, engine
from app.db.models import CustomerAccount, User, Role, Shipment, ShipmentStatus, SupportTicket, ShipmentTrackingEvent
from app.core.security import get_password_hash

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Create Accounts
    acct1 = CustomerAccount(name="Northstar Logistics", plan="Enterprise", contract_file="05_Northstar_Logistics_Enterprise_Agreement.pdf", premium_support=True)
    acct2 = CustomerAccount(name="LumenWorks", plan="Growth", contract_file="06_LumenWorks_Service_Agreement.pdf", premium_support=False)
    
    db.add(acct1)
    db.add(acct2)
    db.commit()
    db.refresh(acct1)
    db.refresh(acct2)

    # Create Users
    u1 = User(account_id=acct1.id, name="Northstar Admin", email="admin@northstar.com", hashed_password=get_password_hash("password"), role=Role.CUSTOMER)
    u2 = User(account_id=acct2.id, name="LumenWorks Admin", email="admin@lumenworks.com", hashed_password=get_password_hash("password"), role=Role.CUSTOMER)
    
    db.add(u1)
    db.add(u2)
    db.commit()
    db.refresh(u1)
    db.refresh(u2)

    # Create Shipments (Orders in AI DB)
    s1 = Shipment(tracking_id="ORD-1001", customer_id=u1.id, account_id=acct1.id, sender_name="Northstar", receiver_name="Customer", origin="Warehouse A", destination="Store 1", current_status=ShipmentStatus.CREATED, carrier="SwiftShip", shipment_fee=4200.0, carrier_fault=False, customer_fault=False)
    s2 = Shipment(tracking_id="ORD-1002", customer_id=u1.id, account_id=acct1.id, sender_name="Northstar", receiver_name="Customer", origin="Warehouse B", destination="Store 2", current_status=ShipmentStatus.PICKED_UP, carrier="BlueDart Pro", shipment_fee=5100.0, carrier_fault=False, customer_fault=False)
    
    db.add(s1)
    db.add(s2)
    db.commit()
    db.refresh(s1)
    db.refresh(s2)
    
    # Tracking Events
    db.add(ShipmentTrackingEvent(shipment_id=s2.id, status=ShipmentStatus.CREATED, description="Shipment created", location="Warehouse B"))
    db.add(ShipmentTrackingEvent(shipment_id=s2.id, status=ShipmentStatus.PICKED_UP, description="Picked up by carrier", location="Warehouse B"))
    db.commit()

    # Support Tickets
    t1 = SupportTicket(ticket_id="TKT-501", account_id=acct1.id, requester_id=u1.id, status="open", subject="All shipment creation is failing", description="Every user at Northstar gets HTTP 500 when creating any shipment.", priority="P1")
    t2 = SupportTicket(ticket_id="TKT-502", account_id=acct2.id, requester_id=u2.id, status="open", subject="Bulk upload fails for 4,200-row CSV", description="The CSV reaches roughly 70% and fails.", priority="P2")
    
    db.add(t1)
    db.add(t2)
    db.commit()

    print("Demo data seeded successfully.")

if __name__ == "__main__":
    seed()
