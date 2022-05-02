import copy
import sqlite3
from sqlite3 import DatabaseError
from collections import namedtuple


class DatabaseConnectError(Exception):
    """
    Occurs when more than one connection to the database is created
    """


class DatabaseHandler:
    """
    Database handler.
    """

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DatabaseHandler, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self._uri = ":memory:"
        self.connection = None
        self.cur = None
        self._paramstyle = "named"
        self._threadsafety = 3

    def __str__(self) -> str:
        return f"Connected to database in {self._uri}"

    def __repr__(self) -> str:
        return f"class DBHandler: paramstyle={self._paramstyle}"

    def __del__(self):
        self.connection.close()

    def connect(self):
        self.connection = sqlite3.connect(self._uri)
        self.cur = self.connection.cursor()
        sqlite3.paramstyle = self._paramstyle

    @property
    def uri(self):
        """
        Database file name.

        Returns:
            (str)
        """
        return self._uri

    @uri.setter
    def uri(self, new_name):
        self._uri = new_name
        self.connect()

    @property
    def paramstyle(self):
        """
        Type of parameter marker formatting expected by the sqlite3 module.
        Required by the DB-API. Default value to "name".

        Returns:
            (str)
        """

        return self._paramstyle

    @paramstyle.setter
    def paramstyle(self, new_paramstyle):
        self._paramstyle = new_paramstyle
        self.connect()

    @property
    def db_config(self):
        """
        All config parameters.

        Returns:
            (namedtuple)
        """
        DBConfig = namedtuple('DBConfig', ['uri',
                                           'paramstyle'])
        return DBConfig(uri=self._uri,
                        paramstyle=self._paramstyle)

    @db_config.setter
    def db_config(self,
                  uri=":memory:",
                  paramstyle="named"):
        self._uri = uri
        self._paramstyle = paramstyle
        self.connect()

    def create_object(self) -> None:
        statement = '''CREATE TABLE IF NOT EXISTS ApolloObject (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guid TEXT UNIQUE NOT NULL,
                    object_type TEXT,
                    name TEXT,
                    state TEXT,
                    control TEXT,
                    config TEXT);'''
        cursor = self.connection.cursor()
        cursor.execute(statement)
        self.connection.commit()
        cursor.close()

    def delete_all(self) -> None:
        cursor = self.connection.cursor()
        cursor.execute('DROP TABLE IF EXISTS ApolloObject;')
        self.connection.commit()
        cursor.close()

    def get_object(self,
                   guid: str) -> tuple:
        cursor = self.connection.cursor()
        statement = '''SELECT *
                    FROM ApolloObject
                    WHERE guid = :guid;'''
        dbquery = cursor.execute(statement, {"guid": guid})
        return tuple(copy.deepcopy(dbquery.fetchall()))

    def add_object(self,
                   guid: str,
                   object_type: str = None,
                   name: str = None,
                   state: str = None,
                   control: str = None,
                   config: str = None) -> str:
        cursor = self.connection.cursor()
        statement = '''INSERT INTO ApolloObject (
                    guid,
                    object_type,
                    name,
                    state,
                    control,
                    config)
                    VALUES (:guid,
                            :object_type,
                            :name,
                            :state,
                            :control,
                            :config);'''
        try:
            cursor.execute(statement, {"guid": guid,
                                       "object_type": object_type,
                                       "name": name,
                                       "state": state,
                                       "control": control,
                                       "config": config})
        except DatabaseError as err:
            return f'Error {str(err)}'
        else:
            self.connection.commit()
            cursor.close()
            return 'Ok'

    def get_all(self) -> tuple:
        cursor = self.connection.cursor()
        statement = '''SELECT *
                    FROM ApolloObject;'''
        dbquery = cursor.execute(statement)
        return tuple(copy.deepcopy(dbquery.fetchall()))

    # def get_timetable(self,
    #                   name: str,
    #                   dnevnik_id: int,
    #                   date: str,
    #                   lesson_number: int) -> tuple:
    #     cursor = self.connection.cursor()
    #     statement = '''SELECT *
    #                 FROM Timetable
    #                 WHERE date = :date
    #                 AND lesson_number = :lesson_number
    #                 AND classes_id IN (SELECT id FROM Classes
    #                                   WHERE name = :name
    #                                   AND dnevnik_id = :dnevnik_id);'''
    #     dbquery = cursor.execute(statement, {"name": name,
    #                                          "dnevnik_id": dnevnik_id,
    #                                          "date": date,
    #                                          "lesson_number": lesson_number})
    #     result = tuple(copy.deepcopy(dbquery.fetchall()))
    #     cursor.close()
    #     return result

    # def add_timetable(self,
    #                   name: str,
    #                   dnevnik_id: int,
    #                   date: str,
    #                   lesson_number: int,
    #                   lesson_name: str,
    #                   lesson_room: str,
    #                   lesson_teacher: str,
    #                   lesson_time: str) -> str:
    #     cursor = self.connection.cursor()
    #     statement = '''INSERT INTO Timetable (
    #                 date,
    #                 lesson_number,
    #                 lesson_name,
    #                 lesson_room,
    #                 lesson_teacher,
    #                 lesson_time,
    #                 classes_id)
    #                 VALUES (:date, :lesson_number, :lesson_name,
    #                 :lesson_room, :lesson_teacher, :lesson_time,
    #                 (SELECT id FROM Classes
    #                 WHERE name = :name
    #                 AND dnevnik_id = :dnevnik_id));'''
    #     try:
    #         cursor.execute(statement, {"date": date,
    #                                    "lesson_number": lesson_number,
    #                                    "lesson_name": lesson_name,
    #                                    "lesson_room": lesson_room,
    #                                    "lesson_teacher": lesson_teacher,
    #                                    "lesson_time": lesson_time,
    #                                    "name": name,
    #                                    "dnevnik_id": dnevnik_id})
    #     except DatabaseError as err:
    #         return f'Error {str(err)}'
    #     else:
    #         self.connection.commit()
    #         cursor.close()
    #         return 'Ok'

    # def get_timetable_by_classes_and_date(self,
    #                                       name: str,
    #                                       date: str) -> tuple:
    #     Timetable = namedtuple('Timetable', ["id",
    #                                          "date",
    #                                          "lesson_number",
    #                                          "lesson_name",
    #                                          "lesson_room",
    #                                          "lesson_teacher",
    #                                          "lesson_time"])
    #     result = []
    #     cursor = self.connection.cursor()
    #     statement = '''SELECT *
    #                 FROM Timetable
    #                 WHERE date = :date
    #                 AND classes_id IN (SELECT id FROM Classes
    #                 WHERE name = :name);'''
    #     dbquery = cursor.execute(statement, {"date": date,
    #                                          "name": name})
    #     all_row = tuple(copy.deepcopy(dbquery.fetchall()))
    #     for row in all_row:
    #         result.append(Timetable(id=row[0],
    #                                 date=row[1],
    #                                 lesson_number=row[2],
    #                                 lesson_name=row[3],
    #                                 lesson_room=row[4],
    #                                 lesson_teacher=row[5],
    #                                 lesson_time=row[6]))
    #     self.connection.commit()
    #     cursor.close()
    #     return tuple(result)
