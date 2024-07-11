import fdb
import random

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

    def execute_update(self, query, parameters=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, parameters)
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
        query = 'SELECT s."id", s."idTeacher", s."idDiscipline", \
            d."acronym", t."initials" FROM "LecturesOffers" s JOIN "Disciplines" d ON s."idDiscipline" = d."id" \
            JOIN "Teachers" t ON s."idTeacher" = t."id" WHERE s."idTeacher" BETWEEN 101 AND 179 OR s."idTeacher" BETWEEN 301 AND 372 \
            ORDER BY s."idTeacher" '
        result = connector.execute_query(query)
        if result:
            return result
        else:
            print("There was an error getting offers!!")

    def get_teacher_availability(self, connector):
        query = "SELECT teacher_id, day_of_week, slot FROM teacher_availability"
        availability_data = connector.execute_query(query)
        print("Got availability data!")
        return availability_data
    

def main():
    connector = DatabaseConnector()
    connector.connect()

    utils = Utils()

    slots = utils.get_teacher_availability(connector)
    slots_to_delete = {}

    for teacher_id, day_of_week, slot in slots:
        if teacher_id not in slots_to_delete:
            slots_to_delete[teacher_id] = []
        slots_to_delete[teacher_id].append((day_of_week, slot))

    delete_queries = []
    for teacher_id, slots in slots_to_delete.items():
        random.shuffle(slots)
        half_count = len(slots) // 2
        for day_of_week, slot in slots[:half_count]:
            delete_queries.append(f"DELETE FROM teacher_availability WHERE teacher_id = {teacher_id} AND day_of_week = {day_of_week} AND slot = {slot}")

    for query in delete_queries:
        connector.execute_update(query)

    print("Done! Queries deleted!")
    

    #Utils.get_parameters(Utils, connector)
    #Utils.get_parameter_weights(Utils, 1, connector)

    # query execution
    #query = "SELECT * FROM TABUSEARCHPARAMETERS"
    #result = connector.execute_query(query)
    #if result:
    #    print("Query result:", result)

    # update execution
    #for id_teacher in range(101, 180):
    #    for id_discipline in range(13, 92):
    #        insert_query = 'INSERT INTO "LecturesOffers" ("id", "idTeacher", "idDiscipline") VALUES (?, ?, ?)'
    #        connector.execute_update(insert_query, (id_value, id_teacher, id_discipline))
    #        id_value += 1

    # Define teacher ranges
    #teacher_ranges = [(101, 179), (301, 372)]

    # Generate availability data for all slots for each teacher
    #availability_data = []

    #for start_id, end_id in teacher_ranges:
     #   for teacher_id in range(start_id, end_id + 1):
      #      for day_of_week in range(5):  # Assuming 5 days in a week (0-4)
       #         for slot in range(7):     # Assuming 7 slots in a day (0-6)
        #            availability_data.append((teacher_id, day_of_week, slot))

    # Insert availability data into the database
    #for entry in availability_data:
     #   teacher_id, day_of_week, slot = entry
      #  connector.execute_update('''
       #     INSERT INTO teacher_availability (teacher_id, day_of_week, slot)
        #    VALUES (?, ?, ?)
        #''', (teacher_id, day_of_week, slot))



    # Close the connection
    connector.disconnect

if __name__ == "__main__":
    main()
