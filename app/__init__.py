from sqlalchemy.orm import sessionmaker, scoped_session
from app.models import engine
from contextlib import contextmanager


# create db session
# use contextlib to try to keep details of session, transaction
# and exception management 
@contextmanager
def session_scope():
    """Provide a transaction scope around a series of operations"""
    session_factory = sessionmaker(autocommit=False, bind=engine,
                                   expire_on_commit=False)
    Session = scoped_session(session_factory)  # this use thread.local()
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        raise
    finally:
        session.expunge_all()
        session.close()

