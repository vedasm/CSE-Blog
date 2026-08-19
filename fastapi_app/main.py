from fastapi import Depends,FastAPI
from sqlalchemy import func,select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from dependencies import require_token
from models.tables import Blog,ContactMessage,Event,Faculty,NewsItem
from routers import auth,blogs,contact,events,faculty,gallery
app=FastAPI(title='CSE Blog API',version='1.0.0',docs_url='/api/v1/docs',openapi_url='/api/v1/openapi.json')
for router in (blogs.router,events.router,faculty.router,gallery.router,contact.router,auth.router):app.include_router(router,prefix='/api/v1')
@app.get('/api/v1/dashboard/stats/',dependencies=[Depends(require_token)],tags=['dashboard'])
async def dashboard_stats(session:AsyncSession=Depends(get_session)):
    async def count(model,*conditions):return (await session.scalar(select(func.count()).select_from(model).where(*conditions))) or 0
    return {'blogs':await count(Blog),'events':await count(Event),'faculty':await count(Faculty),'news':await count(NewsItem),'unread_messages':await count(ContactMessage,ContactMessage.is_read.is_(False))}
@app.get('/healthz',tags=['health'])
async def health():return {'status':'ok'}
