import psycopg2

def get_connection(user_id=None):
    conn = psycopg2.connect(
        host = "localhost",
        database = "kutuphane",
        user = "postgres",
        password = "postgres",
        port = 5432
    )

    if user_id is not None:
        cur = conn.cursor()
        cur.execute("Set application.user_id = %s;", (user_id,))
        cur.close()
    
    return conn


