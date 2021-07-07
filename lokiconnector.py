import pymysql.cursors
import re

class LokiConnector:
    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                          user="db",
                                          password="db",
                                          cursorclass=pymysql.cursors.DictCursor)

    def insert_char(self, name):
        if not self.char_in_table(name):
            sql_statement = f"INSERT INTO characters (character_name) VALUES (%s)"
            self.execute(sql_statement, name)

    def insert_place(self, place_id, place_name):
        if not self.place_in_table(place_id):
            sql_statement = f"INSERT INTO places (place_id, place_name) VALUES (%s, %s)"
            self.execute(sql_statement, (place_id, place_name))

    def insert_scenes(self, scene_id):
        if not self.scene_in_table(scene_id):
            sql = "INSERT into scenes VALUES (%s)"
            self.execute(sql, scene_id)

    def insert_place_scene(self, scene_id, place_id):

        sql = "INSERT INTO scenes_has_places VALUES (%s, %s)"
        self.execute(sql, (scene_id, place_id))

    def insert_line(self, line_id, text, type, char_id, scene_id):
        line = f"INSERT INTO loki.lines (line_id, text, type) VALUES (%s, %s, %s)"
        line_char = f"INSERT INTO loki.lines_has_characters (line_id, character_id) VALUES (%s, %s)"
        line_place = f"INSERT INTO lines_has_scenes(line_id, scene_id) VALUES (%s, %s)"
        self.execute(line, (line_id, text, type))
        self.connection.commit()

        self.execute(line_char, (line_id, char_id))

        if (self.scene_in_table(scene_id)):
            self.execute(line_place, (line_id, scene_id))
        else:
            print("could not enter")

    def insert_switch(self, scene_id, old_id, new_id):
        sql = "INSERT INTO switches VALUES (%s, %s, %s)"
        self.execute(sql, (scene_id, old_id, new_id))

    """ aggregate functions """

    def get_all_characters(self):
        sql = "SELECT * FROM characters"
        return self.query(sql, ())

    """ checks in values are in the table """

    def char_in_table(self, name):
        sql = "SELECT * from characters WHERE character_name = %s"

        return len(self.query(sql, name)) >= 1

    def place_in_table(self, place_id):
        sql = "SELECT * FROM places where place_id = %s"
        return len(self.query(sql, place_id)) >= 1

    def scene_in_table(self, scene_id):
        sql = "SELECT * FROM scenes where scene_id = %s"
        return len(self.query(sql, scene_id)) >= 1

    """ returns ids """

    def character_id(self, name):
        sql = "SELECT character_id FROM characters WHERE character_name = %s"
        if self.char_in_table(name):
            return self.query_one(sql, name)["character_id"]
        else:
            return -1

    """ performs query """

    def execute(self, statement, arguments=()):
        with self.connection.cursor() as cursor:
            cursor.execute(statement, arguments)
        self.connection.commit()

    def query(self, statement, arguments=()):
        with self.connection.cursor() as cursor:
            cursor.execute(statement, arguments)
            result = cursor.fetchall()
            return result

    def query_one(self, statement, arguments=()):
        with self.connection.cursor() as cursor:
            cursor.execute(statement, arguments)
            result = cursor.fetchone()
            return result

    """sets up the database"""

    def exec_sql_file(self):
        sql_file = "/Users/juliecorfman/lokigenerator/loki_database.sql"

        print("\n[INFO] Executing SQL script file: '%s'" % (sql_file))
        statement = ""

        for line in open(sql_file):
            if re.match(r"--", line):  # ignore sql comment lines
                continue
            if not re.search(r';$', line):  # keep appending lines that don't end in ';'
                statement = statement + line
            else:  # when you get a line ending in ';' then exec statement and reset for next statement
                statement = statement + line
                # print "\n\n[DEBUG] Executing SQL statement:\n%s" % (statement)
                try:
                    self.connection.cursor().execute(statement)
                except (Exception) as e:
                    print("\n[WARN] MySQLError during execute statement \n\tArgs: '%s'" % (str(e.args)))

                statement = ""

        self.connection.db = "loki"

    """ closes connection """

    def close(self):
        self.connection.close()
