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
            
            'load': self.load,
            'load_unit': self.load_unit,

            'vo2': self.vo2,
            'vo2_unit': self.vo2_unit,
            'vo2_MC': self.vo2_MC,

            'hr': self.hr,
            'hr_unit': self.hr_unit,
            'hr_MC': self.hr_MC,

            'sv': self.sv,
            'sv_unit': self.sv_unit,
            'sv_MC': self.sv_MC,

            'q': self.q,
            'q_unit': self.q_unit,
            'q_MC': self.q_MC,

            'hb': self.hb,
            'hb_unit': self.hb_unit,
            'hb_MC': self.hb_MC,

            'sao2': self.sao2,
            'sao2_unit': self.sao2_unit,
            'sao2_MC': self.sao2_MC,

            'cao2': self.cao2,
            'cao2_unit': self.cao2_unit,
            'cao2_MC': self.cao2_MC,

            'svo2': self.svo2,
            'svo2_unit': self.svo2_unit,
            'svo2_MC': self.svo2_MC,

            'cvo2': self.cvo2,
            'cvo2_unit': self.cvo2_unit,
            'cvo2_MC': self.cvo2_MC,

            'cavo2': self.cavo2,
            'cavo2_unit': self.cavo2_unit,
            'cavo2_MC': self.cavo2_MC,

            'qao2': self.qao2,
            'qao2_unit': self.qao2_unit,
            'qao2_MC': self.qao2_MC,

            't': self.t,
            't_unit': self.t_unit,
            't_MC': self.t_MC,

            'ph': self.ph,
            'ph_unit': self.ph_unit,
            'ph_MC': self.ph_MC,

            'pvo2': self.pvo2,
            'pvo2_unit': self.pvo2_unit,
            'pvo2_MC': self.pvo2_MC,

            'do2': self.do2,
            'do2_unit': self.do2_unit,
            'do2_MC': self.do2_MC
        }