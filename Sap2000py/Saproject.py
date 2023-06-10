import os
import sys
import comtypes.client
from itertools import chain
import math
import numpy as np

class Saproject(object):
    """---SAP2000 project class---"""

    def __init__(self):
        self.createSap(AttachToInstance = True)
        self.Units = {
            "lb_in_F":1,
            "lb_ft_F":2,
            "Kip_in_F":3,
            "Kip_ft_F":4,
            "KN_mm_C":5,
            "KN_m_C":6,
            "Kgf_mm_C":7,
            "Kgf_m_C":8,
            "N_mm_C":9,
            "N_m_C":10,
            "Tonf_mm_C":11,
            "Tonf_mm_C":12,
            "KN_cm_C":13,
            "Kgf_cm_C":14,
            "N_cm_C":15,
            "Tonf_cm_C":16
        }
        from .SapDeal import SapFile,SapDefinitions,SapAssign,SapAnalyze,SapResults
        self.File = SapFile(self)
        self.Define = SapDefinitions(self)
        self.Assign = SapAssign(self)
        self.Analyze = SapAnalyze(self)
        self.Results = SapResults(self)
        self.Scripts = SapScripts(self)
        
    def createSap(self,AttachToInstance = False,SpecifyPath = False,ProgramPath = "if the flag SpecifyPath is set to True, specify the ProgramPath to SAP2000 here"):
        """
        ---open Sap2000 program---
        if AttachToInstance = True , attatch the pointer to a running API instance, otherwise open a new instance
        if the flag SpecifyPath is set to True, then ProgramPath to your SAP2000 program should be specified
        """
        # Create a new instance of the Helper class
        helper = comtypes.client.CreateObject("SAP2000v1.Helper")
        # Get a strongly_typed reference to the Helper class interface
        helper = helper.QueryInterface(comtypes.gen.SAP2000v1.cHelper)
        if AttachToInstance:
        #attach to a running instance of SAP2000
            try:
                # get the active SapObject(something went wrong)
                sap_object = helper.GetObject("CSI.SAP2000.API.SapObject")
                # get sap model from sap_object
                sap_model = sap_object.SapModel
            except (OSError,AttributeError,comtypes.COMError):
                print("No running API instance of the program found or failed to attach.\nTrying to open a new instance...")
                AttachToInstance = False
        if not AttachToInstance:
            if SpecifyPath:
                try:
                    # Create an instance of the SAPObject from the specified path
                    sap_object = helper.CreateObject(ProgramPath)
                except (OSError, comtypes.COMError):
                    print("Cannot start a new instance of the program from " + ProgramPath)
                    sys.exit(-1)
            else:
                try:
                    # Create SapObject
                    sap_object = helper.CreateObjectProgID("CSI.SAP2000.API.SapObject")
                except (OSError, comtypes.COMError):
                    print("Cannot start a new instance of the program.")
                    sys.exit(-1)
        self._Object = sap_object
        self._Model = sap_object.SapModel

    def openSap(self):
        # Start Application
        self._Object.ApplicationStart()
        # get SapModel obj
        self._Model = self._Object.SapModel
        # init SapModel
        self._Model.InitializeNewModel()
        # make app visiable
        self._Object.Visible = True

    def closeSap(self):
        """
        ---close Sap2000 program---
        P.S. Remember to save before you close the model!
        """
        self._Object.ApplicationExit(True)
        self._Object,self._Model=0,0
    
    def setUnits(self,unitid):
        """
        ---set the units of the current Sap2000 model---
        please see unitsTag in Saproject.Units
        """
        ret = self._Model.SetPresentUnits(unitid)
        if ret==0:
            print("Model Units set as:",lookup(self.Units,unitid))
        else:
            print("Fail to change Units!")

    def getUnits(self):
        """
        ---get the units number of the current sap2000 model---
        lb_in_F=1,lb_ft_F=2,kip_in_F=3,kip_ft_F=4,kN_mm_C=5,kN_m_C=6,kgf_mm_C=7,kgf_m_C=8
        N_mm_C=9,N_m_C=10,Ton_mm_C=11,Ton_m_C=12,kN_cm_C=13,kgf_cm_C=14,N_cm_C=15,Ton_cm_C=16
        """
        UnitNum=self._Model.GetDatabaseUnits()
        UnitStr = lookup(self.Units,UnitNum)
        print("The current model unit is:",UnitStr)
        return UnitStr
    
    def getSapVersion(self):
            """
            ---get the current SAP2000 program version---
            """
            currentVersion=self._Model.GetVersion()
            print("The current SAP2000 program version is:",currentVersion[1])
            return currentVersion[1]

    def getProjectInfo(self):
        """
        ---get the project information ---
        """
        projectInfo=self._Model.GetProjectInfo()
        print(projectInfo)

    def getFileName(self):
            """
            ---get the file name of the current model---
            """
            self.File.name = self._Model.GetModelFilename()
            print("The current model file name is:",self.File.name)
            return self.File.name

    def getCoordSystem(self):
        """
        ---get the name of the present coordinate system---
        """
        currentCoordSysName = self._Model.GetPresentCoordSystem()
        print("The current coordinate system is:",currentCoordSysName)
        return currentCoordSysName

    def RefreshView(self,Window=0,Zoom=False):
        """
        ---refresh View window---
        Window = 0 means all windows or an existing window number
        zoom = True : maintain current window zoom
        zoom = False: return to default zoom
        """
        ret = self._Model.View.RefreshView(Window, Zoom)
        return ret
    

class SapScripts:
    def __init__(self,Sapobj):
        """
        Translation: Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model
        self.Sapobj = Sapobj
        from .Scripts.GetResults import GetResults
        self.GetResults = GetResults(Sapobj)

    def AddCommonMaterialSet(self,standard = "GB"):
        """
        Add Common Material Set for China with your desired standard,
        for China it includes ["GB","JTG","TB","User"]
        """
        from .Scripts.Common_Material_Set import CommonMaterialSet_China
        CommonMaterialSet_China(self.Sapobj,standard)

    def AddJoints(self,Cartesian_coord = np.empty(shape=(0,3))):
        """
        Add Joints by Cartesian coordinates,which must be a numpy array
        input-Cartesian_coord(ndarray)-Nx3 array or Nx2 array in 2D model
        """
        from .Scripts.Add_Joints import Add_Joints_Cartesian
        Add_Joints_Cartesian(self.Sapobj,Cartesian_coord)

    def SelectCombo(self,ComboList):
        """
        Select combo you need for out put
        """
        self.Sapobj.Results.Setup.DeselectAllCasesAndCombosForOutput()
        for combo in ComboList:
            self.Sapobj.Results.Setup.SetComboSelectedForOutput(combo, True)

    def writecell(self,WorkSheet,dataArray,startCell):
        """
        ---write matrix(ndarray) in specified WorkSheet---
        input:
            WorkSheet: pointer to the target worksheet
            dataArray(ndarray): 2d numpy array
            startCell(str): top left corner of the matrix
        """
        import re
        from openpyxl.utils import get_column_letter, column_index_from_string
        colname,rowname = re.findall(r'\d+|\D+', startCell)
        rownum = int(rowname)
        colnum = column_index_from_string(colname)
        m,n = dataArray.shape
        for i in range(m):
            for j in range(n):
                WorkSheet.cell(rownum+i,colnum+j,value = dataArray[i,j])


# define other Funcs
def lookup(look,val):
    """
    ---look up keys by value in a dict---
    """
    if val in look.values():
        return(list(look.keys())[list(look.values()).index(val)])
    else:
        return None

