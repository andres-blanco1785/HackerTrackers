from flask import Flask, json, jsonify, request, Response
from dotenv import load_dotenv
import requests
import psycopg2
import os
from flask_cors import CORS, cross_origin

load_dotenv()
bearerToken = os.environ.get("SOLANA_BEACH_API_KEY")

app = Flask(__name__)
CORS(app)

con = psycopg2.connect(
        host="localhost",
        database="badActors",
        user="postgres",
        password="postgres"
    )

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
    return response.json()

#This methods takes dictionaries from the forward and bakcwards trace and populates the database
def populate_data(table):
    txns = table.keys()
    wallets = table.values()
    cur = con.cursor()
    for i in range(len(table)):
        cur.execute("insert into blacklist (transaction_id, accountwallet) values (%s,%s);", (txns[i],wallets[i]))
    con.commit()
    con.close()

#This function returns a 2D array of the blacklist table
def show_blacklist():
    cur = con.cursor()
    cur.execute("select * from blacklist")
    con.commit()
    blacklist = cur.fetchall()
    con.close()
    return blacklist

if __name__ == '__main__':
    app.run()
