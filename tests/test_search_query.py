from fastapi.testclient import TestClient
from main import app, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import Library
import pytest
import os
import uuid
from generate_samples import generate_embedding

@pytest.fixture(autouse=True)
def set_testing_flag():
    os.environ['TESTING'] = 'True'

@pytest.fixture(scope="module")
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def client():
    return TestClient(app)

def test_search_query_ball_tree(client):
    query = {
        "text": "AI is necessary in healthcare, education and blockchain."
            }
    response = client.post(f"/search/ball-tree/query", json=query)
    response_data = response.json()
    assert response.status_code == 200
    print(f"Sentences returned: {response_data}")
    assert isinstance(response_data, list), "Response should be a list of sentences"

def test_search_query_kd_tree(client):
    query = {
        "text": "AI is necessary in healthcare, education and blockchain."
            }
    response = client.post(f"/search/kd-tree/query", json=query)
    response_data = response.json()
    assert response.status_code == 200
    print(f"Sentences returned: {response_data}")
    assert isinstance(response_data, list), "Response should be a list of sentences"

    