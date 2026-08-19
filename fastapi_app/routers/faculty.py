from fastapi import APIRouter,Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models.tables import Faculty
from schemas.api import FacultyOut
router=APIRouter(prefix='/faculty',tags=['faculty'])
@router.get('/',response_model=list[FacultyOut])
async def list_faculty(designation:str|None=None,session:AsyncSession=Depends(get_session)):
    query=select(Faculty).where(Faculty.is_active.is_(True))
    if designation:query=query.where(Faculty.designation==designation)
    rows=(await session.scalars(query.order_by(Faculty.display_order,Faculty.name))).all()
    return [FacultyOut(id=x.id,name=x.name,designation=x.designation,specialization=x.specialization,email=x.email,phone=x.phone,scholar_link=x.scholar_link,photo_url=f'/media/{x.photo}' if x.photo else None,bio=x.bio) for x in rows]
