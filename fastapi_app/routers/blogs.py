from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy import func,select,update
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models.tables import Blog,Category
from schemas.api import BlogDetailOut,BlogOut,Page
router=APIRouter(prefix='/blogs',tags=['blogs'])
def image_url(path):return f"/media/{path}" if path else None
def serialize(blog,category=None):return BlogOut(id=blog.id,title=blog.title,slug=blog.slug,category=category,featured_image_url=image_url(blog.featured_image),tags=blog.tags,views_count=blog.views_count,published_at=blog.published_at)
@router.get('/',response_model=Page)
async def list_blogs(page:int=Query(1,ge=1),limit:int=Query(6,ge=1,le=100),category:str|None=None,search:str|None=None,status:str='published',session:AsyncSession=Depends(get_session)):
    statement=select(Blog,Category.name).outerjoin(Category,Blog.category_id==Category.id).where(Blog.status==status)
    if category:statement=statement.where(Category.slug==category)
    if search:
        vector=func.to_tsvector('english',func.concat_ws(' ',Blog.title,Blog.content,Blog.tags))
        statement=statement.where(vector.op('@@')(func.plainto_tsquery('english',search)))
    total=(await session.scalar(select(func.count()).select_from(statement.subquery()))) or 0
    rows=(await session.execute(statement.order_by(Blog.published_at.desc()).offset((page-1)*limit).limit(limit))).all()
    return Page(total=total,page=page,limit=limit,results=[serialize(blog,name) for blog,name in rows])
@router.get('/{slug}/',response_model=BlogDetailOut)
async def blog_detail(slug:str,session:AsyncSession=Depends(get_session)):
    row=(await session.execute(select(Blog,Category.name).outerjoin(Category,Blog.category_id==Category.id).where(Blog.slug==slug,Blog.status=='published'))).first()
    if not row:raise HTTPException(404,'Blog not found')
    blog,name=row;await session.execute(update(Blog).where(Blog.id==blog.id).values(views_count=Blog.views_count+1));await session.commit();blog.views_count+=1
    related=[]
    if blog.category_id:
        rows=(await session.execute(select(Blog,Category.name).outerjoin(Category,Blog.category_id==Category.id).where(Blog.category_id==blog.category_id,Blog.id!=blog.id,Blog.status=='published').limit(3))).all();related=[serialize(item,cat) for item,cat in rows]
    return BlogDetailOut(**serialize(blog,name).model_dump(),content=blog.content,related_blogs=related)
