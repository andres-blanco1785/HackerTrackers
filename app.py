from flask import Flask, json, jsonify, request, Response
from dotenv import load_dotenv
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


def get_scammer_address(transID):
    transaction_info = requests.get(f'https://public-api.solscan.io/transaction/{transID}')
    curdict = transaction_info.json()
    inputAccounts = curdict["inputAccount"]
    scammer_address = ""
    for i in inputAccounts:
        if i["signer"] == False & i["writable"]:
            scammer_address = i["account"]
            break
    return scammer_address

# def add_nodes(transID):
#     curnodes = []
#     http_client = Client("https://ssc-dao.genesysgo.net/")
#     trace_nodes = []
#     suspicious_nodes = []
#     response = http_client.get_signatures_for_address(get_scammer_address(transactionID), until=transactionID)
#     transactionlist = response["result"]
#
#
#
#     return curnodes

## if signer = false and writable = true in inputAccount
def get_Data(transactionID):
    # get list of transactions after scam transaction
    http_client = Client("https://ssc-dao.genesysgo.net/")
    transaction_info = requests.get(f'https://public-api.solscan.io/transaction/{transactionID}')
    curdict = transaction_info.json()
    inputAccounts = curdict["inputAccount"]
    useraddress = ""
    for i in inputAccounts:
        if i["signer"]  & i["writable"]:
            useraddress = i["account"]
            break
    soltransfer = curdict["solTransfers"]
    cursolamount = soltransfer[0]["amount"]
    soltransferred = cursolamount * 0.000000001
    trace_nodes = []
    suspicious_accounts = []
    curaddress = get_scammer_address(transactionID)
    trace_nodes += [(useraddress, curaddress, soltransferred)]
    suspicious_accounts+=[curaddress]
    print("Initial trace nodes is: ", trace_nodes, end='\n')
    print("Initial sus accs is: ", suspicious_accounts, end='\n')
    response = http_client.get_signatures_for_address(curaddress, until=transactionID, limit=50)
    transactionlist = response.get("result")
    transactionlist.reverse()
    for i in range(0, len(transactionlist)): # user recursive functions to body build array of suspicious accounts, and nodes
        # error check transactions before adding more nodes
        print("on iteration: ", i, end='\n')
        transaction = transactionlist[i]
        time.sleep(2)
        response1 = http_client.get_transaction(transaction["signature"])
        # try:
        #     response1 = http_client.get_transaction(transaction["signature"])
        # except (RequestException, ReadTimeoutError, socket.timeout):
        #     try:
        #         http_client = Client("https://ssc-dao.genesysgo.net/")
        #         print("error occured sleeping", end='\n')
        #         time.sleep(10)
        #         print("trying again", end='\n')
        #         response1 = http_client.get_transaction(transaction["signature"])
        #     except(SolanaRpcException):
        #         http_client = Client("https://ssc-dao.genesysgo.net/")
        #         print("error occured sleeping", end='\n')
        #         time.sleep(10)
        #         print("trying again", end='\n')
        #         response1 = http_client.get_transaction(transaction["signature"])
        # else:
        #     response1 = http_client.get_transaction(transaction["signature"])


        result = response1.get("result")
        meta = result.get("meta")
        postBalances = meta.get("postBalances")
        preBalances = meta.get("preBalances")
        transaction = result.get("transaction")
        message = transaction.get("message")
        accountKeys = message.get("accountKeys")
        if len(accountKeys) != 3:
            continue
        for i in range(0, len(accountKeys)):
            if accountKeys[i]!="11111111111111111111111111111111" & accountKeys[i]!=useraddress:
                otherloc = i
            else:
                curloc = i
        if postBalances[curloc] >=preBalances[curloc]: #if current account did not send money
            continue


        cursolamount = postBalances[otherloc] - preBalances[otherloc]

        trace_nodes += [(curaddress, accountKeys[otherloc], cursolamount)]
        suspicious_accounts += [accountKeys[otherloc]]

    ## use response.get("result") if response[result] doesnt work
    print("final trace nodes is: ",trace_nodes, end='\n')
    print("final sus accs is: ",suspicious_accounts, end='\n')
    dictionary = {
        "nodes":trace_nodes,
        "transactions":suspicious_accounts
    }

    json_object = json.dumps(dictionary, indent=3)
    print("The json is: ", json_object)

def get_transaction_info(transactionID):
    http_client = Client("https://ssc-dao.genesysgo.net/")
    response = http_client.get_transaction(transactionID)
    result = response.get("result")
    meta = result.get("meta")
    postBalances = meta.get("postBalances")
    print(postBalances)
    preBalances = meta.get("preBalances")
    print(preBalances)
    transaction = result.get("transaction")
    message = transaction.get("message")
    accountKeys = message.get("accountKeys")
    print("len of account keys is: ", len(accountKeys))

if __name__ == '__main__':
    app.run()
