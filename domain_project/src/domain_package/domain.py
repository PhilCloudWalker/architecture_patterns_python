from dataclasses import dataclass
from tkinter.ttk import Style

@dataclass(unsafe_hash=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int

class OutOfStock(Exception):
    """Not enough stock available"""
    pass

class Batch:

    def __init__(self, reference_id, sku, qty=0, eta='stocked' ) -> None:
        self._reference_id = reference_id
        self.sku = sku
        self.eta = eta
        self._allocations = set()
        self._purchased_qty = qty
    
    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def can_allocate(self, line: OrderLine):
        return self.available_qty >= line.qty and self.sku == line.sku
    
    def deallocate(self, line):
        if line in self._allocations:
            self.allocated_orders.remove(line.orderid)

    @property
    def allocated_qty(self):
        return sum([line.qty for line in self._allocations])

    @property
    def available_qty(self):
        return self._purchased_qty - self.allocated_qty

    @property
    def reference_id(self):
        return self._reference_id

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        else:
            return other.reference_id == self.reference_id
    
    def __hash__(self):
        return hash(self.reference_id)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        else: 
            self.eta > other.eta
    
def allocate(line, batches):
    try:
        batch = next(batch for batch in sorted(batches) if batch.can_allocate(line))
        batch.allocate(line)
        return batch.reference_id
    except StopIteration:
        raise OutOfStock(f'Not enough stock for sku {line.sku}')


