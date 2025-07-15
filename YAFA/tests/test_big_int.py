import pytest
from app.model.user import insert_user_data


def test_insert_big_int(app):
    """
    TC-USER-001:
    Test inserting a very large primary-key value.
    """
    BIG_INT = 2**63 - 1

    with app.app_context(), pytest.raises(ValueError):
        insert_user_data(BIG_INT, "bigint_user", "secret")
