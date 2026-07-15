"""Behavioral tests for hello-api's three operational endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_reports_identity_and_version():
    """/ must expose service name, version, and host — the rollout readout."""
    r = client.get("/")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "hello-api"
    assert set(body) == {"service", "version", "host"}


def test_healthz_is_dependency_free_ok():
    """/healthz must answer 200 with no downstream dependencies."""
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_metrics_exposes_prometheus_format():
    """/metrics must expose our counter in Prometheus text format."""
    client.get("/")  # ensure the counter has a sample
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "hello_requests_total" in r.text
