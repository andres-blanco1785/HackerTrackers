from flask import Flask, json, jsonify, request, Response
from dotenv import load_dotenv
from solana.rpc.api import Client
import numpy as npy
import requests
import os

load_dotenv()
bearerToken = os.environ.get("SOLANA_BEACH_API_KEY")

app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route("/transaction/<string:transactionID>")
def get_transaction_info(transactionID):
    request_headers = {
        'Authorization' : f'Bearer {bearerToken}',
        'accept': 'application/json'
    }
    response = requests.get(f'https://api.solanabeach.io/v1/transaction/{transactionID}', headers=request_headers)
    print('this is the response', response.json())
    return response.json()

@app.route("/fin_transaction/<string:transID>")
def get_final_transaction(transID):
    http_client = Client("https://ssc-dao.genesysgo.net/")
    response = http_client.get_transaction(transID)
    result = response['result']
    generalBalChange = -1
    tokenBalChange = -1

    if(len(result['postBalances']) != 0):
        generalBalChange = npy.max(npy.subtract(result['postBalances'], result['preBalances']))
    if(len(result['postTokenBalances']) != 0):
        tokenBalChange = npy.max(npy.subtract(result['postTokenBalances'], result['preTokenBalances']))

    #response = http_client.get_signatures_for_address(address, before=bef_addr)
    list = response['result']

    while(len(list) >= 1000):
        bef_addr = list[0]['signature']
        response = http_client.get_signatures_for_address(address, before=bef_addr)
        list = response['result']
        #print("this is the list[0]: ", list[0])

    return list[0]


if __name__ == '__main__':
    app.run()
