from objects.app import app

class EnvDetails(object):
    def __init__(self):

        envDefaults = app.settings.getEnvDef()

        self.elevation = envDefaults['elevation']
        self.atm = envDefaults['atm']
        self.fio2 = envDefaults['fio2']
        self.temp = envDefaults['temp']

        self.elevationUnit = app.settings.getUnitDef()['Elevation_unit']
        self.atmUnit = app.settings.getUnitDef()['ATM_unit']
        self.fio2Unit = app.settings.getUnitDef()['Elevation_unit']
        self.tempUnit = app.settings.getUnitDef()['Temperature_unit']

        # 0 = US SA
        # 1 = MAE
        self.pio2Method = 0

    def getDetails(self):
        return {
            'elevation': self.elevation,
            'atm': self.atm,
            'fio2': self.fio2,
            'temp': self.temp,
            'pio2Method': self.pio2Method,
            'Elevation_unit': self.elevationUnit,
            'ATM_unit': self.atmUnit,
            'FiO2_unit': self.fio2Unit,
            'Temp_unit': self.tempUnit,
        }

    def setDetail(self, detail, value):
        if detail == 'Elevation_unit':
            self.elevationUnit = value
        elif detail == 'ATM_unit':
            self.atmUnit = value
        elif detail == 'Temperature_unit':
            self.tempUnit = value