from datetime import datetime, timedelta

import requests

from Constants import API_ENDPOINT, PIC_API_ENDPOINT, SYSTEM_CONFIG_API_ENDPOINT


class NetworkRequest:
    """
    Constructs the Network request to SICK analytics for package data
    """

    # noinspection PyPep8Naming
    @staticmethod
    def send_request(barcode):
        # search within the past week
        endDate = datetime.utcnow()
        startDate = endDate - timedelta(days=20)
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
    def send_request_pictures(item, barcode):
        devices = item.get_devices()
        # print(len(item.data))
        # print(devices)
        for system_id in item.get_system_ids():
            pictures = {}
            item.set_system(system_id)
            for device in devices:
                url = PIC_API_ENDPOINT \
                      + str(system_id) \
                      + "/object/" + item.get_id() \
                      + "/device/" + str(device["deviceNumber"]) \
                      + "/media/img-sm"
                payload = {"objectScanTime": item.get_objectScanTime(), "mode": "", "locale": "en-US"}
                r = requests.get(url, params=payload)
                # print(r.url)

                img_data = r.json()["data"]
                if img_data is not None:
                    # image received
                    pictures[device["deviceNumber"]] = img_data
                    # imgdata = base64.b64decode(r.json()["data"] + "=====")
                    # with open("some_image.jpg", "wb") as f:
                    #     f.write(imgdata)
            item.add_pictures_from_system(system_id, pictures)
        return

    @staticmethod
    def send_request_system_config():
        r = requests.get(SYSTEM_CONFIG_API_ENDPOINT)
        json = r.json()
        processed = {}

        for system in json["systemList"]:
            device_map = {}
            for device in system["assignedDevices"]:
                device_map[device["deviceId"]] = device["deviceName"]
            processed[system["systemId"]] = device_map
        return processed


# r = NetworkRequest.send_request("1Z9Y82570410907110")
# print(r)
