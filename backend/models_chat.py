from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database_prod import Base
from datetime import datetime


class ChatRoom(Base):
    __tablename__ = "chat_rooms"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, default="private")  # private / group
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("ChatMessage", back_populates="room")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("chat_rooms.id"))
    sender_id = Column(Integer)
    message_type = Column(String, default="text")  # text / image / video / audio
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_seen = Column(Boolean, default=False)

    room = relationship("ChatRoom", back_populates="messages")


class ChatBlock(Base):
    __tablename__ = "chat_blocks"

    id = Column(Integer, primary_key=True)
    blocker_id = Column(Integer)
    blocked_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
