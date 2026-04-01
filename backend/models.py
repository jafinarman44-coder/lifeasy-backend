"""
LIFEASY V28 ULTRA - Production Ready Database
Real Tenant & OTP Management System
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

DATABASE_URL = "sqlite:///./lifeasy_v30.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Tenant(Base):
    """Real Tenant Model for Apartment Management"""
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    flat = Column(String, nullable=False)
    building = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    bills = relationship("Bill", back_populates="tenant", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="tenant", cascade="all, delete-orphan")


class OTPCode(Base):
    """OTP Verification System"""
    __tablename__ = "otp_codes"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, ForeignKey("tenants.tenant_id"), nullable=False)
    otp = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    is_used = Column(Integer, default=0)  # 0=unused, 1=used

    # Relationship
    tenant = relationship("Tenant", backref="otp_codes")


class Bill(Base):
    """Monthly Bill Management"""
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, ForeignKey("tenants.tenant_id"), nullable=False)
    month = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    paid_amount = Column(Float, default=0.0)
    status = Column(String, default="pending")  # pending, partial, paid
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    tenant = relationship("Tenant", back_populates="bills")


class Payment(Base):
    """Payment Tracking System"""
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, ForeignKey("tenants.tenant_id"), nullable=False)
    bill_id = Column(Integer, ForeignKey("bills.id"), nullable=True)
    amount = Column(Float, nullable=False)
    payment_method = Column(String, default="cash")  # cash, bkash, nagad, bank_transfer
    payment_date = Column(DateTime, default=datetime.utcnow)
    reference = Column(String, nullable=True)  # Transaction ID for bKash/Nagad
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    tenant = relationship("Tenant", back_populates="payments")
    bill = relationship("Bill", backref="payments")


class Notification(Base):
    """Notification System for Tenants"""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    title = Column(String)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant = relationship("Tenant")


class ChatRoom(Base):
    """Chat Rooms for messaging"""
    __tablename__ = "chat_rooms"

    id = Column(Integer, primary_key=True, index=True)
    is_group = Column(Boolean, default=False)  # False = 1-on-1, True = group chat

    # Relationships
    participants = relationship("ChatParticipant", back_populates="room", cascade="all, delete-orphan")
    messages = relationship("ChatMessage", back_populates="room", cascade="all, delete-orphan")


class ChatParticipant(Base):
    """Chat Room Participants"""
    __tablename__ = "chat_participants"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("chat_rooms.id"), nullable=False, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)

    # Relationships
    room = relationship("ChatRoom", back_populates="participants")
    tenant = relationship("Tenant", back_populates="chat_participants")


class ChatMessage(Base):
    """Chat Messages with Delivery Tracking"""
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    receiver_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    room_id = Column(Integer, ForeignKey("chat_rooms.id"), nullable=True, index=True)
    text = Column(Text, nullable=False)
    message_type = Column(String, default="text")  # text, image, video, file
    media_url = Column(Text, nullable=True)  # URL/path for media files
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    delivered = Column(Boolean, default=False)
    seen = Column(Boolean, default=False)
    deleted_by_sender = Column(Boolean, default=False)
    deleted_by_receiver = Column(Boolean, default=False)
    edited_at = Column(DateTime, nullable=True)

    # Relationships
    room = relationship("ChatRoom", back_populates="messages")
    sender = relationship("Tenant", foreign_keys=[sender_id])
    receiver = relationship("Tenant", foreign_keys=[receiver_id])


class BlockedUser(Base):
    """Blocked Users System"""
    __tablename__ = "blocked_users"

    id = Column(Integer, primary_key=True, index=True)
    blocker_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    blocked_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    blocked_at = Column(DateTime, default=datetime.utcnow)


class CallLog(Base):
    """Call Logs for Audio/Video Calls"""
    __tablename__ = "call_logs"

    id = Column(Integer, primary_key=True, index=True)
    caller_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    receiver_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    call_type = Column(String, nullable=False)  # 'audio' or 'video'
    status = Column(String, nullable=False)  # 'answered', 'missed', 'rejected'
    duration = Column(Integer, default=0)  # Call duration in seconds
    created_at = Column(DateTime, default=datetime.utcnow)


class ChatPresence(Base):
    """User Online/Offline Presence Tracking"""
    __tablename__ = "chat_presence"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, unique=True, index=True)
    status = Column(String, default="offline")  # 'online', 'offline', 'away'
    last_seen = Column(DateTime, default=datetime.utcnow)
    building_id = Column(Integer, nullable=True, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ChatTyping(Base):
    """Typing Indicator Tracking"""
    __tablename__ = "chat_typing"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("chat_rooms.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    is_typing = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ChatUnread(Base):
    """Unread Message Count Tracking"""
    __tablename__ = "chat_unread"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("chat_rooms.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    count = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Database helper functions
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database with tables"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database initialized successfully")


if __name__ == "__main__":
    # Create tables
    init_db()
    print("Database location:", DATABASE_URL)
