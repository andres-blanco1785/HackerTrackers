from flask import Flask, json, jsonify, request, Response
from dotenv import load_dotenv
from solana.rpc.api import Client
import numpy as npy
import requests
import psycopg2
import os
from flask_cors import CORS, cross_origin

load_dotenv()
bearerToken = os.environ.get("SOLANA_BEACH_API_KEY")

app = Flask(__name__)
CORS(app)

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

@app.route("/fin_transaction/<string:transID>")
def get_final_transaction(transID):
    transactionID = transID
    http_client = Client("https://bitter-floral-paper.solana-mainnet.quiknode.pro/dec0009263e0e71d4da5def5e085c744dce3d43a/")
    response = http_client.get_transaction(transactionID)
    
    if 'error' in response:
        return "Bad Request", 400
    
    result = response['result']
    accounts = []
    transactions = []
    transactions.append(transID)
    preTokenArray = []
    postTokenArray = []
    genBalChange = -1
    tokenBalChange = -1
    max = False

    #determining which account gained money from the transaction
    if(len(result['meta']['postBalances']) != 0):
        genBalArray = npy.subtract(result['meta']['postBalances'], result['meta']['preBalances'])
        genBalChange = npy.max(genBalArray)
    if(len(result['meta']['postTokenBalances']) != 0):
        for accountToken in result['meta']['postTokenBalances']:
            postTokenArray.append(int(accountToken['uiTokenAmount']['amount']))
        for preAccountToken in result['meta']['preTokenBalances']:
            preTokenArray.append(int(preAccountToken['uiTokenAmount']['amount']))
        tokenBalArray = npy.subtract(postTokenArray, preTokenArray)
        tokenBalChange = npy.max(tokenBalArray)
    if(tokenBalChange > genBalChange):
        account_index = npy.where(tokenBalArray == tokenBalChange)[0][0]
    else:
        account_index = npy.where(genBalArray == genBalChange)[0][0]

    #gets the account id
    account_list = result['transaction']['message']['accountKeys']
    account = account_list[account_index]
    accounts.append(account)

    while(len(accounts) <= 10 and max == False):

        #start going backwards
        response = http_client.get_signatures_for_address(account, before=transactionID)
        list = response['result']
        if(len(list) < 1000):
            transactionID = list[-1]['signature']
            transactions.append(transactionID)
        #get first transaction in an account
        else:
            num_iterations = 0
            while(len(list) >= 1000 and num_iterations < 10):
                bef_addr = list[0]['signature']
                response = http_client.get_signatures_for_address(account, before=bef_addr)
                list = response['result']
                num_iterations += 1
                transactionID = list[-1]['signature']
                if(len(list) < 1000):
                    transactions.append(transactionID)
                if(num_iterations == 10):
                    max = True

        #if the last transaction can't be found, return what has been found
        if(max == True):
            return {"Transactions": transactions, "Accounts": accounts}

        transactionID = transactions[-1]
        response = http_client.get_transaction(transactionID)
        result = response['result']

        #determining which account lost money from the transaction
        if(len(result['meta']['postBalances']) != 0):
            genBalArray = npy.subtract(result['meta']['preBalances'], result['meta']['postBalances'])
            genBalChange = npy.max(genBalArray)
        if(len(result['meta']['postTokenBalances']) != 0):
            for accountToken in result['meta']['postTokenBalances']:
                postTokenArray.append(int(accountToken['uiTokenAmount']['amount']))
            for preAccountToken in result['meta']['preTokenBalances']:
                preTokenArray.append(int(preAccountToken['uiTokenAmount']['amount']))
            tokenBalArray = npy.subtract(preTokenArray, postTokenArray)
            tokenBalChange = npy.max(tokenBalArray)
        if(tokenBalChange > genBalChange):
            account_index = npy.where(tokenBalArray == tokenBalChange)[0][0]
        else:
            account_index = npy.where(genBalArray == genBalChange)[0][0]

        #gets the account id
        account_list = result['transaction']['message']['accountKeys']
        account = account_list[account_index]
        accounts.append(account)
        populate_data(transactionID, account)
    return {"Transactions": transactions, "Accounts": accounts}

#This methods takes dictionaries from the forward and bakcwards trace and populates the database
def populate_data(txn, wallet):
    con = psycopg2.connect(
        host="localhost",
        database="badActors",
        user="postgres",
        password="postgres"
    )
    cur = con.cursor()
    cur.execute("insert into blacklist (transaction_id, accountwallet) values (%s,%s);", (txn,wallet))
    con.commit()
    con.close()
    return

#This function returns a 2D array of the blacklist table
def show_blacklist():
    con = psycopg2.connect(
        host="localhost",
        database="badActors",
        user="postgres",
        password="postgres"
    )
    cur = con.cursor()
    cur.execute("select * from blacklist")
    con.commit()
    blacklist = cur.fetchall()
    con.close()
    return blacklist

if __name__ == '__main__':
    app.run()
