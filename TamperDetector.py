import Constants
from Item import Item


def get_sorted_dimension_list(system):
    """
    Sorts the dimensions of a particular system
    Also provides a map for which values are which labels
    Ex. {
            54.3 : "length"
            34.7 : "width"
            23.9 : "height"
        }

    :param system:
    :return: tuple (sorted dimensions, values_to_label_dict)
    """
    dims_list = []
    values_to_labels = {}
    for label in ["length", "width", "height"]:
        dims_list.append(system[label]["value"])
        values_to_labels[system[label]["value"]] = label
    dims_list.sort()
    return dims_list, values_to_labels


def print_sign(diff):
    """
    :return sign according to diff
    """
    return "-" if diff > 0 else "+"


class TamperDetector:
    """
    Detects is a package has been damaged over several systems.
    """

    @staticmethod
    def detect(item: Item):
        """
        An item is identified as damaged if on of its dimension properties
        changes by more than 5% of its original value

        :param item:
        :return: dict
        """
        # set base truth to be the oldest system
        base_system = item.data[-1]
        base_dims, base_values_to_labels = get_sorted_dimension_list(base_system)

        # list of properties to check for tamper
        # properties = ["length", "width", "height", "weight", "boxFactor"]

        tamper = False
        damage_info = {}
        system_order = []
        # print(item.data)
        for system in item.data:
            # sort the length, width, and height before comparing them
            dims = get_sorted_dimension_list(system)[0]
            local_tamper_flag = False
            local_tamper_properties = []

            length_unit = system['length']['unitLabel']
            # examine dimensions
            for i in range(3):
                diff = base_dims[i] - dims[i]
                if diff / base_dims[i] > Constants.tamper_threshold:
                    # detect damage is difference greater than 5%
                    tamper = True
                    local_tamper_flag = True
                    local_tamper_properties.append(base_values_to_labels[base_dims[i]] + "(" + print_sign(diff) +
                                                   str(round(diff, 2)) + " " + length_unit + ")")
                    # local_tamper_properties.append(
                    #     [base_values_to_labels[base_dims[i]], str(round(diff, 2))
                    #      + " " + length_unit])

            # examine weight
            if base_system["weight"]["value"] is not None and base_system["weight"]["value"] > 0:
                weight_unit = system['weight']['unitLabel']
                diff_weight = base_system["weight"]["value"] - system["weight"]["value"]
                if diff_weight / base_system["weight"]["value"] > Constants.tamper_threshold:
                    tamper = True
                    local_tamper_flag = True
                    local_tamper_properties.append("weight(" + print_sign(diff_weight) + str(round(diff_weight, 2))
                                                   + " " + weight_unit + ")")
                    # local_tamper_properties.append(["weight", str(round(diff_weight, 2))
                    #                                 + " " + weight_unit])

            # if tamper has been detected add that information to the response
            if local_tamper_flag:
                # print(system["systemId"])
                system_order.append(system["systemId"])
                damage_info[system["systemId"]] = local_tamper_properties

            # diff_box_factor = base_system["boxFactor"] - system["boxFactor"]
            # if diff_box_factor / base_system["boxFactor"] > 0.05:
            #     tamper = True
            #     damage_system = system["systemId"]

        # return dict for JSON response
        if tamper:
            # print(damage_info)
            return {
                "tamper": True,
                "tamperDetails": damage_info,
                "tamperOrder": system_order
            }
        else:
            return {
                "tamper": False,
                "tamperDetails": None
            }
