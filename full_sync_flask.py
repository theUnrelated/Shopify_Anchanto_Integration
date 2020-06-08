from flask import Flask, render_template, request, redirect, Response, session, jsonify
import requests
import logging
import time

logging.basicConfig(filename="log.log",level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s')

app = Flask(__name__)

anchanto = {"api_key":"###USE YOUR OWN###",
    "email":'###USE YOUR OWN###',
    "signature":"###USE YOUR OWN###",
    "per_page":250,
    "page":1,
    # "product_skus":"STL01", # (Comma separated Skus in String)
    "request_type":"all" # or selected, per_page and page becomes null
    }
shopify = {"api_key":"###USE YOUR OWN###",
    "password":"###USE YOUR OWN###",
    "hostname":"###USE YOUR OWN###",
    "version":"2020-04",
    }
headers = {"Content-Type": "application/json"}

# variables in json response from shopify order creation webhook can be found:
# https://shopify.dev/docs/admin-api/rest/reference/events/webhook?api[version]=2020-04

@app.route('/fetch_and_sync', methods=['POST'])
def sync():
    # data = request.json

    invAnchanto = requests.post("### ANCHANTO URL ###", json=anchanto, headers=headers)
    invShopify = requests.get("https://{}:{}@{}.myshopify.com/admin/api/{}/products.json".format(shopify["api_key"],shopify["password"],shopify["hostname"],shopify["version"]), headers=headers)
    exists = False
    for i in invAnchanto.json()["products"]:
        exists = False
        for k in invShopify.json()["products"]:
            if i["sku"] == k["variants"][0]["sku"]:
                exists = True
                if i["quantity"] != k["variants"][0]["inventory_quantity"]:
                    quantity_update(k, i["quantity"])
                    time.sleep(0.52)
                    break
        if not exists:
            new_product(i)
            time.sleep(0.52) # to avoid rate-limit

    logging.info("Anchanto inventory" + invAnchanto.text)
    logging.info("Shopify inventory" + invShopify.text)
    newId = invShopify.json()["products"][0]["id"]

    return invShopify.json()

def new_product(data):
    newData = {"product":{
        "title": data["name"],
        # "body_html":"",
        "vendor": "###USE YOUR OWN###",
        "product_type": data["item_type"],
        # "tags": ["Barnes"],
        "variants": [{"option1":"Default Title",
            "price":"12.3",
            "sku":data["sku"],
            "inventory_quantity":data["quantity"],
            "inventory_management":"shopify"
            # "weight":11,
            # "weight_unit":"g"
            }]}}
    newItem = requests.post("https://{}:{}@{}.myshopify.com/admin/api/{}/products.json".format(shopify["api_key"],shopify["password"],shopify["hostname"],shopify["version"]), json=newData, headers=headers)
    logging.info("new product created" + newItem.text)
    return newItem.text

def quantity_update(data, q):
    newData = {"product": {
            "id": data["id"],
            "variants": [{"inventory_quantity":q
        }]}}
    quantityUpdate = requests.put("https://{}:{}@{}.myshopify.com/admin/api/{}/products/{}.json".format(shopify["api_key"],shopify["password"],shopify["hostname"],shopify["version"],data["id"]), json=newData, headers=headers)
    logging.info("Quantity Updated" + quantityUpdate.text)
    return quantityUpdate.text

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
