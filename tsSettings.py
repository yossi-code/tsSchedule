import fdb

class DatabaseConnector:
    def __init__(self):
        self.dsn = 'C:\\Users\\Jose\\Documents\\Code\\TimeTabling3.fdb'
        self.user = 'SYSDBA'
        self.password = 'horus163'
        self.connection = None

    def connect(self):
        try:
            self.connection = fdb.connect(
                dsn=self.dsn,
                user=self.user,
                password=self.password
            )
            print("Connected to database successfully!")
        except fdb.Error as e:
            print(f"Error: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from database.")

    def execute_query(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except fdb.Error as e:
            print(f"Error executing query: {e}")
            return None

    def execute_update(self, query, offer):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, offer)
            self.connection.commit()
            cursor.close()
            print("Update successful.")
        except fdb.Error as e:
            print(f"Error executing update: {e}")

class Utils:
    def get_parameters(self, connector):
        query = "SELECT * FROM TABUSEARCHPARAMETERS"
        result = connector.execute_query(query)
        if result:
            return result
        else:
            print("There was an error getting parameters!!")
    
    def get_offers(self, connector):
        query = "SELECT * FROM TABUSEARCHOFFERS"
        result = connector.execute_query(query)
        if result:
            return result
        else:
            print("There was an error getting offers!!")


def main():
    connector = DatabaseConnector()
    connector.connect()

    # query execution
    #query = "SELECT * FROM TABUSEARCHPARAMETERS"
    #result = connector.execute_query(query)
    #if result:
    #    print("Query result:", result)

    # update execution
    #for offer in offers_data:
    #    update_query = "INSERT INTO TABUSEARCHOFFERS (ID, Subject, Professor) VALUES (?, ?, ?)"
    #    connector.execute_update(update_query, offer)

    connector.disconnect()

if __name__ == "__main__":
    main()
