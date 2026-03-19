from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from database import Base
from datetime import datetime

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, ForeignKey("tenants.tenant_id"))
    bill_id = Column(Integer, ForeignKey("bills.id"))
    amount = Column(Float)
    method = Column(String)  # Cash, bKash, Nagad, Bank Transfer, etc.
    payment_date = Column(DateTime, default=datetime.utcnow)
    receipt_number = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
