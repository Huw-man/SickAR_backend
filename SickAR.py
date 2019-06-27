from flask import Flask, make_response, jsonify

from Item import Item
from ItemCache import ItemCache
from NetworkRequest import NetworkRequest

app = Flask(__name__)
cache = ItemCache()


@app.route('/')
def landing():
    return 'SickAR backend service.'


@app.route('/tamper/<string:barcode>')
def tamper(barcode):
    """
    Detects damage or tamper to a particular package indicated by barcode

    :return True if item has been damaged false otherwise
    """
    # TODO: implement damage/tamper detection
    return True


@app.route('/get/<string:barcode>')
def get(barcode):
    """
    fetch the data from Sick AN service and fetch pictures too
    :param barcode:
    :return:
    """
    json_response = NetworkRequest.send_request(barcode)
    item = Item(json_response["results"])
    cache.add_item(barcode, item)
    NetworkRequest.send_request_pictures(item, barcode)
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
    item = cache.get_item(barcode)
    if item is None:
        resp["results"] = None
    else:
        resp["results"] = item.get_pictures()

    return make_response(jsonify(resp), 200)


if __name__ == '__main__':
    # print(__name__)
    app.run(debug=True)
