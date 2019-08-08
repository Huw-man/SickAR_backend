from datetime import datetime

from flask import jsonify


def sort_systems_by_date(data_array):
    """
    Sort the data_array by system using the objectScanTime and remove repeat instances of the same system data
    Keeps only the most recent system if there are multiple

    objectScanTime is of format "2019-05-21T21:21:31.591Z"
    We use up to the second but no millisecond (ex. .591Z is not included)

    :param data_array:
    :return: sorted array of systems by date
    """
    sorted_data = sorted(data_array,
                         key=lambda system: datetime.strptime(system["objectScanTime"][:-5], "%Y-%m-%dT%H:%M:%S"),
                         reverse=True)
    # remove repeat systems and take only the most recent system if there are multiple instances of the same system
    seen = set()
    no_repeats_data = []
    for system_of_date in sorted_data:
        sys_id = system_of_date["systemId"]
        if sys_id not in seen:
            seen.add(sys_id)
            no_repeats_data.append(system_of_date)

    return no_repeats_data


class Item:
    """Item class to hold data for a single package item"""

    def __init__(self, data_array):
        """
        Initialize an Item object given the full data array from the JSON response

        :param data_array:
        """

        self.num_systems = len(data_array)
        self.data = sort_systems_by_date(data_array)
        self.systems = [sys["systemId"] for sys in self.data]
        # by default we take the latest system
        self.system_idx = 0

        # dict of pics
        # keys are the system the pictures were from and the values are another
        # dictionary of device_id's to pictures
        self.pics = {}

    def get_system_ids(self):
        """
        Returns a list of systems that have data about this item.
        The list is sorted from latest to oldest system.
        """
        return self.systems

    def set_latest(self):
        """
        Sets the system to be the latest one and all the get_ methods
        will retrieve from the latest system.
        The latest system is at index 0
        """
        self.system_idx = 0

    def set_oldest(self):
        """
        Sets the system to be the oldest one and all the get_ methods
        will retrieve from the oldest system.
        The oldest system is at index the last index
        """
        self.system_idx = -1

    def set_system(self, system_id):
        """
        Sets the system to be a particular system and all the get_ methods
        will retrieve from that system.
        """
        self.system_idx = self.systems.index(system_id)

    def get_id(self):
        """
        Get the id for this item from the current system
        """
        return self.data[self.system_idx]["id"]

    def get_devices(self):
        """
        (not used) The devices reported with an item are no used for fetching images anymore
        """
        return self.data[self.system_idx]["devices"]

    def get_objectScanTime(self):
        """
        Get the object scan time for this item from the current system
        """
        return self.data[self.system_idx]["objectScanTime"]

    def add_pictures_from_system(self, system_id, images):
        """
        Add the images associated with this system

        :param system_id:
        :param images:
        """
        self.pics[system_id] = images

    def get_pictures(self):
        """
        The following is an example of the picture dictionary structure.
        The system_id is mapped to another dictionary containing the
        device_id mapped to pictures.

        The following id's are made up but you can get the actual ones from the item data
        {
            "1" : {
                "1" : <picture base 64 string>,
                "15" : <picture base 64 string>,
                "16" : <picture base 64 string>,
                ...
            }
            "3" : {
                ...
            }
        }
        """
        return self.pics

    def get_data_json(self):
        """
        Form the response to be send back to the client about the data of this item

        :return: json data
        """
        resp = {
            "systems": self.systems,
            "results": self.data
        }
        return jsonify(resp)
