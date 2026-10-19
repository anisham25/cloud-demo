"""Run with:  pip install flask pytest  &&  pytest -q"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import app as demo  # noqa: E402


def test_home_serves_page():
    res = demo.app.test_client().get("/")
    assert res.status_code == 200 and b"Where is this app running?" in res.data


def test_where_locally(monkeypatch):
    monkeypatch.delenv("VERCEL", raising=False)
    data = demo.app.test_client().get("/api/where").get_json()
    assert data["running_on"] == "my laptop" and data["region"] == "local"


def test_where_on_vercel(monkeypatch):
    monkeypatch.setenv("VERCEL", "1")
    monkeypatch.setenv("VERCEL_REGION", "iad1")
    data = demo.app.test_client().get("/api/where").get_json()
    assert data["running_on"] == "Vercel" and data["region"] == "iad1"


def test_hits_count_up():
    client = demo.app.test_client()
    first = client.get("/api/where").get_json()["hits_on_this_copy"]
    second = client.get("/api/where").get_json()["hits_on_this_copy"]
    assert second == first + 1
