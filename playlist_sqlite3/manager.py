from PyQt6 import QtSql

class Manager:
    def __init__(self):
        self.playlist = 'playlist_sqlite3/playlist.db'
        
    def createConnection(self):
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(self.playlist)
        print("Создание плейлиста.")
        if not self.db.open():
            print("Failed to open DB:", self.db.lastError().text())
            return

        query = QtSql.QSqlQuery()
        query.exec("""
            CREATE TABLE IF NOT EXISTS playlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                note TEXT NOT NULL
            )
        """)
        # self.db.close()
        # QtSql.QSqlDatabase.removeDatabase(self.db.connectionName())
