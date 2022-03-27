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
def populate_data(txn, wallet):
    con = psycopg2.connect(
        host="localhost",
        database="badActors",
        user="postgres",
        password="postgres"
    )
    cur = con.cursor()
    cur.execute("insert into blacklist (transaction_id, accountwallet) values (%s,%s);", (txn,wallet))
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
    cur.execute("select * from blacklist")
    con.commit()
    blacklist = cur.fetchall()
    con.close()

    blacklistJSON = []
    for account in blacklist:
        blacklistJSON.append({
            "account": account[1],
            "transactions": account[0]
        })

    return jsonify({"blacklistedAccounts" : blacklistJSON})