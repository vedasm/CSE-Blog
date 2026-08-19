import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
DATABASE_URL=os.getenv('DATABASE_URL') or os.getenv('POSTGRES_URL') or f"postgresql+asyncpg://{os.getenv('DB_USER','cseblog_user')}:{os.getenv('DB_PASSWORD','cseblog_password')}@{os.getenv('DB_HOST','localhost')}:{os.getenv('DB_PORT','5432')}/{os.getenv('DB_NAME','cseblog_db')}"
if DATABASE_URL.startswith(('postgres://', 'postgresql://')):
    DATABASE_URL=DATABASE_URL.replace('postgres://','postgresql+asyncpg://',1).replace('postgresql://','postgresql+asyncpg://',1)
engine=create_async_engine(DATABASE_URL,pool_pre_ping=True,connect_args={'statement_cache_size': 0})
AsyncSessionLocal=async_sessionmaker(engine,expire_on_commit=False,class_=AsyncSession)
async def get_session():
    async with AsyncSessionLocal() as session:yield session
