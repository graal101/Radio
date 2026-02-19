#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  main_radio.py
#  Радио онлайн
#  
#  
import vlc
import time
p = vlc.MediaPlayer("https://icecast-radonezh.cdnvideo.ru/rad128")
p.play()
while True:
    time.sleep(1)
