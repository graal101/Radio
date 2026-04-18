#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import vlc
from vlc import Meta
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QStandardItemModel, QStandardItem

from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QFontDialog

from playlist_sqlite3.stations import Stations
from playlist_sqlite3.manager import Manager

# Названия треков онлайн!

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi('ui/main_radio.ui', self)
        
        self.playButton.clicked.connect(self.on_playButton_click)
        self.stopButton.clicked.connect(self.on_stopButton_click)
        self.pushQuit.clicked.connect(self.exit_app)
        self.pushUp.clicked.connect(self.on_pushUp_click)
        self.pauseDown.clicked.connect(self.on_pauseDown_click)
        self.tableView.doubleClicked.connect(self.on_table_double_click)
        self.mn_quit.triggered.connect(self.exit_app)
        self.mn_font.triggered.connect(self.choose_font)
        
        self.tray_icon = QSystemTrayIcon(QIcon('ico/player_music_speaker_audio_sound_cassette_icon_225670.png'), self)
        self.tray_icon.setToolTip('Radio Tray')

        tray_menu = QMenu()
        self.stop_action = QAction('Стоп', self)
        self.exit_action = QAction('Выход', self)
        self.exit_action.triggered.connect(self.exit_app)
        self.stop_action.triggered.connect(self.on_stopButton_click)
        
        
        tray_menu.addAction(self.stop_action)
        tray_menu.addAction(self.exit_action)
        self.grid_show()
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.stop_action.setEnabled(False)
        self.player = None
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_ui)
        
        sql3 = Manager()
        sql3.createConnection()
        
# -------- В отдельный модуль --------------------------
    def ststop(self, start_play=True):
        """Вспомогательная функция старт/плей"""
        if not start_play:
            self.player.stop()
            self.timer.stop()
        else:
            self.player.play()
            self.timer.start()
            
    def buttons_on(self):
        """Делает активными кнопки после старта"""
        self.pauseDown.setEnabled(True)
        self.pushUp.setEnabled(True)
        self.stopButton.setEnabled(True)
        self.stop_action.setEnabled(True)
        
    def grid_show(self):
        self.model = QStandardItemModel()
        self.tableView.setModel(self.model)
        self.model.setHorizontalHeaderLabels(['Имя'])
        for row, value in enumerate(stnm.keys):
            self.model.setItem(row, 0, QStandardItem(str(value)))
        

# ----------------------------------------------------------
    def choose_font(self):
        """Выбор шрифта для таблички"""
        font, ok = QFontDialog.getFont()
        if ok:
            self.tableView.setFont(font)

    def on_table_double_click(self, index):
        """Выбор станций из ячейки таблицы"""
        row_number = index.row()
        stnm.pos = row_number
        st_name = stnm.keys[row_number]
        
        if not self.player:
            # Если нет ещё активного проигрывателя
            self.player = vlc.MediaPlayer(stnm.station_names[st_name])
            self.statusbar.showMessage(st_name)
            self.ststop()
            self.buttons_on()
            return
        
        self.ststop(start_play=False)
        self.statusbar.showMessage(st_name)
        self.player = vlc.MediaPlayer(stnm.station_names[st_name])
        self.ststop()

    def on_playButton_click(self):
        if not self.player:
            self.player = vlc.MediaPlayer(stnm.station_names[stnm.keys[stnm.pos]])
        self.ststop()
        self.buttons_on()
        
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

    def exit_app(self):
        if self.player:
            self.player.stop()
        QtWidgets.QApplication.quit()


if __name__ == '__main__':
    stnm = Stations() # Перенести
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
