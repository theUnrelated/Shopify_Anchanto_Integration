# Shopify Anchanto Integration
Various management processes between shopify and anchanto warehouse management using REST API with Python, request package and flask or AWS. 

## Flask
Flask deployment was tested via local host using [ngrok](https://ngrok.com/) and [beeceptor](https://beeceptor.com/). 

## AWS
[AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html),
[AWS API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/getting-started.html) and 
[AWS Cloudwatch](https://aws.amazon.com/cloudwatch/) (For logging and debugging purposes). <br>
Additional Permissions needed:
* iam:CreateRole
* iam:CreatePolicy

### Setting up requests library
requests package requried as an additional layer in AWS Lambda
```
mkdir python
cd python
pip install requests -t .
``` 
to download in python directory <br>
*Note: folder must be named python and the . in pip install is required.

Zip and upload to AWS Lambda Layers

You can use AWS lambda boto3 and skip the above step
```
from botocore.vendored import requests
```
but I believe it is going to be deprecated in 2021. 

Alternatively, you can use ZAPPA or SAM for the dependencies but personally, that would be much more complicated to the solution above. 

## Functions
1. Order creation
2. Inventory Sync
3. Fulfillment update

### Order Creation
[Shopify webhook](https://shopify.dev/tutorials/manage-webhooks) will be activated at new order creation sending POST request to Anchanto warehouse management. 

### Inventory Sync
Anchanto Webhook will be activated upon change in any inventory quantity, sending POST request to Shopify to update stock count.

### Fulfillment Update
POST request will be sent to shopify updating order to **Fulfilled** upon processing status change webhook request from Anchanto end. 

#### Disclaimer
This is still in dev stage but they do work. Current challenges:
- Confirmation and more vigorous testing required with Anchanto Test Environment (Down atm)
- Key information required for POST requests e.g order ID is different in Anchanto and in Shopify. 
