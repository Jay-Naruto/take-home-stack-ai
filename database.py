from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import create_engine, Column, Integer, String, JSON, ForeignKey
from pgvector.sqlalchemy import Vector
from uuid import uuid4 
from sqlalchemy.dialects.postgresql import UUID
import os
from dotenv import load_dotenv

load_dotenv()


TESTING = os.getenv('TESTING', 'False') == 'True'
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres@postgres:5432/vectordb') 

Base = declarative_base()
SQLALCHEMY_DATABASE_URL = DATABASE_URL if not TESTING else 'sqlite:///./test.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
sessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
print(f"TESTING TRUE/FALSE: {TESTING}")

class ChunkDB(Base):
    __tablename__ = "chunks"
    id = Column(UUID, primary_key=True, index= True, default=uuid4)
    text = Column(String)
    embedding = Column(Vector(384))
    metadata_config = Column(JSON, nullable=False)
    document_id = Column(UUID, ForeignKey("documents.id"))
    document = relationship("DocumentDB", backref="chunk_documents")

class DocumentDB(Base):
    __tablename__ = "documents"
    id = Column(UUID, primary_key=True, index= True, default=uuid4)
    chunks = relationship("ChunkDB", backref="document_chunks", cascade="all, delete-orphan")
    metadata_config = Column(JSON, nullable=False)
    library_id = Column(UUID, ForeignKey("libraries.id"))
    library = relationship("LibraryDB", backref="document_references")

class LibraryDB(Base):
    __tablename__ = "libraries"
    id = Column(UUID, primary_key=True, index= True, default=uuid4)
    name = Column(String)
    documents = relationship("DocumentDB", backref="library_reference", cascade="all, delete-orphan")
    metadata_config = Column(JSON, nullable=True, default=None)

Base.metadata.create_all(bind =engine)