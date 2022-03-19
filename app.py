from flask import Flask, json, jsonify, request, Response
from dotenv import load_dotenv
from solana.rpc.api import Client
import numpy as npy
import requests
import psycopg2
import os
from flask_cors import CORS, cross_origin
import json
import time
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

class TraceData:
  def __init__(self, transactions, accounts):
    self.transactions = []
    self.accounts = []



def get_suspicious_accounts(transactionID, currentaccount): # this functions returns list of accounts which received SOL/tokens within a transaction
    finaldata = TraceData([], [])
    http_client = Client("https://bitter-floral-paper.solana-mainnet.quiknode.pro/dec0009263e0e71d4da5def5e085c744dce3d43a/")
    accounts = []
    balances = []
    transactions = []
    response = http_client.get_transaction(transactionID)
    result = response.get("result")
    meta = result.get("meta")
    errcode = meta.get("err")
    if errcode is not None:
        return finaldata
    postBalances = meta.get("postBalances")
    preBalances = meta.get("preBalances")
    posttokenbal = meta.get("postTokenBalances")
    pretokenbal = meta.get("preTokenBalances")
    accountKeys = result.get("transaction").get("message").get("accountKeys")
    #loop through token balances, if the difference between postand pre is positive, add that account at that index to array
    # check to make sure  who gained is not the current account
    for i in range(0, len(postBalances)):
        if postBalances[i] - preBalances[i] > 0:
            if currentaccount == accountKeys[i]:
                finaldata.accounts = []
                finaldata.transactions = []
                return finaldata
            accounts += [accountKeys[i]]
    tokenamounts = min(len(posttokenbal), len(pretokenbal))
    for j in range(0, tokenamounts):
        temppostoken = posttokenbal[j].get("uiTokenAmount").get("uiAmount")
        temppretoken = pretokenbal[j].get("uiTokenAmount").get("uiAmount")
        if temppostoken is None:
            temppostoken = 0.0
        if temppretoken is None:
            temppretoken = 0.0
        if temppostoken - temppretoken > 0:
            if (currentaccount == accountKeys[posttokenbal[j].get("accountIndex")] ):
                finaldata.accounts = []
                finaldata.transactions = []
                return finaldata
            accounts += [accountKeys[posttokenbal[j].get("accountIndex")]]
            accountresponse = http_client.get_account_info( accountKeys[posttokenbal[j].get("accountIndex")], encoding="jsonParsed" )
            accountresult = accountresponse.get("result")
            if accountresult is not None:
                accountvalue = accountresult.get("value")
                if accountvalue is not None:
                    if (currentaccount == accountvalue.get("data").get("parsed").get("info").get("owner") ):
                        finaldata.accounts = []
                        finaldata.transactions = []
                        return finaldata
                    accounts += [ accountvalue.get("data").get("parsed").get("info").get("owner") ]
    accounts = list(set(accounts))
    for y in range(0, len(accounts)):
        transactions += [(transactionID, currentaccount, accounts[y])]
    finaldata.accounts = accounts
    finaldata.transactions = transactions
    return finaldata


def get_initial_suspicious_accounts(transactionID): # this functions returns list of accounts which received SOL/tokens within a transaction
    finaldata = TraceData([], [])
    http_client = Client("https://bitter-floral-paper.solana-mainnet.quiknode.pro/dec0009263e0e71d4da5def5e085c744dce3d43a/")
    accounts = []
    transactions = []
    response = http_client.get_transaction(transactionID)
    result = response.get("result")
    meta = result.get("meta")
    errcode = meta.get("err")
    if errcode is not None:
        return finaldata
    postBalances = meta.get("postBalances")
    preBalances = meta.get("preBalances")
    posttokenbal = meta.get("postTokenBalances")
    pretokenbal = meta.get("preTokenBalances")
    transaction = result.get("transaction")
    message = transaction.get("message")
    accountKeys = message.get("accountKeys")
    #loop through token balances, if the difference between postand pre is positive, add that account at that index to array
    for i in range(0, len(postBalances)):
        if postBalances[i] - preBalances[i] > 0:
            accounts += [accountKeys[i]]
    tokenamounts = min(len(posttokenbal), len(pretokenbal))
    for j in range(0, tokenamounts):
        temppostoken = posttokenbal[j].get("uiTokenAmount").get("uiAmount")
        temppretoken = pretokenbal[j].get("uiTokenAmount").get("uiAmount")
        if temppostoken is None:
            temppostoken = 0.0
        if temppretoken is None:
            temppretoken = 0.0
        if temppostoken - temppretoken > 0:
            accounts += [accountKeys[posttokenbal[j].get("accountIndex")]]
            accountresponse = http_client.get_account_info( accountKeys[posttokenbal[j].get("accountIndex")], encoding="jsonParsed" )
            #print(accountresponse)
            accountresult = accountresponse.get("result")
            if accountresult is not None:
                accountvalue = accountresult.get("value")
                if accountvalue is not None:
                    accounts += [ accountvalue.get("data").get("parsed").get("info").get("owner") ]
                    #print("added ", accountKeys[posttokenbal[j].get("accountIndex")], "to the account array")
    accounts = list(set(accounts))

    #print(accounts)
    finaldata.accounts = accounts
    finaldata.transactions = transactions
    return finaldata




