import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_user():
    r = client.post("/api/users", json={"username": "john", "email": "john@example.com"})
    assert r.status_code == 200
    assert r.json()["username"] == "john"

def test_get_user():
    r = client.post("/api/users", json={"username": "jane", "email": "jane@example.com"})
    uid = r.json()["id"]
    r = client.get(f"/api/users/{uid}")
    assert r.status_code == 200
    assert r.json()["email"] == "jane@example.com"

def test_update_user():
    r = client.post("/api/users", json={"username": "bob", "email": "bob@example.com"})
    uid = r.json()["id"]
    r = client.put(f"/api/users/{uid}", json={"username": "bobby", "email": "bobby@example.com"})
    assert r.status_code == 200
    assert r.json()["username"] == "bobby"

def test_delete_user():
    r = client.post("/api/users", json={"username": "temp", "email": "temp@example.com"})
    uid = r.json()["id"]
    r = client.delete(f"/api/users/{uid}")
    assert r.status_code == 200
    r = client.get(f"/api/users/{uid}")
    assert r.status_code == 404

def test_create_project():
    u = client.post("/api/users", json={"username": "u1", "email": "u1@e.com"}).json()
    r = client.post("/api/projects", json={"name": "P1", "description": "desc", "owner_id": u["id"]})
    assert r.status_code == 200
    assert r.json()["name"] == "P1"

def test_get_project():
    u = client.post("/api/users", json={"username": "u2", "email": "u2@e.com"}).json()
    p = client.post("/api/projects", json={"name": "P2", "description": "d", "owner_id": u["id"]}).json()
    r = client.get(f"/api/projects/{p['id']}")
    assert r.status_code == 200

def test_update_project():
    u = client.post("/api/users", json={"username": "u3", "email": "u3@e.com"}).json()
    p = client.post("/api/projects", json={"name": "P3", "description": "d", "owner_id": u["id"]}).json()
    r = client.put(f"/api/projects/{p['id']}", json={"name": "P3-new", "description": "d2", "owner_id": u["id"]})
    assert r.json()["name"] == "P3-new"

def test_delete_project():
    u = client.post("/api/users", json={"username": "u4", "email": "u4@e.com"}).json()
    p = client.post("/api/projects", json={"name": "P4", "description": "d", "owner_id": u["id"]}).json()
    r = client.delete(f"/api/projects/{p['id']}")
    assert r.status_code == 200

def test_create_task():
    u = client.post("/api/users", json={"username": "u5", "email": "u5@e.com"}).json()
    p = client.post("/api/projects", json={"name": "P5", "description": "d", "owner_id": u["id"]}).json()
    r = client.post("/api/tasks", json={"title": "T1", "status": "todo", "project_id": p["id"]})
    assert r.status_code == 200
    assert r.json()["title"] == "T1"

def test_get_task():
    u = client.post("/api/users", json={"username": "u6", "email": "u6@e.com"}).json()
    p = client.post("/api/projects", json={"name": "P6", "description": "d", "owner_id": u["id"]}).json()
    t = client.post("/api/tasks", json={"title": "T2", "status": "todo", "project_id": p["id"]}).json()
    r = client.get(f"/api/tasks/{t['id']}")
    assert r.status_code == 200

def test_update_task():
    u = client.post("/api/users", json={"username": "u7", "email": "u7@e.com"}).json()
    p = client.post("/api/projects", json={"name": "P7", "description": "d", "owner_id": u["id"]}).json()
    t = client.post("/api/tasks", json={"title": "T3", "status": "todo", "project_id": p["id"]}).json()
    r = client.put(f"/api/tasks/{t['id']}", json={"title": "T3-done", "status": "done", "project_id": p["id"]})
    assert r.json()["status"] == "done"

def test_delete_task():
    u = client.post("/api/users", json={"username": "u8", "email": "u8@e.com"}).json()
    p = client.post("/api/projects", json={"name": "P8", "description": "d", "owner_id": u["id"]}).json()
    t = client.post("/api/tasks", json={"title": "T4", "status": "todo", "project_id": p["id"]}).json()
    r = client.delete(f"/api/tasks/{t['id']}")
    assert r.status_code == 200

def test_create_comment():
    u = client.post("/api/users", json={"username": "u9", "email": "u9@e.com"}).json()
    p = client.post("/api/projects", json={"name": "P9", "description": "d", "owner_id": u["id"]}).json()
    t = client.post("/api/tasks", json={"title": "T5", "status": "todo", "project_id": p["id"]}).json()
    r = client.post("/api/comments", json={"text": "Nice", "task_id": t["id"], "user_id": u["id"]})
    assert r.status_code == 200

def test_get_comment():
    u = client.post("/api/users", json={"username": "u10", "email": "u10@e.com"}).json()
    p = client.post("/api/projects", json={"name": "P10", "description": "d", "owner_id": u["id"]}).json()
    t = client.post("/api/tasks", json={"title": "T6", "status": "todo", "project_id": p["id"]}).json()
    c = client.post("/api/comments", json={"text": "Hi", "task_id": t["id"], "user_id": u["id"]}).json()
    r = client.get(f"/api/comments/{c['id']}")
    assert r.status_code == 200

def test_update_comment():
    u = client.post("/api/users", json={"username": "u11", "email": "u11@e.com"}).json()
    p = client.post("/api/projects", json={"name": "P11", "description": "d", "owner_id": u["id"]}).json()
    t = client.post("/api/tasks", json={"title": "T7", "status": "todo", "project_id": p["id"]}).json()
    c = client.post("/api/comments", json={"text": "old", "task_id": t["id"], "user_id": u["id"]}).json()
    r = client.put(f"/api/comments/{c['id']}", json={"text": "new", "task_id": t["id"], "user_id": u["id"]})
    assert r.json()["text"] == "new"

def test_delete_comment():
    u = client.post("/api/users", json={"username": "u12", "email": "u12@e.com"}).json()
    p = client.post("/api/projects", json={"name": "P12", "description": "d", "owner_id": u["id"]}).json()
    t = client.post("/api/tasks", json={"title": "T8", "status": "todo", "project_id": p["id"]}).json()
    c = client.post("/api/comments", json={"text": "x", "task_id": t["id"], "user_id": u["id"]}).json()
    r = client.delete(f"/api/comments/{c['id']}")
    assert r.status_code == 200

def test_create_tag():
    r = client.post("/api/tags", json={"name": "urgent"})
    assert r.status_code == 200
    assert r.json()["name"] == "urgent"

def test_get_tag():
    t = client.post("/api/tags", json={"name": "bug"}).json()
    r = client.get(f"/api/tags/{t['id']}")
    assert r.status_code == 200

def test_update_tag():
    t = client.post("/api/tags", json={"name": "old"}).json()
    r = client.put(f"/api/tags/{t['id']}", json={"name": "new"})
    assert r.json()["name"] == "new"

def test_delete_tag():
    t = client.post("/api/tags", json={"name": "temp"}).json()
    r = client.delete(f"/api/tags/{t['id']}")
    assert r.status_code == 200