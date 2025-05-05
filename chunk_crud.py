from sqlalchemy.orm import Session
from models import Library, Chunk, Document, Query
from database import LibraryDB, DocumentDB, ChunkDB 
from fastapi import HTTPException
from uuid import UUID
from generate_samples import generate_embedding

def create_chunk(library_id: UUID, document_id: UUID, chunk: Chunk, db: Session):
    try:
        db.begin()

        db_doc =db.query(DocumentDB).filter(DocumentDB.id == document_id, DocumentDB.library_id == library_id).first()
        if db_doc is None:

            raise HTTPException(status_code=404, detail="The specified document id not found")
        embedding =generate_embedding(chunk.text)
        print(f"Generated embedding: {embedding}")
        if not embedding:
            raise HTTPException(status_code=400, detail="Embedding generation failed, received empty embedding.")
        
        new_chunk =ChunkDB(
            text= chunk.text,
            embedding=embedding,
            metadata_config= chunk.metadata_config
         )

        db_doc.chunks.append(new_chunk)
        db.commit()
        db.refresh(new_chunk)

        return new_chunk
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating chunk: {str(e)}")

def get_chunks(db: Session):
    db_chunks = db.query(ChunkDB).all()
    return [Chunk.from_orm(chunk) for chunk in db_chunks]

def get_chunk(chunk_id:UUID, db: Session):
    db_chunk =db.query(ChunkDB).filter(ChunkDB.id == chunk_id).first()
    if db_chunk is None:
        raise HTTPException(status_code=404, detail="The specified chunk id not found")
    return db_chunk

def update_chunk(library_id: UUID, document_id:UUID, chunk_id: UUID, chunk:Chunk, db:Session ):
    try:
        db.begin()
        db_document =db.query(DocumentDB).filter(DocumentDB.id == document_id, DocumentDB.library_id == library_id).first()
        if db_document is None:
            raise HTTPException(status_code=404, detail="The document not found in the specified library")

        db_chunk =db.query(ChunkDB).filter(ChunkDB.id == chunk_id, ChunkDB.document_id == document_id).first()
        if db_chunk is None:
            raise HTTPException(status_code=404, detail="The specified chunk id not found")

        embedding = generate_embedding(chunk.text)
        print(f"Generated embedding: {embedding}")
        if not embedding:
            raise HTTPException(status_code=400, detail="Embedding generation failed, received empty embedding.")

        db_chunk.text= chunk.text
        db_chunk.embedding=embedding
        db_chunk.metadata_config=chunk.metadata_config

        db.commit()
        db.refresh(db_chunk)
        return db_chunk
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating chunk: {str(e)}")

def delete_chunk(library_id:UUID, document_id: UUID,chunk_id: UUID, db: Session):
    db_document =db.query(DocumentDB).filter(DocumentDB.id == document_id, DocumentDB.library_id == library_id).first()
    if db_document is None:
        raise HTTPException(status_code=404, detail="The document not found in the specified library")

    db_chunk =db.query(ChunkDB).filter(ChunkDB.id == chunk_id, ChunkDB.document_id == document_id).first()
    if db_chunk is None:
        raise HTTPException(status_code=404, detail="The specified chunk id not found")

    db.delete(db_chunk)
    db.commit()
    return db_chunk