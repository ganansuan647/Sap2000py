from Sap2000py.Bridge.Continuous_Bridge import Section_General,Sap_Bearing_Linear,Sap_Double_Box_Pier,SapBase_6Spring,SapPoint,Sap_Box_Girder,Sap_Bearing_PlasticWen

class SapBase:
    Six_Spring = SapBase_6Spring

class SapGirder:
    Box = Sap_Box_Girder
    
class SapPier:
    DoubleBox = Sap_Double_Box_Pier

class SapBearing:
    Linear = Sap_Bearing_Linear
    PlasticWen = Sap_Bearing_PlasticWen

class SapSection:
    General = Section_General

class SapBridge:
    Point = SapPoint
    Base = SapBase
    Section = SapSection
    Bearing = SapBearing
    Pier = SapPier
    Girder = SapGirder
