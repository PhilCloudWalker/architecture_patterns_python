import unittest
from domain_package import *
import datetime as dt

class DomainModelTest(unittest.TestCase):

    def create_batch_and_order(self, batch_id, batch_qty, product, orderid, order_qty):
        batch = Batch(batch_id, product, qty=batch_qty, eta= dt.datetime.today())
        line = OrderLine(orderid, product, order_qty)
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

    def test_prefers_stock_batches_to_shipment(self):
        in_stock_batch = Batch('batch-001', 'SMALL-Table', qty=100, eta= None)
        shipment_batch = Batch('batch-002', 'SMALL-Table', qty=100, eta= dt.datetime.today() + dt.timedelta(days =1))
        line = OrderLine('order-001', 'SMALL-Table', 10)

        allocate(line, [in_stock_batch, shipment_batch])

        self.assertEqual(in_stock_batch.available_qty, 90)
        self.assertEqual(shipment_batch.available_qty, 100)

    def test_prefers_earlier_stock_batches(self):
        earliest_batch = Batch('batch-001', 'SMALL-Table', qty=100,
                               eta= dt.datetime.today())
        middle_batch = Batch('batch-002', 'SMALL-Table', qty=100, 
                            eta= dt.datetime.today() + dt.timedelta(days =1))
        latest_batch = Batch('batch-003', 'SMALL-Table', qty=100, 
                            eta= dt.datetime.today() + dt.timedelta(days = 7))
        line = OrderLine('order-001', 'SMALL-Table', 10)

        allocate(line, [earliest_batch, middle_batch, latest_batch])

        self.assertEqual(earliest_batch.available_qty, 90)
        self.assertEqual(middle_batch.available_qty, 100)
        self.assertEqual(latest_batch.available_qty, 100)
    
    def test_returns_allocated_batch_reference(self):
        in_stock_batch = Batch('batch-001', 'SMALL-Table', qty=100, eta= None)
        shipment_batch = Batch('batch-002', 'SMALL-Table', qty=100, eta= dt.datetime.today() + dt.timedelta(days =1))
        line = OrderLine('order-001', 'SMALL-Table', 10)

        allocation = allocate(line, [in_stock_batch, shipment_batch])

        self.assertEqual(allocation, 'batch-001')
    
    def test_raise_out_of_stock_exception(self):
        batch, line = self.create_batch_and_order('batch-001', 20, 'SMALL-Table', 'order-001', 100)
        
        with self.assertRaises(OutOfStock) as context:
            allocate(line, [batch])









if __name__ == '__main__':
    unittest.main()    

