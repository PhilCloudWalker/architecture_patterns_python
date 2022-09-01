from dataclasses import dataclass
from tkinter.ttk import Style

@dataclass
class OrderLine:
    order_id: str
    product: str
    qty: int

class Batch:

    def __init__(self, reference_id, sku, qty=0, eta='stocked' ) -> None:
        self.reference_id = reference_id
        self.sku = sku
        self.available_qty = qty
        self.eta = eta
    
    def allocate(self, line):
        self.available_qty -= line.qty
    

