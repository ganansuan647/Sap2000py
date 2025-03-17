from Sap2000py.Bridge.Continuous_Bridge import Section_General, Section_Rectangle, Section_NonPrismatic
from Sap2000py.Bridge.Continuous_Bridge import Sap_Bearing_Linear,Sap_Bearing_PlasticWen
from Sap2000py.Bridge.Continuous_Bridge import Sap_Double_Box_Pier
from Sap2000py.Bridge.Continuous_Bridge import SapBase_6Spring, SapBase_Fixed
from Sap2000py.Bridge.Continuous_Bridge import SapPoint, SapFrame
from Sap2000py.Bridge.Continuous_Bridge import Sap_Box_Girder

class SapBase:
    Six_Spring = SapBase_6Spring
    Fixed = SapBase_Fixed

class SapGirder:
    Box = Sap_Box_Girder
    
class SapPier:
    DoubleBox = Sap_Double_Box_Pier

class SapBearing:
    Linear = Sap_Bearing_Linear
    PlasticWen = Sap_Bearing_PlasticWen

class SapSection:
    General = Section_General
    Rectangle = Section_Rectangle
    NonPrismatic = Section_NonPrismatic

class SapBridge:
    Point = SapPoint
    Frame = SapFrame
    Base = SapBase
    Section = SapSection
    Bearing = SapBearing
    Pier = SapPier
    Girder = SapGirder
