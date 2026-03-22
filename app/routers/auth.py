from fastapi import APIRouter
from pydantic import BaseModel
from app.core.security import create_access_token

router = APIRouter()

class LoginRequest(BaseModel):
    tenant_id: str
    password: str

# fake DB
users = {
    "1001": {"password": "123456"}
}

@router.post("/login")
def login(data: LoginRequest):
    user = users.get(data.tenant_id)

    if not user or user["password"] != data.password:
        return {"status": "error", "message": "Invalid credentials"}

    token = create_access_token({"sub": data.tenant_id})

    return {
        "status": "success",
        "access_token": token
    }
