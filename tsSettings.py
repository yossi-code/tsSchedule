import fdb

class DatabaseConnector:
    def __init__(self):
        self.dsn = 'C:\\Users\\Jose\\Documents\\Code\\TimeTabling3.fdb'
        self.user = 'SYSDBA'
        self.password = 'horus163'
        self.connection = None
        self.charset = 'WIN1252'

    def connect(self):
        try:
            self.connection = fdb.connect(
                dsn=self.dsn,
                user=self.user,
                password=self.password,
                charset=self.charset
            )
            print("Connected to database successfully!")
        except fdb.Error as e:
            print(f"Error: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from database.")

    def execute_query(self, query, parameters=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, parameters)
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
            print(result)
            return result
        else:
            print("There was an error getting parameters!!")

    def get_parameter_weights(self, parameter_id, connector):
        query = "SELECT W00, W01, W02, W03, W04 FROM TABUSEARCHPARAMETERS WHERE ID = ?"
        result = connector.execute_query(query, (parameter_id,))
        if result:
            return result
        else:
            print("There was an error getting the parameter weights!!")

    def get_parameter_tabu(self, parameter_id, connector):
        query = "SELECT TABUSEARCH FROM TABUSEARCHPARAMETERS WHERE ID = ?"
        result = connector.execute_query(query, (parameter_id,))
        if result:
            return result
        else:
            print("There was an error getting the tabu parameter")
    
    def get_offers(self, connector):
        query = 'SELECT s."id" , s."idTeacher", s."idDiscipline", \
            d."acronym" , t."initials" FROM "LecturesOffers" s JOIN "Disciplines" d ON s."idDiscipline"  = d."id" JOIN "Teachers" t ON s."idTeacher" = t."id" '
        result = connector.execute_query(query)
        if result:
            return result
        else:
            print("There was an error getting offers!!")


def main():
    connector = DatabaseConnector()
    connector.connect()

    Utils.get_parameters(Utils, connector)
    Utils.get_parameter_weights(Utils, 1, connector)

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
