from fastapi import APIRouter,Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models.tables import GalleryImage
from schemas.api import GalleryOut
router=APIRouter(prefix='/gallery',tags=['gallery'])
@router.get('/',response_model=list[GalleryOut])
async def list_gallery(category:str|None=None,session:AsyncSession=Depends(get_session)):
    query=select(GalleryImage)
    if category:query=query.where(GalleryImage.category==category)
    rows=(await session.scalars(query.order_by(GalleryImage.uploaded_at.desc()))).all()
    return [GalleryOut(id=x.id,title=x.title,category=x.category,thumbnail_url=f'/media/{x.thumbnail}' if x.thumbnail else None,uploaded_at=x.uploaded_at) for x in rows]
