from objects.app import app

class EnvDetails(object):
    def __init__(self):

        envDefaults = app.settings.getEnvDef()

        self.elevation = envDefaults['Elevation']
        self.atm = envDefaults['Atm']
        self.FIO2 = envDefaults['FIO2']
        self.temp = envDefaults['Temp']
        self.rh = envDefaults['Rh']

        self.elevationUnit = app.settings.getUnitDef()['Elevation_unit']
        self.atmUnit = app.settings.getUnitDef()['ATM_unit']
        self.FIO2Unit = '%'
        self.tempUnit = app.settings.getUnitDef()['Temperature_unit']
        self.rhUnit = '%'

        # 0 = US SA
        # 1 = MAE
        self.pio2Method = 0

    def getDetails(self):
        return {
            'Elevation': self.elevation,
            'ATM': self.atm,
            'FIO2': self.FIO2,
            'Temperature': self.temp,
            'Rh': self.rh,
            'PiO2 Method': self.pio2Method,
            'Elevation_unit': self.elevationUnit,
            'ATM_unit': self.atmUnit,
            'FIO2_unit': self.FIO2Unit,
            'Temperature_unit': self.tempUnit,
            'Rh_unit': self.rhUnit
        }

    def setDetail(self, detail, value):
        if detail == 'Elevation':
            self.elevation = value
        elif detail == 'Elevation_unit':
            self.elevationUnit = value
        elif detail == 'ATM':
            self.atm = value
        elif detail == 'ATM_unit':
            self.atmUnit = value
        elif detail == 'FIO2':
            self.FIO2 = value
        elif detail == 'Temperature':
            self.temp = value
        elif detail == 'Temperature_unit':
            self.tempUnit = value
        elif detail == 'Rh':
            self.rh = value
        elif detail == 'PiO2 Method':
            self.pio2Method = value