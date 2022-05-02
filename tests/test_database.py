import unittest
from sqlite3 import OperationalError

from src.database import DatabaseHandler


class TestDBHandlerMainMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = DatabaseHandler()

    def setUp(self) -> None:
        self.db.connect()
        self.db.create_object()
        self.test_uuid = "1234"

    def tearDown(self) -> None:
        del self.test_uuid
        self.db.delete_all()

    def test_create_table_in_database(self) -> None:
        self.db.add_object(guid=self.test_uuid,
                           object_type='button',
                           name='Кнопка')
        result = self.db.get_object(guid=self.test_uuid)
        self.assertIsInstance(result, tuple)
        self.assertTupleEqual(result[0], (1, self.test_uuid, 'button',
                                          'Кнопка', None, None, None))

    def test_delete_database(self) -> None:
        self.db.delete_all()
        self.assertRaises(OperationalError,
                          self.db.get_object,
                          guid="6666")

    def test_str(self) -> None:
        self.assertEqual(str(self.db),
                         "Connected to database in :memory:")

    def test_repr(self) -> None:
        self.assertEqual(repr(self.db),
                         "class DBHandler: paramstyle=named")


class TestDBHandlerMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = DatabaseHandler()

    def setUp(self) -> None:
        self.db.connect()
        self.db.create_object()
        self.db.add_object(guid="1111",
                           object_type="button")
        self.db.add_object(guid="2222",
                           object_type="fader")

    def tearDown(self) -> None:
        self.db.delete_all()

    def test_get_object(self) -> None:
        dbquery = self.db.get_object(guid="2222")
        self.assertIsInstance(dbquery, tuple)
        self.assertEqual(dbquery[0], (2, '2222', "fader",
                                      None, None, None, None))

    def test_add_object(self) -> None:
        dbquery = self.db.add_object(guid="3333",
                                     object_type="panel")
        self.assertEqual(dbquery, 'Ok')
