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
    if cur.fetchone() is None:
        con.close()
        return False
    con.close()
    return True

def wallet_exists(wallet):
    con = psycopg2.connect(
        host="localhost",
        database="badActors",
        user="postgres",
        password="postgres"
    )
    cur = con.cursor()
    cur.execute("select 1 from blacklist where accountwallet = (%s);", (wallet,))
    con.commit()
    if cur.fetchone() is None:
        con.close()
        return False
    con.close()
    return True

def get_wallet_count(wallet):
    con = psycopg2.connect(
        host="localhost",
        database="badActors",
        user="postgres",
        password="postgres"
    )
    cur = con.cursor()
    cur.execute("select count(*) from transactions where sender = (%s);", (wallet,))
    result1 = cur.fetchone()
    sum = 0
    for r in result1:
        sum += r
    cur.execute("select count(*) from transactions where receiver = (%s);", (wallet,))
    result2 = cur.fetchone()
    for r in result2:
        sum += r
    con.commit()
    con.close()
    return sum

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
            cur.execute("insert into transactions (id, transaction_id, sender) values (%s,%s,%s);",
                        (uuid.uuid4(), txn, sender))
        else:
            cur.execute("insert into transactions (id, transaction_id, sender, receiver, depth) values (%s,%s,%s,%s,%s);",
            (uuid.uuid4(), txn, sender, receiver, depth))

    #If the transaction is from the backtrace, then immediately blacklist if that wallet does not exist in the blacklist
    if backtrace:
        if get_wallet_count(sender) == 0:
            cur.execute("insert into blacklist (accountwallet, is_blacklisted) values (%s, %s);", (sender, "true"))

    #If the transaction is in the forward trace, then insert as not blacklisted if it does not exists
    else:
        if get_wallet_count(sender) == 0 and not wallet_exists(sender):
            cur.execute("insert into blacklist (accountwallet, is_blacklisted) values (%s, %s);", (sender, "false"))

        #If this wallet already exists in the blacklist, then we update the value to blacklisted
        else:
            if get_wallet_count(sender) > 0:
                cur.execute("update blacklist set is_blacklisted = true where (accountwallet) = (%s);", (sender,))
        if get_wallet_count(receiver) == 0 and not wallet_exists(receiver):
            cur.execute("insert into blacklist (accountwallet, is_blacklisted) values (%s, %s);", (receiver, "false"))
        else:
            if get_wallet_count(receiver) > 0:
                cur.execute("update blacklist set is_blacklisted = true where (accountwallet) = (%s);", (receiver,))

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
        txns = []
        cur.execute("select transaction_id from transactions where sender = (%s);", (account))
        con.commit()
        txns += cur.fetchall()
        cur.execute("select transaction_id from transactions where receiver = (%s);", (account))
        con.commit()
        blacklistJSON.append({
            "account": account,
            "transactions": txns
        })
    con.close()
    return jsonify({"blacklistedAccounts" : blacklistJSON})