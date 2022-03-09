import psycopg2

# Connect to DB
con = psycopg2.connect(
            host = "localhost",
            database = "badActors",
            user = "postgres",
            password = "postgres"
)
# Cursor
cur = con.cursor()

cur.execute("insert into blacklist (accountwallet, transactions) values ('Jonathan','5678')")
con.commit()

# Close the connection
con.close()