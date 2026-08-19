import os
from datetime import datetime,timedelta,timezone
from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from jose import JWTError,jwt
security=HTTPBearer()
SECRET=os.getenv('JWT_SECRET_KEY','development-only-change-me');ALGORITHM=os.getenv('JWT_ALGORITHM','HS256')
def create_token(subject:str):return jwt.encode({'sub':subject,'exp':datetime.now(timezone.utc)+timedelta(minutes=int(os.getenv('JWT_EXPIRE_MINUTES','60')))},SECRET,algorithm=ALGORITHM)
async def require_token(credentials:HTTPAuthorizationCredentials=Depends(security)):
    try:return jwt.decode(credentials.credentials,SECRET,algorithms=[ALGORITHM])
    except JWTError:raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid or expired token')
