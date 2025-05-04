from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, sessionLocal
from models import Library, Chunk, Document, Query
from database import LibraryDB, DocumentDB, ChunkDB 
from typing import List
from uuid import UUID

from library_crud import create_library, get_libraries, get_library, update_library, delete_library
from chunk_crud import create_chunk, get_chunks, get_chunk, update_chunk, delete_chunk
from search_query import search_query_ball_tree, search_query_kd_tree

app = FastAPI()

def get_db():
    db = sessionLocal()
    try: 
        yield db
    finally:
        db.close()


# CRUD operations on Library table

@app.post("/libraries/", response_model=Library)
def create_library_endpoint(library: Library, db: Session = Depends(get_db)):
    return create_library(library, db)

@app.get("/libraries/", response_model=List[Library])
def get_libraries_endpoint(db: Session = Depends(get_db)):
    db_libraries = db.query(LibraryDB).all()
    return [Library.from_orm(library) for library in db_libraries]

@app.get("/libraries/{library_id}", response_model=Library)
def get_library_endpoint(library_id: UUID, db: Session = Depends(get_db)):
    return get_library(library_id, db)

@app.put("/libraries/{library_id}", response_model=Library)
def update_library_endpoint(library_id:UUID, library: Library, db: Session = Depends(get_db)):
    return update_library(library_id, library, db)

@app.delete("/libraries/{library_id}", response_model=Library)
def delete_library_endpoint(library_id:UUID, db: Session = Depends(get_db)):
    return delete_library(library_id, db)



# CRUD operations on Chunk table

@app.post("/libraries/{library_id}/documents/{document_id}/chunk", response_model = Chunk)
def create_chunk_endpoint(library_id: UUID, document_id: UUID, chunk: Chunk, db: Session = Depends(get_db)):
    return create_chunk(library_id, document_id, chunk, db)

@app.get("/chunks", response_model = List[Chunk])
def get_chunks_endpoint(db: Session = Depends(get_db)):
    return get_chunks(db)


@app.get("/chunk/{chunk_id}", response_model=Chunk)
def get_chunk_endpoint(chunk_id:UUID, db: Session= Depends(get_db)):
    return get_chunk(chunk_id, db)

@app.put("/libraries/{library_id}/documents/{document_id}/chunks/{chunk_id}", response_model=Chunk)
def update_chunk_endpoint(library_id: UUID, document_id:UUID, chunk_id: UUID, chunk:Chunk, db:Session = Depends(get_db)):
    return update_chunk(library_id, document_id, chunk_id, chunk, db)

@app.delete("/libraries/{library_id}/documents/{document_id}/chunks/{chunk_id}", response_model=Chunk)
def delete_chunk_endpoint(library_id:UUID, document_id: UUID,chunk_id: UUID, db: Session = Depends(get_db)):
    return delete_chunk(library_id, document_id, chunk_id, db)

# Search endpoint

@app.post("/search/ball-tree/query", response_model=List[str])
def search_query_ball_tree_endpoint(query: Query,  db: Session = Depends(get_db)):
    return search_query_ball_tree(query, db)
    
@app.post("/search/kd-tree/query", response_model=List[str])
def search_query_kd_tree_endpoint(query: Query,  db: Session = Depends(get_db)):
    return search_query_kd_tree(query, db)