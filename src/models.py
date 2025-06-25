from sqlalchemy.ext.declarative import declarative_base

# stub Base so Base.metadata.create_all(engine) is a no-op
Base = declarative_base()

# stub get_db so dependency override syntax still works
def get_db():
    """
    Test suite will override this, so we can just raise here.
    """
    raise RuntimeError("get_db() not implemented yet")
