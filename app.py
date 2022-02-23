from flask import Flask, json, jsonify, request, Response
from dotenv import load_dotenv
from solana.rpc.api import Client
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

@app.route("/fin_transaction/<string:address>/<string:bef_addr>")
def get_final_transaction(address, bef_addr):
    http_client = Client("https://api.mainnet-beta.solana.com")
    response = http_client.get_signatures_for_address(address, before=bef_addr)

    if(len(response.get("result")) < 1000):
        return response[-1]

    else:
        last = response[len(response) - 1]

        return get_final_transaction(address, last.get)


if __name__ == '__main__':
    app.run()
