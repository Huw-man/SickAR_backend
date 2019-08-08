from datetime import datetime, timedelta

import requests

import Constants
from Constants import API_ENDPOINT, PIC_API_ENDPOINT, SYSTEM_CONFIG_API_ENDPOINT
from ItemCache import ItemCache


class NetworkRequest:
    """
    Constructs the Network requests to SICK Package Analytics
    """

    # noinspection PyPep8Naming
    @staticmethod
    def send_request(barcode):
        """
        Send the API call to Package Analytics for the data of an item

        :param barcode:
        :return:
        """
        # search within the past week
        endDate = datetime.utcnow()
        startDate = endDate - timedelta(days=Constants.SEARCH_DAYS)
        # construct body of post request
        body = {
            "type": "byBarcode",
            "values": {
                "systemName": None,
                "systemGroupId": None,
                "startDate": startDate.isoformat() + "Z",
                "endDate": endDate.isoformat() + "Z",
                "searchPattern": barcode
            },
            "conditions": {}
        }

        return requests.post(API_ENDPOINT, json=body).json()

    @staticmethod
    def send_request_pictures(item):
        """
        Send the request to the media server for the images associated with and
        item.

        :param item:
        :return:
        """
        # iterate through all the systems
        for system_id in item.get_system_ids():
            pictures = {}
            item.set_system(system_id)
            # iterate through all the devices of this system
            for device_id in ItemCache.get_instance().system_config[system_id].keys():
                url = PIC_API_ENDPOINT \
                      + str(system_id) \
                      + "/object/" + item.get_id() \
                      + "/device/" + str(device_id) \
                      + "/media/img-sm"
                payload = {"objectScanTime": item.get_objectScanTime(), "mode": "", "locale": "en-US"}
                r = requests.get(url, params=payload)
                # print(r.url)
                if "error" not in r.json():
                    img_data = r.json()["data"]
                    if img_data is not None:
                        # image received
                        pictures[device_id] = img_data
                        # imgdata = base64.b64decode(r.json()["data"] + "=====")
                        # with open("some_image.jpg", "wb") as f:
                        #     f.write(imgdata)
            item.add_pictures_from_system(system_id, pictures)
        return item.get_pictures()

    @staticmethod
    def send_request_system_config():
        """
        Send the request for the system configuration of facility 1
        The facility is specified in the SYSTEM_CONFIG_API_ENDPOINT

        :return:
        """
        r = requests.get(SYSTEM_CONFIG_API_ENDPOINT)
        json = r.json()
        # print(json)
        processed = {}
        # iterate through systems
        for system in json["systemList"]:
            device_map = {}
            # iterate through all the devices

            for device in system["assignedDevices"]:
                if device["deviceType"]["readsBarcode"]:
                    device_map[device["deviceId"]] = device["deviceName"]
            processed[system["systemId"]] = device_map
        # cache the configuration
        ItemCache.get_instance().set_system_config(processed)
        return processed


# r = NetworkRequest.send_request("1Z9Y82570410907110")
# print(r)
