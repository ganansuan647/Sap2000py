from Sap2000py.SapMaterial import SapMaterial
from Sap2000py.SapSection import SapSection
from Sap2000py.SapConstraints import jointConstraints
from Sap2000py.Sapfunctions import Sapfunctions
from Sap2000py.Sapload import SapLoadCases,SapLoadPatterns
from Sap2000py.SapObj import SapPointObj,SapFrameObj,SapTendonObj,SapAreaObj,SapSolidObj,SapLinkObj
import os
from pathlib import Path
from typing import Union
from loguru import logger

class SapFile():
    def __init__(self,Sapobj):
        """
        Translation: Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.Sapobj = Sapobj
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model 

    def Open(self,FileName : Union[Path , str] = Path('.')/"NewSapProj.sdb"):
        """
        ---This function opens an existing Sap2000 file. The file name must have an sdb, $2k, s2k, xlsx, xls, or
        mdb extension. Files with sdb extensions are opened as standard Sap2000 files. Files with $2k and s2k
        extensions are imported as text files. Files with xlsx and xls extensions are imported as Microsoft Excel
        files. Files with mdb extensions are imported as Microsoft Access files
        ---
        inputs:
        FileName(str)-The full path of a model file to be opened in the Sap2000 application
        """
        # make sure filepath exists
        if type(FileName) == str:FileName = Path(FileName)
        if not FileName.suffix == '.sdb':
            logger.critical("File extension must be .sdb")
            return -1
        
        if not FileName.exists():
            if not FileName.parent.resolve().exists():
                logger.warning(f"Path {FileName.parent.resolve()} does not exist! Creating path...")
                FileName.parent.mkdir(parents=True,exist_ok=True)
            
            # create the file
            FileName.touch()
            # get the full path of the file
            FileName = FileName.resolve()
            logger.warning(f"File {FileName} does not exist! Creating file...")
            # create new blank model
            ret = self.__Model.File.NewBlank()
            if(ret!=0):logger.error("Cannot create new Blank Sap model")
            # save sdb file
            ret = self.Save(FileName)
            if(ret!=0):logger.error(f"Cannot save file at path:{FileName}")
        else:
            # open the sdbFile
            ret = self.__Model.File.OpenFile(str(FileName))  # open an existing file
            if(ret!=0):logger.error(f"Cannot open file at path:{FileName}")
        self.Sapobj.setDefaultProjectInfo()
        return ret

    def New_Blank(self):
        """
        ---create a new blank model---
        """
        self.__Model.File.NewBlank()

    def Save(self,FileName : Union[Path , str] = Path('.')/"NewSapProj.sdb"):
        """
        ---save Sap model file---
        save at savepath\savename
        """
        # make sure filepath exists
        if type(FileName) == str:FileName = Path(FileName).resolve()
        ret = self.__Model.File.Save(str(FileName))
        return ret
    
    def New_2DFrame(self,TempType,NumberStorys,StoryHeight,NumberBays,BayWidth,Restraint=True,
                        Beam="Default",Column="Default",Brace="Default"):
        """
        ---Do not use this function to add to an existing model. This function should be used only for creating a new
         model and typically would be preceded by calls to ApplicationStart or InitializeNewModel.The function returns
         zero if the new 2D frame model is successfully created, otherwise it returns a nonzero value.---
        inputs:
        TempType(int)-One of the following 2D frame template types in the e2DFrameType enumeration.
            PortalFrame = 0,ConcentricBraced = 1,EccentricBraced = 2
        NumberStorys(int)-The number of stories in the frame.
        StoryHeight(float)-The height of each story. [L]
        NumberBays(int)-The number of bays in the frame.
        BayWidth(float)-The width of each bay. [L]
        Restraint(bool)-Joint restraints are provided at the base of the frame when this item is True.
        Beam(str)-The frame section property used for all beams in the frame. This must either be Default or
            the name of a defined frame section property.
        Column(str)-The frame section property used for all columns in the frame. This must either be Default
            or the name of a defined frame section property.
        Brace(str)-The frame section property used for all braces in the frame. This must either be Default or the
            name of a defined frame section property. This item does not apply to the portal frame.
        """
        self.__Model.File.New2DFrame(TempType,NumberStorys,StoryHeight,NumberBays,BayWidth,Restraint,Beam,Column,Brace)

    def New_Wall(self,NumberXDivisions,DivisionWidthX,NumberZDivisions,DivisionWidthZ,Restraint=True,Area="Default"):
        """
        ---Do not use this function to add to an existing model. This function should be used only for creating a new
        model and typically would be preceded by calls to ApplicationStart or InitializeNewModel.
        ---
        inputs:
        NumberXDivisions(int)-The number of area objects in the global X direction of the wall.
        DivisionWidthX(float)-The width of each area object measured in the global X direction. [L]
        NumberZDivisions(int)-The number of area objects in the global Z direction of the wall
        DivisionWidthZ(float)-The height of each area object measured in the global Z direction. [L]
        Restraint(bool)-Joint restraints are provided at the base of the wall when this item is True.
        Area(str)-The shell section property used for the wall. This must either be Default or the name of
            a defined shell section property.
        """
        self.__Model.File.NewWall(NumberXDivisions,DivisionWidthX,NumberZDivisions,DivisionWidthZ,Restraint,Area)

    def New_3DFrame(self,TempType,NumberStorys,StoryHeight,NumberBayX,BayWidthX,NumberBaysY,BayWidthY,
                        Restraint=True,Beam="Default",Column="Default",Area="Default",NumberXDivisions=4,NumberYDivisions=4):
        """
        ---Do not use this function to add to an existing model. This function should be used only for creating a
        new model and typically would be preceded by calls to ApplicationStart or InitializeNewModel
        ---
        inputs:
        TempType(int)-One of the following 3D frame template types in the e3DFrameType enumeration.
            OpenFrame = 0,PerimeterFrame = 1,BeamSlab = 2,FlatPlate = 3
        NumberStorys(int)-The number of stories in the frame
        StoryHeight(float)-The height of each story. [L]
        NumberBayX(int)-The number of bays in the global X direction of the frame.
        BayWidthX(float)-The width of each bay in the global X direction of the frame. [L]
        NumberBayY(int)-The number of bays in the global Y direction of the frame
        BayWidthY(float)-The width of each bay in the global Y direction of the frame. [L]
        Restraint(bool)-Joint restraints are provided at the base of the frame when this item is True
        Beam(str)-The frame section property used for all beams in the frame. This must either be Default or
            the name of a defined frame section property
        Column(str)-The frame section property used for all columns in the frame. This must either be Default or
            the name of a defined frame section property
        Area(str)-The shell section property used for all floor slabs in the frame. This must either be Default or the
            name of a defined shell section property. This item does not apply to the open and perimeter frames
        NumberXDivisions(int)-The number of divisions for each floor area object in the global X direction. This
            item does not apply to the open and perimeter frames
        NumberYDivisions(int)-The number of divisions for each floor area object in the global Y direction. This
            item does not apply to the open and perimeter frames
        """
        self.__Model.File.New3DFrame(TempType,NumberStorys,StoryHeight,NumberBayX,BayWidthX,NumberBaysY,BayWidthY,
                        Restraint,Beam,Column,Area,NumberXDivisions,NumberYDivisions)

    def New_SolidBlock(self,XWidth,YWidth,Height,Restraint=True,Solid="Default",NumberXDivisions=5,
                           NumberYDivisions=8,NumberZDivisions=10):
        """
        ---The function returns zero if the new solid block model is successfully created, otherwise it returns a nonzero value---
        inputs:
        XWidth(float)-The total width of the solid block measured in the global X direction. [L]
        YWidth(float)-The total width of the solid block measured in the global Y direction. [L]
        Height(float)-The total height of the solid block measured in the global Z direction. [L]
        Restraint(bool)-Joint restraints are provided at the base of the solid block when this item is True
        Solid(str)-The solid property used for the solid block. This must either be Default or the name of a defined solid property
        NumberXDivisions(int)-The number of solid objects in the global X direction of the block
        NumberYDivisions(int)-The number of solid objects in the global Y direction of the block
        NumberZDivisions(int)-The number of solid objects in the global Z direction of the block
        """
        self.__Model.File.NewSolidBlock(XWidth,YWidth,Height,Restraint,Solid,NumberXDivisions,
                           NumberYDivisions,NumberZDivisions)


class MassSource:
    def __init__(self,Sapobj):
        """
        Translation: Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def SetDefault(self,name):
        """
        ---This function sets the default mass source---
        inputs:
        name(str)-The name of the mass source to be flagged as the default mass source.
        """
        self.__Model.SourceMass.SetDefault(name)

    def SetMassSource(self,name,MassFromElements,MassFromMasses,MassFromLoads,
                                                    IsDefault,NumberLoads=0,LoadPat=[],SF=[]):
        """
        ---This function adds a new mass source to the model or reinitializes an existing mass source---
        inputs:
        name(str)-The mass source name.
        MassFromElements(bool)-If this item is True then element self mass is included in the mass.
        MassFromMasses(bool)-If this item is True then assigned masses are included in the mass.
        MassFromLoads(bool)-If this item is True then specified load patterns are included in the mass.
        IsDefault(bool)-If this item is True then the mass source is the default mass source.  Only one
            mass source can be the default mass source so when this assignment is True all other mass sources
            are automatically set to have the IsDefault flag False.
        NumberLoads(int)-The number of load patterns specified for the mass source.  This item is only applicable
            when the MassFromLoads item is True.
        LoadPat(str list)-This is an array of load pattern names specified for the mass source.
        SF(float list)-This is an array of load pattern multipliers specified for the mass source.
        """
        self.__Model.SourceMass.SetMassSource(name,MassFromElements,MassFromMasses,MassFromLoads,
                                                    IsDefault,NumberLoads,LoadPat,SF)

