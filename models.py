import psycopg2

con = psycopg2.connect(
        host="localhost",
        database="badActors",
        user="postgres",
        password="postgres"
    )

cur = con.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS blacklist (accountwallet text PRIMARY KEY,'
                                 'is_blacklisted boolean NOT NULL);'
                                 )

cur.execute('CREATE TABLE IF NOT EXISTS transactions (id text PRIMARY KEY,'
                                 'transaction_id text NOT NULL,'
                                 'accountwallet text NOT NULL);'
                                 )

cur.commit()
con.close()
