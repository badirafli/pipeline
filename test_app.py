import unittest
from app import get_db_connection, create_user, read_users, update_user, delete_user, close_connection

class TestCRUD(unittest.TestCase):

    def setUp(self):
        # Membuka koneksi database untuk setiap uji coba
        self.conn = get_db_connection()
        # Membuat tabel users sebelum uji coba
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )''')
        self.conn.commit()

    def tearDown(self):
        # Membersihkan database dengan menghapus tabel users
        cursor = self.conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS users')
        self.conn.commit()
        # Menutup koneksi database setelah setiap uji coba
        close_connection(self.conn)

    def test_create_user(self):
        create_user(self.conn, "Alice", 30)
        users = read_users(self.conn)
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]['name'], "Alice")
        self.assertEqual(users[0]['age'], 30)

    def test_update_user(self):
        create_user(self.conn, "Alice", 30)
        update_user(self.conn, 1, "Alice Updated", 31)
        users = read_users(self.conn)
        self.assertEqual(users[0]['name'], "Alice Updated")
        self.assertEqual(users[0]['age'], 31)

    def test_delete_user(self):
        create_user(self.conn, "Alice", 30)
        delete_user(self.conn, 1)
        users = read_users(self.conn)
        self.assertEqual(len(users), 0)

if __name__ == "__main__":
    unittest.main()
