from .order_items import OrderItem


class MarketplaceSubseller:

    def __init__(self, subseller_sales_amount: int, subseller_id: int):

        self.subseller_sales_amount = subseller_sales_amount
        self.subseller_id = subseller_id
        self.order_items = []

    def add_order_item(self, order_item: OrderItem):

        self.order_items.append(order_item.as_dict())

    def as_dict(self):

        return self.__dict__.copy()
