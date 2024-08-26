import sys
import comtypes.client
import numpy as np
from numpy.typing import NDArray
from typing import Literal, Union
from loguru import logger
from datetime import datetime
from pathlib import Path
import json


class SapMeta(type):
    """Meta class for ensuring the Saproject singleton pattern.

    This metaclass is used to enforce a singleton design pattern for the
    Saproject class, ensuring only one instance is created. This class should
    not be inherited.
    """

    __instance = None

    def __init__(self, class_name, class_bases, class_dic):
        """Initializes the singleton instance."""
        self.__instance = object.__new__(self)
        self.__init__(self.__instance)

    def __call__(self, *args, **kwargs):
        """Ensures only one instance of the Saproject class exists.

        If the instance is already created and no arguments are passed,
        the existing instance is returned. Otherwise, a new instance is
        created and returned.
        """
        if args or kwargs:
            obj = object.__new__(self)
            self.__init__(obj, *args, **kwargs)
            return obj
        else:
            return self.__instance


class SapScripts:
    """SAP2000 script class.

    This class integrates some commonly used SAP2000 scripts under the
    Saproject class, providing methods for frequently used functionalities.
    """

    def __init__(self, Sapobj):
        """Initializes the SapScripts with a parent Saproject object.

        Args:
            Sapobj: The parent Saproject object.
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

    def AddCommonMaterialSet(self, standard: Literal["GB", "JTG", "TB", "User"] = "GB"):
        """Adds common material sets for China.

        Adds a common material set according to the specified standard. For
        China, the available standards include ["GB", "JTG", "TB", "User"].

        Args:
            standard (str): The desired standard for material sets. Defaults
                to "GB".
        """
        from Sap2000py.Scripts.Common_Material_Set import CommonMaterialSet_China

        CommonMaterialSet_China(self.Sapobj, standard)

    def AddJoints(self, Cartesian_coord: NDArray[np.float64] = np.empty(shape=(0, 3))):
        """Adds joints using Cartesian coordinates.

        Args:
            Cartesian_coord (ndarray): Nx3 array or Nx2 array (for 2D models)
                of Cartesian coordinates.
        """
        from .Scripts.Build_Model import Add_Joints_Cartesian

        Add_Joints_Cartesian(self.Sapobj, Cartesian_coord)

    def AddElements(self, Connections: NDArray[np.float64] = np.empty(shape=(0, 2))):
        """Adds elements by their connections.

        Args:
            Connections (ndarray): Nx2 array of connections.
        """
        from .Scripts.Build_Model import Add_Elements

        Add_Elements(self.Sapobj, Connections)

    def SelectCombo_Case(self, Combo_CaseList: Union[list[str], str]):
        """Selects the specified combination or case for output.

        Deselects all combinations and cases for output, then selects the
        specified combinations or cases.

        Args:
            Combo_CaseList (list or str): List of combination or case names to
                be selected for output.
        """
        self.Sapobj.Results.Setup.DeselectAllCasesAndCombosForOutput()
        if isinstance(Combo_CaseList, str):
            Combo_CaseList = [Combo_CaseList]
        for combo_case in Combo_CaseList:
            self.Sapobj.Results.Setup.Set.ComboSelectedForOutput(combo_case, True)
            ret = self.Sapobj.Results.Setup.Get.ComboSelectedForOutput(combo_case)
            if ret[1] != 0:
                self.Sapobj.Results.Setup.Set.CaseSelectedForOutput(combo_case, True)
                ret = self.Sapobj.Results.Setup.Get.CaseSelectedForOutput(combo_case)
            if not ret[0]:
                logger.warning(
                    f"[orange1]{combo_case}[/orange1] may not be name of a combo/case, please check!"
                )

    @staticmethod
    def writecell(WorkSheet, dataArray: NDArray[np.float64], startCell: str):
        """Writes a 2D numpy array to the specified worksheet starting from a given cell.

        Args:
            WorkSheet: Pointer to the target worksheet.
            dataArray (ndarray): 2D numpy array to be written to the worksheet.
            startCell (str): Top-left corner of the matrix in Excel notation (e.g., 'A1').
        """
        import re
        from openpyxl.utils import column_index_from_string

        colname, rowname = re.findall(r"\d+|\D+", startCell)
        rownum = int(rowname)
        colnum = column_index_from_string(colname)
        m, n = dataArray.shape
        for i in range(m):
            for j in range(n):
                WorkSheet.cell(rownum + i, colnum + j, value=dataArray[i, j])


class Saproject(metaclass=SapMeta):
    """SAP2000 project class.

    This class encapsulates the SAP2000 API, providing various methods to
    interact with and manipulate SAP2000 models. It follows the singleton
    pattern enforced by the `SapMeta` metaclass, ensuring only one instance
    of this class can be created.

    Classes:
        File: An instance of the `SapFile` class to handle file operations.
        Define: An instance of the `SapDefinitions` class to manage model
            definitions.
        Assign: An instance of the `SapAssign` class to assign properties to
            model objects.
        Analyze: An instance of the `SapAnalyze` class to perform analyses.
        Results: An instance of the `SapResults` class to retrieve analysis
            results.
        Scripts: An instance of the `SapScripts` class that provides access
            to additional script-based functionalities.

    Attributes:
        _Object: A reference to the SAP2000 application object.
        _Model: A reference to the SAP2000 model object.
        SapVersion: Returns the current SAP2000 program version.
        ProjectInfo: Returns the project information as a dictionary.
        FilePath: Returns the file path of the current model.
        FileName: Returns the file name of the current model.
        CoordSystem: Returns the name of the present coordinate system.
        Unitdict: Returns a dictionary mapping unit names to unit IDs.
        Unitdict_rev: Returns a dictionary mapping unit IDs to unit names.
        Objectdict: Returns a dictionary mapping object types to IDs.
        Unitid: Returns the unit ID of the current SAP2000 model.
        Units: Returns the unit name of the current SAP2000 model.
        is_locked: Checks if the model is locked.


    Methods:
        createSap: Opens the SAP2000 program and initializes the API instance.
        openSap: Starts the SAP2000 application and initializes a new model.
        closeSap: Closes the SAP2000 program.
        lockModel: Locks the current model.
        unlockModel: Unlocks the current model.
        getUnits: Logs and returns the units and unit ID of the current model.
        setUnits: Sets the units of the current SAP2000 model.
        getSapVersion: Logs and returns the current SAP2000 program version.
        getProjectInfo: Logs the project information.
        setProjectInfo: Sets the project information fields.
        setDefaultProjectInfo: Sets the default project information.
        getFileName: Logs and returns the file name of the current model.
        getCoordSystem: Logs and returns the name of the present coordinate
            system.
        RefreshView: Refreshes the view window.

    Example:
        The following example demonstrates how to use the Saproject class:

        ```python
        from pathlib import Path
        from Sap2000py import Saproject
        
        Sap = Saproject()
        Sap.openSap()
        Sap.File.New_Blank()
        Sap.File.Open(Path('.') / "Test" / "Test.sdb")

        print(Sap.Units)
        Sap.getUnits()

        print(Sap.SapVersion)
        Sap.getSapVersion()

        Sap.setProjectInfo(field="Company Name", value="Tongji University")
        Sap.setProjectInfo("Author", "Gou Lingyun")
        Sap.setProjectInfo("Email", "gulangyu@tongji.edu.cn")
        print(Sap.ProjectInfo)
        Sap.getProjectInfo()

        print(Sap.FileName)
        Sap.getFileName()

        print(Sap.CoordSystem)
        Sap.getCoordSystem()

        # Test setting units
        Sap.setUnits("KN_m_E")  # This will log an error as "KN_m_E" is not a supported unit
        Sap.setUnits("KN_m_C")  # This will successfully change the units to KN_m_C
        ```
    """

    def __init__(self, AttachToInstance: Literal[True, False] = True):
        """Initializes the Saproject instance.

        Args:
            AttachToInstance (bool): Whether to attach to an existing SAP2000
                instance. Defaults to True.
        """
        self.createSap(AttachToInstance)
        from Sap2000py.SapDeal import (
            SapFile,
            SapDefinitions,
            SapAssign,
            SapAnalyze,
            SapResults,
        )

        self.File = SapFile(self)
        self.Define = SapDefinitions(self)
        self.Assign = SapAssign(self)
        self.Analyze = SapAnalyze(self)
        self.Results = SapResults(self)
        self.Scripts = SapScripts(self)

    @classmethod
    def new(cls, *args, **kwargs):
        """Creates a new instance of the Saproject class.

        This method is used to create a new instance of the Saproject class
        with the specified arguments and keyword arguments.

        Returns:
            Saproject: A new instance of the Saproject class.
        """
        newinstance = object.__new__(cls)
        newinstance.__init__(AttachToInstance = False)
        return newinstance

    @property
    def SapVersion(self):
        """Gets the current SAP2000 program version."""
        return self._Model.GetVersion()[1]

    @property
    def ProjectInfo(self):
        """project information.

        Returns:
            ProjectInfo(dict): Dictionary containing project information fields and their
                corresponding values.

        Example:
            ProjectInfo = {
                "Company Name": "Tongji University",
                "Author": "Gou Lingyun",
                }
        """
        projectInfo = self._Model.GetProjectInfo()
        num_fields = projectInfo[0]
        if num_fields:
            ProjectInfoDict = dict(zip(projectInfo[1], projectInfo[2]))
            if isinstance(projectInfo[3], dict):
                ProjectInfoDict.update(projectInfo[3])
            else:
                logger.trace("No User Defined Info!")
            return ProjectInfoDict
        else:
            self.setDefaultProjectInfo()
            return self.ProjectInfo

    @property
    def FilePath(self):
        """file path of the current model.

        Returns:
            FilePath(str): file path of the current model.
        """
        return self._Model.GetModelFilepath()

    @property
    def FileName(self):
        """file name of the current model.

        Returns:
            FileName(str): file name of the current model.
        """
        return self._Model.GetModelFilename()

    @property
    def CoordSystem(self):
        """name of the present coordinate system."""
        return self._Model.GetPresentCoordSystem()

    @property
    def Unitdict(self):
        """Dictionary mapping unit names to unit IDs."""
        return {
            "lb_in_F": 1,
            "lb_ft_F": 2,
            "Kip_in_F": 3,
            "Kip_ft_F": 4,
            "KN_mm_C": 5,
            "KN_m_C": 6,
            "Kgf_mm_C": 7,
            "Kgf_m_C": 8,
            "N_mm_C": 9,
            "N_m_C": 10,
            "Ton_mm_C": 11,
            "Ton_m_C": 12,
            "KN_cm_C": 13,
            "Kgf_cm_C": 14,
            "N_cm_C": 15,
            "Ton_cm_C": 16,
        }

    @property
    def Unitdict_rev(self):
        """Reversed dictionary mapping unit IDs to unit names."""
        return {value: key for key, value in self.Unitdict.items()}

    @property
    def Objectdict(self):
        """Dictionary mapping object types to IDs."""
        return {
            "Point": 1,
            "Frame": 2,
            "Cable": 3,
            "Tendon": 4,
            "Area": 5,
            "Solid": 6,
            "Link": 7,
        }

    @property
    def Unitid(self):
        """unit ID of the current SAP2000 model."""
        return self._Model.GetDatabaseUnits()

    @property
    def Units(self):
        """unit name of the current SAP2000 model."""
        return self.Unitdict_rev[self.Unitid]

    @property
    def is_locked(self):
        """Checks if the model is locked."""
        return self._Model.GetModelIsLocked()

    def createSap(
        self,
        AttachToInstance: Literal[True, False] = False,
        SpecifyPath: Literal[True, False] = False,
        ProgramPath: str = "",
    ):
        """Create SAP2000 Object and Model Pointer

        Using comtypes to create a SAP2000 object and model pointer. Default object is **"SAP2000v1.Helper"** and **""CSI.SAP2000.API.SapObject""**

        Args:
            AttachToInstance (bool): Attach to a running API instance if True.
            SpecifyPath (bool): If True, the path to the SAP2000 program must
                be specified.
            ProgramPath (str): Path to the SAP2000 program if SpecifyPath is
                True.
        """
        helper = comtypes.client.CreateObject("SAP2000v1.Helper")
        helper = helper.QueryInterface(comtypes.gen.SAP2000v1.cHelper)
        if AttachToInstance:
            try:
                sap_object = helper.GetObject("CSI.SAP2000.API.SapObject")
            except (OSError, AttributeError, comtypes.COMError):
                logger.warning(
                    "No running API instance of the program found or failed to attach."
                )
                logger.info("Trying to open a new instance...")
                AttachToInstance = False
            if sap_object is None:
                AttachToInstance = False
        if not AttachToInstance:
            if SpecifyPath:
                try:
                    sap_object = helper.CreateObject(ProgramPath)
                except (OSError, comtypes.COMError):
                    logger.error(
                        f"Cannot start a new instance of the program from {ProgramPath}"
                    )
                    sys.exit(-1)
            else:
                try:
                    sap_object = helper.CreateObjectProgID("CSI.SAP2000.API.SapObject")
                except (OSError, comtypes.COMError):
                    logger.error("Cannot start a new instance of the program.")
                    sys.exit(-1)
        self._Object = sap_object
        self._Model = sap_object.SapModel

    def openSap(self):
        """Starts the SAP2000 application and initializes a new model."""
        self._Object.ApplicationStart()
        self._Model = self._Object.SapModel
        self._Model.InitializeNewModel()
        self._Object.Visible = True

    def closeSap(self):
        """Closes the SAP2000 program.

        !!! note "Caution!"
            Remember to save the model before closing the program.
        """
        self._Object.ApplicationExit(True)
        self._Object, self._Model = 0, 0

    def lockModel(self):
        """Lock the current model."""
        ret = self._Model.SetModelIsLocked(True)
        if ret == 0:
            logger.success("Model Locked!")
        else:
            logger.warning("Fail to lock the model!")

    def unlockModel(self):
        """Unlock the current model."""
        ret = self._Model.SetModelIsLocked(False)
        if ret == 0:
            logger.success("Model Unlocked!")
        else:
            logger.warning("Fail to unlock the model!")

    def getUnits(self):
        """Logs and returns the units and unit ID of the current model."""
        logger.opt(colors=True).info(
            f"Current Unit is <yellow>{self.Units}</yellow>, id = <blue>{self.Unitid}</blue>"
        )
        return self.Units

    def setUnits(
        self,
        Unit: Literal[
            "KN_m_C",
            "KN_cm_C",
            "KN_mm_C",
            "N_m_C",
            "N_cm_C",
            "N_mm_C",
            "Kgf_m_C",
            "Kgf_cm_C",
            "Kgf_mm_C",
            "Tonf_m_C",
            "Tonf_cm_C",
            "Tonf_mm_C",
            "lb_in_F",
            "lb_ft_F",
            "Kip_in_F",
            "Kip_ft_F",
        ],
    ):
        """Sets the units of the current SAP2000 model.

        Args:
            Unit (str): The desired units to set. Must be one of the following:["KN_m_C", "KN_cm_C", "KN_mm_C","N_m_C", "N_cm_C", "N_mm_C","Kgf_m_C", "Kgf_cm_C", "Kgf_mm_C","Tonf_m_C", "Tonf_cm_C", "Tonf_mm_C","lb_in_F", "lb_ft_F","Kip_in_F", "Kip_ft_F"]

        """
        if Unit not in self.Unitdict.keys():
            logger.opt(colors=True).error(
                f"Unit <yellow>{Unit}</yellow> is not supported! Must be one of these: <cyan>{list(self.Unitdict.keys())}</cyan>"
            )
            return
        unitid = self.Unitdict[Unit]
        if unitid == self._Model.GetDatabaseUnits():
            logger.info(f"Model Units is already {Unit}")
        else:
            ret = self._Model.SetPresentUnits(unitid)
            if ret == 0:
                logger.opt(colors=True).success(
                    f"Model Units set as: <yellow>{Unit}</yellow>"
                )
            else:
                logger.opt(colors=True).warning(
                    f"Fail to change Units to <yellow>{Unit}</yellow>! Please check!"
                )

    def getSapVersion(self):
        """Logs and returns the current SAP2000 program version.

        Returns:
            SapVersion(str): The current SAP2000 program version.
        """
        logger.opt(colors=True).info(
            f"The current SAP2000 program version is: <yellow>{self.SapVersion}</yellow>"
        )
        return self.SapVersion

    def getProjectInfo(self):
        """Logs the project information.

        Returns:
            ProjectInfo(dict): Dictionary containing project information fields and their
                corresponding values.
        """
        logger.info(f"Project Information:{json.dumps(self.ProjectInfo, indent=4)}")

    def setProjectInfo(
        self,
        field: Literal[
            "Company Name",
            "Client Name",
            "Project Name",
            "Project Number",
            "Model Name",
            "Model Description",
            "Revision Number",
            "Frame Type",
            "Engineer",
            "Checker",
            "Supervisor",
            "Issue Code",
            "Design Code",
            "UserDefined",
        ] = "",
        value: str = "",
        info_dict: dict = {},
        show_log=True,
    ):
        """Sets the project information.

        Args:
            field (str): The field name to set.
            value (str): The value to set for the specified field.
            info_dict (dict): A dictionary of field-value pairs to set.
            show_log (bool): Whether to log the result of setting the info.

        returns:
            ret(int): 0 if success, 1 if fail.

        Example:
            ```python
            from Sap2000py import Saproject
            Sap = Saproject()
            Sap.openSap()
            Sap.File.New_Blank()
            # use field and value
            Sap.setProjectInfo(field="Company Name", value="Tongji University")

            # use position arguments
            Sap.setProjectInfo("Author", "Gou Lingyun")

            # use info_dict
            self.setProjectInfo(info_dict={
                "Company Name": "Tongji University",
                "Author": "Gou Lingyun",
                "Sap2000 Version": str(self.SapVersion),
                "Date": str(datetime.today()),
                "Created By": "Sap2000py Module",
                "Link": "https://github.com/ganansuan647/Sap2000py"
            }, show_log=False)
            ```
        """
        ret = self._Model.SetProjectInfo(field, value)

        if info_dict:
            ret = []
            for key, value in info_dict.items():
                ret.append(self.setProjectInfo(key, value, show_log=show_log))
            ret = any(ret)

        if show_log:
            if ret == 0:
                logger.opt(colors=True).success(
                    f"Project Information <yellow>{field}</yellow> set as <cyan>{value}</cyan>!"
                )
            else:
                logger.opt(colors=True).warning(
                    f"Fail to set Project Information <yellow>{field}</yellow> as <cyan>{value}</cyan>! Please check!"
                )
        return ret

    def setDefaultProjectInfo(self):
        """Sets the default project information."""
        self.setProjectInfo(
            info_dict={
                "Company Name": "Tongji University",
                "Author": "Gou Lingyun",
                "Sap2000 Version": str(self.SapVersion),
                "Date": str(datetime.today()),
                "Created By": "Sap2000py Module",
                "Link": "https://github.com/ganansuan647/Sap2000py",
            },
            show_log=False,
        )

    def getFileName(self):
        """Logs and returns the file name of the current model.

        Actually using property **FileName** to get the file name.

        Returns:
            FileName(str): The file name of the current model.
        """
        path = Path(f"{self.FileName}")
        logger.opt(colors=True).info(f"The current model file name is: {path}")
        return self.FileName

    def getCoordSystem(self):
        """Logs and returns the name of the present coordinate system.

        Actually using property **CoordSystem** to get the coordinate system name.

        Returns:
            CoordSystem(str): The name of the present coordinate system.
        """
        logger.opt(colors=True).info(
            f"The current coordinate system is: <yellow>{self.CoordSystem}</yellow>"
        )
        return self.CoordSystem

    def RefreshView(self, Window: int = 0, Zoom: Literal[True, False] = False):
        """Refreshes the view window.

        Args:
            Window (int): Window number, or 0 to refresh all windows.
            Zoom (bool): Whether to maintain the current zoom level. If False,
                the view will return to the default zoom level.

        Returns:
            ret(int): 0 if success, 1 if fail.
        """
        ret = self._Model.View.RefreshView(Window, Zoom)
        return ret


if __name__ == "__main__":
    sys.path.append(".")
    Sap = Saproject()
    Sap.openSap()
    Sap.File.New_Blank()
    Sap.File.Open(Path(".") / "Test" / "Test.sdb")

    print(Sap.Units)
    Sap.getUnits()

    print(Sap.SapVersion)
    Sap.getSapVersion()

    Sap.setProjectInfo(field="Company Name", value="Tongji University")
    Sap.setProjectInfo("Author", "Gou Lingyun")
    Sap.setProjectInfo("Email", "gulangyu@tongji.edu.cn")
    print(Sap.ProjectInfo)
    Sap.getProjectInfo()

    print(Sap.FileName)
    Sap.getFileName()

    print(Sap.CoordSystem)
    Sap.getCoordSystem()
    # Test setUnits
    Sap.setUnits("KN_m_E")
    Sap.setUnits("KN_m_C")
