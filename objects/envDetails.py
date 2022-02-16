from objects.app import app

class EnvDetails(object):
    def __init__(self):

        envDefaults = app.settings.getEnvDef()

        self.elevation = envDefaults['elevation']
        self.atm = envDefaults['atm']
        self.fio2 = envDefaults['fio2']
        self.temp = envDefaults['temp']
        # 0 = US SA
        # 1 = MAE
        self.pio2Method = 0

    def getDetails(self):
        return {
            'elev': self.elevation,
            'atm': self.atm,
            'fio2': self.fio2,
            'temp': self.temp,
            'pio2Method': self.pio2Method
        }