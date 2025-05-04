from pydantic import BaseModel, Field, Json
from typing import List, Optional, Dict, Any
from uuid import uuid4, UUID

class Chunk(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    text: str
    embedding: Optional[List[float]] = Field(default_factory=list)
    metadata_config: Dict[str, str]
    document_id: UUID= Field(default_factory=uuid4) 
    class Config:
        from_attributes = True
        orm_mode = True


class Document(BaseModel):
    id: UUID = Field(default_factory=uuid4) 
    chunks: List[Chunk]
    metadata_config: Dict[str, str]
    library_id: UUID =Field(default_factory=uuid4) 
    class Config:
        from_attributes = True
        orm_mode = True

class Library(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    documents: List[Document]
    metadata_config: Optional[Dict[str, str]] = {}
    class Config:
        from_attributes = True
        orm_mode = True

class Query(BaseModel):
    text: str

# print(Chunk.model_fields)