from flask import Flask, request, jsonify
from forwardtrace import *
from flask_cors import CORS, cross_origin
import psycopg2
import psycopg2.extras
import uuid
from psycopg2 import Error

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

@app.route("/address/<string:address>")
@cross_origin()
def get_info(address):
    return get_account_info(address)

#This function returns a 2D array of the blacklist table
@app.route("/get-blacklisted-accounts")
@cross_origin()
def blacklist_data():
    return show_blacklist()

@app.route('/blacklisted/', methods=['GET'])
def blacklist_api_call():
    account = request.args.get("account", None)
    response = {}
    if not account:
        response["err"] = "no account found"
    else:
        try:
            con = psycopg2.connect(
            host="localhost",
            database="badActors",
            user="postgres",
            password="postgres"
            )
            cur = con.cursor()
            cur.execute("select is_blacklisted from blacklist where accountwallet = %s", (account,))
            record = cur.fetchall()
            con.close()
            if len(record) == 0:
                response["err"] = "account not found"
            response["result"] = record[0][0]
        except(Exception, Error) as error:
            response["err"] = "error querying database"

    return jsonify(response)

@app.route('/blacklist/', methods=['GET'])
def blacklisted():
    try:
        con = psycopg2.connect(
            host="localhost",
            database="badActors",
            user="postgres",
            password="postgres"
        )
        cur = con.cursor()
        cur.execute("select accountwallet from blacklist;")
        blacklist = cur.fetchall()
        con.close()
        if len(blacklist) == 0:
            return jsonify({"err" : "empty database" })
        return jsonify({"result" : blacklist})
    except(Exception, Error) as error:
        return jsonify({"err" : "error querying database" })


if __name__ == '__main__':
    app.run()
