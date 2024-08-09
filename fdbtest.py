import fdb

def create_connection():
    try:
        conn = fdb.connect(
            dsn='C:\\Users\\Jose\\Documents\\Code\\TimeTabling3.fdb',
            user='SYSDBA',
            password='horus163',
            sql_dialect=3, charset='UTF8'
        )
        return conn
    except fdb.Error as e:
        print(f"Error: {e}")
        return None
    
def test_connection(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM RDB$DATABASE')
        cursor.close()
        return True
    except fdb.Error:
        return False

def main():
    conn = create_connection()
    if conn is not None:
        print("Connection established successfully!")
        conn.close()

if __name__ == "__main__":
    main()