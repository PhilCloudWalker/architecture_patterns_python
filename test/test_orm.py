import unittest
from domain_package import *
from sqlalchemy.orm import clear_mappers

#https://www.oreilly.com/library/view/essential-sqlalchemy-2nd/9781491916544/ch04.html

class TestORM(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.session = create_in_memory_session()
        start_mappers()

    def tearDown(self):
        clear_mappers()

    def test_orderline_mapper_can_load_lines(self):
        self.session.execute(
            "INSERT INTO order_lines (orderid, sku, qty) VALUES "
            '("order1", "RED-CHAIR", 12),'
            '("order1", "RED-TABLE", 13),'
            '("order2", "BLUE-LIPSTICK", 14)'
        )
        expected = [
            OrderLine("order1", "RED-CHAIR", 12),
            OrderLine("order1", "RED-TABLE", 13),
            OrderLine("order2", "BLUE-LIPSTICK", 14),
        ]
        self.assertEqual(self.session.query(OrderLine).all(), expected)

    def test_orderline_mapper_can_save_lines(self):
        new_line = OrderLine("order1", "DECO-WIDGET", 12)
        self.session.add(new_line)
        self.session.commit()

        rows = list(self.session.execute('SELECT orderid, sku, qty FROM "order_lines"'))
        self.assertEqual(rows, [("order1",  "DECO-WIDGET", 12)])

if __name__ == '__main__':
    unittest.main()
