from fastapi import APIRouter,Depends,Query
from sqlalchemy import func,select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models.tables import Event
from schemas.api import EventOut,Page
router=APIRouter(prefix='/events',tags=['events'])
def out(item):return EventOut(id=item.id,title=item.title,category=item.category,event_date=item.event_date,event_time=item.event_time,venue=item.venue,image_url=f'/media/{item.image}' if item.image else None,description=item.description,registration_link=item.registration_link,status=item.status)
@router.get('/',response_model=Page)
async def list_events(page:int=Query(1,ge=1),limit:int=Query(12,ge=1,le=100),status:str|None=None,category:str|None=None,session:AsyncSession=Depends(get_session)):
    query=select(Event)
    if status:query=query.where(Event.status==status)
    if category:query=query.where(Event.category==category)
    total=(await session.scalar(select(func.count()).select_from(query.subquery()))) or 0
    rows=(await session.scalars(query.order_by(Event.event_date).offset((page-1)*limit).limit(limit))).all();return Page(total=total,page=page,limit=limit,results=[out(item) for item in rows])
