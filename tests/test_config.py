# tests/test_config.py
import os
import pytest
from pydantic import ValidationError

from src.config import create_test_settings, create_settings

def test_create_test_settings():
    settings = create_test_settings()

    # hard-coded test values
    assert settings.DEBUG is True
    assert settings.TESTING is True
    assert settings.CSRF_ENABLED is False
    assert settings.SECRET_KEY == "test"
    assert settings.DATABASE_URL == "sqlite:///./test.db"

def test_create_settings_reads_env(monkeypatch):
    # simulate environment variables
    monkeypatch.setenv("SECRET_KEY", "supersecret")
    monkeypatch.setenv("DATABASE_URL", "postgres://user:pass@db/mydb")

    settings = create_settings()
    assert settings.DEBUG is False
    assert settings.TESTING is False
    assert settings.CSRF_ENABLED is True
    assert settings.SECRET_KEY == "supersecret"
    assert settings.DATABASE_URL == "postgres://user:pass@db/mydb"

def test_missing_env_raises(monkeypatch):
    # ensure no SECRET_KEY or DATABASE_URL in env
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)

    # without these, create_settings() should raise a ValidationError
    with pytest.raises(ValidationError) as excinfo:
        create_settings()

    # check that both fields are reported as missing
    errs = excinfo.value.errors()
    missing = { e["loc"][-1] for e in errs }
    assert "SECRET_KEY" in missing
    assert "DATABASE_URL" in missing
