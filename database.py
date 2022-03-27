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

#This methods takes dictionaries from the forward and bakcwards trace and populates the database
def populate_data(txn, wallet, blacklist_flag):
    con = psycopg2.connect(
        host="localhost",
        database="badActors",
        user="postgres",
        password="postgres"
    )
    cur = con.cursor()
    psycopg2.extras.register_uuid()
    if blacklist_flag:
        cur.execute("insert into transactions (id, transaction_id, accountwallet) values (%s,%s,%s);", (uuid.uuid4(),txn,wallet))
        cur.execute("insert into blacklist (accountwallet, is_blacklisted) values (%s, %s);", (wallet, "true"))
    else:
        cur.execute("insert into transactions (id, transaction_id, accountwallet) values (%s,%s,%s);", (uuid.uuid4(),txn,wallet))
    con.commit()
    con.close()
    return

def show_blacklist():
    con = psycopg2.connect(
        host="localhost",
        database="badActors",
        user="postgres",
        password="postgres"
    )
    cur = con.cursor()
    cur.execute("select accountwallet from blacklist;")
    con.commit()
    blacklist = cur.fetchall()
    blacklistJSON = []
    for account in blacklist:
        cur.execute("select transaction_id from transactions where accountwallet = (%s);", (account))
        con.commit()
        txns = cur.fetchall()
        blacklistJSON.append({
            "account": account,
            "transactions": txns
        })
    con.close()
    return jsonify({"blacklistedAccounts" : blacklistJSON})