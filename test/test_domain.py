from difflib import unified_diff
import unittest
from domain_package import OrderLine, Batch
import datetime as dt

class DomainModelTest(unittest.TestCase):

    def test_successfull_allocation(self):
        batch = Batch('batch-001', 'SMALL-Table', qty=20, eta=dt.datetime.today())
        line = OrderLine('order-001', 'SMALL-Table', 2)

        batch.allocate(line)
    
        self.assertEqual(batch.available_qty,18)

    def test_failed_allocation(self):
        batch = Batch('batch-001', 'SMALL-Table', qty=1, eta=dt.datetime.today())
        line = OrderLine('order-001', 'SMALL-Table', 2)

        batch.allocate(line)
        self.assertRaises()
        self.assertEqual(batch.available_qty,18)




if __name__ == '__main__':
    unittest.main()    

