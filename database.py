from flask import jsonify
import psycopg2
import psycopg2.extras
import uuid

#This methods takes dictionaries from the forward and bakcwards trace and populates the database
def populate_data(txn, sender, receiver, depth, blacklist_flag):
    con = psycopg2.connect(
        host="localhost",
        database="badActors",
        user="postgres",
        password="postgres"
    )
    cur = con.cursor()
    psycopg2.extras.register_uuid()
    #Insert transaction if that transaction does not already exists
    cur.execute("insert into transactions (id, transaction_id, sender, receiver, depth) values (%s,%s,%s,%d);",
                (uuid.uuid4(), txn, sender, receiver, depth))

    #If the transaction is from the backtrace, then immediately flag
    if blacklist_flag:
        cur.execute("insert into blacklist (accountwallet, is_blacklisted) values (%s, %s);", (sender, "true"))
        cur.execute("insert into blacklist (accountwallet, is_blacklisted) values (%s, %s);", (receiver, "true"))

    #If the transaction is in the forward trace, then check if that account exists
    else:
        cur.execute("insert into transactions (id, transaction_id, sender, receiver, depth) values (%s,%s,%s);", (uuid.uuid4(),txn,sender, receiver, depth))
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