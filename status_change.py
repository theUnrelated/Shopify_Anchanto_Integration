import json
import requests
import logging
import smtplib

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def stockSync(event, context):
    try:
        shopify = {"api_key":"###USE YOUR OWN###",
        "password":"###USE YOUR OWN###", # also the X-access token
        "hostname":"###USE YOUR OWN###",
        "version":"2020-04"
        }
        
        logger.info(event)
        
        headers = {"Content-Type": "application/json"}
        ordID = event["event"]["tracking_number"] 
        
        newData = {
        "fulfillment": {
        "location_id": ###USE YOUR OWN###, # Location ID of warehouse. change in shopify admin.
        "tracking_number": event["event"]["tracking_number"] ,
        "status": "success"
    #     "tracking_urls": [], 
          }
        }
        
        if event["event"]["new_state"] == "complete":
            statusUpdate = requests.post("https://{}:{}@{}.myshopify.com/admin/api/{}/orders/{}/fulfillments.json".format(shopify["api_key"],shopify["password"],shopify["hostname"],shopify["version"],ordID), json=newData, headers=headers)
            logging.info("Status Updated" + statusUpdate.text)
    except Exception as e:
        logger.info("StatusChange error " + str(e))
        # server = smtplib.SMTP('smtp.mailgun.org', 587)
        # server.ehlo()
        # server.starttls()
        # server.login('###USE YOUR OWN###','###USE YOUR OWN###')
        # server.sendmail('###USE YOUR OWN###', recipients, str(e))
        # server.quit()

        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from statusChange!')
    }