class LoadCombo:
    def __init__(self,Sapobj):
        """
        Translation: Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def Add(self,name,comboType):
        """
        ---This function adds a new load combination---
        inputs:
        name(str)-The name of a new load combination.
        comboType(int)-This is 0, 1, 2, 3 or 4 indicating the load combination type.0 = Linear Additive,
            1 = Envelope,2 = Absolute Additive,3 = SRSS,4 = Range Additive
        """
        self.__Model.RespCombo.Add(name,comboType)

    def SetCaseList(self,name,CNameType,CName,SF):
        """
        ---This function adds or modifies one load case or response combination in the list of
        cases included in the load combination specified by the Name item.---
        inputs:
        name(str)-The name of an existing load combination.
        CNameType(int)-This is one of the following items in the eCNameType enumeration:LoadCase = 0,
            LoadCombo = 1,This item indicates if the CName item is an load case (LoadCase) or a load
            combination (LoadCombo).
        CName(str)-The name of the load case or load combination to be added to or modified in the combination
            specified by the Name item. If the load case or combination already exists in the combination specified
            by the Name item, the scale factor is modified as indicated by the SF item for that load case or
            combination. If the analysis case or combination does not exist in the combination specified by the
            Name item, it is added.
        SF(float)-The scale factor multiplying the case or combination indicated by the CName item.
        """
        self.__Model.RespCombo.SetCaseList(name,CNameType,CName,SF)

class SapDefinitions:
    def __init__(self,Sapobj):
        """
        Translation: Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model
        self.material = SapMaterial(Sapobj)
        self.section = SapSection(Sapobj)
        self.jointConstraints = jointConstraints(Sapobj)
        self.function = Sapfunctions(Sapobj)
        self.loadcases = SapLoadCases(Sapobj)
        self.loadpatterns = SapLoadPatterns(Sapobj)
        self.masssource = MassSource(Sapobj)
        self.LoadCombo = LoadCombo(Sapobj)


class SapAssign:
    def __init__(self,Sapobj):
        """
        Translation: Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model
        self.PointObj = SapPointObj(Sapobj)
        self.FrameObj = SapFrameObj(Sapobj)
        self.TendonObj = SapTendonObj(Sapobj)
        self.AreaObj = SapAreaObj(Sapobj)
        self.SolidObj = SapSolidObj(Sapobj)
        self.Link = SapLinkObj(Sapobj)


class SapAnalyze:
    def __init__(self,Sapobj):
        """
        Translation: Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def CreateAnalysisModel(self):
        """
        ---This function creates the analysis model. If the analysis model is already created and current, nothing is done.
        The function returns zero if the analysis model is successfully created or it already exists and is current,
        otherwise it returns a nonzero value.It is not necessary to call this function before running an analysis.
        The analysis model is automatically created, if necessary, when the model is run
        ---
        """
        self.__Model.Analyze.CreateAnalysisModel()

    def SetActiveDOF(self,DOF):
        """
        ---This function sets the model global degrees of freedom---
        inputs:
        DOF(bool list)-This is an array of 6 boolean values, indicating if the specified model global
            degree of freedom is active.
            DOF(0) = UX,DOF(1) = UY,DOF(2) = UZ,DOF(3) = RX,DOF(4) = RY,DOF(5) = RZ
        """
        self.__Model.Analyze.SetActiveDOF(DOF)

    def SetRunCaseFlag(self,Name,Run,All=False):
        """
        ---This function sets the run flag for load cases---
        inputs:
        Name(str)-The name of an existing load case that is to have its run flag set
        Run(bool)-If this item is True, the specified load case is to be run
        All(bool)-If this item is True, the run flag is set as specified by the Run item for all load cases,
            and the Name item is ignored
        """
        self.__Model.Analyze.SetRunCaseFlag(Name,Run,All)

    def SetSolverOption_2(self,SolverType,SolverProcessType,NumberParallelRuns,StiffCase):
        """
        ---This function sets the model solver options---
        inputs:
        SoverType(int)-This is 0, 1 or 2, indicating the solver type.
            0 = Standard solver
            1 = Advanced solver
            2 = Multi-threaded solver
        SolverProcessType(int)-This is 0, 1 or 2, indicating the process the analysis is run.
            0 = Auto (program determined)
            1 = GUI process
            2 = Separate process
        NumberParallelRuns(int)-This is an integer between -8 and 8, inclusive, not including -1.
            -8 to -2 = Auto parallel (use up to all physical cores - max 8). Treated the same as 0.
            -1 = Illegal value; will return an error.
            0 = Auto parallel (use up to all physical cores).
            1 = Serial.
            2 to 8 = User defined parallel (use up to this fixed number of cores - max 8).
        StiffCase(str)-The name of the load case used when outputting the mass and stiffness matrices to
            text files If this item is blank, no matrices are output
        """
        self.__Model.Analyze.SetSolverOption_2(SolverType,SolverProcessType,NumberParallelRuns,StiffCase)

    def MergeAnalysisResults(self,FileName):
        """
        ---See “Merging Analysis Results” section in program help file for requirements and limitations.
        The analysis model is automatically created as part of this function.
        The function returns zero if analysis results are successfully merged, otherwise it returns a nonzero value.
        IMPORTANT NOTE: Your model must have a file path defined before merging analysis results. If the model is
        opened from an existing file, a file path is defined. If the model is created from scratch, the File.Save
        function must be called with a file name before merging analysis results. Saving the file creates the file path.
        ---
        inputs:
        FileName(str)-The full path of a model file from which the analysis results are to be merged
        """
        self.__Model.Analyze.MergeAnalysisResults(FileName)

    def ModifyUnDeformedGeometry(self,CaseName,SF,Stage=-1,Original=False):
        """
        ---This function modifies the undeformed geometry based on displacements obtained from a specified load case---
        inputs:
        CaseName(str)-The name of the static load case from which displacements are obtained
        SF(float)-The scale factor applied to the displacements
        Stage(int)-This item applies only when the specified load case is a staged construction load case. It is the
            stage number from which the displacements are obtained. Specifying a -1 for this item means to use the last run stage
        Original(bool)-If this item is True, all other input items in this function are ignored and the original
            undeformed geometry data is reinstated
        """
        self.__Model.Analyze.ModifyUnDeformedGeometry(CaseName,SF,Stage,Original)

    def RunAnalysis(self):
        """
        ---This function runs the analysis. The analysis model is automatically created as part of this function.
        The function returns zero if the analysis model is successfully run, otherwise it returns a nonzero value.
        IMPORTANT NOTE: Your model must have a file path defined before running the analysis. If the model is opened
        from an existing file, a file path is defined. If the model is created from scratch, the File.Save function
        must be called with a file name before running the analysis. Saving the file creates the file path.
        ---
        """
        self.__Model.Analyze.RunAnalysis()

    def DeleteResults(self,CaseName):
        """
        ---This function deletes the results for a specified load case---
        inputs:
        CaseName(str)-The name of a load case
        """
        ret = self.__Model.Analyze.DeleteResults(CaseName)
        return ret

    def ModifyUnDeformedGeometryModeShape(self,CaseName,Mode,MaxDisp,Direction,Original=False):
        """
        ---This function modifies the undeformed geometry based on the shape of a specified mode from a specified
        modal or buckling load case
        ---
        inputs:
        CaseName(str)-The name of a modal or buckling load case
        Mode(int)-The mode shape to consider
        MaxDisp(float)-The maximum displacement to which the mode shape will be scaled
        Direction(int)-The direction in which to apply the geometry modification
        Original(bool)-If this item is True, all other input items in this function are ignored and
            the original undeformed geometry data is reinstated
        """
        self.__Model.Analyze.ModifyUndeformedGeometryModeShape(CaseName,Mode,MaxDisp,Direction,Original)

    def GetActiveDOF(self):
        """
        ---This function retrieves the model global degrees of freedom---
        return:
        [index,DOF]

        DOF(bool list)-This is an array of 6 boolean values, indicating if the specified model global degree of
            freedom is active.
            DOF(0) = UX
            DOF(1) = UY
            DOF(2) = UZ
            DOF(3) = RX
            DOF(4) = RY
            DOF(5) = RZ
        """
        result=self.__Model.Analyze.GetActiveDOF()
        return result

    def GetCaseStatus(self):
        """
        ---This function retrieves the status for all load cases---
        return:
        [index,NumberItems,CaseName,Status]

        NumberItems(int)-The number of load cases for which the status is reported
        CaseName(str list)-This is an array that includes the name of each analysis case for which the status is reported
        Status(int list)-This is an array of that includes 1, 2, 3 or 4, indicating the load case status.
            1 = Not run
            2 = Could not start
            3 = Not finished
            4 = Finished
        """
        result=self.__Model.Analyze.GetCaseStatus()
        return result

    def GetRunCaseFlag(self):
        """
        ---This function retrieves the run flags for all analysis cases---
        return:
        [index,NumberItems,CaseName,Run]

        NumberItems(int)-The number of load cases for which the run flag is reported
        CaseName(str list)-This is an array that includes the name of each analysis case for which the run flag is reported
        Run(bool list)-This is an array of boolean values indicating if the specified load case is to be run
        """
        result=self.__Model.Analyze.GetRunCaseFlag()
        return result

    def GetSolverOption_2(self):
        """
        ---This function retrieves the model solver options---
        return:
        [index,SoverType,SolverProcessType,NumberParallelRuns,StiffCase]

        SoverType(int)-This is 0, 1 or 2, indicating the solver type.
            0 = Standard solver
            1 = Advanced solver
            2 = Multi-threaded solver
        SolverProcessType(int)-This is 0, 1 or 2, indicating the process the analysis is run.
            0 = Auto (program determined)
            1 = GUI process
            2 = Separate process
        NumberParallelRuns(int)-This is an integer between -8 and 8, inclusive, not including -1.
            -8 to -2 = Auto parallel (use up to all physical cores - max 8). Treated the same as 0.
            -1 = Illegal value; will return an error.
            0 = Auto parallel (use up to all physical cores).
            1 = Serial.
            2 to 8 = User defined parallel (use up to this fixed number of cores - max 8).
        StiffCase(str)-The name of the load case used when outputting the mass and stiffness matrices to
            text files If this item is blank, no matrices are output
        """
        result=self.__Model.Analyze.GetSolverOption_2()
        return result



