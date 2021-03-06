from backtrace import *
import json

api_link = "https://ssc-dao.genesysgo.net/"

class TraceData:
    def __init__(self, transactions, accounts):
        self.transactions = []
        self.accounts = []

def get_suspicious_accounts(transactionID, currentaccount, level): # this functions returns list of accounts which received SOL/tokens within a transaction
    finaldata = TraceData([], [])
    http_client = Client(api_link)
    accounts = []
    transactions = []
    response = http_client.get_transaction(transactionID)
    if 'error' in response:
        return finaldata
    result = response.get("result")
    if result is None:
        return finaldata
    meta = result.get("meta")
    errcode = meta.get("err")
    if errcode is not None:
        return finaldata
    postBalances = meta.get("postBalances")
    preBalances = meta.get("preBalances")
    posttokenbal = meta.get("postTokenBalances")
    pretokenbal = meta.get("preTokenBalances")
    accountKeys = result.get("transaction").get("message").get("accountKeys")
    # check to make sure who gained tokens or sol is not currentaccount, if not on level 0
    # if current account did not gain tokens/sol, add receiving accounts to array
    for i in range(0, len(postBalances)):
        if postBalances[i] - preBalances[i] > 0:
            if level > 0:
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
            if level > 0:
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
                    if level > 0:
                        if (currentaccount == accountvalue.get("data").get("parsed").get("info").get("owner") ):
                            finaldata.accounts = []
                            finaldata.transactions = []
                            return finaldata
                    accounts += [ accountvalue.get("data").get("parsed").get("info").get("owner") ]
    accounts = list(set(accounts))
    if level > 0:
        for y in range(0, len(accounts)):
            transactions += [(transactionID, currentaccount, accounts[y], level)]
    finaldata.accounts = accounts
    finaldata.transactions = transactions
    return finaldata

def get_trace_data(transID, level, currentaccount):
    http_client = Client(api_link)
    curlevel = level
    transactions = []
    accounts = []
    finaldata = TraceData([], [])
    if curlevel >=3:
        finaldata.accounts = accounts
        finaldata.transactions = transactions
        return finaldata
    # if level 3 has not been reached, analyze accounts found in transaction to find more transactions/branches
    response = http_client.get_signatures_for_address(currentaccount, until=transID)
    transactionlist = response["result"]
    transactionlist.reverse()
    if len(transactionlist) == 1000:
        return finaldata
    rangetransactions = 5
    if len(transactionlist)<=5:
        rangetransactions = len(transactionlist)
    for i in range(0, rangetransactions):
        transaction = transactionlist[i]
        result = get_suspicious_accounts(transaction["signature"], currentaccount, curlevel)
        transactions += result.transactions
        accounts += result.accounts
        if curlevel+1 <3:
            for f in range(0, len(result.accounts)):
                curtrace = get_trace_data(transaction["signature"], curlevel + 1, result.accounts[f])
                transactions += curtrace.transactions
                accounts += curtrace.accounts
    finaldata.transactions = transactions
    finaldata.accounts = accounts
    return finaldata

def get_Data(transactionID):
    http_client = Client(api_link)

    separation_level = 0
    initialdata = get_suspicious_accounts(transactionID, "none", separation_level)
    if len(initialdata.accounts) == 0:
        return "Bad Request", 400
    transactions = []
    accounts = []
    accounts+=initialdata.accounts
    separation_level+=1
    for z in range(0, len(initialdata.accounts)):
        response = http_client.get_signatures_for_address(initialdata.accounts[z], until=transactionID)
        transactionlist = response.get("result")
        transactionlist.reverse()
        if len(transactionlist) == 1000:
            continue
        lookuprange = 5
        if len(transactionlist) <= 5:
            lookuprange = len(transactionlist)
        for i in range(0, lookuprange): # this level adds first level of transactions
            transaction = transactionlist[i]
            result = get_suspicious_accounts(transaction["signature"], initialdata.accounts[z], separation_level)
            # adds first level of transaction
            transactions += result.transactions
            accounts += result.accounts
            for g in range(0, len(result.accounts)): # adds 2nd++ level of transactions
                curtrace = get_trace_data(transaction["signature"], separation_level+1, result.accounts[g])
                transactions += curtrace.transactions
                accounts += curtrace.accounts

    accounts = list(set(accounts))

    dictionary = {
        "Transactions": transactions, # array(tuple(transhash, sender, receiver, depth))
        "Accounts": accounts #
    }

    for i in range(len(transactions)):
        populate_data(transactions[i][0], transactions[i][1], transactions[i][2], transactions[i][3], backtrace=False)

    json_object = json.dumps(dictionary, indent=3)

    return dictionary