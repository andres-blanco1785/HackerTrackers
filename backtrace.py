from solana.rpc.api import Client
from database import *
import numpy as npy

api_link = "https://frosty-autumn-night.solana-mainnet.quiknode.pro/5e5903c7cccbe98c7f2da9058e393cb4ad6ca578/"

def get_final_transaction(transID):
    transactionID = transID
    http_client = Client(api_link)
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
    response = http_client.get_account_info(account)
    if 'value' in response['result']:
        if response['result']['value'] != None:
            if 'data' in response['result']['value']:
                if(response['result']['value']['data'][0] != ""):
                    return accounts
    accounts.append(account)
    populate_data(transactionID, account, "", 0, backtrace=True)

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
        response = http_client.get_account_info(account)
        if 'value' in response['result']:
            if response['result']['value'] != None:
                if 'data' in response['result']['value']:
                    if(response['result']['value']['data'][0] != ""):
                        break
        accounts.append(account)
        populate_data(transactionID, account, "", 0, backtrace=True)
    return {"Transactions": transactions, "Accounts": accounts}

def get_account_info(address):
    wallet = address
    http_client = Client(api_link)
    response = http_client.get_account_info(wallet, encoding="jsonParsed")
    return response