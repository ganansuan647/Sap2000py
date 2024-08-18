import sys
import comtypes.client
import numpy as np
from typing import Literal
from loguru import logger
from datetime import datetime
from pathlib import Path
import json

class SapMeta(type):
    __instance = None
    def __init__(self,class_name,class_bases,class_dic):
        self.__instance=object.__new__(self)  # Initialize the object corresponding to the singleton Saproject class.
        self.__init__(self.__instance)

    def __call__(self, *args, **kwargs):
        if args or kwargs:
            obj = object.__new__(self)
            self.__init__(obj, *args, **kwargs)
            return obj
        else:
            return self.__instance

class SapScripts:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model
        self.Sapobj = Sapobj
        from Sap2000py.Scripts.GetResults import GetResults
        self.GetResults = GetResults(Sapobj)
        from Sap2000py.Scripts.Analyze import SapAnalyze
        self.Analyze = SapAnalyze(Sapobj)
        from Sap2000py.Scripts.Group import SapGroup
        self.Group = SapGroup(Sapobj)

    def AddCommonMaterialSet(self,standard = "GB"):
        """
        Add Common Material Set for China with your desired standard,
        for China it includes ["GB","JTG","TB","User"]
        """
        from Sap2000py.Scripts.Common_Material_Set import CommonMaterialSet_China
        CommonMaterialSet_China(self.Sapobj,standard)

    def AddJoints(self,Cartesian_coord = np.empty(shape=(0,3))):
        """
        Add Joints by Cartesian coordinates,which must be a numpy array
        input-Cartesian_coord(ndarray)-Nx3 array or Nx2 array in 2D model
        """
        from .Scripts.Build_Model import Add_Joints_Cartesian
        Add_Joints_Cartesian(self.Sapobj,Cartesian_coord)

    def AddElements(self,Connections):
        """
        Add Elements by Element_type,Element_coord,Element_name
        input Connections(ndarray)-Nx2 array
        """
        from .Scripts.Build_Model import Add_Elements
        Add_Elements(self.Sapobj,Connections)

    def SelectCombo_Case(self,Combo_CaseList):
        """
        Select combo or case you need for out put
        """
        self.Sapobj.Results.Setup.DeselectAllCasesAndCombosForOutput()
        if isinstance(Combo_CaseList,str):
            Combo_CaseList = [Combo_CaseList]
        for combo_case in Combo_CaseList:
            self.Sapobj.Results.Setup.Set.ComboSelectedForOutput(combo_case,True)
            ret = self.Sapobj.Results.Setup.Get.ComboSelectedForOutput(combo_case)
            if ret[1]!=0:
                self.Sapobj.Results.Setup.Set.CaseSelectedForOutput(combo_case,True)
                ret = self.Sapobj.Results.Setup.Get.CaseSelectedForOutput(combo_case)
            if ret[0]==False:
                logger.warning(f"[orange1]{combo_case}[/orange1] may not be name of a combo/case, please check!")

    @staticmethod
    def writecell(WorkSheet,dataArray,startCell):
        """
        ---write matrix(ndarray) in specified WorkSheet---
        input:
            WorkSheet: pointer to the target worksheet
            dataArray(ndarray): 2d numpy array
            startCell(str): top left corner of the matrix
        """
        import re
        from openpyxl.utils import column_index_from_string
        colname,rowname = re.findall(r'\d+|\D+', startCell)
        rownum = int(rowname)
        colnum = column_index_from_string(colname)
        m,n = dataArray.shape
        for i in range(m):
            for j in range(n):
                WorkSheet.cell(rownum+i,colnum+j,value = dataArray[i,j])

