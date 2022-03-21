from objects.app import app
import uuid

class WorkLoadDetails(object):
    def __init__(self):
        testDefaults = app.settings.getTestDef()

        self.id = uuid.uuid1()
        self.Load = 0
        self.VO2 = 0
        self.HR = 0
        self.Sv = 0
        self.Q = 0
        self.Hb = 0
        self.SaO2 = 0
        self.CaO2 = 0
        self.SvO2 = 0
        self.CvO2 = 0
        self.CavO2 = 0
        self.QaO2 = 0
        self.T0 = testDefaults['Tc @ rest']
        self.pHrest = testDefaults['pH @ rest']
        # self.T = testDefaults['Tc\u209A\u2091\u2090\u2096']
        # self.pH = testDefaults['pH\u209A\u2091\u2090\u2096']
        self.T = testDefaults['Tc @ rest']
        self.pH = testDefaults['pH @ rest']
        self.PvO2 = 0
        self.DO2 = 0

        self.y = None
        self.y2 = None
        self.xi = None
        self.yi = None

        defUnits = app.settings.getUnitDef()

        self.Load_unit = defUnits['Load_unit']
        self.VO2_unit = defUnits['VO2_unit']
        self.HR_unit = defUnits['HR_unit']
        self.Sv_unit = defUnits['Sv_unit']
        self.Q_unit = defUnits['Q_unit']
        self.Hb_unit = defUnits['Hb_unit']
        self.SaO2_unit = defUnits['SaO2_unit']
        self.CaO2_unit = defUnits['CaO2_unit']
        self.SvO2_unit = defUnits['SvO2_unit']
        self.CvO2_unit = defUnits['CvO2_unit']
        self.CavO2_unit = defUnits['CavO2_unit']
        self.QaO2_unit = defUnits['QaO2_unit']
        self.T0_unit = defUnits['Tc @ rest_unit']
        self.T_unit = defUnits['Tc\u209A\u2091\u2090\u2096_unit']
        self.pHrest_unit = 0
        self.pH_unit = 0
        self.PvO2_unit = defUnits['PvO2_unit']
        self.DO2_unit = defUnits['DO2_unit']

        defMc = app.settings.getMcDef()

        # 0 = Measured
        # 1 = Calculated
        self.VO2_MC = defMc['VO2_mc']
        self.HR_MC = defMc['HR_mc']
        self.Sv_MC = defMc['Sv_mc']
        self.Q_MC = defMc['Q_mc']
        self.Hb_MC = defMc['Hb_mc']
        self.SaO2_MC = defMc['SaO2_mc']
        self.CaO2_MC = defMc['CaO2_mc']
        self.SvO2_MC = defMc['SvO2_mc']
        self.CvO2_MC = defMc['CvO2_mc']
        self.CavO2_MC = defMc['CavO2_mc']
        self.QaO2_MC = defMc['QaO2_mc']
        self.T0_MC = defMc['Tc @ rest_mc']
        self.T_MC = defMc['Tc\u209A\u2091\u2090\u2096_mc']
        self.pHrest_MC = defMc['pH @ rest_mc']
        self.pH_MC = defMc['pH\u209A\u2091\u2090\u2096_mc']
        self.PvO2_MC = defMc['PvO2_mc']
        self.DO2_MC = defMc['DO2_mc']

    def setUnit(self, label, unit):
        # print(f'UPDATING UNIT {label}, to {unit}')
        if label == 'Load_unit':
            self.Load_unit = unit

        if label == 'VO2_unit':
            self.VO2_unit = unit
 
        if label == 'HR_unit': 
            self.HR_unit = unit

        if label == 'Sv_unit':
            self.Sv_unit = unit
        
        if label == 'Q_unit': 
            self.Q_unit = unit

        if label == 'Hb_unit': 
            self.Hb_unit = unit

        if label == 'SaO2_unit': 
            self.SaO2_unit = unit
        
        if label == 'CaO2_unit': 
            self.CaO2_unit = unit

        if label == 'SvO2_unit':
            self.SvO2_unit = unit

        if label == 'CvO2_unit': 
            self.CvO2_unit = unit
        
        if label == 'CavO2_unit': 
            self.CavO2_unit = unit

        if label == 'QaO2_unit': 
            self.QaO2_unit = unit

        if label == 'Tc @ rest_unit': 
            self.T_unit = unit

        if label == 'Tc\u209A\u2091\u2090\u2096_unit': 
            self.T_unit = unit

        if label == 'PvO2_unit': 
            self.PvO2_unit = unit

        if label == 'DO2_unit': 
            self.DO2_unit = unit

    def setMC(self, label, value):
        # print('UPDATING MC')
        if label == 'VO2_MC':
            self.VO2_MC = value
 
        if label == 'HR_MC': 
            self.HR_MC = value

        if label == 'Sv_MC':
            self.Sv_MC = value
        
        if label == 'Q_MC': 
            self.Q_MC = value

        if label == 'Hb_MC': 
            self.Hb_MC = value

        if label == 'SaO2_MC': 
            self.SaO2_MC = value
        
        if label == 'CaO2_MC': 
            self.CaO2_MC = value

        if label == 'SvO2_MC':
            self.SvO2_MC = value

        if label == 'CvO2_MC': 
            self.CvO2_MC = value
        
        if label == 'CavO2_MC': 
            self.CavO2_MC = value

        if label == 'QaO2_MC': 
            self.QaO2_MC = value

        if label == 'T0_MC': 
            self.T_MC = value

        if label == 'T_MC': 
            self.T_MC = value

        if label == 'PvO2_MC': 
            self.PvO2_MC = value

        if label == 'DO2_MC': 
            self.DO2_MC = value

    def setValue(self, label, value):
        # print('UPDATING VALUE')
        if label == 'Load':
            self.Load = value

        if label == 'VO2':
            self.VO2 = value
 
        if label == 'HR': 
            self.HR = value

        if label == 'Sv':
            self.Sv = value
        
        if label == 'Q': 
            self.Q = value

        if label == 'Hb': 
            self.Hb = value

        if label == 'SaO2': 
            self.SaO2= value
        
        if label == 'CaO2': 
            self.CaO2 = value

        if label == 'SvO2':
            self.SvO2 = value

        if label == 'CvO2': 
            self.CvO2 = value
        
        if label == 'CavO2': 
            self.CavO2 = value

        if label == 'QaO2': 
            self.QaO2 = value

        if label == 'Tc @ rest': 
            self.T0 = value

        if label == 'Tc\u209A\u2091\u2090\u2096': 
            self.T = value

        if label == 'T': 
            self.T = value

        if label == 'pH': 
            self.pH = value

        if label == 'pH @ rest': 
            self.pHrest = value

        if label == 'pH\u209A\u2091\u2090\u2096': 
            self.pH = value

        if label == 'PvO2': 
            self.PvO2 = value

        if label == 'DO2': 
            self.DO2 = value

    def getWorkLoadDetails(self):
        return {
            'id': self.id,
            
            'Load': self.Load,
            'Load_unit': self.Load_unit,

            'VO2': self.VO2,
            'VO2_unit': self.VO2_unit,
            'VO2_MC': self.VO2_MC,

            'HR': self.HR,
            'HR_unit': self.HR_unit,
            'HR_MC': self.HR_MC,

            'Sv': self.Sv,
            'Sv_unit': self.Sv_unit,
            'Sv_MC': self.Sv_MC,

            'Q': self.Q,
            'Q_unit': self.Q_unit,
            'Q_MC': self.Q_MC,

            'Hb': self.Hb,
            'Hb_unit': self.Hb_unit,
            'Hb_MC': self.Hb_MC,

            'SaO2': self.SaO2,
            'SaO2_unit': self.SaO2_unit,
            'SaO2_MC': self.SaO2_MC,

            'CaO2': self.CaO2,
            'CaO2_unit': self.CaO2_unit,
            'CaO2_MC': self.CaO2_MC,

            'CvO2': self.CvO2,
            'CvO2_unit': self.CvO2_unit,
            'CvO2_MC': self.CvO2_MC,

            'CavO2': self.CavO2,
            'CavO2_unit': self.CavO2_unit,
            'CavO2_MC': self.CavO2_MC,

            'QaO2': self.QaO2,
            'QaO2_unit': self.QaO2_unit,
            'QaO2_MC': self.QaO2_MC,

            'SvO2': self.SvO2,
            'SvO2_unit': self.SvO2_unit,
            'SvO2_MC': self.SvO2_MC,

            'PvO2': self.PvO2,
            'PvO2_unit': self.PvO2_unit,
            'PvO2_MC': self.PvO2_MC,

            'T': self.T,
            'T_unit': self.T_unit,
            'T_MC': self.T_MC,

            'Tc @ rest': self.T0,
            'Tc @ rest_unit': self.T0_unit,
            'Tc @ rest_MC': self.T0_MC,

            'Tc\u209A\u2091\u2090\u2096': self.T,
            'Tc\u209A\u2091\u2090\u2096_unit': self.T_unit,
            'Tc\u209A\u2091\u2090\u2096_MC': self.T_MC,

            'pH @ rest': self.pHrest,
            'pH @ rest_unit': self.pHrest_unit,
            'pH @ rest_MC': self.pHrest_MC,

            'pH\u209A\u2091\u2090\u2096': self.pH,
            'pH\u209A\u2091\u2090\u2096_unit': self.pH_unit,
            'pH\u209A\u2091\u2090\u2096_MC': self.pH_MC,

            'pH': self.pH,
            'pH_unit': self.pH_unit,
            'pH_MC': self.pH_MC,

            'DO2': self.DO2,
            'DO2_unit': self.DO2_unit,
            'DO2_MC': self.DO2_MC
        }

    def getCoords(self):
        return {
            'y': self.y,
            'y2': self.y2,
            'xi': self.xi,
            'yi': self.yi
        }

    def setCalcResults(self, y, y2, xi, yi, VO2, Q, Hb, SaO2, CaO2, SvO2, CvO2, CavO2, QaO2, T0, T, pHrest, pH, PvO2, DO2):
        self.y = y
        self.y2 = y2
        self.xi = xi
        self.yi = yi
        self.VO2 = VO2
        #self.Sv = Sv
        self.Q = Q
        self.Hb = Hb
        self.SaO2 = SaO2
        self.CaO2 = CaO2
        self.SvO2 = SvO2
        self.CvO2 = CvO2
        self.CavO2 = CavO2
        self.QaO2 = QaO2
        self.T0 = T0
        self.T = T
        self.pHrest = pHrest
        self.pH = pH
        self.PvO2 = PvO2
        self.DO2 = DO2

    def resetValues(self):
        self.Q = 0
        self.CaO2 = 0
        self.SvO2 = 0
        self.CvO2 = 0
        self.CavO2 = 0
        self.QaO2 = 0
        self.PvO2 = 0
        self.DO2 = 0