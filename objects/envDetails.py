class EnvDetails(object):
    def __init__(self):
        self.elevation = 0
        self.atm = 0
        self.fio2 = 0
        self.temp = 0
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