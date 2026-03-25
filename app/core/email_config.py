from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel

class EmailSchema(BaseModel):
    email: str
    subject: str
    body: str

conf = ConnectionConfig(
    MAIL_USERNAME="your_email@gmail.com",
    MAIL_PASSWORD="your_app_password",
    MAIL_FROM="your_email@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="LIFEASY SYSTEM",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)

fm = FastMail(conf)
