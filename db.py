import mysql.connector

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
        )
        self.cursor = self.connection.cursor()
        self._init_db()

    def _init_db(self):
        self.cursor.execute("SHOW DATABASES")
        if ('password_manager',) not in self.cursor.fetchall():
            self.cursor.execute("CREATE DATABASE password_manager")
        self.connection.database = 'password_manager'

        self.cursor.execute("SHOW TABLES")
        if ('passwords',) not in self.cursor.fetchall():
            self.cursor.execute("""
                CREATE TABLE passwords (
                    id INT NOT NULL AUTO_INCREMENT,
                    przeznaczenie VARCHAR(30),
                    HASLO VARCHAR(30),
                    PRIMARY KEY (id)
                )
            """)
        self.connection.commit()

class Connection:
    def __init__(self):
        self._connection = None
        self._cursor = None

    def __enter__(self):
        self._connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='password_manager'
        )
        self._cursor = self._connection.cursor()
        return self._cursor, self._connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._connection:
            self._connection.commit()
            self._cursor.close()
            self._connection.close()