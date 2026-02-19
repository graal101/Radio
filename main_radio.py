#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  main_radio.py
#  Радио онлайн
#  
# 
import sys
from PyQt6 import QtWidgets, uic
from PyQt6 import QtSql
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu#, QAction
from PyQt6.QtGui import QAction
from PyQt6.QtGui import QIcon


class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.playlist = 'playlist_sqlite3/playlist.db'
        uic.loadUi('ui/main_radio.ui', self)
        self.createConnection()

        # Настройка иконки в трей
        self.tray_icon = QSystemTrayIcon(QIcon('ico/radio-in-a-rounded-square_icon-icons.com_70636.svg'), self)
        self.tray_icon.setToolTip('My Radio Tray App')
        
        # Создание контекстного меню для трей и добавление действий
    
        tray_menu = QMenu()
        exit_action = QAction('Выход', self)
        exit_action.triggered.connect(self.exit_app)
        tray_menu.addAction(exit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        
        self.tray_icon.show()
        
    def createConnection(self):
        """Создание плейлиста базы если не существует."""
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(self.playlist)

        # Создание таблицы, если она не существует
        query = QtSql.QSqlQuery()
        query.exec('''
            CREATE TABLE IF NOT EXISTS playlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                note TEXT NOT NULL
            )
        ''')

        print("База данных успешно создана или открыта.")
        
    def exit_app(self):
        QtWidgets.QApplication.quit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
''' 
import vlc
import time
p = vlc.MediaPlayer("https://icecast-radonezh.cdnvideo.ru/rad128")
p.play()
while True:
    time.sleep(1)
'''
