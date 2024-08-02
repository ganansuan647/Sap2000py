from .Continuous_Bridge import Section_General,Sap_Bearing_Linear,Sap_Double_Box_Pier,SapBase_6Spring,SapPoint,Sap_Box_Girder

class SapBridge:
    def __init__(self,Sapobj):
        self.__Object = Sapobj._Object
        self.__Model = Sapobj._Model
        self._Sapobj = Sapobj
        self.Basic = SapBasic(Sapobj)
        self.Base = SapBase(Sapobj)
        self.Section = SapSection(Sapobj)
        self.Bearing = SapBearing(Sapobj)
        self.Pier = SapPier(Sapobj)
        self.Girder = SapGirder(Sapobj)

class SapBase:
    def __init__(self,Sapobj):
        self.__Object = Sapobj._Object
        self.__Model = Sapobj._Model
        self._Sapobj = Sapobj
        self.Six_Spring = SapBase_6Spring(Sapobj)

class SapGirder:
    def __init__(self,Sapobj):
        self.__Object = Sapobj._Object
        self.__Model = Sapobj._Model
        self._Sapobj = Sapobj
        self.Box = Sap_Box_Girder(Sapobj)

class SapPier:
    def __init__(self,Sapobj):
        self.__Object = Sapobj._Object
        self.__Model = Sapobj._Model
        self._Sapobj = Sapobj
        self.DoubleBox = Sap_Double_Box_Pier(Sapobj)

class SapBearing:
    def __init__(self,Sapobj):
        self.__Object = Sapobj._Object
        self.__Model = Sapobj._Model
        self._Sapobj = Sapobj
        self.Linear = Sap_Bearing_Linear(Sapobj)

class SapBasic:
    def __init__(self,Sapobj):
        self.__Object = Sapobj._Object
        self.__Model = Sapobj._Model
        self._Sapobj = Sapobj
        self.Point = SapPoint(Sapobj)

class SapSection:
    def __init__(self,Sapobj):
        self.__Object = Sapobj._Object
        self.__Model = Sapobj._Model
        self._Sapobj = Sapobj
        self.General = Section_General(Sapobj)
        
        