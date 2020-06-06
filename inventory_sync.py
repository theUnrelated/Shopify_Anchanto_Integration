import json
import requests
import logging
import smtplib

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def stockSync(event, context):
    
    shopify = {"api_key":"###USE YOUR OWN###",
    "password":"###USE YOUR OWN###", # also the X-access token
    "hostname":"###USE YOUR OWN###",
    "version":"2020-04",
    }
    
    gqlheaders = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": shopify["password"]
    }
    
    headers = {"Content-Type": "application/json"}
    try:
      for p in event["products"]:
        query = """
        query($sku: String){
        productVariants(first: 1, query: $sku) {
          edges {
            node {
              product{ 
                  id
                  }
            }
          }
        }
        }
        """
        variables = {"sku":"sku:" + p["sku"]}
        request = requests.post('https://{}.myshopify.com/admin/api/2020-04/graphql.json'.format(shopify["hostname"]), json={'query': query, 'variables':variables}, headers=gqlheaders)
        # logger.info("Response" + str(request))
        # logger.info(request.json())
        prodID = request.json()["data"]["productVariants"]["edges"][0]["node"]["product"]["id"].split("/")[-1]
        
        newData = {"product": {
                "id": prodID,
                "variants": [{"inventory_quantity":p["quantity"] #NOTE QUANTITY HERE. DEPENDS ON ANCHANTO WEBHOOK SIDE
            }]}}
            
        quantityUpdate = requests.put("https://{}:{}@{}.myshopify.com/admin/api/{}/products/{}.json".format(shopify["api_key"],shopify["password"],shopify["hostname"],shopify["version"],prodID), json=newData, headers=headers)
        logging.info("Quantity Updated" + p["sku"] + p["quantity"])
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
        'body': json.dumps('Hello from stockSync!')
    }

