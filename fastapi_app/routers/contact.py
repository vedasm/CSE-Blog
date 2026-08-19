from collections import defaultdict,deque
from datetime import datetime,timedelta,timezone
from fastapi import APIRouter,BackgroundTasks,Depends,HTTPException,Request,status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models.tables import ContactMessage
from schemas.api import ContactIn
from utils.email import send_contact_email
router=APIRouter(prefix='/contact',tags=['contact'])
requests=defaultdict(deque)
@router.post('/',status_code=status.HTTP_201_CREATED)
async def contact(payload:ContactIn,request:Request,tasks:BackgroundTasks,session:AsyncSession=Depends(get_session)):
    ip=request.client.host if request.client else 'unknown';now=datetime.now(timezone.utc);window=now-timedelta(hours=1);bucket=requests[ip]
    while bucket and bucket[0]<window:bucket.popleft()
    if len(bucket)>=3:raise HTTPException(429,'Contact request limit reached; try again later.')
    bucket.append(now);item=ContactMessage(name=payload.name,email=str(payload.email),message=payload.message,is_read=False,created_at=now);session.add(item);await session.commit();tasks.add_task(send_contact_email,payload.name,str(payload.email),payload.message);return {'id':item.id,'detail':'Message received.'}
