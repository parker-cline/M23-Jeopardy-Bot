import unittest


# TODO: move to unit_test.py
def test_select(engine):
    with engine.connect() as conn:
        stmt = select(clues).where(clues.c.id == 10000)
        print(conn.execute(stmt).first())