# tests/conftest.py


# 0) FIRST: patch out NiceGUI’s ASGI lifetime guards and JSON dumps,
#    *before* anything else imports nicegui or your app factory.

from unittest.mock import MagicMock
import nicegui.app    as _ng_app
import nicegui.client as _ng_client
import nicegui.json.orjson_wrapper as _orjson

# — patch the server‐start guard —
_ng_app.config = MagicMock(
    has_run_config=True,       # bypass “must call ui.run()”
    title="Test App",          # needed by resolve_title()
    quasar_config={},          # needed by build_response
    reconnect_timeout=0,       # avoid real timeouts
    binding_refresh_interval=0 # avoid background‐task sleeps
)

# — wrap the orjson_wrapper.dumps so MagicMocks serialize as strings —
_original_dumps = _orjson.dumps
def _safe_dumps(obj, *args, **kwargs):
    try:
        return _original_dumps(obj, *args, **kwargs)
    except TypeError:
        # fall back to str(obj)
        return _original_dumps(str(obj), *args, **kwargs)
_orjson.dumps = _safe_dumps

# also patch the client namespace if it refers to `json.dumps` there
# (NiceGUI’s client.build_response sometimes does `import json`)
try:
    _ng_client.json.dumps = _safe_dumps
except AttributeError:
    pass

# ── 1. Standard pytest + TestClient setup ──
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# import your app factory and your models/get_db dependency
from src.app import create_app       # <-- your factory
from src.models import Base, get_db   # <-- SQLAlchemy Base and dependency

@pytest.fixture(scope="session")
def db_engine(tmp_path_factory):
    """
    Create a fresh SQLite file-based DB for the test session.
    """
    db_file = tmp_path_factory.mktemp("data") / "test.db"
    engine = create_engine(f"sqlite:///{db_file}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture(scope="function")
def db_session(db_engine):
    """
    Create a transactional session for each test and override the get_db dependency.
    """
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = SessionLocal()

    # dependency override
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    # instantiate the app and override
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db

    yield session

    session.rollback()
    session.close()

@pytest.fixture(scope="function")
def client(db_session):
    """
    Provide a TestClient wrapping the NiceGUI-mounted FastAPI app.
    """
    # recreate the app so each test gets a fresh dependency override
    app = create_app()
    app.dependency_overrides[get_db] = lambda: db_session

    with TestClient(app) as test_client:
        yield test_client
