import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

load_dotenv()

DB_URL = os.getenv("DB_URL")
USER=os.getenv("DB_USER","cp_user")
PASSWORD=os.getenv("DB_PASSWORD", "cp_pass")
HOST=os.getenv("DB_HOST","localhost")
PORT=os.getenv("DB_PORT","5432")
DB_NAME=os.getenv("DB_NAME","crowdpulse")


if DB_URL:
    DATABASE_URL = DB_URL
else:
    from sqlalchemy.engine import URL
    DATABASE_URL = DB_URL or URL.create(
        drivername="postgresql+asyncpg",
        username=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        database=DB_NAME,
    )
print("Connected via :", DATABASE_URL)
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)
print("Connected -> ", engine)

# 🔑 Session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

async def get_db():
     async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()  # 🔥 rollback on error
            raise