import pytest
from app import session_scope
from app.utils import get_soup
from app.models import engine, Info


@pytest.fixture(scope='module')
def test_request():
    assert get_soup('https://vnexpress.net').status_code == 200


def init_db():
    with session_scope() as session:
        info = Info(content='test', link='link.test')
        session.add(info)
        session.commit()


@pytest.fixture(scope='module')
def test_db():
    init_db()
    info_test = Info(content='test', link='link.test')
    
    with session_scope() as session:
        assert info_test == session.query(Info).filter(
            Info.content == 'test').all()
