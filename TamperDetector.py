from Item import Item


def get_sorted_dimension_list(system):
    dims_list = []
    for label in ["length", "width", "height"]:
        dims_list.append(system[label]["value"])
    dims_list.sort()
    return dims_list


class TamperDetector:
    """
    Detects is a package has been damaged over several systems.
    """

    @staticmethod
    def detect(item: Item):
        """
        An item is identified as damaged is on of its dimension properties
        changes by more than 5% of its original value
        :param item:
        :return: dict
        """
        # set base truth to be the oldest system
        base_system = item.data[-1]
        base_dims = get_sorted_dimension_list(base_system)

        # list of properties to check for tamper
        # properties = ["length", "width", "height", "weight", "boxFactor"]

        tamper = False
        damage_system = 0
        for system in item.data:
            # sort the length, width, and height before comparing them
            dims = get_sorted_dimension_list(system)

            for i in range(3):
                diff = base_dims[i] - dims[i]
                if diff / base_dims[i] > 0.05:
                    # detect damage is difference greater than 5%
                    tamper = True
                    damage_system = system["systemId"]

            if base_system["weight"]["value"] > 0:
                diff_weight = base_system["weight"]["value"] - system["weight"]["value"]
                if diff_weight / base_system["weight"]["value"] > 0.05:
                    tamper = True
                    damage_system = system["systemId"]

            diff_box_factor = base_system["boxFactor"] - system["boxFactor"]
            if diff_box_factor / base_system["boxFactor"] > 0.05:
                tamper = True
                damage_system = system["systemId"]

        # return dict for JSON response
        if tamper:
            return {
                "tamper": "true",
                "system": str(damage_system)
            }
        else:
            return {
                "tamper": "false",
                "system": None
            }
