from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    password = Column(String)
    flat_number = Column(String)
    unit_number = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
