import importlib
import pytest
import app as modulo

@pytest.fixture
def client(monkeypatch):
    monkeypatch.delenv("APP_VERSION", raising=False)
    monkeypatch.delenv("GIT_SHA", raising=False)
    importlib.reload(modulo)
    return modulo.app.test_client()

def test_home(client):
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert b"pulso" in resposta.data
    assert modulo.VERSION.encode() in resposta.data

def test_version(client):
    resposta = client.get("/api/version")
    assert resposta.status_code == 200
    assert resposta.get_json() == {"version": "1.0.0", "commit": "local"}

def test_healthz(client):
    resposta = client.get("/healthz")
    assert resposta.status_code == 200
    assert resposta.get_json() == {"status": "ok"}

def test_environment(monkeypatch):
    with monkeypatch.context() as env:
        env.setenv("APP_VERSION", "9.9.9")
        env.setenv("GIT_SHA", "abc123")
        importlib.reload(modulo)
        client = modulo.app.test_client()
        assert client.get("/api/version").get_json() == {"version": "9.9.9", "commit": "abc123"}
        assert b"9.9.9" in client.get("/").data
        assert b"abc123" in client.get("/").data
    importlib.reload(modulo)

def test_not_found(client):
    assert client.get("/inexistente").status_code == 404
