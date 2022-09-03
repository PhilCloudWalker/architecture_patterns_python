
import unittest
from domain_package import OrderLine, Batch
import datetime as dt

class DomainModelTest(unittest.TestCase):

    def create_batch_and_order(self, batch_id, batch_qty, product, order_id, order_qty):
        batch = Batch(batch_id, product, qty=batch_qty, eta= dt.datetime.today())
        line = OrderLine(order_id, product, order_qty)
        return batch, line

    def test_successfull_allocation(self):
        batch, line = self.create_batch_and_order('batch-001', 20, 'SMALL-Table', 'order-001', 2)
        batch.allocate(line)
        self.assertEqual(batch.available_qty,18)

    def test_can_be_allocated(self):
        batch, line = self.create_batch_and_order('batch-001', 20, 'SMALL-Table', 'order-001', 2)
        self.assertTrue(batch.can_allocate(line))
    
    def test_cannot_be_allocated_not_enough_qty(self):
        batch, line = self.create_batch_and_order('batch-001', 2, 'SMALL-Table', 'order-001', 4)
        self.assertFalse(batch.can_allocate(line))

    def test_cannot_be_allocated_product_mismatch(self):
        batch = Batch('batch-001', 'SMALL-Table', qty=20, eta= dt.datetime.today())
        line = OrderLine('order-001', 'LARGE-Table', 2)
        self.assertFalse(batch.can_allocate(line))

    def test_deallocate_only_allocated_line(self):
        batch, line = self.create_batch_and_order('batch-001', 20, 'SMALL-Table', 'order-001', 2)
        batch.deallocate(line)
        self.assertEqual(batch.available_qty, 20)

    def test_ensure_no_double_handline(self):
        batch, line = self.create_batch_and_order('batch-001', 20, 'SMALL-Table', 'order-001', 2)
        batch.allocate(line)
        batch.allocate(line)
        self.assertEqual(batch.available_qty, 18)

    def test_reference_id_is_readonly(self):
        batch = Batch('batch-001', 'SMALL-Table', qty=20, eta= dt.datetime.today())
        with self.assertRaises(AttributeError) as context:
            batch.reference_id = 'new_id'






if __name__ == '__main__':
    unittest.main()    

