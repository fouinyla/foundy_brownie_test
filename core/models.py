from dataclasses import dataclass

@dataclass
class Token:
    name: str
    address: str
    amount: float
    price: float
    
    def __post_init__(self) -> None:
        self.total_price = self.price * self.amount
