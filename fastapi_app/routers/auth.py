import base64,hashlib,hmac
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from dependencies import create_token
from models.tables import AdminUser
from schemas.api import TokenIn,TokenOut
router=APIRouter(prefix='/auth',tags=['auth'])
def check_django_password(password,encoded):
    try:
        algorithm,iterations,salt,digest=encoded.split('$',3)
        if algorithm!='pbkdf2_sha256':return False
        actual=base64.b64encode(hashlib.pbkdf2_hmac('sha256',password.encode(),salt.encode(),int(iterations))).decode().strip()
        return hmac.compare_digest(actual,digest)
    except (ValueError,TypeError):return False
@router.post('/token/',response_model=TokenOut)
async def token(payload:TokenIn,session:AsyncSession=Depends(get_session)):
    user=await session.scalar(select(AdminUser).where(AdminUser.email==str(payload.email),AdminUser.is_active.is_(True)))
    if not user or not check_django_password(payload.password,user.password):raise HTTPException(401,'Invalid credentials',headers={'WWW-Authenticate':'Bearer'})
    return TokenOut(access_token=create_token(str(user.id)))
