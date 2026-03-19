"""
LIFEASY V28 ULTRA - Production Ready Database
Real Tenant & OTP Management System
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

DATABASE_URL = "sqlite:///./lifeasy_v28.db"

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
