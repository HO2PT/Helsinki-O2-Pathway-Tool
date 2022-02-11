class WorkLoadDetails(object):
    def __init__(self,test):
        self.id = test.nWorkLoads()
        self.load = 0
        self.vo2 = 0
        self.hr = 0
        self.sv = 0
        self.q = 0
        self.hb = 0
        self.sao2 = 0
        self.cao2 = 0
        self.svo2 = 0
        self.cvo2 = 0
        self.cavo2 = 0
        self.qao2 = 0
        self.t = 0
        self.ph = 0
        self.pvo2 = 0
        self.do2 = 0

        self.load_unit = 0
        self.vo2_unit = 0
        self.hr_unit = 0
        self.sv_unit = 0
        self.q_unit = 0
        self.hb_unit = 0
        self.sao2_unit = 0
        self.cao2_unit = 0
        self.svo2_unit = 0
        self.cvo2_unit = 0
        self.cavo2_unit = 0
        self.qao2_unit = 0
        self.t_unit = 0
        self.ph_unit = 0
        self.pvo2_unit = 0
        self.do2_unit = 0

        # 0 = Measured
        # 1 = Calculated
        self.vo2_MC = 0
        self.hr_MC = 0
        self.sv_MC = 0
        self.q_MC = 0
        self.hb_MC = 0
        self.sao2_MC = 0
        self.cao2_MC = 0
        self.svo2_MC = 0
        self.cvo2_MC = 0
        self.cavo2_MC = 0
        self.qao2_MC = 0
        self.t_MC = 0
        self.ph_MC = 0
        self.pvo2_MC = 0
        self.do2_MC = 0

    def getWorkLoadDetails(self):
        return {
            'id': self.id,
            
            'Load': self.load,
            'Load_unit': self.load_unit,

            'VO2': self.vo2,
            'VO2_unit': self.vo2_unit,
            'VO2_MC': self.vo2_MC,

            'HR': self.hr,
            'HR_unit': self.hr_unit,
            'HR_MC': self.hr_MC,

            'Sv': self.sv,
            'Sv_unit': self.sv_unit,
            'Sv_MC': self.sv_MC,

            'Q': self.q,
            'Q_unit': self.q_unit,
            'Q_MC': self.q_MC,

            'Hb': self.hb,
            'Hb_unit': self.hb_unit,
            'Hb_MC': self.hb_MC,

            'SaO2': self.sao2,
            'SaO2_unit': self.sao2_unit,
            'SaO2_MC': self.sao2_MC,

            'CaO2': self.cao2,
            'CaO2_unit': self.cao2_unit,
            'CaO2_MC': self.cao2_MC,

            'SvO2': self.svo2,
            'SvO2_unit': self.svo2_unit,
            'SvO2_MC': self.svo2_MC,

            'CvO2': self.cvo2,
            'CvO2_unit': self.cvo2_unit,
            'CvO2_MC': self.cvo2_MC,

            'CavO2': self.cavo2,
            'CavO2_unit': self.cavo2_unit,
            'CavO2_MC': self.cavo2_MC,

            'QaO2': self.qao2,
            'QaO2_unit': self.qao2_unit,
            'QaO2_MC': self.qao2_MC,

            'T': self.t,
            'T_unit': self.t_unit,
            'T_MC': self.t_MC,

            'pH': self.ph,
            'pH_unit': self.ph_unit,
            'pH_MC': self.ph_MC,

            'pVO2': self.pvo2,
            'pVO2_unit': self.pvo2_unit,
            'pVO2_MC': self.pvo2_MC,

            'DO2': self.do2,
            'DO2_unit': self.do2_unit,
            'DO2_MC': self.do2_MC
        }