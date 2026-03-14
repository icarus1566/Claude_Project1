# SQLAlchemy Skeleton
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

Base = declarative_base()

class DocumentMeta(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True)
    filename = Column(String)
    s3_url = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

class MetadataService:
    def __init__(self, database_uri: str):
        self.engine = create_engine(database_uri)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def create_document(self, doc_id: str, filename: str, s3_url: str):
        with self.SessionLocal() as session:
            doc = DocumentMeta(id=doc_id, filename=filename, s3_url=s3_url)
            session.add(doc)
            session.commit()
