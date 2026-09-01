from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Boolean, Numeric, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum

class Role(str, enum.Enum):
    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"
    DRIVER = "DRIVER"
    GUEST = "GUEST"

class ShipmentStatus(str, enum.Enum):
    CREATED = "CREATED"
    ASSIGNED = "ASSIGNED"
    PICKED_UP = "PICKED_UP"
    IN_TRANSIT = "IN_TRANSIT"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    RETURNED = "RETURNED"

class NotificationType(str, enum.Enum):
    SHIPMENT_ASSIGNED = "SHIPMENT_ASSIGNED"
    SHIPMENT_PICKED_UP = "SHIPMENT_PICKED_UP"
    SHIPMENT_IN_TRANSIT = "SHIPMENT_IN_TRANSIT"
    SHIPMENT_OUT_FOR_DELIVERY = "SHIPMENT_OUT_FOR_DELIVERY"
    SHIPMENT_DELIVERED = "SHIPMENT_DELIVERED"
    SHIPMENT_FAILED = "SHIPMENT_FAILED"
    SHIPMENT_CANCELLED = "SHIPMENT_CANCELLED"
    SHIPMENT_RETURNED = "SHIPMENT_RETURNED"

class CustomerAccount(Base):
    __tablename__ = "customer_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    plan = Column(String, default="Standard", nullable=False)
    contract_file = Column(String, nullable=True)
    premium_support = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship("User", back_populates="account")
    orders = relationship("Order", back_populates="account")
    shipments = relationship("Shipment", back_populates="account")
    support_tickets = relationship("SupportTicket", back_populates="account")
    conversations = relationship("Conversation", back_populates="account")
    agent_actions = relationship("AgentAction", back_populates="account")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("customer_accounts.id"), nullable=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.CUSTOMER, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    account = relationship("CustomerAccount", back_populates="users")
    shipments = relationship("Shipment", back_populates="customer", cascade="all, delete-orphan")
    driver_profile = relationship("Driver", back_populates="user", uselist=False, cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    phone = Column(String, nullable=False)
    vehicle_number = Column(String, nullable=False, unique=True)
    vehicle_type = Column(String, nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="driver_profile")
    assigned_shipments = relationship("Shipment", back_populates="driver")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, unique=True, index=True, nullable=False)
    account_id = Column(Integer, ForeignKey("customer_accounts.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    account = relationship("CustomerAccount", back_populates="orders")
    shipments = relationship("Shipment", back_populates="order")

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    tracking_id = Column(String, unique=True, index=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False) # The requester user
    account_id = Column(Integer, ForeignKey("customer_accounts.id"), nullable=True) # Linked account
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True) # Linked order
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)
    
    sender_name = Column(String, nullable=False)
    receiver_name = Column(String, nullable=False)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    current_status = Column(Enum(ShipmentStatus), default=ShipmentStatus.CREATED, nullable=False)
    estimated_delivery = Column(DateTime(timezone=True), nullable=True)
    
    # SLA Fields
    carrier = Column(String, nullable=True)
    pickup_window_start = Column(DateTime(timezone=True), nullable=True)
    pickup_window_end = Column(DateTime(timezone=True), nullable=True)
    pickup_actual_at = Column(DateTime(timezone=True), nullable=True)
    shipment_fee = Column(Numeric(10, 2), nullable=True)
    carrier_fault = Column(Boolean, default=False, nullable=False)
    customer_fault = Column(Boolean, default=False, nullable=False)
    cancellation_requested_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    customer = relationship("User", back_populates="shipments")
    account = relationship("CustomerAccount", back_populates="shipments")
    order = relationship("Order", back_populates="shipments")
    driver = relationship("Driver", back_populates="assigned_shipments")
    tracking_events = relationship("ShipmentTrackingEvent", back_populates="shipment", cascade="all, delete-orphan", order_by="ShipmentTrackingEvent.created_at")

class ShipmentTrackingEvent(Base):
    __tablename__ = "shipment_tracking_events"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"), nullable=False)
    status = Column(Enum(ShipmentStatus), nullable=False)
    location = Column(String, nullable=True)
    description = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    shipment = relationship("Shipment", back_populates="tracking_events")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"), nullable=True)
    type = Column(Enum(NotificationType), nullable=False)
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    read_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="notifications")
    shipment = relationship("Shipment")

class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, unique=True, index=True, nullable=False)
    account_id = Column(Integer, ForeignKey("customer_accounts.id"), nullable=False)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="open", nullable=False)
    subject = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String, default="P2", nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    account = relationship("CustomerAccount", back_populates="support_tickets")
    requester = relationship("User")

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("customer_accounts.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    account = relationship("CustomerAccount", back_populates="conversations")
    user = relationship("User")
    messages = relationship("ConversationMessage", back_populates="conversation", cascade="all, delete-orphan", order_by="ConversationMessage.created_at")

class ConversationMessage(Base):
    __tablename__ = "conversation_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    tool_calls = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    conversation = relationship("Conversation", back_populates="messages")

class AgentAction(Base):
    __tablename__ = "agent_actions"
    
    id = Column(Integer, primary_key=True, index=True)
    action_id = Column(String, unique=True, index=True, nullable=False)
    account_id = Column(Integer, ForeignKey("customer_accounts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action_type = Column(String, nullable=False)
    reference_entity = Column(String, nullable=True)
    reference_id = Column(String, nullable=True)
    status = Column(String, default="pending", nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    executed_at = Column(DateTime(timezone=True), nullable=True)
    
    account = relationship("CustomerAccount", back_populates="agent_actions")
    user = relationship("User")
