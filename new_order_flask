from flask import Flask, request, Response, session
import requests
import logging

logging.basicConfig(filename="logs/log.log",level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s')

app = Flask(__name__)


# variables in json response from shopify order creation webhook can be found:
# https://shopify.dev/docs/admin-api/rest/reference/events/webhook?api[version]=2020-04

@app.route("/")
def home():
    return "<h1>THIS IS HOMEEEE</h1>"

@app.route('/order_created', methods=['POST'])
def create_order():
    data = request.json
    newData = {"api_key":"##REPLACE WITH OWN##",
        "email":'##REPLACE WITH OWN##',
        "signature":"##REPLACE WITH OWN##",
        "version":2.0,
        "order_bucket":{"client":"##REPLACE WITH OWN##", #short ID of customer in Asendia FBA system, hardcoded.
            "ordernumber":data["order_number"], #Order Number of items, must be unique per order
            "tracking":data["token"], #Additional identifier for order
            "packet":data["id"], #Packet ID of items must be unique per order. this will be use to retrieve tracking updates.
            "consignee":"TESTER" + data["customer"]["first_name"] + " " + data["customer"]["last_name"], #Full Name of Customer
            "address1":data["shipping_address"]["address1"], #Shipping address used instead of billing address
            "address2":data["shipping_address"]["address2"],
            "city":data["shipping_address"]["city"],
            "state":data["shipping_address"]["province"],
            "zipcode":data["shipping_address"]["zip"],
            "country":data["shipping_address"]["country_code"], #country code used here but full name of country is available in data
            "iso3166":data["shipping_address"]["country_code"], #ISO2 Country Code e.g. AU, GB, US, SG
            "phone":data["customer"]["phone"], #Contact phone number of the customer. Must be in integer and no alphanumeric
            "sku1":data["line_items"][0]["sku"],
            "qty1":data["line_items"][0]["quantity"],
            # "bro_sku1":"", #brochure or any additional insert per order
            # "bro_qty1":"",
            # "bro_sku2":"",
            # "bro_qty2":"",
            # "bro_sku3":"",
            # "bro_qty3":"",
            # "bro_sku4":"",
            # "bro_qty4":"",
            # "description":"", #description of orders in CN22 declaration. Unable to find matching variable
            "value":data["total_price"], #value of items for CN declaration. Diff from total_line_items_price
            "weight":data["total_weight"], #weight of items in KG
            # "maildate":"", #expected maildate of items DD/MM/YYYY Format. Unable to find matching variable
            "ServiceType":"###USE YOUR OWN###" #service channel assigns for the order, hardcoded.
    }}

    for i in range(1,10):
        try:
            newData["order_bucket"]["sku"+str(i+1)] = data["line_items"][i]["sku"]
            newData["order_bucket"]["qty"+str(i+1)] = data["line_items"][i]["quantity"]
        except:
            break
            
    if newData["order_bucket"]["country"] == "US":
        newData["order_bucket"]["carrier_code"] = "FEDEX";
		newData["order_bucket"]["ServiceType"] = "NA";
        }

    # logging.info(newData)
    headers = {"Content-Type": "application/json"}
    response = requests.post("###ANCHANTO URL###", json=newData, headers=headers)
    # logging.info(response.text)
    return response.text

if __name__ == "__main__":
    app.run()
