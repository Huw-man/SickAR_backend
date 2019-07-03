class ItemCache:
    """ ItemCache holds the items requested by an application """

    def __init__(self):
        self.order = []
        self.data = {}

    def add_item(self, barcode, item):
        self.order.append(barcode)
        self.data[barcode] = item

    def get_item(self, barcode):
        return self.data.get(barcode, None)