class Results_Setup:
    def __init__(self,Sapobj):
        """
        Translation: Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def SelectAllSectionCutsForOutput(self,Selected):
        """
        ---This function selects or deselects all section cuts for output.The function returns 0 if the selected flag
        is successfully set, otherwise it returns nonzero.Please note that all section cuts are, by default, selected
        for output when they are created
        ---
        inputs:
        Selected(bool)-This item is True if all section cuts are to be selected for output, or False if no section
            cuts are to be selected for output
        """
        self.__Model.Results.Setup.SelectAllSectionCutsForOutput(Selected)

    def DeselectAllCasesAndCombosForOutput(self):
        """
        ---The function deselects all load cases and response combinations for output---
        """
        self.__Model.Results.Setup.DeselectAllCasesAndCombosForOutput()

    def SetCaseSelectedForOutput(self,Name,Selected=True):
        """
        ---This function sets an load case selected for output flag---
        inputs:
        Name(str)-The name of an existing load case
        Selected(bool)-This item is True if the specified load case is to be selected for output, otherwise it is False
        """
        self.__Model.Results.Setup.SetCaseSelectedForOutput(Name,Selected)

    def SetComboSelectedForOutput(self,Name,Selected=True):
        """
        ---This function sets a load combination selected for output flag---
        inputs:
        Name(str)-The name of an existing load combination
        Selected(bool)-This item is True if the specified load combination is to be selected for output, otherwise it is False
        """
        self.__Model.Results.Setup.SetComboSelectedForOutput(Name,Selected)

    def SetOptionBaseReactLoc(self,gx,gy,gz):
        """
        ---This function sets the global coordinates of the location at which the base reactions are reported---
        inputs:
        gx,gy,gz(float)-The global coordinates of the location at which the base reactions are reported
        """
        self.__Model.Results.Setup.SetOptionBaseReactLoc(gx,gy,gz)

    def SetOptionBucklingMode(self,BuckModeStart,BuckModeEnd,BuckModeAll=False):
        """
        ---This function sets the buckling modes for which buckling factors are reported---
        inputs:
        BuckModeStart(int)-The first buckling mode for which the buckling factor is reported when the BuckModeAll item is False
        BuckModeEnd(int)-The last buckling mode for which the buckling factor is reported when the BuckModeAll item is False
        BuckModeAll(bool)-If this item is True, buckling factors are reported for all calculated buckling modes.
            If it is False, buckling factors are reported for the buckling modes indicated by the BuckModeStart and BuckModeEnd items
        """
        self.__Model.Results.Setup.SetOptionBucklingMode(BuckModeStart,BuckModeEnd,BuckModeAll)

    def SetOptionDirectHist(self,Value):
        """
        ---This function sets the output option for direct history results---
        inputs:
        Value(int)-This item is 1, 2 or 3
            1 = Envelopes
            2 = Step-by-Step
            3 = Last Step
        """
        self.__Model.Results.Setup.SetOptionDirectHist(Value)

    def SetOptionModalHist(self,Value):
        """
        ---This function sets the output option for modal history results---
        inputs:
        Value(int)-This item is 1, 2 or 3
            1 = Envelopes
            2 = Step-by-Step
            3 = Last Step
        """
        self.__Model.Results.Setup.SetOptionModalHist(Value)

    def SetOptionModeShape(self,ModeShapeStart,ModeShapeEnd,ModeShapesAll=False):
        """
        ---This function sets the modes for which mode shape results are reported---
        inputs:
        ModeShapeStart(int)-The first mode for which results are reported when the ModeShapesAll item is False
        ModeShapeEnd(int)-The last mode for which results are reported when the ModeShapesAll item is False
        ModeShapesAll(bool)-If this item is True, results are reported for all calculated modes. If it is False,
            results are reported for the modes indicated by the ModeShapeStart and ModeShapeEnd items
        """
        self.__Model.Results.Setup.SetOptionModeShape(ModeShapeStart,ModeShapeEnd,ModeShapesAll)

    def SetOptionMultiStepStatic(self,Value):
        """
        ---This function sets the output option for multistep static linear results---
        inputs:
        Value(int)-This item is 1, 2 or 3
            1 = Envelopes
            2 = Step-by-Step
            3 = Last Step
        """
        self.__Model.Results.Setup.SetOptionMultiStepStatic(Value)

    def SetOptionMultiValuedCombo(self,Value):
        """
        ---This function sets the output option for multi-valued load combination results---
        inputs:
        Value(int)-This item is either 1, 2, or 3.
            1 = Envelopes
            2 = Multiple values, if possible
            3 = Correspondence
        """
        self.__Model.Results.Setup.SetOptionMultiValuedCombo(Value)

    def SetOptionNLStatic(self,Value):
        """
        ---This function sets the output option for nonlinear static results---
        inputs:
        Value(int)-This item is 1, 2 or 3
            1 = Envelopes
            2 = Step-by-Step
            3 = Last Step
        """
        self.__Model.Results.Setup.SetOptionNLStatic(Value)

    def SetOptionPSD(self,Value):
        """
        ---This function sets the output option for power spectral density results---
        inputs:
        Value(int)-This item is either 1 or 2
            1 = RMS
            2 = sqrt(PSD)
        """
        self.__Model.Results.Setup.SetOptionPSD(Value)

    def SetOptionSteadyState(self,Value,SteadyStateOption):
        """
        ---This function sets the output option for steady state results---
        inputs:
        Value(int)-This item is either 1 or 2
            1 = Envelopes
            2 = At Frequencies
        SteadyStateOption(int)-This item is 1, 2 or 3
            1 = In and Out of Phase
            2 = Magnitude
            3 = All
        """
        self.__Model.Results.Setup.SetOptionSteadyState(Value,SteadyStateOption)

    def SetSectionCutSelectedForOutput(self,Name,Selected):
        """
        ---This function selects or deselects a defined section cut for output---
        inputs:
        Name(str)-The name of a defined section cut
        Selected(bool)-This item is True if the section cut is to be selected for output, or False if no section
            cut should not be selected for output
        """
        self.__Model.Results.Setup.SetSectionCutSelectedForOutput(Name,Selected)

    def GetCaseSelectedForOutput(self,Name):
        """
        ---This function checks if an load case is selected for output---
        inputs:
        Name(str)-The name of an existing load case
        return:
        [index,Selected]

        Selected(bool)-This item is True if the specified load case is selected for output
        """
        result=self.__Model.Results.Setup.GetCaseSelectedForOutput(Name)
        return result

    def GetComboSelectedForOutput(self,Name):
        """
        ---This function checks if a load combination is selected for output---
        inputs:
        Name(str)-The name of an existing load combination
        return:
        [index,Selected]
        Selected(bool)-This item is True if the specified load combination is selected for output
        """
        result=self.__Model.Results.Setup.GetComboSelectedForOutput(Name)
        return result

    def GetOptionBaseReactLoc(self):
        """
        ---This function retrieves the global coordinates of the location at which the base reactions are reported---
        return:
        [index,gx,gy,gz]

        gx,gy,gz(float)-The global coordinates of the location at which the base reactions are reported
        """
        result=self.__Model.Results.Setup.GetOptionBaseReactLoc()
        return result

    def GetOptionBucklingMode(self):
        """
        ---This function retrieves the buckling modes for which buckling factors are reported---
        return:
        [index,BuckModeStart,BuckModeEnd,BuckModeAll]

        BuckModeStart(int)-The first buckling mode for which the buckling factor is reported when the BuckModeAll item is False
        BuckModeEnd(int)-The last buckling mode for which the buckling factor is reported when the BuckModeAll item is False
        BuckModeAll(bool)-If this item is True, buckling factors are reported for all calculated buckling modes.
            If it is False, buckling factors are reported for the buckling modes indicated by the BuckModeStart and BuckModeEnd items
        """
        result=self.__Model.Results.Setup.GetOptionBucklingMode()
        return result

    def GetOptionDirectHist(self):
        """
        ---This function retrieves the output option for direct history results---
        return:
        [index,Value]

        Value(int)-This item is either 1, 2 or 3
            1 = Envelopes
            2 = Step-by-Step
            3 = Last Step
        """
        result=self.__Model.Results.Setup.GetOptionDirectHist()
        return result

    def GetOptionModalHist(self):
        """
        ---This function retrieves the output option for modal history results---
        return:
        [index,Value]

        Value(int)-This item is either 1, 2 or 3
            1 = Envelopes
            2 = Step-by-Step
            3 = Last Step
        """
        result=self.__Model.Results.Setup.GetOptionModalHist()
        return result

    def GetOptionModeShape(self):
        """
        ---This function retrieves the modes for which mode shape results are reported---
        return:
        [index,ModeShapeStart,ModeShapeEnd,ModeShapesAll]

        ModeShapeStart(int)-The first mode for which results are reported when the ModeShapesAll item is False
        ModeShapeEnd(int)-The last mode for which results are reported when the ModeShapesAll item is False
        ModeShapesAll(bool)-If this item is True, results are reported for all calculated modes. If it is False,
            results are reported for the modes indicated by the ModeShapeStart and ModeShapeEnd items
        """
        result=self.__Model.Results.Setup.GetOptionModeShape()
        return result

    def GetOptionMultiStepStatic(self):
        """
        ---This function retrieves the output option for multistep static linear results---
        return:
        [index,Value]

        Value(int)-This item is either 1, 2 or 3
            1 = Envelopes
            2 = Step-by-Step
            3 = Last Step
        """
        result=self.__Model.Results.Setup.GetOptionMultiStepStatic()
        return result

    def GetOptionMultiValuedCombo(self):
        """
        ---This function retrieves the output option for multi-valued load combination results---
        return:
        [index,Value]

        Value(int)-This item is either 1, 2, or 3
            1 = Envelopes
            2 = Multiple values, if possible
            3 = Correspondence
        """
        result=self.__Model.Results.Setup.GetOptionMultiValuedCombo()
        return result

    def GetOptionNLStatic(self):
        """
        ---This function retrieves the output option for nonlinear static results---
        return:
        [index,Value]

        Value(int)-This item is either 1, 2 or 3
            1 = Envelopes
            2 = Step-by-Step
            3 = Last Step
        """
        result=self.__Model.Results.Setup.GetOptionNLStatic()
        return result

    def GetOptionPSD(self):
        """
        ---This function retrieves the output option for power spectral density results---
        return:
        [index,Value]

        Value(int)-This item is either 1 or 2
            1 = RMS
            2 = sqrt(PSD)
        """
        result=self.__Model.Results.Setup.GetOptionPSD()
        return result

    def GetOptionSteadyState(self):
        """
        ---This function retrieves the output option for steady state results---
        return:
        [index,Value,SteadyStateOption]

        Value(int)-This item is either 1 or 2
            1 = Envelopes
            2 = At Frequencies
        SteadyStateOption(int)-This item is 1, 2 or 3
            1 = In and Out of Phase
            2 = Magnitude
            3 = All
        """
        result=self.__Model.Results.Setup.GetOptionSteadyState()
        return result

    def GetSectionCutSelectedForOutput(self,Name):
        """
        ---This function retrieves whether a defined section cut is selected for output---
        inputs:
        Name(str)-The name of a defined section cut
        return:
        [index,Selected]

        Selected(bool)-This item is True if the section cut is to be selected for output, or False if the section cut
            is not selected for output
        """
        result=self.__Model.Results.Setup.GetSectionCutSelectedForOutput(Name)
        return result

class SapResults:
    def __init__(self,Sapobj):
        """
        Translation: Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model
        self.Setup = Results_Setup(Sapobj)

    def AreaForceShell(self,Name,itemTypeElm=0):
        """
        ---This function reports the area forces for the specified area elements that are assigned shell section
        properties (not plane or asolid properties). Note that the forces reported are per unit of in-plane length
        ---
        inputs:
        Name(str)-The name of an existing area object, area element or group of objects, depending on the value of the
            ItemTypeElm item
        itemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the area elements corresponding to the area object
            specified by the Name item.
            If this item is Element, the result request is for the area element specified by the Name item.
            If this item is GroupElm, the result request is for the area elements corresponding to all area objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for area elements corresponding to all selected area
            objects, and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,F11,F22,F12,FMax,Fmin,FAngle,FVM,M11,
        M22,M12,MMax,MMin,MAngle,V13,V23,VMax,VAngle]
        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the area object name associated with each result, if any
        Elm(str list)-This is an array that includes the area element name associated with each result
        PointElm(str list)-This is an array that includes the name of the point element where the results are reported
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated
            with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        F11(float list)-The area element internal F11 membrane direct force per length reported in the area element
            local coordinate system. [F/L]
        F22(float list)-The area element internal F22 membrane direct force per length reported in the area element
            local coordinate system. [F/L]
        F12(float list)-The area element internal F12 membrane shear force per length reported in the area element
            local coordinate system. [F/L]
        FMax(float list)-The maximum principal membrane force per length. [F/L]
        FMin(float list)-The minimum principal membrane force per length. [F/L]
        FAngle(float list)-The angle measured counter clockwise (when the local 3 axis is pointing toward you) from
            the area local 1 axis to the direction of the maximum principal membrane force. [deg]
        FVM(float list)-The area element internal Von Mises membrane force per length. [F/L]
        M11(float list)-The area element internal M11 plate bending moment per length reported in the area element
            local coordinate system. This item is only reported for area elements with properties that allow plate
            bending behavior. [FL/L]
        M22(float list)-The area element internal M22 plate bending moment per length reported in the area element
            local coordinate system. This item is only reported for area elements with properties that allow plate
            bending behavior. [FL/L]
        M12(float list)-The area element internal M12 plate twisting moment per length reported in the area element
            local coordinate system. This item is only reported for area elements with properties that allow plate
            bending behavior. [FL/L]
        MMax(float list)-The maximum principal plate moment per length. This item is only reported for area elements
            with properties that allow plate bending behavior. [FL/L]
        MMin(float list)-The minimum principal plate moment per length. This item is only reported for area elements
            with properties that allow plate bending behavior. [FL/L]
        MAngle(float list)-The angle measured counter clockwise (when the local 3 axis is pointing toward you) from
            the area local 1 axis to the direction of the maximum principal plate moment. This item is only reported
            for area elements with properties that allow plate bending behavior. [deg]
        V13(float list)-The area element internal V13 plate transverse shear force per length reported in the area
            element local coordinate system. This item is only reported for area elements with properties that
            allow plate bending behavior. [F/L]
        V23(float list)-The area element internal V23 plate transverse shear force per length reported in the area
            element local coordinate system. This item is only reported for area elements with properties that
            allow plate bending behavior. [F/L]
        VMax(float list)-The maximum plate transverse shear force. It is equal to the square root of the sum of the
            squares of V13 and V23. This item is only reported for area elements with properties that allow plate
            bending behavior. [F/L]
        VAngle(float list)-The angle measured counter clockwise (when the local 3 axis is pointing toward you) from
            the area local 1 axis to the direction of Vmax. This item is only reported for area elements with properties
            that allow plate bending behavior. [deg]
        """
        result=self.__Model.Results.AreaForceShell(Name,itemTypeElm)
        return result

    def AreaJointForcePlane(self,Name,ObjectElm=0):
        """
        ---This function reports the area joint forces for the point elements at each corner of the specified plane
        elements that have plane-type or asolid-type properties (not shell).
        ---
        inputs:
        Name(str)-The name of an existing area object, area element or group of objects depending on the value of the
            ItemTypeElm item
        ObjectElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the plane elements corresponding to the area object
            specified by the Name item.
            If this item is Element, the result request is for the plane element specified by the Name item.
            If this item is GroupElm, the result request is for the plane elements corresponding to all area objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for plane elements corresponding to all selected area
            objects and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,F1,F2,F3,M1,M2,M3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the area object name associated with each result, if any
        Elm(str list)-This is an array that includes the plane element name associated with each result
        PointElm(str list)-This is an array that includes the point element name associated with each result.
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination
            associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        F1,F2,F3(float list)-These are one dimensional arrays that include the joint force components in the
            point element local axes directions. [F]
        M1,M2,M3(float list)-These are one dimensional arrays that include the joint moment components about
            the point element local axes. [FL]
        """
        result=self.__Model.Results.AreaJointForcePlane(Name,ObjectElm)
        return result

    def AreaJointForceShell(self,Name,ItemTypeElm=0):
        """
        ---This function reports the area joint forces for the point elements at each corner of the specified area
        elements that have shell-type properties (not plane or asolid).
        ---
        inputs:
        Name(str)-The name of an existing area object, area element or group of objects, depending on the value of
            the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the area elements corresponding to the area object
            specified by the Name item.
            If this item is Element, the result request is for the area element specified by the Name item.
            If this item is GroupElm, the result request is for the area elements corresponding to all area objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for area elements corresponding to all selected area
            objects and the Name item is ignored
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,F1,F2,F3,M1,M2,M3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the area object name associated with each result, if any
        Elm(str list)-This is an array that includes the area element name associated with each result
        PointElm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination
            associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        F1,F2,F3(float list)-These are one dimensional arrays that include the joint force components in the point
            element local axes directions. [F]
        M1,M2,M3(float list)-These are one dimensional arrays that include the joint moment components about the
            point element local axes. [FL]
        """
        result=self.__Model.Results.AreaJointForceShell(Name,ItemTypeElm)
        return result

    def AreaStrainShell(self,Name,ItemTypeElm=0):
        """
        ---This function reports the area strains for the specified area elements that are assigned shell section
        properties (not plane or asolid properties). Strains are reported at each point element associated with
        the area element
        ---
        inputs:
        Name(str)-The name of an existing area object, area element or group of objects, depending on the value of
            the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the area elements corresponding to the area
            object specified by the Name item.
            If this item is Element, the result request is for the area element specified by the Name item.
            If this item is GroupElm, the result request is for the area elements corresponding to all area objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for area elements corresponding to all selected area
            objects and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,E11Top,E22Top,G12Top,E11Bot,E22Bot,G12Bot,
        EMaxTop,EMinTop,EMaxBot,EMinBot,EAngleTop,EAngleBot,EVMTop,EVMBot,G13Avg,G23Avg,GMaxAvg,GAngleAvg]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the area object name associated with each result, if any
        Elm(str list)-This is an array that includes the area element name associated with each result
        PointElm(str list)-This is an array that includes the name of the point element where the results are reported
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        E11Top,E22Top,G12Top,E11Bot,E22Bot,G12Bot(float)-The area element internal E11, E22 and G12 strains, at the
            top or bottom of the specified area element, at the specified point element location, reported in the
            area element local coordinate system
        EMaxTop,EMinTop,EMaxBot,EMinBot(float)-The area element maximum and minimum principal strains, at the top or
            bottom of the specified area element, at the specified point element location
        EAngleTop,EAngleBot(float)-The angle measured counter clockwise (when the local 3 axis is pointing toward
            you) from the area local 1 axis to the direction of the maximum principal strain, at the top or bottom
            of the specified area element. [deg]
        EVMTop,EVMBot(float)-The area element internal top or bottom Von Mises strain at the specified point element
        G13Avg,G23Avg(float)-The area element average G13 or G23 out-of-plane shear strain at the specified point
            element. These items are only reported for area elements with properties that allow plate bending behavior
        GMaxAvg(float)-The area element maximum average out-of-plane shear strain. It is equal to the square root
            of the sum of the squares of G13Avg and G23Avg. This item is only reported for area elements with properties
            that allow plate bending behavior
        GAngleAvg(float)-The angle measured counter clockwise (when the local 3 axis is pointing toward you) from the
            area local 1 axis to the direction of GMaxAvg. This item is only reported for area elements with
            properties that allow plate bending behavior. [deg]
        """
        result=self.__Model.Results.AreaStrainShell(Name,ItemTypeElm)
        return result

    def AreaStrainShellLayered(self,Name,ItemTypeElm=0):
        """
        ---This function reports the area strains for the specified area elements that are assigned layered shell
        section properties
        ---
        inputs:
        Name(str)-The name of an existing area object, area element or group of objects, depending on the value
            of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the area elements corresponding to the area object
            specified by the Name item.
            If this item is Element, the result request is for the area element specified by the Name item.
            If this item is GroupElm, the result request is for the area elements corresponding to all area objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for area elements corresponding to all selected area
            objects and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,Layer,IntPtNum,IntPtLoc,PointElm,LoadCase,StepType,StepNum,E11,E22,G12,EMax,
        EMin,EAngle,EVM,G13Avg,G23Avg,GMaxAvg,GangleAvg]
        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the area object name associated with each result, if any
        Elm(str list)-This is an array that includes the area element name associated with each result
        Layer(str list)-This is an array that includes the layer name associated with each result
        IntPtNum(int list)-This is an array that includes the integration point number within the specified layer of
            the area element
        IntPtLoc(float list)-This is an array that includes the integration point relative location within the specified
            layer of the area element. The location is between -1 (bottom of layer) and +1 (top of layer), inclusive. The
            midheight of the layer is at a value of 0
        PointElm(str list)-This is an array that includes the name of the point element where the results are reported
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated
            with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        E11,E22,G12(float list)-The area element internal E11, E22 and G12 strains, at the specified point element
            location, for the specified layer and layer integration point, reported in the area element local coordinate system
        EMax,EMin(float)-The area element maximum and minimum principal strains, at the specified point element location,
            for the specified layer and layer integration point
        EAngle(float)-The angle measured counter clockwise (when the local 3 axis is pointing toward you) from the area
            local 1 axis to the direction of the maximum principal strain. [deg
        EVM(float)-The area element internal Von Mises strain at the specified point element location, for the specified
            layer and layer integration point
        G13Avg,G23Avg(float)-The area element average G13 or G23 out-of-plane shear strain at the specified point element
            location, for the specified layer and layer integration point
        GMaxAvg(float)-The area element maximum average out-of-plane shear strain for the specified layer and layer
            integration point. It is equal to the square root of the sum of the squares of G13Avg and G23Avg
        GAngleAvg(float)-The angle measured counter clockwise (when the local 3 axis is pointing toward you) from the area
            local 1 axis to the direction of GMaxAvg. [deg]
        """
        result=self.__Model.Results.AreaStrainShellLayered(Name,ItemTypeElm)
        return result

    def AreaStressPlane(self,Name,ItemTypeElm=0):
        """
        ---This function reports the stresses for the specified plane elements that are assigned plane or asolid
        section properties (not shell properties).
        ---
        inputs:
        Name(str)-The name of an existing area object, area element or group of objects, depending on the value
            of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the plane elements corresponding to the area object
            specified by the Name item.
            If this item is Element, the result request is for the plane element specified by the Name item.
            If this item is GroupElm, the result request is for the plane elements corresponding to all area objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for plane elements corresponding to all selected area
            objects, and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,S11,S22,S33,S12,SMax,SMin,SAngle,SVM]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the area object name associated with each result, if any
        Elm(str list)-This is an array that includes the plane element name associated with each result
        PointElm(str list)-This is an array that includes the name of the point element where the results are reported
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        S11,S22,S33,S12(float)-The plane element internal S11, S22, S33 and S12 stresses, at the specified point
            element location, reported in the area element local coordinate system. [F/L2]
        SMax,SMin(float)-The plane element maximum and minimum principal stresses at the specified point element location. [F/L2]
        SAngle(float)-The angle measured counter clockwise (when the local 3 axis is pointing toward you) from the
            plane element local 1 axis to the direction of the maximum principal stress. [deg]
        SVM(float)-The plane element internal Von Mises stress at the specified point element. [F/L2]
        """
        result=self.__Model.Results.AreaStressPlane(Name,ItemTypeElm)
        return result

    def AreaStressShell(self,Name,ItemTypeElm=0):
        """
        ---This function reports the area stresses for the specified area elements that are assigned shell section
        properties (not plane or asolid properties). Stresses are reported at each point element associated with
        the area element
        ---
        inputs:
        Name(str)-The name of an existing area object, area element or group of objects, depending on the value of
            the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the area elements corresponding to the area object
            specified by the Name item.
            If this item is Element, the result request is for the area element specified by the Name item.
            If this item is GroupElm, the result request is for the area elements corresponding to all area objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for area elements corresponding to all selected area
            objects and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,S11Top,S22Top,S12Top,S11Bot,S22Bot,S12Bot,
        SMaxTop,SMinTop,SMaxBot,SMinBot,SAngleTop,SAngleBot,SVMTop,SVMBot,S13Avg,S23Avg,SMaxAvg,SAngleAvg]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the area object name associated with each result, if any
        Elm(str list)-This is an array that includes the area element name associated with each result
        PointElm(str list)-This is an array that includes the name of the point element where the results are reported
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated
            with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        S11Top,S22Top,S12Top,S11Bot,S22Bot,S12Bot(float)-The area element internal S11, S22 and S12 stresses, at
            the top or bottom of the specified area element, at the specified point element location, reported in
            the area element local coordinate system. [F/L2]
        SMaxTop,SMinTop,SMaxBot,SMinBot(float)-The area element maximum and minimum principal stresses, at the top or
            bottom of the specified area element, at the specified point element location. [F/L2]
        SAngleTop,SAngleBot(float)-The angle measured counter clockwise (when the local 3 axis is pointing toward you)
            from the area local 1 axis to the direction of the maximum principal stress, at the top or bottom of the
            specified area element. [deg]
        SVMTop,SVMBot(float)-The area element internal top or bottom Von Mises stress at the specified point element. [F/L2]
        S13Avg,S23Avg(float)-The area element average S13 or S23 out-of-plane shear stress at the specified point element.
            These items are only reported for area elements with properties that allow plate bending behavior. [F/L2]
        SMaxAvg(float)-The area element maximum average out-of-plane shear stress. It is equal to the square root of
            the sum of the squares of S13Avg and S23Avg. This item is only reported for area elements with properties
            that allow plate bending behavior. [F/L2]
        SAngleAvg(float)-The angle measured counter clockwise (when the local 3 axis is pointing toward you) from the
            area local 1 axis to the direction of SMaxAvg. This item is only reported for area elements with properties
            that allow plate bending behavior. [deg]
        """
        result=self.__Model.Results.AreaStressShell(Name,ItemTypeElm)
        return result

    def AreaStressShellLayered(self,Name,ItemTypeElm=0):
        """
        ---This function reports the area stresses for the specified area elements that are assigned layered shell
        section properties
        ---
        inputs:
        Name(str)-The name of an existing area object, area element or group of objects, depending on the value of the
            ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the area elements corresponding to the area object
            specified by the Name item.
            If this item is Element, the result request is for the area element specified by the Name item.
            If this item is GroupElm, the result request is for the area elements corresponding to all area objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for area elements corresponding to all selected area
            objects and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,Layer,IntPtNum,IntPtLoc,PointElm,LoadCase,StepType,StepNum,S11,S22,S12,SMax,SMin,
        SAngle,SVM,S13Avg,S23Avg,SMaxAvg,SAngleAvg]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the area object name associated with each result, if any
        Elm(str list)-This is an array that includes the area element name associated with each result
        Layer(str list)-This is an array that includes the layer name associated with each result
        IntPtNum(int list)-This is an array that includes the integration point number within the specified
            layer of the area element
        IntPtLoc(float list)-This is an array that includes the integration point relative location within the
            specified layer of the area element. The location is between -1 (bottom of layer) and +1 (top of layer),
            inclusive. The midheight of the layer is at a value of 0
        PointElm(str list)-This is an array that includes the name of the point element where the results are reported
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated
            with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        S11,S22,S12(float)-The area element internal S11, S22 and S12 stresses, at the specified point element
            location, for the specified layer and layer integration point, reported in the area element local
            coordinate system. [F/L2]
        SMax,SMin(float)-The area element maximum and minimum principal stresses, at the specified point element
            location, for the specified layer and layer integration point. [F/L2]
        SAngle(float)-The angle measured counter clockwise (when the local 3 axis is pointing toward you) from
            the area local 1 axis to the direction of the maximum principal stress. [deg]
        SVM(float)-The area element internal Von Mises stress at the specified point element location, for the
            specified layer and layer integration point. [F/L2]
        S13Avg,S23Avg(float)-The area element average S13 or S23 out-of-plane shear stress at the specified point
            element location, for the specified layer and layer integration point. [F/L2]
        SMaxAvg(float)-The area element maximum average out-of-plane shear stress for the specified layer and layer
            integration point. It is equal to the square root of the sum of the squares of S13Avg and S23Avg. [F/L2]
        SAngleAvg(float)-The angle measured counter clockwise (when the local 3 axis is pointing toward you) from
            the area local 1 axis to the direction of SMaxAvg. [deg]
        """
        result=self.__Model.Results.AreaStressShellLayered(Name,ItemTypeElm)
        return result

    def AssembledJointMass_1(self,MassSourceName,Name,itemTypeElm):
        """
        ---This function reports the assembled joint masses for the specified point elements---
        inputs:
        MassSourceName(str)-The name of an existing mass source definition. If this value is left empty or
            unrecognized, data for all mass sources will be returned
        Name(str)-The name of an existing point element or group of objects, depending on the value of the ItemTypeElm item
        itemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the point element corresponding to the point
            object specified by the Name item.
            If this item is Element, the result request is for the point element specified by the Name item.
            If this item is GroupElm, the result request is for all point elements directly or indirectly specified
            in the group specified by the Name item.
            If this item is SelectionElm, the result request is for all point elements directly or indirectly
            selected and the Name item is ignored.
        return:
        [index,NumberResults,PointElm,MassSource,U1,U2,U3,R1,R2,R3]

        NumberResults(int)-The total number of results returned by the program
        PointElm(str list)-This is an array that includes the point element name associated with each result
        MassSource(str list)-This is an array that includes the mass source name associated with each result
        U1,U2,U3(float)-These are one dimensional arrays that include the translational mass in the point
            element local 1, 2 and 3 axes directions, respectively, for each result. [M]
        R1,R2,R3(float)-These are one dimensional arrays that include the rotational mass moment of inertia
            about the point element local 1, 2 and 3 axes, respectively, for each result. [ML2]
        """
        result=self.__Model.Results.AssembledJointMass_1(MassSourceName,Name,itemTypeElm)
        return result

    def BaseReact(self):
        """
        ---This function reports the structure total base reactions---
        return:
        [index,NumberResults,LoadCase,StepType,StepNum,FX,Fy,Fz,Mx,My,Mz,gx,gy,gz]

        NumberResults(int)-The total number of results returned by the program
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated with each resul
        StepType(str list)-This is an array that includes the step type, if any, for each result.
        StepNum(int)-This is an array that includes the step number, if any, for each result
        Fx,Fy,Fz(float list)-These are one dimensional arrays that include the base reaction forces in the global
            X, Y and Z directions, respectively, for each result. [F]
        Mx,My,Mz(float list)-These are one dimensional arrays that include the base reaction moments about the global
            X, Y and Z axes, respectively, for each result. [FL]
        gx,gy,gz(float)-These are the global X, Y and Z coordinates of the point at which the base reactions are reported. [L]
        """
        result=self.__Model.Results.BaseReact()
        return result

    def BaseReactWithCentroid(self):
        """
        ---This function reports the structure total base reactions and includes information on the centroid of the
        translational reaction forces
        ---
        return:
        [index,NumberResults,LoadCase,StepType,StepNum,Fx,Fy,Fz,Mx,My,Mz,gx,gy,gz,XCentroidForFx,YCentroidForFx,
        ZCentroidForFx,XCentroidForFy,YCentroidForFy,ZCentroidForFy,XCentroidForFz,YCentroidForFz,ZCentroidForFz]

        NumberResults(int)-The total number of results returned by the program
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int)-This is an array that includes the step number, if any, for each result
        Fx,Fy,Fz(float list)-These are one dimensional arrays that include the base reaction forces in the global
            X, Y and Z directions, respectively, for each result. [F]
        Mx,My,Mz(float list)-These are one dimensional arrays that include the base reaction moments about the global
            X, Y and Z axes, respectively, for each result. [FL]
        gx,gy,gz(float)-These are the global X, Y and Z coordinates of the point at which the base reactions are reported. [L]
        XCentroidForFx,YCentroidForFx,ZCentroidForFx(float list)-These are arrays of the global X, Y and Z coordinates,
            respectively, of the centroid of all global X-direction translational reaction forces for each result
        XCentroidFforFy,YCentroidForFy,ZCentroidForFy(float list)-These are arrays of the global X, Y and Z coordinates,
            respectively, of the centroid of all global Y-direction translational reaction forces for each result
        XCentroidForFz,YCentroidForFz,ZCentroidForFz(float list)-These are arrays of the global X, Y and Z coordinates,
            respectively, of the centroid of all global Z-direction translational reaction forces for each result
        """
        result=self.__Model.Results.BaseReactWithCentroid()
        return result

    def BucklingFactor(self):
        """
        ---This function reports buckling factors obtained from buckling load cases---
        return:
        [index,NumberResults,LoadCase,StepType,StepNum,Factor]

        NumberResults(int)-The total number of results returned by the program
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated with each result
        StepType(str list)-This is an array that includes the step type for each result. For buckling factors, the step type is always Mode
        StepNum(int list)-This is an array that includes the step number for each result. For buckling factors,
            the step number is always the buckling mode number
        Factor(float list)-This is an array that includes the buckling factors
        """
        result=self.__Model.Results.BucklingFactor()
        return result

    def FrameForce(self,Name,ItemTypeElm=0):
        """
        ---This function reports the frame forces for the specified line elements---
        return:
        [index,NumberResults,Obj,ObjSta,Elm,ElmSta,LoadCase,StepType,StepNum,P,V2,V3,T,M2,M3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the line object name associated with each result, if any
        ObjSta(float list)-This is an array that includes the distance measured from the I-end of the line object
            to the result location
        Elm(str list)-This is an array that includes the line element name associated with each result
        ElmSta(float list)-This is an array that includes the distance measured from the I-end of the line
            element to the result location
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination
            associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        P,V2,V3(float list)-These are one dimensional arrays that include the axial force, shear force in the
            local 2 direction, and shear force in the local 3 direction, respectively, for each result. [F]
        T,M2,M3(float list)-These are one dimensional arrays that include the torsion, moment about the local 2axis,
            and moment about the local 3-axis, respectively, for each result. [FL]
        """
        result=self.__Model.Results.FrameForce(Name,ItemTypeElm)
        return result

    def FrameJointForce(self,Name,ItemTypeElm=0):
        """
        ---This function reports the frame joint forces for the point elements at each end of the specified line elements---
        inputs:
        Name(str)-The name of an existing line object, line element or group of objects depending on the value of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the line elements corresponding to the line object
            specified by the Name item.
            If this item is Element, the result request is for the line element specified by the Name item.
            If this item is GroupElm, the result request is for the line elements corresponding to all line objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for line elements corresponding to all selected line
            objects and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,F1,F2,F3,M1,M2,M3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the line object name associated with each result, if any
        Elm(str list)-This is an array that includes the line element name associated with each result
        PointElm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        F1,F2,F3(float list)-These are one dimensional arrays that include the joint force components in the point
            element local axes directions. [F]
        M1,M2,M3(float list)-These are one dimensional arrays that include the joint moment components about the
            point element local axes. [FL]
        """
        result=self.__Model.Results.FrameJointForce(Name,ItemTypeElm)
        return result

    def GeneralizedDispl(self,Name):
        """
        ---This function reports the displacement values for the specified generalized displacements---
        inputs:
        Name(str)-The name of an existing generalized displacement for which results are returned. If the program does
            not recognize this name as a defined generalized displacement, it returns results for all selected generalized
            displacements, if any. For example, entering a blank string (i.e., "") for the name will prompt the program
            to return results for all selected generalized displacements
        return:
        [index,NumberResults,GD,LoadCase,StepType,StepNum,DType,Value]

        NumberResults(int)-The total number of results returned by the program
        GD(str list)-This is an array that includes the generalized displacement name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination
            associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        DType(str list)-This is an array that includes the generalized displacement type for each result.
            It is either Translation or Rotation
        Value(float list)-This is an array of the generalized displacement values for each result.[L] when DType is
            Translation , [rad] when DType is Rotation
        """
        result=self.__Model.Results.GeneralizedDispl(Name)
        return result

    def JointAcc(self,Name,ItemTypeElm=0):
        """
        ---This function reports the joint accelerations for the specified point elements. The accelerations
        reported by this function are relative accelerations
        ---
        inputs:
        Name(str)-The name of an existing point object, point element, or group of objects,
            depending on the value of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the point element corresponding to the point
            object specified by the Name item.
            If this item is Element, the result request is for the point element specified by the Name item.
            If this item is GroupElm, the result request is for all point elements directly or indirectly specified in
            the group specified by the Name item.
            If this item is SelectionElm, the result request is for all point elements directly or indirectly selected
            and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,LoadCase,StepType,StepNum,U1,U2,U3,R1,R2,R3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the point object name associated with each result, if any.
            Some results will have no point object associated with them. For those cases, this item will be blank
        Elm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination
            associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        U1,U2,U3(float list)-These are one dimensional arrays that include the translational acceleration in the point
            element local 1, 2 and 3 axes directions, respectively, for each result. [L/s2]
        R1,R2,R3(float list)-These are one dimensional arrays that include the rotational acceleration about the point
            element local 1, 2 and 3 axes, respectively, for each result. [rad/s2]
        """
        result=self.__Model.Results.JointAcc(Name,ItemTypeElm)
        return result

    def JointAccAbs(self,Name,ItemTypeElm=0):
        """
        ---This function reports the joint absolute accelerations for the specified point elements. Absolute and
        relative accelerations are the same, except when reported for time history load cases subjected to acceleration
        loading
        ---
        inputs:
        Name(str)-The name of an existing point object, point element, or group of objects depending on the value
            of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the point element corresponding to the point object
            specified by the Name item.
            If this item is Element, the result request is for the point element specified by the Name item.
            If this item is GroupElm, the result request is for all point elements directly or indirectly specified in
            the group specified by the Name item.
            If this item is SelectionElm, the result request is for all point elements directly or indirectly selected
            and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,LoadCase,StepType,StepNum,U1,U2,U3,R1,R2,R3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the point object name associated with each result, if any.
            Some results will have no point object associated with them. For those cases, this item will be blank
        Elm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination
            associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        U1,U2,U3(float list)-These are one dimensional arrays that include the translational acceleration in the point
            element local 1, 2 and 3 axes directions, respectively, for each result. [L/s2]
        R1,R2,R3(float list)-These are one dimensional arrays that include the rotational acceleration about the point
            element local 1, 2 and 3 axes, respectively, for each result. [rad/s2]
        """
        result=self.__Model.Results.JointAccAbs(Name,ItemTypeElm)
        return result

    def JointDispl(self,Name,ItemTypeElm=0):
        """
        ---This function reports the joint displacements for the specified point elements. The displacements reported
        by this function are relative displacements
        ---
        inputs:
        Name(str)-The name of an existing point object, point element, or group of objects depending on the value
            of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the point element corresponding to the point object
            specified by the Name item.
            If this item is Element, the result request is for the point element specified by the Name item.
            If this item is GroupElm, the result request is for all point elements directly or indirectly specified in
            the group specified by the Name item.
            If this item is SelectionElm, the result request is for all point elements directly or indirectly selected
            and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,LoadCase,StepType,StepNum,U1,U2,U3,R1,R2,R3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the point object name associated with each result, if any.
            Some results will have no point object associated with them. For those cases, this item will be blank
        Elm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination
            associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        U1,U2,U3(float list)-These are one dimensional arrays that include the displacement in the point element
            local 1, 2 and 3 axes directions, respectively, for each result. [L]
        R1,R2,R3(float list)-These are one dimensional arrays that include the rotation about the point element
            local 1, 2 and 3 axes, respectively, for each result. [rad]
        """
        result=self.__Model.Results.JointDispl(Name,ItemTypeElm)
        return result

    def JointDisplAbs(self,Name,ItemTypeElm=0):
        """
        ---This function reports the absolute joint displacements for the specified point elements. Absolute and
        relative displacements are the same except when reported for time history load cases subjected to acceleration
        loading
        ---
        inputs:
        Name(str)-The name of an existing point object, point element, or group of objects depending on the value
            of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the point element corresponding to the point object
            specified by the Name item.
            If this item is Element, the result request is for the point element specified by the Name item.
            If this item is GroupElm, the result request is for all point elements directly or indirectly specified in
            the group specified by the Name item.
            If this item is SelectionElm, the result request is for all point elements directly or indirectly selected
            and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,LoadCase,StepType,StepNum,U1,U2,U3,R1,R2,R3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the point object name associated with each result, if any.
            Some results will have no point object associated with them. For those cases, this item will be blank
        Elm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination
            associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        U1,U2,U3(float list)-These are one dimensional arrays that include the displacement in the point element
            local 1, 2 and 3 axes directions, respectively, for each result. [L]
        R1,R2,R3(float list)-These are one dimensional arrays that include the rotation about the point element
            local 1, 2 and 3 axes, respectively, for each result. [rad]
        """
        result=self.__Model.Results.JointDisplAbs(Name,ItemTypeElm)
        return result

    def JointReact(self,Name,ItemTypeElm=0):
        """
        ---This function reports the joint reactions for the specified point elements. The reactions reported are from
        restraints, springs and grounded (one-joint) links---
        inputs:
        Name(str)-The name of an existing line object, line element or group of objects depending on the value of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the line elements corresponding to the line object
            specified by the Name item.
            If this item is Element, the result request is for the line element specified by the Name item.
            If this item is GroupElm, the result request is for the line elements corresponding to all line objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for line elements corresponding to all selected line
            objects and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,F1,F2,F3,M1,M2,M3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the line object name associated with each result, if any
        Elm(str list)-This is an array that includes the line element name associated with each result
        PointElm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        F1,F2,F3(float list)-These are one dimensional arrays that include the reaction forces in the point element
            local 1, 2 and 3 axes directions, respectively, for each result. [F]
        M1,M2,M3(float list)-These are one dimensional arrays that include the reaction moments about the point
            element local 1, 2 and 3 axes, respectively, for each result. [FL]
        """
        result=self.__Model.Results.JointReact(Name,ItemTypeElm)
        return result

    def JointVel(self,Name,ItemTypeElm=0):
        """
        ---This function reports the joint velocities for the specified point elements. The velocities reported by
        this function are relative velocities
        ---
        inputs:
        Name(str)-The name of an existing point object, point element, or group of objects depending on the value
            of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the point element corresponding to the point object
            specified by the Name item.
            If this item is Element, the result request is for the point element specified by the Name item.
            If this item is GroupElm, the result request is for all point elements directly or indirectly specified in
            the group specified by the Name item.
            If this item is SelectionElm, the result request is for all point elements directly or indirectly selected
            and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,LoadCase,StepType,StepNum,U1,U2,U3,R1,R2,R3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the point object name associated with each result, if any.
            Some results will have no point object associated with them. For those cases, this item will be blank
        Elm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination
            associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        U1,U2,U3(float list)-These are one dimensional arrays that include the translational velocity in the
            point element local 1, 2 and 3 axes directions, respectively, for each result. [L/s]
        R1,R2,R3(float list)-These are one dimensional arrays that include the rotational velocity about the
            point element local 1, 2 and 3 axes, respectively, for each result. [rad/s]
        """
        result=self.__Model.Results.JointVel(Name,ItemTypeElm)
        return result

    def JointVelAbs(self,Name,ItemTypeElm=0):
        """
        ---This function reports the joint absolute velocities for the specified point elements. Absolute and
        relative velocities are the same, except when reported for time history load cases subjected to acceleration
        loading---
        inputs:
        Name(str)-The name of an existing point object, point element, or group of objects depending on the value
            of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the point element corresponding to the point object
            specified by the Name item.
            If this item is Element, the result request is for the point element specified by the Name item.
            If this item is GroupElm, the result request is for all point elements directly or indirectly specified in
            the group specified by the Name item.
            If this item is SelectionElm, the result request is for all point elements directly or indirectly selected
            and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,LoadCase,StepType,StepNum,U1,U2,U3,R1,R2,R3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the point object name associated with each result, if any.
            Some results will have no point object associated with them. For those cases, this item will be blank
        Elm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination
            associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        U1,U2,U3(float list)-These are one dimensional arrays that include the translational velocity in the
            point element local 1, 2 and 3 axes directions, respectively, for each result. [L/s]
        R1,R2,R3(float list)-These are one dimensional arrays that include the rotational velocity about the
            point element local 1, 2 and 3 axes, respectively, for each result. [rad/s]
        """
        result=self.__Model.Results.JointVelAbs(Name,ItemTypeElm)
        return result

    def LinkDeformation(self,Name,ItemTypeElm=0):
        """
        ---This function reports the link internal deformations---
        inputs:
        Name(str)-The name of an existing point object, point element, or group of objects depending on the value
            of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the point element corresponding to the point object
            specified by the Name item.
            If this item is Element, the result request is for the point element specified by the Name item.
            If this item is GroupElm, the result request is for all point elements directly or indirectly specified in
            the group specified by the Name item.
            If this item is SelectionElm, the result request is for all point elements directly or indirectly selected
            and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,LoadCase,StepType,StepNum,U1,U2,U3,R1,R2,R3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the point object name associated with each result, if any.
            Some results will have no point object associated with them. For those cases, this item will be blank
        Elm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination
            associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        U1,U2,U3(float list)-These are one dimensional arrays that include the internal translational deformation
            of the link in the link element local axes directions. [L]
        R1,R2,R3(float list)-These are one dimensional arrays that include the internal rotational deformation
            of the link about the link element local axes. [rad]
        """
        result=self.__Model.Results.LinkDeformation(Name,ItemTypeElm)
        return result

    def LinkForce(self,Name,ItemTypeElm=0):
        """
        ---This function reports the link forces at the point elements at the ends of the specified link elements---
        inputs:
        Name(str)-The name of an existing point object, point element, or group of objects depending on the value
            of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the point element corresponding to the point object
            specified by the Name item.
            If this item is Element, the result request is for the point element specified by the Name item.
            If this item is GroupElm, the result request is for all point elements directly or indirectly specified in
            the group specified by the Name item.
            If this item is SelectionElm, the result request is for all point elements directly or indirectly selected
            and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,P,V2,V3,T,M2,M3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the line object name associated with each result, if any
        Elm(str list)-This is an array that includes the line element name associated with each result
        PointElm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        P(float list)-This is an array that includes the link axial force (in the link local 1-axis direction)
            at the specified point element. [F]
        V2,V3(float list)-These are one dimensional arrays that include the link shear force components in the link
            element local axes directions. [F]
        T(float list)-This is an array that includes the link torsion (about the link local 1-axis) at the specified
            point element. [FL]
        M2,M3(float list)-These are one dimensional arrays that include the link moment components about the link
            element local axes. [FL]
        """
        result=self.__Model.Results.LinkForce(Name,ItemTypeElm)
        return result

    def LinkJointForce(self,Name,ItemTypeElm=0):
        """
        ---This function reports the joint forces for the point elements at the ends of the specified link elements---
        inputs:
        Name(str)-The name of an existing line object, line element or group of objects depending on the value of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the line elements corresponding to the line object
            specified by the Name item.
            If this item is Element, the result request is for the line element specified by the Name item.
            If this item is GroupElm, the result request is for the line elements corresponding to all line objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for line elements corresponding to all selected line
            objects and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,F1,F2,F3,M1,M2,M3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the line object name associated with each result, if any
        Elm(str list)-This is an array that includes the line element name associated with each result
        PointElm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result
        F1,F2,F3(float list)-These are one dimensional arrays that include the joint force components in the point
            element local axes directions. [F]
        M1,M2,M3(float list)-These are one dimensional arrays that include the joint moment components about the
            point element local axes. [FL]
        """
        result=self.__Model.Results.LinkJointForce(Name,ItemTypeElm)
        return result

    def ModalLoadParticipationRatios(self):
        """
        ---This function reports the modal load participation ratios for each selected modal analysis case---
        return:[index,NumberResults,LoadCase,ItemType,Item,Stat,Dyn]

        NumberResults(int)-The total number of results returned by the program
        LoadCase(str list)-This is an array that includes the name of the modal load case associated with each result
        ItemType(str list)-This is an array that includes Load Pattern, Acceleration, Link or Panel Zone. It specifies
            the type of item for which the modal load participation is reported.
        Item(str list)-This is an array whose values depend on the ItemType. If the ItemType is Load Pattern,
            this is the name of the load pattern.
            If the ItemType is Acceleration, this is UX, UY, UZ, RX, RY, or RZ, indicating the acceleration direction.
            If the ItemType is Link, this is the name of the link followed by U1, U2, U3, R1, R2, or R3 (in parenthesis),
            indicating the link degree of freedom for which the output is reported.
            If the ItemType is Panel Zone, this is the name of the joint to which the panel zone is assigned, followed
            by U1, U2, U3, R1, R2, or R3 (in parenthesis), indicating the degree of freedom for which the output is reported.

        Stat(float list)-This is an array that includes the percent static load participation ratio
        Dyn(float list)-This is an array that includes the percent dynamic load participation ratio
        """
        result=self.__Model.Results.ModalLoadParticipationRatios()
        return result

    def ModalParticipatingMassRatios(self):
        """
        ---This function reports the modal participating mass ratios for each mode of each selected modal analysis case---
        return:
        [index,NumberResults,LoadCase,StepType,StepNum,Period,Ux,Uy,Uz,SumUx,SUmUy,SumUz,Rx,Ry,Rz,SumRx,SumRy,SumRz]

        NumberResults(int)-The total number of results returned by the program
        LoadCase(str list)-This is an array that includes the name of the modal load case associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result. For modal results, this will always be Mode
        StepNum(int list)-This is an array that includes the step number for each result. For modal results, this is always the mode number
        Period(float)-This is an array that includes the period for each result. [s]
        Ux(float list)-This is an array that includes the modal participating mass ratio for the structure Uy degree of
            freedom. The ratio applies to the specified mode.
        Uy(float list)-This is an array that includes the modal participating mass ratio for the structure Uy degree of
            freedom. The ratio applies to the specified mode.
        Uz(float list)-This is an array that includes the modal participating mass ratio for the structure Uz degree of
            freedom. The ratio applies to the specified mode
        SumUx(float list)-This is an array that includes the cumulative sum of the modal participating mass ratios for
            the structure Ux degree of freedom
        SumUy(float list)-This is an array that includes the cumulative sum of the modal participating mass ratios for
            the structure Uy degree of freedom
        SumUz(float list)-This is an array that includes the cumulative sum of the modal participating mass ratios for
            the structure Uz degree of freedom
        Rx(float list)-This is an array that includes the modal participating mass ratio for the structure Rx degree of
            freedom. The ratio applies to the specified mode
        Ry(float list)-This is an array that includes the modal participating mass ratio for the structure Ry degree of
            freedom. The ratio applies to the specified mode
        Rz(float list)-This is an array that includes the modal participating mass ratio for the structure Rz degree of
            freedom. The ratio applies to the specified mode
        SumRx(float list)-This is an array that includes the cumulative sum of the modal participating mass ratios for
            the structure Rx degree of freedom
        SumRy(float list)-This is an array that includes the cumulative sum of the modal participating mass ratios for
            the structure Ry degree of freedom
        SumRz(float list)-This is an array that includes the cumulative sum of the modal participating mass ratios for
            the structure Rz degree of freedom
        """
        result=self.__Model.Results.ModalParticipatingMassRatios()
        return result

    def ModalParticipationFactors(self):
        """
        ---This function reports the modal participation factors for each mode of each selected modal analysis case---
        return:
        [index,NumberResults,LoadCase,StepType,StepNum,Period,Ux,Uy,Uz,Rx,Ry,Rz,ModalMass,ModalStiff]

        NumberResults(int)-The total number of results returned by the program
        LoadCase(str list)-This is an array that includes the name of the modal load case associated with each result.
        StepType(str list)-This is an array that includes the step type, if any, for each result. For modal results,
            this will always be Mode.
        StepNum(int list)-This is an array that includes the step number for each result. For modal results, this will
            always be the mode number.
        Period(float list)-This is an array that includes the period for each result. [s]
        Ux(float list)-This is an array that includes the modal participation factor for the structure Ux degree of
            freedom. The factor applies to the specified mode. [Fs2]
        Uy(float list)-This is an array that includes the modal participation factor for the structure Uy degree of
            freedom. The factor applies to the specified mode. [Fs2]
        Uz(float list)-This is an array that includes the modal participation factor for the structure Uz degree of
            freedom. The factor applies to the specified mode. [Fs2]
        Rx(float list)-This is an array that includes the modal participation factor for the structure Rx degree of
            freedom. The factor applies to the specified mode. [FLs2]
        Ry(float list)-This is an array that includes the modal participation factor for the structure Ry degree of
            freedom. The factor applies to the specified mode. [FLs2]
        Rz(float list)-This is an array that includes the modal participation factor for the structure Rz degree of
            freedom. The factor applies to the specified mode. [FLs2]
        ModalMass(float list)-This is an array that includes the modal mass for the specified mode.  This is a measure
            of the kinetic energy in the structure as it is deforming in the specified mode. [FLs2]
        ModalStiff(float list)-This is an array that includes the modal stiffness for the specified mode.  This is a
            measure of the strain energy in the structure as it is deforming in the specified mode. [FL]
        """
        result=self.__Model.Results.ModalParticipationFactors()
        return result

    def ModalPeriod(self):
        """
        ---SapModel.Results.ModalPeriod(NumberResults, LoadCase, StepType, StepNum, Period, Frequency, CircFreq, EigenValue)---
        return:
        [index,NumberResults,LoadCase,StepType,StepNum,Period,Frequency,CricFreq,EigenValue]

        NumberResults(int)-The number total of results returned by the program
        LoadCase(str list)-This is an array that includes the name of the modal analysis case associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result. For modal results
            this is always be Mode
        StepNum(int list)-This is an array that includes the step number for each result. For modal results this is
            always the mode number
        Period(float list)-This is an array that includes the period for each result. [s]
        Frequency(float list)-This is an array that includes the cyclic frequency for each result. [1/s]
        CircFreq(float list)-This is an array that includes the circular frequency for each result. [rad/s]
        EigenValue(float list)-This is an array that includes the eigenvalue for the specified mode for each result. [rad2/s2]
        """
        result=self.__Model.Results.ModalPeriod()
        return result

    def ModeShape(self,Name,ItemTypeElm=0):
        """
        ---This function reports the modal displacements (mode shapes) for the specified point elements---
        inputs:
        Name(str)-The name of an existing point element or group of objects, depending on the value of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the point element corresponding to the point object
                specified by the Name item.
            If this item is Element, the result request is for the point element specified by the Name item.
            If this item is GroupElm, the result request is for all point elements directly or indirectly specified in
            the group specified by the Name item.
            If this item is SelectionElm, the result request is for all point elements directly or indirectly selected
            and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,LoadCase,StepType,StepNum,U1,U2,U3,R1,R2,R3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the point object name associated with each result, if any.
            Some results will have no point object associated with them. For these cases this item will be blank
        Elm(str list)-This is an array that includes the point element name associated with each result.
        LoadCase(str list)-This is an array that includes the name of the modal analysis case associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result. For mode shape results,
            this is always be Mode.
        StepNum(int list)-This is an array that includes the step number for each result. For mode shape results,
            this is always the mode number
        U1,U2,U3(float list)-These are one dimensional arrays that include the displacement in the point element
            local 1, 2 and 3 axes directions, respectively, for each result. [L]
        R1,R2,R3(float list)-These are one dimensional arrays that include the rotation about the point element
            local 1, 2 and 3 axes, respectively, for each result. [rad]
        """
        result=self.__Model.Results.ModeShape(Name,ItemTypeElm)
        return result

    def SolidJointForce(self,Name,ItemTypeElm=0):
        """
        ---This function reports the joint forces for the point elements at each corner of the specified solid elements---
        inputs:
        Name(str)-The name of an existing solid object, solid element, or group of objects, depending on the value of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the solid elements corresponding to the solid object
            specified by the Name item.
            If this item is Element, the result request is for the solid element specified by the Name item.
            If this item is GroupElm, the result request is for the solid elements corresponding to all solid objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for solid elements corresponding to all selected solid
            objects and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,F1,F2,F3,M1,M2,M3]

        NumberResults(int)-The total number of results returned by the program.
        Obj(str list)-This is an array that includes the solid object name associated with each result, if any.
        Elm(str list)-This is an array that includes the solid element name associated with each result
        PointElm(str list)-This is an array that includes the point element name associated with each result
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination
            associated with each result
        StepType(str list)-This is an array that includes the step type, if any, for each result
        StepNum(int list)-This is an array that includes the step number, if any, for each result.
        F1,F2,F3(float list)-These are one dimensional arrays that include the joint force components in the point
            element local axes directions. [F]
        M1,M2,M3(float list)-These are one dimensional arrays that include the joint moment components about the
            point element local axes. [FL]
        """
        result=self.__Model.Results.SolidJointForce(Name,ItemTypeElm)
        return result

    def SolidStrain(self,Name,ItemTypeElm=0):
        """
        ---This function reports the strains for the specified solid elements. Strains are reported at each point
        element associated with the solid element---
        inputs:
        Name(str)-The name of an existing solid object, solid element, or group of objects, depending on the value of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the solid elements corresponding to the solid object
            specified by the Name item.
            If this item is Element, the result request is for the solid element specified by the Name item.
            If this item is GroupElm, the result request is for the solid elements corresponding to all solid objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for solid elements corresponding to all selected solid
            objects and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,E11,E22,E33,G12,G13,G23,EMax,EMid,EMin,EVM,
        DirCosMax1,DirCosMax2,DirCosMax3,DirCosMid1,DirCosMid2,DirCosMid3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the solid object name associated with each result, if any
        Elm(str list)-This is an array that includes the solid element name associated with each result
        PointElm(str list)-This is an array that includes the name of the point element where the results are reported
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated
            with each result.
        StepType(str list)-This is an array that includes the step type, if any, for each result.
        StepNum(int list)-This is an array that includes the step number, if any, for each result.
        E11,E22,E33,G12,G13,G23(float)-The solid element internal E11, E22, E33, G12, G13 and G23 strains at the
            specified point element location, reported in the solid element local coordinate system.
        EMax,EMid,EMin(float)-The solid element maximum, middle and minimum principal strains at the specified point element location
        EVM(float)-The solid element internal Von Mises strain at the specified point element location
        DirCosMax1,DirCosMax2,DirCosMax3(float)-These are three direction cosines defining the orientation of the
            maximum principal strain with respect to the solid element local axes.
        DirCosMid1,DirCosMid2,DirCosMid3(float)-These are three direction cosines defining the orientation of the
            middle principal strain with respect to the solid element local axes
        DirCosMin1,DirCosMin2,DirCosMin3(float)-These are three direction cosines defining the orientation of the
            minimum principal strain with respect to the solid element local axes.
        """
        result=self.__Model.Results.SolidStrain(Name,ItemTypeElm)
        return result

    def SolidStress(self,Name,ItemTypeElm=0):
        """
        ---This function reports the stresses for the specified solid elements. Stresses are reported at
        each point element associated with the solid element---
        inputs:
        Name(str)-The name of an existing solid object, solid element, or group of objects, depending on the value of the ItemTypeElm item
        ItemTypeElm(int)-This is one of the following items in the eItemTypeElm enumeration:
            ObjectElm = 0
            Element = 1
            GroupElm = 2
            SelectionElm = 3
            If this item is ObjectElm, the result request is for the solid elements corresponding to the solid object
            specified by the Name item.
            If this item is Element, the result request is for the solid element specified by the Name item.
            If this item is GroupElm, the result request is for the solid elements corresponding to all solid objects
            included in the group specified by the Name item.
            If this item is SelectionElm, the result request is for solid elements corresponding to all selected solid
            objects and the Name item is ignored.
        return:
        [index,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,S11,S22,S33,S12,S13,S23,SMax,SMid,SMin,SVM,
        DirCosMax1,DirCosMax2,DirCosMax3,DirCosMid1,DirCosMid2,DirCosMid3]

        NumberResults(int)-The total number of results returned by the program
        Obj(str list)-This is an array that includes the solid object name associated with each result, if any
        Elm(str list)-This is an array that includes the solid element name associated with each result
        PointElm(str list)-This is an array that includes the name of the point element where the results are reported
        LoadCase(str list)-This is an array that includes the name of the analysis case or load combination associated
            with each result.
        StepType(str list)-This is an array that includes the step type, if any, for each result.
        StepNum(int list)-This is an array that includes the step number, if any, for each result.
        S11,S22,S33,S12,S13,S23(float)-The solid element internal S11, S22, S33, S12, S13 and S23 stresses at the
            specified point element location, reported in the solid element local coordinate system. [F/L2]
        SMax,SMid,SMin(float)-The solid element maximum, middle and minimum principal stresses at the specified point
            element location. [F/L2]
        DirCosMax1,DirCosMax2,DirCosMax3(float)-These are three direction cosines defining the orientation of the
            maximum principal stress with respect to the solid element local axes.
        DirCosMid1,DirCosMid2,DirCosMid3(float)-These are three direction cosines defining the orientation of the
            middle principal stress with respect to the solid element local axes
        DirCosMin1,DirCosMin2,DirCosMin3(float)-These are three direction cosines defining the orientation of the
            minimum principal stress with respect to the solid element local axes.
        """
        result=self.__Model.Results.SolidStress(Name,ItemTypeElm)
        return result

    def StepLabel(self):
        """
        ---This function generates the step label for analyzed linear multi-step, nonlinear multi-step, or
        staged-construction load cases. For other load case types, the label will be blank---
        return:
        [index,LoadCase,StepNum,Label]

        LoadCase(str)-The name of an existing linear multi-step, nonlinear multi-step, or staged-construction load case
        StepNum(int)-This is an overall step number from the specified load case. The range of values of StepNum for a
            given load case can be obtained from most analysis results calls, such as SapObject.SapModel.Results.JointDispl
        Label(str)-The is the step label, including the name or number of the stage, the step number within the stage,
            and the age of the structure for time-dependent load cases
        """
        result=self.__Model.Results.StepLabel()
        return result
