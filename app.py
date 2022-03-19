from flask import Flask, json, jsonify, request, Response
from dotenv import load_dotenv

from solana.rpc.api import Client
import numpy as npy
import requests
import os
from flask_cors import CORS, cross_origin
from requests import RequestException
from solana.exceptions import SolanaRpcException
from solana.rpc.api import Client
import requests
import json
import time
import socket
from urllib3.exceptions import ReadTimeoutError
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


class TraceData:
  def __init__(self, transactions, accounts):
    self.transactions = []
    self.accounts = []

def get_initial_data(transID):
    transaction_info = requests.get(f'https://public-api.solscan.io/transaction/{transID}')
    curdict = transaction_info.json()
    inputAccounts = curdict["inputAccount"]
    scammer_address = ""
    user_address = ""

    for i in inputAccounts:
        if i["signer"] == False and i["writable"]:
            scammer_address = i["account"]
        elif i["signer"]  and i["writable"]:
            user_address = i["account"]
    soltransfer = curdict["solTransfers"]
    cursolamount = soltransfer[0]["amount"]
    sol_exchanged = cursolamount * 0.000000001
    return True, transID, user_address, scammer_address, sol_exchanged





def get_transaction_data(transactionID, curaddress):
    # IGNORE NON-SOL TRANSFERS
    http_client = Client("https://bitter-floral-paper.solana-mainnet.quiknode.pro/dec0009263e0e71d4da5def5e085c744dce3d43a/")
    response = http_client.get_transaction(transactionID)
    result = response.get("result")
    meta = result.get("meta")
    postBalances = meta.get("postBalances")
    preBalances = meta.get("preBalances")
    transaction = result.get("transaction")
    message = transaction.get("message")
    accountKeys = message.get("accountKeys")
    if len(accountKeys) != 3:
        return False, 0, 0, 0, 0
    for i in range(0, len(accountKeys)):
        if accountKeys[i] == curaddress:
            curloc = i
            continue
        elif accountKeys[i] == "11111111111111111111111111111111":
            progloc = i
            continue
        else:
            otherloc = i
            continue
    if postBalances[curloc] >= preBalances[curloc]:  # if current account did not send SOL
        return False, 0, 0, 0, 0
    # else, the current account sent SOL return data
    cursolamount = (postBalances[otherloc] - preBalances[otherloc])* 0.000000001 # calculate SOL other account gained
    return True, transactionID, curaddress, accountKeys[otherloc], cursolamount

def get_trace_data(transID, level):
    http_client = Client("https://bitter-floral-paper.solana-mainnet.quiknode.pro/dec0009263e0e71d4da5def5e085c744dce3d43a/")
    transactions = []
    accounts = []
    finaldata = TraceData([], [])
    if level == 3:
        return finaldata
    curdata = get_initial_data(transID)
    scammer_address = curdata[3]
    response = http_client.get_signatures_for_address(curdata[3], until=transID)
    transactionlist = response["result"]
    transactionlist.reverse()
    if len(transactionlist) == 1000:
        return finaldata
    rangetransactions = 10
    if len(transactionlist)<=10:
        rangetransactions = len(transactionlist)
    for i in range(0, rangetransactions):
        transaction = transactionlist[i]
        result = get_transaction_data(transaction["signature"], scammer_address)
        if result[0] == False:
            continue
        else:
            transactions += [(result[1], result[2], result[3], result[4])]
            accounts += [result[3]]
            if level + 1 <3:
                curtrace = get_trace_data(transaction["signature"], level + 1)
                transactions += curtrace.transactions
                accounts += curtrace.accounts
    finaldata.transactions = transactions
    finaldata.accounts = accounts
    return finaldata

def get_Data(transactionID):
    # get list of transactions after scam transaction
    http_client = Client("https://bitter-floral-paper.solana-mainnet.quiknode.pro/dec0009263e0e71d4da5def5e085c744dce3d43a/")

    initialdata = get_initial_data(transactionID)
    transactions = []
    accounts = []
    scammer_address = initialdata[3]
    transactions += [(initialdata[1], initialdata[2], initialdata[3], initialdata[4])]
    accounts+=[scammer_address]
    response = http_client.get_signatures_for_address(scammer_address, until=transactionID)
    transactionlist = response.get("result")
    transactionlist.reverse()
    if len(transactionlist) == 1000:
        tempdict = {
            "accounts":[],
            "transactions":[]
        }
        return json.dumps(tempdict, indent=3)
    separation_level = 1
    rangetransactions = 50
    if len(transactionlist) <= 50:
        rangetransactions = len(transactionlist)
    for i in range(0, rangetransactions):
        # error check transactions before adding more nodes

        transaction = transactionlist[i]

        result = get_transaction_data(transaction["signature"],scammer_address)
        if result[0] == False:
            continue
        else:
            transactions += [(result[1], result[2], result[3], result[4])]
            accounts += [result[3]]
            curtrace = get_trace_data(transaction["signature"], separation_level+1)
            transactions += curtrace.transactions
            accounts += curtrace.accounts
    accounts = list(set(accounts))

    dictionary = {
        "transactions": transactions,
        "accounts": accounts
    }

    json_object = json.dumps(dictionary, indent=3)
    #print("The json is: ", json_object)



@app.route("/fin_transaction/<string:transID>")
def get_final_transaction(transID):
    transactionID = transID
    http_client = Client("https://ssc-dao.genesysgo.net/")
    response = http_client.get_transaction(transactionID)
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

    return {"Transactions": transactions, "Accounts": accounts}

if __name__ == '__main__':
    app.run()
