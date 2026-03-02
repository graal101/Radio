#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import vlc
from PyQt6 import QtWidgets, uic
from PyQt6 import QtSql
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QTimer


class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.playlist = 'playlist_sqlite3/playlist.db'
        uic.loadUi('ui/main_radio.ui', self)
        self.createConnection()
        
        self.playButton.clicked.connect(self.on_playButton_click)

        self.tray_icon = QSystemTrayIcon(QIcon('ico/radio-in-a-rounded-square_icon-icons.com_70636.svg'), self)
        self.tray_icon.setToolTip('My Radio Tray App')

        tray_menu = QMenu()
        exit_action = QAction('Выход', self)
        exit_action.triggered.connect(self.exit_app)
        tray_menu.addAction(exit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.player = None
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_ui)

    def on_playButton_click(self):
        if not self.player:
            self.player = vlc.MediaPlayer("https://icecast-radonezh.cdnvideo.ru/rad128")
        self.player.play()
        self.timer.start()
        
    def update_ui(self):
        pass

    def createConnection(self):
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(self.playlist)

        query = QtSql.QSqlQuery()
        query.exec('''
            CREATE TABLE IF NOT EXISTS playlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                note TEXT NOT NULL
            )
        ''')

        print("База данных успешно создана или открыта.")
        
    def exit_app(self):
        if self.player:
            self.player.stop()
        QtWidgets.QApplication.quit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
