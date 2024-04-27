from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


class Database:
    Base = declarative_base()

    def __init__(self, database_url: str):
        logger.info(f"DB_URL: {database_url}")
        self.database_url = database_url
        self.engine = create_engine(self.database_url, echo=True)
        self.session_local = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        )

    def get_db(self):
        db = self.session_local()
        try:
            yield db
        finally:
            db.close()

    def create_tables(self):
        self.Base.metadata.create_all(bind=self.engine)
