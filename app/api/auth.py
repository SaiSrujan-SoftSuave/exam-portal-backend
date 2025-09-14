import jwt
from fastapi import APIRouter

from app.core.config import config

router=APIRouter()

@router.get("/user_details")
async def get_user_details(
        token: str
):
    # data = jwt.decode(token, config.AUTH_JWT_SECRET_KEY, algorithms=["HS256"])

    return {
        "usercode" : "U12345",
        "passcode" : "P12345"
    }