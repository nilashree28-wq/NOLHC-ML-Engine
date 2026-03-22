"""Tests for raw ML FastAPI app (Task 7)."""

import pytest
from fastapi.testclient import TestClient

from ml_api import create_app
from ml_engine import PROJECT_ROOT


def test_health_503_when_no_models(tmp_path):
    app = create_app(models_root=tmp_path)
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 503
    assert r.json()["error"] == "model_not_ready"


@pytest.mark.integration
def test_health_200_when_models_present():
    reg = PROJECT_ROOT / "models" / "v1" / "registry.json"
    if not reg.is_file():
        pytest.skip("no trained models")
    app = create_app()
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert data["model_version"] == "v1"
    assert "training_runs" in data
    assert data["phase1_models"] == 101
    assert data["phase2_models_pending"] == 35


@pytest.mark.integration
def test_predict_empty_body():
    reg = PROJECT_ROOT / "models" / "v1" / "registry.json"
    if not reg.is_file():
        pytest.skip("no trained models")
    app = create_app()
    client = TestClient(app)
    r = client.post("/predict", json={})
    assert r.status_code == 200
    assert len(r.json()) == 136


@pytest.mark.integration
def test_predict_selective_unknown_output():
    reg = PROJECT_ROOT / "models" / "v1" / "registry.json"
    if not reg.is_file():
        pytest.skip("no trained models")
    app = create_app()
    client = TestClient(app)
    r = client.post(
        "/predict/selective",
        json={"outputs": ["not_a_real_slug_xyz"], "VolAllPImGB": 1.0},
    )
    assert r.status_code == 422
    assert r.json()["error"] == "unknown_output"


@pytest.mark.integration
def test_outputs_and_inputs_lists():
    reg = PROJECT_ROOT / "models" / "v1" / "registry.json"
    if not reg.is_file():
        pytest.skip("no trained models")
    app = create_app()
    client = TestClient(app)
    o = client.get("/outputs")
    assert o.status_code == 200
    assert len(o.json()) == 136
    i = client.get("/inputs")
    assert i.status_code == 200
    assert len(i.json()) == 153
