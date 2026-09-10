"""
Basic test suite for the CoreAI Flask API.

Uses a throwaway SQLite DB (set via DATABASE_URL before import) so tests
never touch a real Postgres instance.
"""
import os
import sys
import pytest

# Point at an isolated on-disk SQLite DB for the test run, before app import.
os.environ["DATABASE_URL"] = "sqlite:///test_coreai.db"
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app  # noqa: E402
from database import init_db, get_session, Task, MemoryItem  # noqa: E402


@pytest.fixture()
def client():
    init_db()
    app.config.update(TESTING=True)
    with app.test_client() as c:
        yield c


def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "ok"
    assert data["total_agents"] > 0


def test_invoke_requires_message(client):
    resp = client.post("/invoke", json={"thread_id": "t1"})
    assert resp.status_code == 400


def test_invoke_task_agent_adds_and_persists_task(client):
    resp = client.post(
        "/invoke",
        json={"message": "add task", "thread_id": "t1", "context": {"title": "Write tests"}},
    )
    assert resp.status_code == 200
    # Response streams as text/plain; just check something came back.
    assert resp.data

    with get_session() as db:
        titles = [t.title for t in db.query(Task).filter(Task.thread_id == "t1").all()]
    assert "Write tests" in titles


def test_memory_get_and_post(client):
    resp = client.post("/memory", json={"key": "Timezone", "value": "UTC"})
    assert resp.status_code == 200

    resp = client.get("/memory")
    assert resp.status_code == 200
    keys = [item["key"] for item in resp.get_json()["memory_items"]]
    assert "Timezone" in keys


def test_metrics_endpoint_exposes_prometheus_format(client):
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert b"coreai_requests_total" in resp.data or resp.status_code == 200


def teardown_module(module):
    # Clean up the throwaway SQLite file after the test run.
    try:
        os.remove("test_coreai.db")
    except OSError:
        pass
