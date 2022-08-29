import numpy as np

class O2PTSolver():
    def __init__(self, workloadObject, detailsDict):
        self.w = workloadObject
        self.d = detailsDict

    def formatQ(self):
        try:
            Q = float(self.d["Q"])
        except ValueError:
            Q = 0
        unit = self.d["Q_unit"]

        if Q == 0:
            HR = float(self.d['HR'])
            SV = float(self.d['SV'])
            SvUnit = self.d['SV_unit']
            self.w.setMC('Q_MC', 1)

            # If HR and SV is given
            if HR != 0 and SV != 0:
                if unit == 'l/min': # Convert Q to l/min
                    if SvUnit == 'ml': # ml -> l
                        SV = SV / 1000

                elif unit == 'ml/min': # Convert Q to ml/min
                    if SvUnit == 'l':
                        SV = SV * 1000 # l -> ml
                    
                return HR * SV
                
            # If HR and SV not given, try with VO2 and CavO2
            else:
                VO2 = float(self.d['VO2'])
                VO2unit = self.d['VO2_unit']
                CavO2 = float(self.d['C(a-v)O2'])
                CavO2unit = self.d['C(a-v)O2_unit']

                # If VO2 and CavO2 is given
                if VO2 != 0 and CavO2 != 0:
                    if unit == 'l/min': # Convert Q to l/min

                        if VO2unit == 'ml/min':
                            VO2 = VO2 / 1000

                        if CavO2unit == 'ml/l': # -> l/l
                            CavO2 = CavO2 / 1000
                        elif CavO2unit == 'ml/dl':
                            CavO2 = CavO2 / 100

                        return VO2 / CavO2 # l/min

                    elif unit == 'ml/min': # Convert Q to ml/min
                        if VO2unit == 'l/min':
                            VO2 = VO2 / 1000

                        if CavO2unit == 'ml/l': # -> l/l
                            CavO2 = CavO2 / 1000
                        elif CavO2unit == 'ml/dl':
                            CavO2 = CavO2 / 100

                        return VO2 / CavO2 # l/min
                else:
                    return 0
        else:
            return Q

    def formatVO2(self, Q, VO2 = None):
        unit = self.d['VO2_unit']

        if VO2 == None:
            VO2 = float(self.d['VO2'])
        else:
            if unit == 'l/min':
                VO2 = VO2/1000
            else:
                VO2 = VO2

        if VO2 == 0:
            CavO2 = float(self.d['C(a-v)O2'])
            CavO2Unit = self.d['C(a-v)O2_unit']
            QUnit = self.d['Q_unit']
            self.w.setMC('VO2_MC', 1)

            if Q != 0 and CavO2 != 0:
                if CavO2Unit == 'ml/dl': # -> l/l
                    CavO2 = CavO2 / 100
                else:
                    CavO2 = CavO2 / 1000 # -> l/l

                if QUnit == 'ml/min': # -> l/min
                    Q = Q / 1000

                if unit == 'l/min': # Convert VO2 to l/min
                    return Q * CavO2

                elif unit == 'ml/min': # Convert VO2 to ml/min
                    return Q * CavO2 * 1000
        else:
            return VO2
    
    def formatHb(self):
        Hb = float(self.d['[Hb]'])
        unit = self.d['[Hb]_unit']

        return Hb

    def formatCavO2(self, VO2, Q, CaO2):
        try:
            CavO2 = float(self.d['C(a-v)O2'])
        except ValueError:
            CavO2 = 0
        unit = self.d['C(a-v)O2_unit']
        # CaO2 = float(self.d['CaO2'])
        CaO2unit = self.d['CaO2_unit']
        try:
            CvO2 = float(self.d['CvO2'])
        except ValueError:
            CvO2 = 0
        CvO2unit = self.d['CvO2_unit']

        if CavO2 == 0:
            self.w.setMC('C(a-v)O2_MC', 1)

            # If CaO2 and CvO2 is given
            if CaO2 != 0 and CvO2 != 0:
                if unit == 'ml/l':
                    if CaO2unit == 'ml/dl': # -> ml/l
                        CaO2 = CaO2 * 10
                    if CvO2unit == 'ml/dl': # -> ml/l
                        CvO2 = CvO2 * 10

                    return CaO2 - CvO2 # ml/l
                elif unit == 'ml/dl':
                    if CaO2unit == 'ml/l': # -> ml/dl
                        CaO2 = CaO2 / 10
                    if CvO2unit == 'ml/l': # -> ml/dl
                        CvO2 = CvO2 / 10

                    return CaO2 - CvO2 # ml/dl
            else:
                VO2Unit = self.d['VO2_unit']
                QUnit = self.d['Q_unit']
                
                if unit == 'ml/l':
                    if VO2Unit == 'l/min': # -> ml/min
                        VO2 = VO2 * 1000
                    if QUnit == 'ml/min': # -> l/min
                        Q = Q / 1000
                    
                    return VO2 / Q

                elif unit == 'ml/dl':
                    if VO2Unit == 'l/min': # -> ml/min
                        VO2 = VO2 * 1000
                    if QUnit == 'l/min': # -> dl/min
                        Q = Q * 10
                    elif QUnit == 'ml/min':
                        Q = Q / 100
                    
                    return VO2 / Q
        else:
            return CavO2
            
    def formatCaO2(self, Hb, SaO2):
        try:
            CaO2 = float(self.d['CaO2'])
        except ValueError:
            CaO2 = 0
        unit = self.d['CaO2_unit']

        if CaO2 == 0:
            self.w.setMC('CaO2_MC', 1) # Mark as calculated
            HbUnit = self.d['[Hb]_unit']

            if unit == 'ml/l':
                if HbUnit == 'g/dl': # -> g/l
                    Hb = Hb * 10
            elif unit == 'ml/dl':
                if HbUnit == 'g/l': # -> g/dl
                    Hb = Hb / 10
            return 1.34 * Hb * SaO2
        else:
            return CaO2

    def formatCvO2(self, Hb, CaO2, CavO2, SvO2):
        try:
            CvO2 = float(self.d['CvO2'])
        except ValueError:
            CvO2 = 0
        unit = self.d['CvO2_unit']

        if CvO2 == 0:
            self.w.setMC('CvO2_MC', 1)
            HbUnit = self.d['[Hb]_unit']
            
            if unit == 'ml/l':
                if HbUnit == 'g/dl': # -> g/l
                    Hb = Hb * 10
            elif unit == 'ml/dl':
                if HbUnit == 'g/l': # -> g/dl
                    Hb = Hb / 10
            
            return 1.34 * Hb * SvO2
        else:
            return CvO2 
    
    def formatSvO2(self, CavO2, CaO2, Hb):
        try:
            SvO2 = float(self.d['SvO2'])
        except ValueError:
            SvO2 = 0

        if SvO2 == 0:
            self.w.setMC('SvO2_MC', 1)
            CaO2Unit = self.d['CaO2_unit']
            CavO2Unit = self.d['C(a-v)O2_unit']
            HbUnit = self.d['[Hb]_unit']

            if CaO2Unit == 'ml/l': # -> ml/dl
                CaO2 = CaO2 / 10
            if CavO2Unit == 'ml/l': # -> ml/dl
                CavO2 = CavO2 / 10
            if HbUnit == 'g/l': # -> g/dl
                Hb = Hb / 10

            return (CaO2 - CavO2) / 1.34 / Hb
        else:
            return SvO2 / 100

    def formatQaO2(self, Q, CaO2):
        try:
            QO2 = float(self.d['QaO2'])
        except ValueError:
            QO2 = 0
        unit = self.d['QaO2_unit']
        QUnit = self.d['Q_unit']
        CaO2Unit = self.d['CaO2_unit']

        if QO2 == 0:
            self.w.setMC('QaO2_MC', 1)
        
            if CaO2Unit == 'ml/l': # l/l
                CaO2 = CaO2 / 1000
            elif CaO2Unit == 'ml/dl': # -> dl/dl
                CaO2 = CaO2 / 100

            if unit == 'ml/min':
                if QUnit == 'l/min': # -> ml/min
                    Q = Q * 1000
            elif unit == 'l/min':
                if QUnit == 'ml/min': # -> l/min
                    Q = Q / 1000
            
            return Q * CaO2
        else:
            return QO2

    def formatPvO2(self, a, b):
        try:
            PvO2 = float(self.d['PvO2'])
        except ValueError:
            PvO2 = 0
        self.w.setMC('PvO2_MC', 1)
        
        if PvO2 == 0:
            return np.float_power( a+b, (1/3)) - np.float_power( b-a, (1/3))
        else:
            return PvO2

    def phTempCorrection(self, pH0, pH, T0, T, PvO2_calc):
        lnPvO2 = np.log(PvO2_calc)
        isCorrected = False

        if pH != pH0 or T != T0:
            lnPO2pH = (pH - pH0) * (-1.1)
            lnPO2Temp = (T-T0) * 0.058 * np.float_power(0.243 * np.float_power(PvO2_calc/100, 3.88) + 1, -1) + (T-T0) * 0.013
            isCorrected = True
        else:
            lnPO2pH = 0
            lnPO2Temp = 0

        PvO2_calc = np.exp( lnPvO2 + lnPO2Temp + lnPO2pH )

        return PvO2_calc, isCorrected

    def formatT(self, label):
        T = float(self.d[label])
        unit = self.d[f'{label}_unit']

        if unit == 'F':
            return (T - 32)/1.8
        if unit == 'K':
            return T - 273.15
        else:
            return T

    def solveDO2(self, VO2, PvO2_calc):
        VO2Unit = self.d['VO2_unit']

        if VO2Unit == 'ml/min': # -> l/min
            VO2 = VO2 / 1000
        
        return VO2 / 2 / PvO2_calc * 1000

    def calc(self): #w=workload object, details=dict
        validValues = True
        Q = self.formatQ()
        VO2 = self.formatVO2(Q)
        if VO2 == 0 or VO2 == None:
            validValues = False
            return validValues
        Hb = self.formatHb()
        SaO2 = float(self.d['SaO2'])

        CaO2 = self.formatCaO2(Hb, SaO2/100)
        CavO2 = self.formatCavO2(VO2, Q, CaO2)
        SvO2_calc = self.formatSvO2(CavO2, CaO2, Hb)
        CvO2 = self.formatCvO2(Hb, CaO2, CavO2, SvO2_calc)
        QaO2 = self.formatQaO2(Q, CaO2)

        # Calculate diffusion DO2
        a = 11700 * np.float_power( ( np.float_power(SvO2_calc,-1) - 1 ), -1 )
        b = np.float_power( 50**3 + np.float_power(a,2), 0.5 )
        PvO2_calc = self.formatPvO2(a, b) # mmHg

        if PvO2_calc < 0:
            validValues = False
            return validValues

        # pH + temp correction
        pH = float(self.d['pH'])
        pH0 = float(self.d['pH @ rest']) # verrataanko rest vs. kuorma VAI aikaisemman kuorman max vs kuorman max?
        T = self.formatT('T')
        T0 = self.formatT('Tc @ rest')

        PvO2_calc, isCorrected = self.phTempCorrection(pH0, pH, T0, T, PvO2_calc)

        DO2 = self.solveDO2(VO2, PvO2_calc)

        # Calculate datapoints for diffusion line
        PvO2 = np.arange(0,100,1)
        y = 2 * DO2 * PvO2

        # Prevent runtimewarning (divide by 0)
        with np.errstate(divide='ignore'):
            SvO2 = np.float_power( ( 23400 * np.float_power( (PvO2)**3 + 150*PvO2, -1 ) ) + 1, -1 )
        SvO2[np.isnan(SvO2)] = 0

        # Convert to l/min
        if self.d['Q_unit'] == 'ml/min':
            Q = Q / 1000

        if self.d['[Hb]_unit'] == 'g/l': # -> g/dl
            Hb = Hb / 10

        # Calculate datapoints for convective curve
        y2 = Q * ( 1.34 * Hb * ( SaO2/ 100 - SvO2 ) ) * 10

        # Correction and calculation of intersection point
        idx = np.argwhere(np.diff(np.sign(y - y2))).flatten()
        yDiff = []

        for i in np.arange(0, 1, 0.1):
            y_temp = 2* DO2 * (PvO2[idx]+i)
            y2_temp = Q * ( 1.34 * Hb * ( SaO2/ 100 - np.float_power( ( 23400 * np.float_power( (PvO2[idx]+i)**3 + 150*(PvO2[idx]+i), -1 ) ) + 1, -1 ) ) ) * 10

            try:
                yDiff.append( (float(y_temp)-float(y2_temp)) )
            except TypeError:
                validValues = False
                return validValues

        constant = np.where( np.abs(yDiff) == np.amin(np.abs(yDiff)) )[0] / 10
        yi = float( Q * ( 1.34 * Hb * ( SaO2/ 100 - np.float_power( ( 23400 * np.float_power( (PvO2[idx]+constant)**3 + 150*(PvO2[idx]+constant), -1 ) ) + 1, -1 ) ) ) * 10 )
        xi = float(PvO2[idx]+constant)

        if isCorrected:
            VO2 = self.formatVO2(Q=Q, VO2=yi)
            CavO2 = self.formatCavO2(VO2, Q, CaO2)
            SvO2_calc = self.formatSvO2(CavO2, CaO2, Hb*10)
            CvO2 = self.formatCvO2(Hb, CaO2, CavO2, SvO2_calc)
            QaO2 = self.formatQaO2(Q, CaO2)

        if self.d['[Hb]_unit'] == 'g/l': # g/dl -> g/l
            Hb = Hb * 10

        if self.d['Q_unit'] == 'ml/min': # l/min -> ml/min
            Q = Q * 1000

        SvO2_calc = SvO2_calc * 100

        self.w.setCalcResults(y, y2, xi, yi, VO2, Q, Hb, SaO2, CaO2, SvO2_calc, CvO2, CavO2, QaO2, T0, T, pH0, pH, PvO2_calc, DO2)

        return validValues