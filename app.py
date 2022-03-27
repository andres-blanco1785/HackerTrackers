from flask import Flask, json, jsonify, request, Response
from dotenv import load_dotenv
from solana.rpc.api import Client
from backtrace import *
from database import *
from forwardtrace import *
import numpy as npy
import requests
import psycopg2
import os
from flask_cors import CORS, cross_origin
import json
import time
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