def get_trace_data(transID, level, currentaccount):
    http_client = Client("https://bitter-floral-paper.solana-mainnet.quiknode.pro/dec0009263e0e71d4da5def5e085c744dce3d43a/")
    transactions = []
    accounts = []
    finaldata = TraceData([], [])
    if level == 3:
        return finaldata

    curdata = get_suspicious_accounts(transID, currentaccount)
    transactions += curdata.transactions
    accounts += curdata.accounts
    for t in range(0, len(curdata.accounts)):
        response = http_client.get_signatures_for_address(curdata.accounts[t], until=transID)
        transactionlist = response["result"]
        transactionlist.reverse()
        if len(transactionlist) == 1000:
            continue
        rangetransactions = 10
        if len(transactionlist)<=10:
            rangetransactions = len(transactionlist)
        for i in range(0, rangetransactions):
            transaction = transactionlist[i]
            result = get_suspicious_accounts(transaction["signature"], curdata.accounts[t])
            transactions += result.transactions
            accounts += result.accounts
            if level +1 < 3:
                for f in range(0, len(result.accounts)):
                    curtrace = get_trace_data(transaction["signature"], level + 1, result.accounts[f])
                    transactions += curtrace.transactions
                    accounts += curtrace.accounts
    finaldata.transactions = transactions
    finaldata.accounts = accounts
    return finaldata

def get_Data(transactionID):
    # get list of transactions after scam transaction
    http_client = Client("https://bitter-floral-paper.solana-mainnet.quiknode.pro/dec0009263e0e71d4da5def5e085c744dce3d43a/")
    timestamp1 = time.time()
    # Your code here
    print("Starting algorithm...")
    initialdata = get_initial_suspicious_accounts(transactionID)
    transactions = []
    accounts = []
    accounts+=initialdata.accounts
    for z in range(0, len(initialdata.accounts)):
        response = http_client.get_signatures_for_address(initialdata.accounts[z], until=transactionID)
        transactionlist = response.get("result")
        transactionlist.reverse()
        if len(transactionlist) == 1000:
            continue
        separation_level = 1
        rangetransactions = 50
        if len(transactionlist) <= 50:
            rangetransactions = len(transactionlist)
        for i in range(0, rangetransactions):
            # error check transactions before adding more nodes

            transaction = transactionlist[i]

            result = get_suspicious_accounts(transaction["signature"], initialdata.accounts[z])
            transactions += result.transactions
            accounts += result.accounts
            for g in range(0, len(result.accounts)):
                curtrace = get_trace_data(transaction["signature"], separation_level+1, result.accounts[g]) # maybe feed in current account or initialdata.accounts[z]
                transactions += curtrace.transactions
                accounts += curtrace.accounts

    accounts = list(set(accounts))

    dictionary = {
        "transactions": transactions, # array(tuple(transhash, sender, receiver))
        "accounts": accounts #
    }
    timestamp2 = time.time()
    print("This algorithm took %.2f seconds" % (timestamp2 - timestamp1))
    json_object = json.dumps(dictionary, indent=3)
    print("The json is: ", json_object)



@app.route("/fin_transaction/<string:transID>")
def get_final_transaction(transID):
    transactionID = transID
    http_client = Client("https://ssc-dao.genesysgo.net/")
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

    return {"Transactions": transactions, "Accounts": accounts}

if __name__ == '__main__':
    app.run()
