from flask import Flask
from dotenv import load_dotenv
from forwardtrace import *
from flask_cors import CORS
load_dotenv()

app = Flask(__name__)
CORS(app)

class TraceData:
    def __init__(self, transactions, accounts):
        self.transactions = []
        self.accounts = []

@app.route("/forwards-trace/<string:transactionID>")
def forwardstrace(transactionID):
    return get_Data(transactionID)

@app.route("/fin_transaction/<string:transID>")
def get_backtrace(transID):
    return get_final_transaction(transID)

#This function returns a 2D array of the blacklist table
@app.route("/get-blacklisted-accounts")
def blacklist_data():
    return show_blacklist()


if __name__ == '__main__':
    app.run()
