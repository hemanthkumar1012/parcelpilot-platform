import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# Get Demo Account ID and a customer_id
cursor.execute("SELECT id FROM customer_accounts WHERE name = 'Demo Account'")
res = cursor.fetchone()
if not res:
    print("No Demo Account found. Creating one.")
    cursor.execute("INSERT INTO customer_accounts (name, plan) VALUES ('Demo Account', 'Standard')")
    account_id = cursor.lastrowid
else:
    account_id = res[0]

cursor.execute("SELECT id FROM users LIMIT 1")
customer_id = cursor.fetchone()[0]

# Generate shipments
shipments = [
    ("PP-DEMO-2001", "Acme Corp", "Tech Solutions", "Mumbai", "Delhi", "IN_TRANSIT", 1, 0, 0),
    ("PP-DEMO-2002", "Acme Corp", "Design Studio", "Chennai", "Kolkata", "DELIVERED", -2, 0, 0),
    ("PP-DEMO-2003", "Acme Corp", "Retail Hub", "Pune", "Ahmedabad", "IN_TRANSIT", 2, 0, 0),
    ("PP-DEMO-2004", "Acme Corp", "Global Export", "Bangalore", "Hyderabad", "DELIVERED", -5, 0, 0),
    ("PP-DEMO-2005", "Acme Corp", "Medical Supply", "Delhi", "Chandigarh", "FAILED", 0, 1, 0),
    ("PP-DEMO-2006", "Acme Corp", "Book Store", "Jaipur", "Lucknow", "IN_TRANSIT", 3, 0, 0),
    ("PP-DEMO-2007", "Acme Corp", "Fashion Outlet", "Mumbai", "Pune", "DELIVERED", -1, 0, 0),
    ("PP-DEMO-2008", "Acme Corp", "Electronics Inc", "Kolkata", "Patna", "CREATED", None, 0, 0),
    ("PP-DEMO-2009", "Acme Corp", "Food Goods", "Surat", "Ahmedabad", "DELAYED", 2, 0, 1), # Wait, Delayed isn't in ShipmentStatus Enum. Let's use IN_TRANSIT with alerts. Actually the enum in models.py has CREATED, PICKED_UP, IN_TRANSIT, OUT_FOR_DELIVERY, DELIVERED, FAILED, CANCELLED, RETURNED.
    ("PP-DEMO-2010", "Acme Corp", "Auto Parts", "Chennai", "Madurai", "OUT_FOR_DELIVERY", 0, 0, 0),
]

# Clean existing demo shipments (except 1001 to keep history if we want, or just wipe them)
cursor.execute("DELETE FROM shipments WHERE account_id = ? AND tracking_id != 'PP-DEMO-1001'", (account_id,))

now = datetime.utcnow()
for s in shipments:
    tracking_id, sender, receiver, origin, dest, status, days_offset, carrier_fault, customer_fault = s
    if status == "DELAYED":
        status = "IN_TRANSIT"
        carrier_fault = 1
    
    if days_offset is not None:
        eta = (now + timedelta(days=days_offset)).isoformat()
    else:
        eta = None
        
    cursor.execute("""
        INSERT INTO shipments 
        (tracking_id, customer_id, account_id, sender_name, receiver_name, origin, destination, current_status, estimated_delivery, carrier_fault, customer_fault)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (tracking_id, customer_id, account_id, sender, receiver, origin, dest, status, eta, carrier_fault, customer_fault))
    shipment_id = cursor.lastrowid
    
    # Also create some notifications for the user
    if status == "FAILED":
        cursor.execute("""
            INSERT INTO notifications (user_id, shipment_id, type, title, message, is_read)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (customer_id, shipment_id, "ALERT", f"Delivery Failed: {tracking_id}", "The delivery attempt failed. Action required.", 0))

# Add a general notification
cursor.execute("""
    INSERT INTO notifications (user_id, type, title, message, is_read)
    VALUES (?, ?, ?, ?, ?)
""", (customer_id, "SYSTEM", "Welcome to ParcelPilot", "Your dashboard is ready and seeded with sample data.", 0))

conn.commit()
print("Realistic demo data seeded successfully!")