class Saproject(metaclass=SapMeta):
    """---SAP2000 project class---"""

    def __init__(self,AttachToInstance = True):
        self.createSap(AttachToInstance)
        from Sap2000py.SapDeal import SapFile,SapDefinitions,SapAssign,SapAnalyze,SapResults
        self.File = SapFile(self)
        self.Define = SapDefinitions(self)
        self.Assign = SapAssign(self)
        self.Analyze = SapAnalyze(self)
        self.Results = SapResults(self)
        self.Scripts = SapScripts(self)
    
    @property
    def SapVersion(self):
        """
        ---the current SAP2000 program version---
        """
        return self._Model.GetVersion()[1]
    
    @property
    def ProjectInfo(self):
        """
        ---get the project information---
        self._Model.GetProjectInfo() returns a list of 4 elements:
        [num_fields:int, Defaultfieldnames:list[str], Defaultfieldkeys:list[str], UserDefinedInfo:Dict[str,str]]
        Defaultfields = ["Company Name","Client Name","Project Name","Project Number","Model Name","Model Description","Revision Number","Frame Type","Engineer","Checker","Supervisor","Issue Code","Design Code"]
        """
        projectInfo = self._Model.GetProjectInfo()
        num_fields = projectInfo[0]
        if num_fields:
            ProjectInfoDict = dict(zip(projectInfo[1],projectInfo[2]))
            if type(projectInfo[3])==dict:
                ProjectInfoDict.update(projectInfo[3])
            else:
                logger.trace("No User Defined Info!")
            return ProjectInfoDict
        else:
            self.setDefaultProjectInfo()
            return self.ProjectInfo
    
    @property
    def FilePath(self):
        """
        ---get the file path of the current model---
        """
        return self._Model.GetModelFilepath()
    
    @property
    def FileName(self):
        """
        ---get the file name of the current model---
        """
        return self._Model.GetModelFilename()

    @property
    def CoordSystem(self):
        """
        ---the name of the present coordinate system---
        """
        return self._Model.GetPresentCoordSystem()

    @property
    def Unitdict(self):
        return {
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
    
    @property
    def Unitdict_rev(self):
        return {value: key for key, value in self.Unitdict.items()}
    
    @property
    def Objectdict(self):
        return {
            'Point':1,
            'Frame':2,
            'Cable':3,
            'Tendon':4,
            'Area':5,
            'Solid':6,
            'Link':7
        }
    
    @property
    def Unitid(self):
        """
        ---the units number of the current sap2000 model---
        lb_in_F=1,lb_ft_F=2,kip_in_F=3,kip_ft_F=4,kN_mm_C=5,kN_m_C=6,kgf_mm_C=7,kgf_m_C=8
        N_mm_C=9,N_m_C=10,Ton_mm_C=11,Ton_m_C=12,kN_cm_C=13,kgf_cm_C=14,N_cm_C=15,Ton_cm_C=16
        """
        return self._Model.GetDatabaseUnits()

    @property
    def Units(self):
        """
        ---get the units name of the current sap2000 model---
        lb_in_F=1,lb_ft_F=2,kip_in_F=3,kip_ft_F=4,kN_mm_C=5,kN_m_C=6,kgf_mm_C=7,kgf_m_C=8
        N_mm_C=9,N_m_C=10,Ton_mm_C=11,Ton_m_C=12,kN_cm_C=13,kgf_cm_C=14,N_cm_C=15,Ton_cm_C=16
        """
        return self.Unitdict_rev[self.Unitid]
    
    @property
    def is_locked(self):
        """
        ---check if the model is locked---
        """
        return self._Model.GetModelIsLocked()
    
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
            except (OSError,AttributeError,comtypes.COMError):
                logger.warning("No running API instance of the program found or failed to attach.")
                logger.info("Trying to open a new instance...")
                AttachToInstance = False
            if sap_object == None:
                AttachToInstance = False
        if not AttachToInstance:
            if SpecifyPath:
                try:
                    # Create an instance of the SAPObject from the specified path
                    sap_object = helper.CreateObject(ProgramPath)
                except (OSError, comtypes.COMError):
                    logger.error(f"Cannot start a new instance of the program from {ProgramPath}")
                    sys.exit(-1)
            else:
                try:
                    # Create SapObject
                    sap_object = helper.CreateObjectProgID("CSI.SAP2000.API.SapObject")
                except (OSError, comtypes.COMError):
                    logger.error("Cannot start a new instance of the program.")
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
    
    def lockModel(self):
        """
        ---lock the current model---
        """
        ret = self._Model.SetModelIsLocked(True)
        if ret==0:
            logger.success("Model Locked!")
        else:
            logger.warning("Fail to lock the model!")
            
    def unlockModel(self):
        """
        ---unlock the current model---
        """
        ret = self._Model.SetModelIsLocked(False)
        if ret==0:
            logger.success("Model Unlocked!")
        else:
            logger.warning("Fail to unlock the model!")
    
    def getUnits(self):
        """
        ---get the units and unitid of the current sap2000 model---
        """
        logger.opt(colors=True).info(f"Current Unit is <yellow>{self.Units:}</yellow>, id = <blue>{self.Unitid}</blue>")
        return self.Units
    
    def setUnits(self, Unit:Literal[
        "KN_m_C","KN_cm_C","KN_mm_C",
        "N_m_C","N_cm_C","N_mm_C",
        "Kgf_m_C","Kgf_cm_C","Kgf_mm_C",
        "Tonf_m_C","Tonf_cm_C","Tonf_mm_C",
        "lb_in_F","lb_ft_F",
        "Kip_in_F","Kip_ft_F"])->None:
        """
        ---set the units of the current Sap2000 model---
        """
        if Unit not in self.Unitdict.keys():
            logger.opt(colors=True).error(f"Unit <yellow>{Unit}</yellow> is not supported! Must be one of these: <cyan>{list(self.Unitdict.keys())}</cyan>")
            return
        unitid = self.Unitdict[Unit]
        if unitid == self._Model.GetDatabaseUnits():
            logger.info(f"Model Units is already {Unit}")
        else:
            ret = self._Model.SetPresentUnits(unitid)
            if ret==0:
                logger.opt(colors=True).success(f"Model Units set as: <yellow>{Unit}</yellow>")
            else:
                logger.opt(colors=True).warning(f"Fail to change Units to <yellow>{Unit}</yellow>! Please check!")

    def getSapVersion(self):
            """
            ---Print the current SAP2000 program version---
            """
            logger.opt(colors=True).info(f"The current SAP2000 program version is: <yellow>{self.SapVersion}</yellow>")
            return self.SapVersion

    def getProjectInfo(self):
        """
        ---get the project information ---
        """
        logger.info(f"Project Information:{json.dumps(self.ProjectInfo,indent=4)}")

    def setProjectInfo(self, field:Literal["Company Name","Client Name","Project Name","Project Number","Model Name","Model Description","Revision Number","Frame Type","Engineer","Checker","Supervisor","Issue Code","Design Code","UserDefined"] = "", value:str = "", info_dict:dict = {}, show_log=True)->None:
        """
        ---set the project information---
        input: ProjectInfoDict(dict)
        """
        ret = self._Model.SetProjectInfo(field, value)
        
        if info_dict:
            ret=[]
            for key,value in info_dict.items():
                ret.append(self.setProjectInfo(key, value, show_log = show_log))
            ret = any(ret)
                
        if show_log:
            if ret==0:
                logger.opt(colors=True).success(f"Project Information <yellow>{field}</yellow> set as <cyan>{value}</cyan>!")
            else:
                logger.opt(colors=True).warning(f"Fail to set Project Information <yellow>{field}</yellow> as <cyan>{value}</cyan>! Please check!")
        return ret
    
    def setDefaultProjectInfo(self):
        """
        ---set the default project information---
        """
        self.setProjectInfo(info_dict={
            "Company Name":"Tongji University",
            "Author":"Gou Lingyun",
            "Sap2000 Version": str(self.SapVersion),
            "Date": str(datetime.today()),
            "Created By": "Sap2000py Module",
            "Link": "https://github.com/ganansuan647/Sap2000py"
            },show_log=False)
    
    def getFileName(self):
            """
            ---get the file name of the current model---
            """
            path = Path(f"{self.FileName}")
            logger.opt(colors=True).info(f"The current model file name is: {path}")
            return self.FileName

    def getCoordSystem(self):
        """
        ---get and print the name of the present coordinate system---
        """
        logger.opt(colors=True).info(f"The current coordinate system is: <yellow>{self.CoordSystem}</yellow>")
        return self.CoordSystem

    def RefreshView(self,Window=0,Zoom=False):
        """
        ---refresh View window---
        Window = 0 means all windows or an existing window number
        zoom = True : maintain current window zoom
        zoom = False: return to default zoom
        """
        ret = self._Model.View.RefreshView(Window, Zoom)
        return ret

if __name__ == "__main__":
    sys.path.append(".")
    Sap = Saproject()
    Sap.openSap()
    Sap.File.New_Blank()
    Sap.File.Open(Path('.')/"Test"/"Test.sdb")
    
    print(Sap.Units)
    Sap.getUnits()
    
    print(Sap.SapVersion)
    Sap.getSapVersion()
    
    Sap.setProjectInfo(field="Company Name",value="Tongji University")
    Sap.setProjectInfo("Author","Gou Lingyun")
    Sap.setProjectInfo("Email","gulangyu@tongji.edu.cn")
    print(Sap.ProjectInfo)
    Sap.getProjectInfo()
    
    print(Sap.FileName)
    Sap.getFileName()
    
    print(Sap.CoordSystem)
    Sap.getCoordSystem()
    # Test setUnits
    Sap.setUnits("KN_m_E")
    Sap.setUnits("KN_m_C")
    
    