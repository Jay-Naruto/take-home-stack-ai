from sqlalchemy.orm import Session
from models import Library, Chunk, Document, Query
from database import LibraryDB, DocumentDB, ChunkDB 
from fastapi import HTTPException
from uuid import UUID

def create_library(library, db: Session):
    try:
        db.begin()

        db_docs = []
        for doc in library.documents:
            db_chunks =[]
            for chunk in doc.chunks:
                db_chunk =ChunkDB(
                    id=chunk.id, 
                    text=chunk.text, 
                    embedding=chunk.embedding,
                    metadata_config=chunk.metadata_config,
                    document_id=doc.id 
                )
                db_chunks.append(db_chunk)

            db_document = DocumentDB(
                id=doc.id,
                chunks=db_chunks,
                metadata_config=doc.metadata_config,
                library_id=library.id
            )

            db_docs.append(db_document)

        db_library = LibraryDB(
            name=library.name,
            metadata_config=library.metadata_config if library.metadata_config else {},
            documents=db_docs
        )

        db.add(db_library)
        db.commit()
        db.refresh(db_library)

        return Library(
            id= db_library.id,
            name= db_library.name,
            documents= [
                Document(
                    id=doc.id,
                    chunks=[
                        Chunk(
                            id=chunk.id,
                            text=chunk.text,
                            embedding=chunk.embedding,
                            metadata_config=chunk.metadata_config
                        ) for chunk in doc.chunks
                    ],
                    metadata_config=doc.metadata_config
                ) for doc in db_library.documents
            ],
            metadata_config= db_library.metadata_config
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating library: {str(e)}")

def get_libraries(db: Session):
    db_libraries = db.query(LibraryDB).all()
    return [Library.from_orm(library) for library in db_libraries]

def get_library(library_id: UUID, db: Session ):
    db_library = db.query(LibraryDB).filter(LibraryDB.id == library_id).first()
    if db_library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    return db_library


def update_library(library_id:UUID, library, db: Session):
    try:
        db.begin()
        db_library = db.query(LibraryDB).filter(LibraryDB.id == library_id).first()
        if db_library is None:
            raise HTTPException(status_code=404, detail="The specified library id not found")

        db_library.name = library.name

        db_library.metadata_config = library.metadata_config

        for doc in library.documents:
            db_doc = db.query(DocumentDB).filter(DocumentDB.id == doc.id, DocumentDB.library_id == library_id).first()
            if db_doc is None:
                raise HTTPException(status_code=404, detail="Document not found in the specified library")

            db_doc.metadata_config = doc.metadata_config
            for chunk in doc.chunks:
                db_chunk = db.query(ChunkDB).filter(ChunkDB.id == chunk.id, ChunkDB.document_id == doc.id).first()

                if db_chunk:
                    db_chunk.text =chunk.text
                    db_chunk.embedding =chunk.embedding
                    db_chunk.metadata_config =chunk.metadata_config
                else: 
                    new_chunk =ChunkDB(
                        id=chunk.id,
                        text=chunk.text,
                        embedding=chunk.embedding,
                        metadata_config=chunk.metadata_config,
                        document_id=doc.id
                    )
                    db_doc.chunks.append(new_chunk)


        db.commit()
        db.refresh(db_library)
        return db_library
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating library: {str(e)}")


def delete_library(library_id:UUID, db: Session):
    db_library = db.query(LibraryDB).filter(LibraryDB.id == library_id).first()
    if db_library is None:
        raise HTTPException(status_code=404, detail="The specified library id not found")

    db.delete(db_library)
    db.commit()
    return db_library