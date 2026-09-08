import pytest

from db.session import get_db

def test_get_db_yields_a_session_and_closes_it():
    generator = get_db()
    db = next(generator)
    assert db is not None

    with pytest.raises(StopIteration):
        next(generator)