from flask import Flask
from dotenv import load_dotenv
from forwardtrace import *
from flask_cors import CORS, cross_origin
load_dotenv()

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

class TraceData:
    def __init__(self, transactions, accounts):
        self.transactions = []
        self.accounts = []

@app.route("/forwards-trace/<string:transactionID>")
@cross_origin()
def forwardstrace(transactionID):
    return get_Data(transactionID)

@app.route("/fin_transaction/<string:transID>")
@cross_origin()
def get_backtrace(transID):
    return get_final_transaction(transID)

#This function returns a 2D array of the blacklist table
@app.route("/get-blacklisted-accounts")
@cross_origin()
def blacklist_data():
    return show_blacklist()


if __name__ == '__main__':
    app.run()
