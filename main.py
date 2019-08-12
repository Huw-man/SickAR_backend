from flask import Flask, make_response, jsonify, render_template

from Item import Item
from ItemCache import ItemCache
from NetworkRequest import NetworkRequest
from TamperDetector import TamperDetector

app = Flask(__name__, template_folder='templates')


@app.route('/')
def landing():
    """
    Landing page that describes the endpoints
    """
    return render_template('index.html')


@app.route('/tamper/<string:barcode>')
def tamper(barcode):
    """
    Detects damage or tamper to a particular package indicated by barcode

    :return True if item has been damaged false otherwise
    """

    item = ItemCache.get_instance().get_item(barcode)
    response = TamperDetector.detect(item)

    return make_response(jsonify(response), 200)


@app.route('/get/<string:barcode>')
def get(barcode):
    """
    fetch the data from SICK Package Analytics

    :param barcode:
    :return: {
        results : {
            <system data from package analytics>
            }
        systems: {
            <chronological order of systems for this item sorted from latest to oldest>
            }
        }
    }
    """
    json_response = NetworkRequest.send_request(barcode)
    # print(json_response)
    if json_response is not None and "results" in json_response and json_response["results"]:
        # only add item if response contains data
        item = Item(json_response["results"])
        ItemCache.get_instance().add_item(barcode, item)
        # NetworkRequest.send_request_pictures(item, barcode)
        # print("sending picture request")
        return make_response(item.get_data_json(), 200)
    else:
        return make_response(jsonify(json_response), 200)


@app.route('/get_pictures/<string:barcode>')
def get_pictures(barcode):
    """
    retrieve the pictures of a particular item and return them as a JSON with
    the "results" mapped to the dictionary of pictures in item
    {
        "results": <pictures dict: see Item.get_pictures for more details>
    }

    if no item present for the barcode request returns
    {
        "results": null
    }
    """
    resp = {}
    item = ItemCache.get_instance().get_item(barcode)
    if item is None:
        resp["results"] = None
    else:
        resp["results"] = NetworkRequest.send_request_pictures(item)
    # print(resp)
    return make_response(jsonify(resp), 200)


@app.route('/get_system_config')
def get_system_config():
    """
    Gets the system configuration for facility 1 (defined in the url endpoint)
    returns a dictionary that maps system to another map of deviceId to deviceName

    :return: see example below
        {
            "1": {
                "1": "Top",
                "2": "LF",
                "3": "LB",
                "4": "RB",
                "5": "RF",
                "6": "Bot",
                "7": "CLV1",
                "8": "CLV2",
            },
        ...
        }
    """
    return make_response(jsonify(NetworkRequest.send_request_system_config()))


if __name__ == '__main__':
    # print(__name__)
    # app.run(debug=True)
    app.run(host="192.168.0.221", debug=True)
