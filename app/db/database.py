from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings


# Keep database failures bounded in serverless runtimes. A dead/unreachable
# PostgreSQL endpoint should return an API error instead of leaving the
# browser waiting until the platform function times out.
connect_args = {}
if settings.DATABASE_URL.startswith(("postgresql://", "postgresql+psycopg2://")):
    connect_args["connect_timeout"] = 5

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    pool_recycle=300,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
