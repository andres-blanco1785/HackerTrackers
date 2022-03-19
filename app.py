from flask import Flask, json, jsonify, request, Response
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin
import requests
import os
import psycopg2

load_dotenv()
bearerToken = os.environ.get("SOLANA_BEACH_API_KEY")

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ.get('DATABASE_URL')

con = psycopg2.connect('DATABASE_URL')

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route("/transaction/<string:transactionID>")
@cross_origin()
def get_transaction_info(transactionID):
    request_headers = {
        'Authorization' : f'Bearer {bearerToken}',
        'accept': 'application/json'
    }
    response = requests.get(f'https://api.solanabeach.io/v1/transaction/{transactionID}', headers=request_headers)
    print('this is the response', response.json())
    populate_data("wallet", "txns")
    return response.json()

def populate_data(wallet, txns):
    # Cursor
    cur = con.cursor()

    cur.execute("insert into blacklist (accountwallet, transactions) values (%s,%s);", (wallet,txns))
    con.commit()

    con.close()

if __name__ == '__main__':
    app.run()