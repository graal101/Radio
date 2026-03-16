#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import vlc
from PyQt6 import QtWidgets, uic
from PyQt6 import QtSql
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QTimer

class Stations:
    """Класс настроек для радиостанций"""
    def __init__(self):
        self.station_names = {'Радонеж-128':'https://icecast-radonezh.cdnvideo.ru/rad128',
                              'Teos':'https://myradio24.org/radioteos', 
                              'Smoothjazz':'http://smoothjazz.cdnstream1.com/2585_64.aac',
                              'Bootliquor-128':'http://ice2.somafm.com/bootliquor-128-mp3',
                              'РетроФм-256':'https://retro.hostingradio.ru:8043/retro256.mp3',
                               # https://radiopotok-fm.ru/retrofm
                              }
        self.pos = 0
        self.keys = list(self.station_names.keys()) # Список названий станций(ключей)
        
    def upplay(self):
        if self.pos == (len(self.station_names) - 1):
            return self.keys[-1]
        else:
             self.pos += 1
             return self.keys[self.pos]
            
    def downplay(self):
        if self.pos == 0:
            return self.keys[0]
        else:
            self.pos -= 1
            return self.keys[self.pos]
            

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.playlist = 'playlist_sqlite3/playlist.db'
        uic.loadUi('ui/main_radio.ui', self)
        self.createConnection()
        
        self.playButton.clicked.connect(self.on_playButton_click)
        self.stopButton.clicked.connect(self.on_stopButton_click)
        self.pushUp.clicked.connect(self.on_pushUp_click)
        self.pauseDown.clicked.connect(self.on_pauseDown_click)
        
        self.tray_icon = QSystemTrayIcon(QIcon('ico/player_music_speaker_audio_sound_cassette_icon_225670.png'), self)
        self.tray_icon.setToolTip('Radio Tray')

        tray_menu = QMenu()
        stop_action = QAction('Стоп', self)
        exit_action = QAction('Выход', self)
        exit_action.triggered.connect(self.exit_app)
        stop_action.triggered.connect(self.on_stopButton_click)
        
        tray_menu.addAction(stop_action) #FIXME crash when no player 
        tray_menu.addAction(exit_action)
        
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.player = None
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_ui)
        
    def ststop(self, start_play=True):
        """Вспомогательная функция старт/плей"""
        if start_play == False:
            self.player.stop()
            self.timer.stop()
        else:
            self.player.play()
            self.timer.start()

    def on_playButton_click(self):
        if not self.player:
            self.player = vlc.MediaPlayer(stnm.station_names[stnm.keys[stnm.pos]])
        self.ststop()
        
    def on_stopButton_click(self):
        self.ststop(start_play=False)
        
    def on_pushUp_click(self):
        self.ststop(start_play=False)
        self.player = vlc.MediaPlayer(stnm.station_names[stnm.upplay()])
        self.statusbar.showMessage(stnm.keys[stnm.pos])
        self.ststop()
        
    def on_pauseDown_click(self):
        self.ststop(start_play=False)
        self.player = vlc.MediaPlayer(stnm.station_names[stnm.downplay()])
        self.statusbar.showMessage(stnm.keys[stnm.pos])
        self.ststop()
        
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

        
    def exit_app(self):
        if self.player:
            self.player.stop()
        QtWidgets.QApplication.quit()


if __name__ == '__main__':
    stnm = Stations()
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
