import unittest
from domain_package import *

class TestRepository(unittest.TestCase):

    def setUp(self):
        self.session = create_in_memory_session()
        start_mappers()

    def tearDown(self):
        clear_mappers()

    def test_repo_can_save_batch(self):
        batch = Batch('ref-001', 'CUTIE-TEDDY', 10)

        repo = SqlAlchemyRepository(session=self.session)
        repo.add(batch)
        session.commit()

        rows = session.execute('Select * from batches')

        self.assertIn(batch, rows)