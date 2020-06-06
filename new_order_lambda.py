import json
import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def newOrder(event, context):
    try: 
        newData = {"api_key":"###USE YOUR OWN###",
            "email":'###USE YOUR OWN###',
            "signature": "###USE YOUR OWN###",
            "version":2.0,
            "order_bucket":{"client":"###USE YOUR OWN###", #short ID of customer in Asendia FBA system, hardcoded.
                "ordernumber": event["order_number"], #Order Number of items, must be unique per order
                "tracking":event["token"], #Additional identifier for order
                "packet": event["id"], #Packet ID of items must be unique per order. this will be use to retrieve tracking updates.
                "consignee":"TEST 123" + event["customer"]["first_name"] + " " + event["customer"]["last_name"], #Full Name of Customer
                "address1":event["shipping_address"]["address1"], #Shipping address used instead of billing address
                "address2":event["shipping_address"]["address2"],
                "city":event["shipping_address"]["city"],
                "state":event["shipping_address"]["province"],
                "zipcode":event["shipping_address"]["zip"],
                "country":event["shipping_address"]["country_code"], #country code used here but full name of country is available in data
                "iso3166":event["shipping_address"]["country_code"], #ISO2 Country Code e.g. AU, GB, US, SG
                "phone":event["customer"]["phone"], #Contact phone number of the customer. Must be in integer and no alphanumeric
                "sku1":event["line_items"][0]["sku"],
                "qty1":event["line_items"][0]["quantity"],
                # "bro_sku1":"", #brochure or any additional insert per order
                # "bro_qty1":"",
                # "bro_sku2":"",
                # "bro_qty2":"",
                # "bro_sku3":"",
                # "bro_qty3":"",
                # "bro_sku4":"",
                # "bro_qty4":"",
                # "description":"", #description of orders in CN22 declaration. Unable to find matching variable
                "value":event["total_price"], #value of items for CN declaration. Diff from total_line_items_price
                "weight":event["total_weight"], #weight of items in KG
                # "maildate":"", #expected maildate of items DD/MM/YYYY Format. Unable to find matching variable
                "ServiceType":"" #service channel assigns for the order, hardcoded.
        }}
    
        for i in range(1,10):
            try:
                newData["order_bucket"]["sku"+str(i+1)] = event["line_items"][i]["sku"]
                newData["order_bucket"]["qty"+str(i+1)] = event["line_items"][i]["quantity"]
            except Exception as e:
                # logging.info(e)
                break
        
        if newData["order_bucket"]["country"] == "US":
            newData["order_bucket"]["carrier_code"] = "FEDEX";
            newData["order_bucket"]["ServiceType"] = "NA";
    	
        # logging.info(str(event))
        # logging.info(newData)
        
        headers = {"Content-Type": "application/json"}
        response = requests.post("###ANCHANTO URL###", json=newData, headers=headers)
        logging.info(response.text)
        
    except Exception as e:
        logger.info("Exception" + str(e))
        # server = smtplib.SMTP('smtp.mailgun.org', 587)
        # server.ehlo()
        # server.starttls()
        # server.login('###USE YOUR OWN###','###USE YOUR OWN###')
        # server.sendmail('###USE YOUR OWN###', recipients, str(e))
        # server.quit()
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from new-order Function')
    }
