from flask import jsonify
import psycopg2
import psycopg2.extras
import uuid

def transaction_exists(txn):
    con = psycopg2.connect(
        host="localhost",
        database="badActors",
        user="postgres",
        password="postgres"
    )
    cur = con.cursor()
    cur.execute("select 1 from transactions where transaction_id = (%s);", (txn,))
    con.commit()
    con.close()
    if cur.fetchall is None:
        return False
    return True

def get_wallet_count(wallet):
    con = psycopg2.connect(
        host="localhost",
        database="badActors",
        user="postgres",
        password="postgres"
    )
    cur = con.cursor()
    cur.execute("select count(sender) from transactions where sender = (%s);", (wallet,))
    con.commit()
    result1 = cur.fetchone()
    cur.execute("select count(sender) from transactions where sender = (%s);", (wallet,))
    con.commit()
    result2 = cur.fetchone()
    return result1 + result2

#This methods takes dictionaries from the forward and bakcwards trace and populates the database
def populate_data(txn, sender, receiver, depth, backtrace):
    con = psycopg2.connect(
        host="localhost",
        database="badActors",
        user="postgres",
        password="postgres"
    )
    cur = con.cursor()
    psycopg2.extras.register_uuid()

    #Insert transaction if that transaction does not already exists
    if not transaction_exists(txn):
        if backtrace:
            cur.execute("insert into transactions (id, transaction_id, sender) values (%s,%s);",
                        (uuid.uuid4(), txn, sender))
        else:
            cur.execute("insert into transactions (id, transaction_id, sender, receiver, depth) values (%s,%s,%s,%d);",
            (uuid.uuid4(), txn, sender, receiver, depth))

    #If the transaction is from the backtrace, then immediately blacklist if that wallet does not exist in the blacklist
    if backtrace:
        if get_wallet_count(sender) == 0:
            cur.execute("insert into blacklist (accountwallet, is_blacklisted) values (%s, %s);", (sender, "true"))
        if get_wallet_count(receiver) == 0:
            cur.execute("insert into blacklist (accountwallet, is_blacklisted) values (%s, %s);", (receiver, "true"))

    #If the transaction is in the forward trace, then insert as not blacklisted if it does not exists
    else:
        if get_wallet_count(sender) == 0:
            cur.execute("insert into blacklist (accountwallet, is_blacklisted) values (%s, %s);", (sender, "false"))

        #If this wallet already exists in the blacklist, then we update the value to blacklisted
        else:
            if get_wallet_count(sender) > 1:
                cur.execute("update blacklist set (is_blacklisted) = (%s) where (accountwallet) = (%s);", ("true", sender))
        if get_wallet_count(receiver) == 0:
            cur.execute("insert into blacklist (accountwallet, is_blacklisted) values (%s, %s);", (receiver, "false"))
        else:
            if get_wallet_count(receiver) > 1:
                cur.execute("update blacklist set (is_blacklisted) = (%s) where (accountwallet) = (%s);", ("true", sender))

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
    cur.execute("select accountwallet from blacklist where is_blacklisted = true;")
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