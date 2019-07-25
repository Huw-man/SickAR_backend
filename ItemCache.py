class ItemCache:
    """ ItemCache holds the items requested by an application """

    class __Cache:
        def __init__(self):
            self.order = []
            self.data = {}
            self.system_config = {}

        def add_item(self, barcode, item):
            self.order.append(barcode)
            self.data[barcode] = item

        def get_item(self, barcode):
            return self.data.get(barcode, None)

        def set_system_config(self, response):
            self.system_config = response

    instance = None

    @staticmethod
    def get_instance():
        if not ItemCache.instance:
            ItemCache.instance = ItemCache.__Cache()
        return ItemCache.instance
