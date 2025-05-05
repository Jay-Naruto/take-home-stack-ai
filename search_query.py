from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Library, Chunk, Document, Query
from database import LibraryDB, DocumentDB, ChunkDB 
from uuid import UUID
from ballTree import BallTree
from kdTree import KDTree
from generate_samples import generate_embedding

def search_query_generic(query: Query, db: Session, index_algorithm):
    response = generate_embedding(query.text)
    chunks =  db.query(ChunkDB).all()
    all_embeddings = [chunk.embedding for chunk in chunks]
    chunk_ids =[chunk.id for chunk in chunks]
    index = index_algorithm(all_embeddings, chunk_ids)
    nearest_nbhs = index.knn_search(response, k=3)

    result_texts =[]
    
    for nbh in nearest_nbhs:
        chunk_id =nbh[0]
        chunk= db.query(ChunkDB).filter(ChunkDB.id == chunk_id).first()
        if chunk:
            result_texts.append(chunk.text)

    return result_texts

def search_query_ball_tree(query: Query, db: Session):
    return search_query_generic(query, db, BallTree)

def search_query_kd_tree(query: Query, db: Session):
    return search_query_generic(query, db, KDTree)