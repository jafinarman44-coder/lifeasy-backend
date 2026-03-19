from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from database import Base
from datetime import datetime

class Bill(Base):
    __tablename__ = "bills"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, ForeignKey("tenants.tenant_id"))
    month = Column(String)
    year = Column(Integer)
    amount = Column(Float)
    status = Column(String)  # paid, unpaid, partial
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
