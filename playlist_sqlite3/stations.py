class Stations:
    """Класс настроек для радиостанций"""
    def __init__(self):
        self.station_names = {'Радонеж-128': 'https://icecast-radonezh.cdnvideo.ru/rad128',
                              'Teos': 'https://myradio24.org/radioteos', 
                              'Smoothjazz': 'http://smoothjazz.cdnstream1.com/2585_64.aac',
                              'Bootliquor-128': 'http://ice2.somafm.com/bootliquor-128-mp3',
                              'РетроФм-256': 'https://retro.hostingradio.ru:8043/retro256.mp3',
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
            
