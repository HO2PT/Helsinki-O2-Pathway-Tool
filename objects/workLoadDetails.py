class WorkLoadDetails(object):
    def __init__(self,test):
        self.id = test.nWorkLoads()
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
        self.T = 0
        self.pH = 0
        self.pVO2 = 0
        self.DO2 = 0

        self.Load_unit = 0
        self.VO2_unit = 0
        self.HR_unit = 0
        self.Sv_unit = 0
        self.Q_unit = 0
        self.Hb_unit = 0
        self.SaO2_unit = 0
        self.CaO2_unit = 0
        self.SvO2_unit = 0
        self.CvO2_unit = 0
        self.CavO2_unit = 0
        self.QaO2_unit = 0
        self.T_unit = 0
        self.pH_unit = 0
        self.pVO2_unit = 0
        self.DO2_unit = 0

        # 0 = Measured
        # 1 = Calculated
        self.VO2_MC = 0
        self.hr_MC = 0
        self.Sv_MC = 0
        self.Q_MC = 0
        self.Hb_MC = 0
        self.SaO2_MC = 0
        self.CaO2_MC = 0
        self.SvO2_MC = 0
        self.CvO2_MC = 0
        self.CavO2_MC = 0
        self.QaO2_MC = 0
        self.T_MC = 0
        self.pH_MC = 0
        self.pVO2_MC = 0
        self.DO2_MC = 0

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
            'HR_MC': self.hr_MC,

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

            'SvO2': self.SvO2,
            'SvO2_unit': self.SvO2_unit,
            'SvO2_MC': self.SvO2_MC,

            'CvO2': self.CvO2,
            'CvO2_unit': self.CvO2_unit,
            'CvO2_MC': self.CvO2_MC,

            'CavO2': self.CavO2,
            'CavO2_unit': self.CavO2_unit,
            'CavO2_MC': self.CavO2_MC,

            'QaO2': self.QaO2,
            'QaO2_unit': self.QaO2_unit,
            'QaO2_MC': self.QaO2_MC,

            'T': self.T,
            'T_unit': self.T_unit,
            'T_MC': self.T_MC,

            'pH': self.pH,
            'pH_unit': self.pH_unit,
            'pH_MC': self.pH_MC,

            'pVO2': self.pVO2,
            'pVO2_unit': self.pVO2_unit,
            'pVO2_MC': self.pVO2_MC,

            'DO2': self.DO2,
            'DO2_unit': self.DO2_unit,
            'DO2_MC': self.DO2_MC
        }