class OrderItem:

    def __init__(self, amount: int, id: str, description: str, tax_percent: float = None, tax_amount: float = None, currency: str = "BRL"):

        self.amount = amount
        self.id = id
        self.description = description
        if tax_percent:
            self.tax_percent = tax_percent
        elif tax_amount:
            self.tax_amount = tax_amount
        self.currency = currency

    def as_dict(self):

        return self.__dict__.copy()
