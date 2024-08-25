from typing import Literal
class SapLoadPatterns:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model
        
    def Add(self,name,myType,SelfWTMultiplier=0,AddLoadCase=True):
        """
        ---This function adds a new load pattern---
        inputs:
        name(str)-The name for the new load pattern.
        myType(int)-This is one of the following items in the eLoadPatternType enumeration:
            LTYPE_DEAD = 1,LTYPE_SUPERDEAD = 2,LTYPE_LIVE = 3,LTYPE_REDUCELIVE = 4,LTYPE_QUAKE = 5
            LTYPE_WIND= 6,LTYPE_SNOW = 7,LTYPE_OTHER = 8,LTYPE_MOVE = 9,LTYPE_TEMPERATURE = 10
            LTYPE_ROOFLIVE = 11,LTYPE_NOTIONAL = 12,LTYPE_PATTERNLIVE = 13,LTYPE_WAVE= 14,LTYPE_BRAKING = 15
            LTYPE_CENTRIFUGAL = 16,LTYPE_FRICTION = 17,LTYPE_ICE = 18,LTYPE_WINDONLIVELOAD = 19
            LTYPE_HORIZONTALEARTHPRESSURE = 20,LTYPE_VERTICALEARTHPRESSURE = 21,LTYPE_EARTHSURCHARGE = 22
            LTYPE_DOWNDRAG = 23,LTYPE_VEHICLECOLLISION = 24,LTYPE_VESSELCOLLISION = 25,LTYPE_TEMPERATUREGRADIENT = 26
            LTYPE_SETTLEMENT = 27,LTYPE_SHRINKAGE = 28,LTYPE_CREEP = 29,LTYPE_WATERLOADPRESSURE = 30,LTYPE_LIVELOADSURCHARGE = 31
            LTYPE_LOCKEDINFORCES = 32,LTYPE_PEDESTRIANLL = 33,LTYPE_PRESTRESS = 34,LTYPE_HYPERSTATIC = 35,LTYPE_BOUYANCY = 36
            LTYPE_STREAMFLOW = 37,LTYPE_IMPACT = 38,LTYPE_CONSTRUCTION = 39
        SelfWTMultiplier(float)-The self weight multiplier for the new load pattern.
        AddLoadCase(bool)-If this item is True, a linear static load case corresponding to the new load pattern is added.
        """
        ret = self.__Model.LoadPatterns.Add(name,myType,SelfWTMultiplier,AddLoadCase)
        return ret

class load_StaticLinear:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def SetCase(self,name):
        """
        ---This function initializes a static linear load case---
        inputs:
        name(str)-The name of an existing or new load case.
        """
        ret = self.__Model.LoadCases.StaticLinear.SetCase(name)
        return ret

    def SetInitialCase(self,name,initialCase=None):
        """
        ---This function sets the initial condition for the specified load case---
        inputs:
        name(str)-The name of an existing static linear load case.
        initialCase-This is blank, None or the name of an existing analysis case. This item specifies if the
            load case starts from zero initial conditions, that is, an unstressed state, or if it starts using
            the stiffness that occurs at the end of a nonlinear static or nonlinear direct integration time
            history load case.
        """
        ret = self.__Model.LoadCases.StaticLinear.SetInitialCase(name,initialCase)
        return ret

    def SetLoads(self,name,numberLoads,loadType,loadName,scaleFactor):
        """
        ---This function sets the load data for the specified analysis case.---
        inputs:
        name(str)-The name of an existing static linear load case.
        numberLoads(int)-The number of loads assigned to the specified analysis case.
        loadType(str list)-This is a list that includes either Load or Accel, indicating the type of each
            load assigned to the load case.
        loadName(str list)-This is a list that includes the name of each load assigned to the load case.
            If the LoadType item is Load, this item is the name of a defined load pattern.
            If the LoadType item is Accel, this item is UX, UY, UZ, RX, RY or RZ, indicating the direction of the load.
        scaleFactor(float list)-This is a list that includes the scale factor of each load assigned to the load case.
            [L/s2] for Accel UX UY and UZ; otherwise unitless
        """
        ret = self.__Model.LoadCases.StaticLinear.SetLoads(name,numberLoads,loadType,loadName,scaleFactor)
        return ret

class load_StaticLinearMultistep:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def SetCase(self,name):
        """
        ---This function initializes a static linear multistep analysis case.---
        inputs:
        name(str)-The name of an existing or new load case.
        """
        ret = self.__Model.LoadCases.StaticLinearMultistep.SetCase(name)
        return ret

    def SetInitialCase(self,name,InitialCase=None):
        """
        ---This function sets the initial condition for the specified load case---
        inputs:
        name(str)-The name of an existing static linear multistep analysis case.
        initialCase-This is blank, None, or the name of an existing analysis case. This item specifies if
            the load case starts from zero initial conditions, that is, an unstressed state, or if it
            starts using the stiffness that occurs at the end of a nonlinear static or nonlinear direct
            integration time history load case.If the specified initial case is a nonlinear static or
            nonlinear direct integration time history load case, the stiffness at the end of that case
            is used. If the initial case is anything else, zero initial conditions are assumed.
        """
        ret = self.__Model.LoadCases.StaticLinearMultistep.SetInitialCase(name,InitialCase)
        return ret

    def SetLoads_1(self,name,numberLoads,LoadType,LoadName,scaleFactor,
                            stepRange,firstLoadStep,lastLoadStep,startCaseStep,extrapolateOption):
        """
        ---This function sets the load data for the specified analysis case.---
        inputs:
        name(str)-The name of an existing static linear multistep analysis case.
        numberLoads(int)-The number of loads assigned to the specified analysis case.
        loadType(str list)-This is a list that includes either Load or Accel, indicating the type of
            each load assigned to the load case.
        loadName(str list)-This is list that includes the name of each load assigned to the load case.
            If the LoadType item is Load, this item is the name of a defined load pattern.If the LoadType
            item is Accel, this item is UX, UY, UZ, RX, RY or RZ, indicating the direction of the load.
        scaleFactor(float list)-This is a list that includes the scale factor of each load assigned to
            the load case. [L/s2] for Accel UX UY and UZ; otherwise unitless
        stepRange(int list)-This is a list that identifies the step range type to consider for each load
        assigned to the load case. The allowed values are:0 = All,1 = User
        FirstLoadStep(int list)-This is a list that specifies the first load step to consider for each
            load assigned to the load case. This value is only applicable when StepRange = User.
        lastLoadStep(int list)-This is a list that specifies the last load step to consider for each
            load assigned to the load case. This value is only applicable when StepRange = User.
        StartCaseStep(int list)-This is a list that specifies the load case step at which to start
            applying each load assigned to the load case.
        extrapolateOption(int list)-This is a list that identifies the extrapolation option for each load
            assigned to the load case. The allowed values are:0 = None,1 = Last Step,2 = Repeat Range
        """

        ret = self.__Model.LoadCases.StaticLinearMultistep.SetLoads_1(name,numberLoads,LoadType,LoadName,scaleFactor,
                stepRange,firstLoadStep,lastLoadStep,startCaseStep,extrapolateOption)
        return ret

class load_StaticNonlinear:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def SetCase(self,name):
        """
        ---This function initializes a static nonlinear analysis case---
        inputs:
        name(str)-The name of an existing or new load case.
        """
        ret = self.__Model.LoadCases.StaticNonlinear.SetCase(name)
        return ret

    def SetGeometricNonlinearity(self,name,NLGeomType=0):
        """
        ---This function sets the geometric nonlinearity option for the specified load case.---
        inputs:
        name(str)-The name of an existing static nonlinear load case.
        NLGeomType(int)-This is 0, 1 or 2, indicating the geometric nonlinearity option selected for the load case.
            0 = None,1 = P-delta,2 = P-delta plus large displacements
        """
        ret = self.__Model.LoadCases.StaticNonlinear.SetGeometricNonlinearity(name,NLGeomType)
        return ret

    def SetHingeUnloading(self,name,UnloadType):
        """
        ---This function sets the hinge unloading option for the specified load case.---
        inputs:
        name(str)-The name of an existing static nonlinear load case.
        UNLoadType(int)-This is 1, 2 or 3, indicating the hinge unloading option selected for the load case.
            1 = Unload entire structure,2 = Apply local redistribution,3 = Restart using secant stiffness
        """
        ret = self.__Model.LoadCases.StaticNonlinear.SetHingeUnloading(name,UnloadType)
        return ret

    def SetInitialCase(self,name,initialCase=None):
        """
        ---This function sets the initial condition for the specified load case.---
        inputs:
        name(str)-The name of an existing static nonlinear load case.
        initialCase-This is blank, None, or the name of an existing analysis case. This item specifies if
            the load case starts from zero initial conditions, that is, an unstressed state, or if it starts
            from the state at the end of a nonlinear static or nonlinear direct integration time history load case.
            If the specified initial case is a nonlinear static or nonlinear direct integration time history
            load case, the state at the end of that case is used. If the initial case is anything else, zero initial
            conditions are assumed.
        """
        ret = self.__Model.LoadCases.StaticNonlinearMultistep.SetInitialCase(name,initialCase)
        return ret

    def SetLoadApplication(self,name,LoadControl,DispType,Displ,Monitor,DOF,
                                                            PointName,GDispl):
        """
        ---This function sets the load application control parameters for the specified load case---
        inputs:
        name(str)-The name of an existing static nonlinear load case.
        LoadControl(int)-This is either 1 or 2, indicating the load application control method.1 = Full load,
            2 = Displacement control
        DispType(int)-This is either 1 or 2 indicating the control displacement type.1 = Conjugate displacement,
            2 = Monitored displacement
        Displ(float)-This item applies only when displacement control is used, that is, LoadControl = 2. The
            structure is loaded to a monitored displacement of this magnitude. [L] when DOF = 1, 2 or 3 and [rad]
            when DOF = 4, 5 or 6
        Monitor(int)-This is either 1 or 2, indicating the monitored displacement.1 = Displacement at a specified
            point object,2 = Generalized displacement
        DOF(int)-This is 1, 2, 3, 4, 5 or 6, indicating the degree of freedom for which the displacement at a point
            object is monitored.1 = U1,2 = U2,3 = U3,4 = R1,5 = R2,6 = R3,This item applies only when Monitor = 1.
        PointName(str)-The name of the point object at which the displacement is monitored. This item applies only
            when Monitor = 1.
        GDispl(str)-The name of the generalized displacement for which the displacement is monitored. This item
            applies only when Monitor = 2.
        """
        ret = self.__Model.LoadCases.StaticNonlinear.SetLoadApplication(name,LoadControl,DispType,Displ,Monitor,
                        DOF,PointName,GDispl)
        return ret

    def SetLoads(self,name,NumberLoads,LoadType,LoadName,SF):
        """
        ---This function sets the load data for the specified analysis case---
        inputs:
        name(str)-The name of an existing static nonlinear load case.
        NumberLoads(int)-The number of loads assigned to the specified analysis case.
        LoadType(str list)-This is a list that includes either Load or Accel, indicating the type of
            each load assigned to the load case.
        LoadName(str list)-This is a list that includes the name of each load assigned to the load case.
            If the LoadType item is Load, this item is the name of a defined load pattern.
            If the LoadType item is Accel, this item is UX, UY, UZ, RX, RY or RZ indicating the direction
            of the load.
        SF(float list)-This is a list that includes the scale factor of each load assigned to the load case.
            [L/s2] for Accel UX UY and UZ; otherwise unitless
        """
        ret = self.__Model.LoadCases.StaticNonlinear.SetLoads(name,NumberLoads,LoadType,LoadName,SF)
        return ret

    def SetMassSource(self,name,Source=""):
        """
        ---This function sets the mass source to be used for the specified load case.---
        inputs:
        name(str)-The name of an existing static nonlinear load case.
        Source(str)-This is the name of an existing mass source or a blank string. Blank indicates to use the
        mass source from the previous load case or the default mass source if the load case starts from zero
        initial conditions.
        """
        ret = self.__Model.LoadCases.StaticNonlinear.SetMassSource(name,Source)
        return ret

    def SetModalCase(self,name,ModalCase):
        """
        ---This function sets the modal case for the specified analysis case---
        inputs:
        name(str)-The name of an existing static nonlinear load case.
        ModalCase(str)-This is the name of an existing modal load case. It specifies the modal load case
            on which any mode-type load assignments to the specified load case are based.
        """
        ret = self.__Model.LoadCases.StaticNonlinear.SetModalCase(name,ModalCase)
        return ret

    def SetResultsSaved(self,name,SaveMultipleSteps,MinSavedStates=10,
                                                            MaxSavedStates=100,PositiveOnly=True):
        """
        ---This function sets the results saved parameters for the specified load case---
        inputs:
        name(str)-The name of an existing static nonlinear load case.
        SaveMultipleSteps(bool)-This item is True if multiple states are saved for the nonlinear analysis.
            It is False only if the final state is saved.
        MinSavedStates(int)-This item only applies when SaveMultipleSteps = True. It is the minimum number
            of saved steps.
        MaxSavedStates(int)-This item only applies when SaveMultipleSteps = True. It is the maximum number
            of saved steps.
        PositiveOnly(bool)-If this item is True, only positive displacement increments are saved. If it is False,
            all displacement increments are saved.
        """
        ret = self.__Model.LoadCases.StaticNonlinear.SetResultsSaved(name,SaveMultipleSteps,MinSavedStates,
                                                                MaxSavedStates,PositiveOnly)
        return ret

    def SetSolControlParameters(self,name,MaxTotalSteps,MaxFailedSubSteps,
        MaxIterCS,MaxIterNR,TolConvD,UseEventStepping,TolEventD,MaxLineSearchPerIter,TolLineSearch,LineSearchStepFact):
        """
        ---This function sets the solution control parameters for the specified load case---
        inputs:
        name(str)-The name of an existing static nonlinear load case.
        MaxTotalSteps(int)-The maximum total steps per stage.
        MaxFailedSubSteps(int)-The maximum null (zero) steps per stage.
        MaxIterCS(int)-The maximum constant-stiffness iterations per step.
        MaxIterNR(int)-The maximum Newton_Raphson iterations per step.
        TolConvD(float)-The relative iteration convergence tolerance.
        UseEventStepping(bool)-This item is True if event-to-event stepping is used.
        TolEventD(float)-The relative event lumping tolerance.
        MaxLineSearchPerIter(int)-The maximum number of line searches per iteration.
        TolLineSearch(float)-The relative line-search acceptance tolerance.
        LineSearchStepFact(float)-The line-search step factor.
        """
        ret = self.__Model.LoadCases.StaticNonlinear.SetSolControlParameters(name,MaxTotalSteps,MaxFailedSubSteps,
        MaxIterCS,MaxIterNR,TolConvD,UseEventStepping,TolEventD,MaxLineSearchPerIter,TolLineSearch,LineSearchStepFact)
        return ret

    def SetTargetForceParameters(self,name,TolConvF,MaxIter,AccelFact,NoStop):
        """
        ---This function sets the target force iteration parameters for the specified load case---
        inputs:
        name(str)-The name of an existing static nonlinear load case.
        TolConvF(float)-The relative convergence tolerance for target force iteration.
        MaxIter(int)-The maximum iterations per stage for target force iteration.
        AccelFact(float)-The acceleration factor.
        NoStop(bool)-If this item is True, the analysis is continued when there is no convergence in the target
            force iteration.
        """
        ret = self.__Model.LoadCases.StaticNonlinear.SetTargetForceParameters(name,TolConvF,MaxIter,AccelFact,NoStop)
        return ret

class load_Buckling:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model
        
    def SetCase(self,name):
        """
        ---This function initializes a buckling load case.---
        inputs:
        name(str)-The name of an existing or new load case.
        """
        ret = self.__Model.LoadCases.Buckling.SetCase(name)
        return ret

    def SetInitialCase(self,name,InitialCase=None):
        """
        ---This function sets the initial condition for the specified load case.---
        inputs:
        name(str)-The name of an existing buckling load case.
        InitialCase-This is blank, None or the name of an existing analysis case. This item specifies if the
            load case starts from zero initial conditions, that is, an unstressed state, or if it starts using
            the stiffness that occurs at the end of a nonlinear static or nonlinear direct integration time
            history load case.If the specified initial case is a nonlinear static or nonlinear direct integration
            time history load case, the stiffness at the end of that case is used. If the initial case is anything
            else, zero initial conditions are assumed.
        """
        ret = self.__Model.LoadCases.Buckling.SetInitialCase(name,InitialCase)
        return ret

    def SetLoads(self,name,NumberLoads,LoadType,LoadName,SF):
        """
        ---This function sets the load data for the specified analysis case---
        inputs:
        name(str)-The name of an existing buckling load case.
        NumberLoads(int)-The number of loads assigned to the specified analysis case.
        LoadType(str list)-This is a list that includes either Load or Accel, indicating the type of each
            load assigned to the load case.
        LoadName(str list)-This is a list that includes the name of each load assigned to the load case.
            If the LoadType item is Load, this item is the name of a defined load pattern.
            If the LoadType item is Acce, this item is UX, UY, UZ, RX, RY or RZ, indicating the direction of the load.
        SF(float list)-This is a list that includes the scale factor of each load assigned to the load case.
            [L/s2] for Accel UX UY and UZ; otherwise unitless
        """
        ret = self.__Model.LoadCases.Buckling.SetLoads(name,NumberLoads,LoadType,LoadName,SF)
        return ret

    def SetParameters(self,name,NumBucklingModes=6,EigenTol=1.0e-9):
        """
        ---This function sets various parameters for the specified buckling load case---
        inputs:
        name(str)-The name of an existing buckling load case.
        NumBucklingModes(int)-The number of buckling modes requested.
        EigenTol(float)-The relative convergence tolerance for eigenvalues.
        """
        ret = self.__Model.LoadCases.Buckling.SetParameters(name,NumBucklingModes,EigenTol)
        return ret

class load_DirHistLinear:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model
        
    def SetCase(self,name):
        """
        ---This function initializes a linear direct integration time history load case---
        inputs:
        name(str)-The name of an existing or new load case.
        """
        ret = self.__Model.LoadCases.DirHistLinear.SetCase(name)
        return ret

    def SetDampProportional(self,name,DampType,Dampa,Dampb,Dampf1=0,
                                                            Dampf2=0,Dampd1=0,Dampd2=0):
        """
        ---This function sets proportional modal damping data for the specified load case---
        inputs:
        name(str)-The name of an existing linear direct integration time history load case.
        DampType(int)-This is 1, 2 or 3, indicating the proportional modal damping type.1 = Mass and stiffness
            proportional damping by direct specification,2 = Mass and stiffness proportional damping by period
            3 = Mass and stiffness proportional damping by frequency
        Dampa(float)-The mass proportional damping coefficient. This item applies only when DampType = 1.
        Dampb(float)-The stiffness proportional damping coefficient. This item applies only when DampType = 1.
        Dampf1(float)-This is the period or the frequency (depending on the value of the DampType item) for point 1.
            [s] for DampType = 2 and [cyc/s] for DampType = 3
        Dampf2(float)-This is either the period or the frequency (depending on the value of the DampType item)
            for point 2. [s] for DampType = 2 and [cyc/s] for DampType = 3
        Dampd1(float)-This is the damping at point 1 (0 <= Dampd1 < 1).This item applies only when DampType = 2 or 3.
        Dampd2(float)-This is the damping at point 2 (0 <= Dampd2 < 1).This item applies only when DampType = 2 or 3.
        """
        ret = self.__Model.LoadCases.DirHistLinear.SetDampProportional(name,DampType,Dampa,Dampb,Dampf1,Dampf2,Dampd1,Dampd2)
        return ret

    def SetInitialCase(self,name,initialCase=None):
        """
        ---This function sets the initial condition for the specified load case---
        inputs:
        name(str)-The name of an existing linear direct integration time history load case.
        initialCase-This is blank, None, or the name of an existing analysis case. This item specifies if the load
            case starts from zero initial conditions, that is, an unstressed state, or if it starts using the
            stiffness that occurs at the end of a nonlinear static or nonlinear direct integration time history
            load case.If the specified initial case is a nonlinear static or nonlinear direct integration time
            history load case. the stiffness at the end of that case is used. If the initial case is anything else,
            zero initial conditions are assumed.
        """
        ret = self.__Model.LoadCases.DirHistLinear.SetInitialCase(name,initialCase)
        return ret

    def SetLoads(self,name,NumberLoads,LoadType,LoadName,Func,SF=None,TF=None,AT=None,
                                                CSys=None,Ang=None):
        """
        ---This function sets the load data for the specified analysis case---
        inputs:
        name(str)-The name of an existing linear direct integration time history load case.
        NumberLoads(int)-The number of loads assigned to the specified analysis case.
        LoadType(str list)-This is a str list that includes Load or Accel, indicating the type of each load
            assigned to the load case.
        LoadName(str list)-This is a str list that includes the name of each load assigned to the load case.
            If the LoadType item is Load, this item is the name of a defined load pattern.
            If the LoadType item is Accel, this item is U1, U2, U3, R1, R2 or R3, indicating the direction of the load.
        Func(str list)-This is a str list that includes the name of the time history function associated with each load.
        SF(float list)-This is a str list that includes the scale factor of each load assigned to the load case.
            [L/s2] for U1 U2 and U3; otherwise unitless
        TF(float list)-This is a str list that includes the time scale factor of each load assigned to the load case.
        AT(float list)-This is a str list that includes the arrival time of each load assigned to the load case.
        CSys(str float)-This is a str list that includes the name of the coordinate system associated with each load.
            If this item is a blank string, the Global coordinate system is assumed.This item applies only when the
            LoadType item is Accel.
        Ang(float list)-This is a float list that includes the angle between the acceleration local 1 axis and
            the +X-axis of the coordinate system specified by the CSys item. The rotation is about the Z-axis
            of the specified coordinate system. [deg] This item applies only when the LoadType item is Accel.
        """
        if SF==None:
            SF=[1.0 for each in range(NumberLoads)]
        if TF==None:
            TF=[1.0 for each in range(NumberLoads)]
        if AT==None:
            AT=[0.0 for each in range(NumberLoads)]
        if CSys==None:
            CSys=["Global" for each in range(NumberLoads)]
        if Ang == None:
            Ang=[0.0 for each in range(NumberLoads)]
        ret = self.__Model.LoadCases.DirHistLinear.SetLoads(name,NumberLoads,LoadType,LoadName,Func,SF,TF,AT,CSys,Ang)
        return ret

    def SetTimeIntegration(self,name,IntegrationType=4):
        """
        ---This function sets time integration data for the specified load case---
        inputs:
        name(str)-The name of an existing linear direct integration time history load case.
        IntegrationType(int)-This is 1, 2, 3, 4 or 5, indicating the time integration type.1 = Newmark,2 = Wilson,
        3 = Collocation,4 = Hilber-Hughes-Taylor,5 = Chung and Hulbert
        """
        Alpha,Beta,Gamma,Theta,m=0.0,0.0,0.0,0.0,0.0
        if IntegrationType==1:
            Gamma,Beta=0.5,0.25
        if IntegrationType==2:
            Theta=1.0
        if IntegrationType==3:
            Gamma,Beta,Theta=0.5,0.1667,1.0
        if IntegrationType==4:
            Alpha=0.0
        if IntegrationType==5:
            Gamma,Beta,Alpha,m=0.5,0.25,0.0,0.0
        ret = self.__Model.LoadCases.DirHistLinear.SetTimeIntegration(name,IntegrationType,Alpha,Beta,Gamma,Theta,m)
        return ret

    def SetTimeStep(self,name,nstep,DT):
        """
        ---This function sets the time step data for the specified load case---
        inputs:
        name(str)-The name of an existing linear direct integration time history load case.
        nstep(int)-The number of output time steps.
        DT(float)-The output time step size.
        """
        ret = self.__Model.LoadCases.DirHistLinear.SetTimeStep(name,nstep,DT)
        return ret

class load_DirHistNonlinear:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model
        
    def SetCase(self,name):
        """
        ---This function initializes a nonlinear direct integration time history load case---
        inputs:
        name(str)-The name of an existing or new load case
        """
        ret = self.__Model.LoadCases.DirHistNonlinear.SetCase(name)
        return ret

    def SetDampProportional(self,name,DampType=Literal['MassStiffness','Period','Frequency'],Dampa=0,Dampb=0,Dampf1=0,
                                                            Dampf2=0,Dampd1=0,Dampd2=0):
        """
            ---This function sets proportional modal damping data for the specified load case---
            inputs:
            name(str)-The name of an existing linear direct integration time history load case.
            DampType(int)-This is 1, 2 or 3, indicating the proportional modal damping type.1 = Mass and stiffness
                proportional damping by direct specification,2 = Mass and stiffness proportional damping by period
                3 = Mass and stiffness proportional damping by frequency
            Dampa(float)-The mass proportional damping coefficient. This item applies only when DampType = 1.
            Dampb(float)-The stiffness proportional damping coefficient. This item applies only when DampType = 1.
            Dampf1(float)-This is the period or the frequency (depending on the value of the DampType item) for point 1.
                [s] for DampType = 2 and [cyc/s] for DampType = 3
            Dampf2(float)-This is either the period or the frequency (depending on the value of the DampType item)
                for point 2. [s] for DampType = 2 and [cyc/s] for DampType = 3
            Dampd1(float)-This is the damping at point 1 (0 <= Dampd1 < 1).This item applies only when DampType = 2 or 3.
            Dampd2(float)-This is the damping at point 2 (0 <= Dampd2 < 1).This item applies only when DampType = 2 or 3.
            """
        typeid = {'MassStiffness':1,'Period':2,'Frequency':3}[DampType]
        ret = self.__Model.LoadCases.DirHistNonlinear.SetDampProportional(name,typeid,Dampa,Dampb,Dampf1,Dampf2,Dampd1,Dampd2)
        return ret

    def SetGeometricNonlinearity(self,name,NLGeomType=0):
        """
        ---This function sets the geometric nonlinearity option for the specified load case---
        inputs:
        name(str)-The name of an existing nonlinear direct integration time history load case.
        NLGeomType(int)-This is 0, 1 or 2, indicating the geometric nonlinearity option selected for the load case.
            0 = None,1 = P-delta,2 = P-delta plus large displacements
        """
        ret = self.__Model.LoadCases.DirHistNonlinear.SetGeometricNonlinearity(name,NLGeomType)
        return ret

    def SetInitialCase(self,name,initialCase=None):
        """
        ---This function sets the initial condition for the specified load case.---
        inputs:
        name(str)-The name of an existing nonlinear direct integration time history load case.
        initialCase-This is blank, None or the name of an existing analysis case. This item specifies if the load
            case starts from zero initial conditions, that is, an unstressed state, or if it starts from the state
            at the end of a nonlinear static or nonlinear direct integration time history load case.If the specified
            initial case is a nonlinear static or nonlinear direct integration time history load case, the state at
            the end of that case is used. If the initial case is anything else, zero initial conditions are assumed.
        """
        ret = self.__Model.LoadCases.DirHistNonlinear.SetInitialCase(name,initialCase)
        return ret

    def SetLoads(self,name,NumberLoads,LoadType,LoadName,Func,SF=None,
                                                    TF=None,AT=None,CSys=None,Ang=None):
        """
        ---This function sets the load data for the specified analysis case---
        inputs:
        name(str)-The name of an existing nonlinear direct integration time history load case.
        NumberLoads(int)-The number of loads assigned to the specified analysis case.
        LoadType(str list)-This is a str list that includes Load or Accel, indicating the type of each load
            assigned to the load case.
        LoadName(str list)-This is a str list that includes the name of each load assigned to the load case.
            If the LoadType item is Load, this item is the name of a defined load pattern.
            If the LoadType item is Accel, this item is U1, U2, U3, R1, R2 or R3, indicating the direction of the load.
        Func(str list)-This is a str list that includes the name of the time history function associated with each load.
        SF(float list)-This is a str list that includes the scale factor of each load assigned to the load case.
            [L/s2] for U1 U2 and U3; otherwise unitless
        TF(float list)-This is a str list that includes the time scale factor of each load assigned to the load case.
        AT(float list)-This is a str list that includes the arrival time of each load assigned to the load case.
        CSys(str float)-This is a str list that includes the name of the coordinate system associated with each load.
            If this item is a blank string, the Global coordinate system is assumed.This item applies only when the
            LoadType item is Accel.
        Ang(float list)-This is a float list that includes the angle between the acceleration local 1 axis and
            the +X-axis of the coordinate system specified by the CSys item. The rotation is about the Z-axis
            of the specified coordinate system. [deg] This item applies only when the LoadType item is Accel.
        """
        if SF==None:
            SF=[1.0 for each in range(NumberLoads)]
        if TF==None:
            TF=[1.0 for each in range(NumberLoads)]
        if AT==None:
            AT=[0.0 for each in range(NumberLoads)]
        if CSys==None:
            CSys=["Global" for each in range(NumberLoads)]
        if Ang == None:
            Ang=[0.0 for each in range(NumberLoads)]
        ret = self.__Model.LoadCases.DirHistNonlinear.SetLoads(name,NumberLoads,LoadType,LoadName,Func,SF,TF,AT,CSys,Ang)
        return ret

    def SetMassSource(self,name,source=""):
        """
        ---This function sets the mass source to be used for the specified load case.---
        inputs:
        name(str)-The name of an existing nonlinear direct integration time history load case.
        source(str)-This is the name of an existing mass source or a blank string. Blank indicates to use the mass
            source from the previous load case or the default mass source if the load case starts from zero initial
            conditions.
        """
        ret = self.__Model.LoadCases.DirHistNonlinear.SetMassSource(name,source)
        return ret

    def SetSolControlParameters(self,name,DTMax=0,DTMin=0,MaxIterCS=10,MaxIterNR=40,
                TolConvD=1e-4,UseEventStepping=False,TolEventD=0.01,MaxLineSearchPerIter=20,TolLineSearch=0.1,
                                                                    LineSearchStepFact=1.618):
        """
        ---This function sets the solution control parameters for the specified load case---
        inputs:
        name(str)-The name of an existing nonlinear direct integration time history load case.
        DTMax(float)-The maximum substep size
        DTMin(float)-The minimum substep size.
        MaxIterCS(int)-The maximum constant-stiffness iterations per step.
        MaxIterNR(int)-The maximum Newton_Raphson iterations per step.
        TolConvD(float)-The relative iteration convergence tolerance.
        UseEventStepping(bool)-This item is True if event-to-event stepping is used.
        TolEventD(float)-The relative event lumping tolerance.
        MaxLineSearchPerIter(int)-The maximum number of line searches per iteration.
        TolLineSearch(float)-The relative line-search acceptance tolerance.
        LineSearchStepFact(float)-The line-search step factor.
        """
        ret = self.__Model.LoadCases.DirHistNonlinear.SetSolControlParameters(name,DTMax,DTMin,MaxIterCS,MaxIterNR,
                TolConvD,UseEventStepping,TolEventD,MaxLineSearchPerIter,TolLineSearch,LineSearchStepFact)
        return ret

    def SetTimeIntegration(self,name,IntegrationType:Literal['Newmark','Wilson','Collocation','Hilber-Hughes-Taylor','Chung and Hulbert']):
        """
            ---This function sets time integration data for the specified load case---
            inputs:
            name(str)-The name of an existing linear direct integration time history load case.
            IntegrationType(int)-This is 1, 2, 3, 4 or 5, indicating the time integration type.1 = Newmark,2 = Wilson,
            3 = Collocation,4 = Hilber-Hughes-Taylor,5 = Chung and Hulbert
            """
        Alpha, Beta, Gamma, Theta, m = 0.0, 0.0, 0.0, 0.0, 0.0
        if IntegrationType == 'Newmark':
            Gamma, Beta = 0.5, 0.25
            typeid = 1
        if IntegrationType == 'Wilson':
            Theta = 1.0
            typeid = 2
        if IntegrationType == 'Collocation':
            Gamma, Beta, Theta = 0.5, 0.1667, 1.0
            typeid = 3
        if IntegrationType == 'Hilber-Hughes-Taylor':
            Alpha = 0.0
            typeid = 4
        if IntegrationType == 'Chung and Hulbert':
            Gamma, Beta, Alpha, m = 0.5, 0.25, 0.0, 0.0
            typeid = 5
        ret = self.__Model.LoadCases.DirHistNonlinear.SetTimeIntegration(name,typeid,Alpha,Beta,Gamma,Theta,m)
        return ret

    def SetTimeStep(self,name,nstep,DT):
        """
        ---This function sets the time step data for the specified load case---
        inputs:
        name(str)-The name of an existing linear direct integration time history load case.
        nstep(int)-The number of output time steps.
        DT(float)-The output time step size.
        """
        ret = self.__Model.LoadCases.DirHistNonlinear.SetTimeStep(name,nstep,DT)
        return ret

class load_ModalEigen:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model
        
    def SetCase(self,name):
        """
        ---This function initializes a modal eigen load case---
        inputs:
        name(str)-The name of an existing or new load case.
        """
        ret = self.__Model.LoadCases.ModalEigen.SetCase(name)
        return ret

    def SetInitialCase(self,name,initialCase=None):
        """
        ---This function sets the initial condition for the specified load case---
        inputs:
        name(str)-The name of an existing modal eigen load case.
        initialCase-This is blank, None, or the name of an existing analysis case. This item specifies if the
            load case starts from zero initial conditions, that is, an unstressed state, or if it starts using
            the stiffness that occurs at the end of a nonlinear static or nonlinear direct integration time
            history load case.If the specified initial case is a nonlinear static or nonlinear direct integration
            time history load case, the stiffness at the end of that case is used. If the initial case is anything
            else, zero initial conditions are assumed.
        """
        ret = self.__Model.LoadCases.ModalEigen.SetInitialCase(name,initialCase)
        return ret

    def SetLoads(self,name,NumberLoads,LoadType,LoadName,TargetPar=None,StaticCorrect=None):
        """
        ---This function sets the load data for the specified analysis case---
        inputs:
        name(str)-The name of an existing modal eigen load case.
        NumberLoads(int)-The number of loads assigned to the specified analysis case.
        LoadTyp(str list)-This is a str list that includes Load, Accel or Link, indicating the type of each load
            assigned to the load case.
        LoadName(str list)-This is a str list that includes the name of each load assigned to the load case.
            If the LoadType item is Load, this item is the name of a defined load pattern.If the LoadType item
            is Accel, this item is UX, UY, UZ, RX, RY or RZ, indicating the direction of the load.If the LoadType
            item is Link, this item is not used.
        TargetPar(float list)-This is a float list that includes the target mass participation ratio.
        StaticCorrect(int list)-This is a int list that includes either 0 or 1, indicating if static correction
            modes are to be calculated.
        """
        if TargetPar==None:
            TargetPar=[99 for each in range(NumberLoads)]
        if StaticCorrect==None:
            StaticCorrect=[0 for each in range(NumberLoads)]
        ret = self.__Model.LoadCases.ModalEigen.SetLoads(name,NumberLoads,LoadType,LoadName,TargetPar,StaticCorrect)
        return ret

    def SetNumberModes(self,name,MaxModes=12,MinModes=1):
        """
        ---This function sets the number of modes requested for the specified load case---
        inputs:
        name(str)-The name of an existing modal eigen load case.
        MaxModes(int)-The maximum number of modes requested.
        MinModes(int)-The minimum number of modes requested.
        """
        ret = self.__Model.LoadCases.ModalEigen.SetNumberModes(name,MaxModes,MinModes)
        return ret

    def SetParameters(self,name,EigenShiftFreq=0,EigenCutOff=0,EigenTol=1e-9,
                                                    AllowAutoFreqShift=1):
        """
        ---This function sets various parameters for the specified modal eigen load case---
        inputs:
        name(str)-The name of an existing modal eigen load case.
        EigenShiftFreq(float)-The eigenvalue shift frequency. [cyc/s]
        EigenCutOff(float)-The eigencutoff frequency radius. [cyc/s]
        EigenTol(float)-The relative convergence tolerance for eigenvalues.
        AllowAutoFreqShift(int)-This is either 0 or 1, indicating if automatic frequency shifting is allowed.
            0 = Automatic frequency shifting is NOT allowed,1 = Automatic frequency shifting is allowed
        """
        ret = self.__Model.LoadCases.ModalEigen.SetParameters(name,EigenShiftFreq,EigenCutOff,EigenTol,AllowAutoFreqShift)
        return ret

class load_ModalRitz:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def SetCase(self,name):
        """
        ---This function initializes a modal ritz load case---
        inputs:
        name(str)-The name of an existing or new load case.
        """
        ret = self.__Model.LoadCases.ModalRitz.SetCase(name)
        return ret

    def SetInitialCase(self,name,initialCase=None):
        """
        ---This function sets the initial condition for the specified load case---
        inputs:
        name(str)-The name of an existing modal eigen load case.
        initialCase-This is blank, None, or the name of an existing analysis case. This item specifies if the
            load case starts from zero initial conditions, that is, an unstressed state, or if it starts using
            the stiffness that occurs at the end of a nonlinear static or nonlinear direct integration time
            history load case.If the specified initial case is a nonlinear static or nonlinear direct integration
            time history load case, the stiffness at the end of that case is used. If the initial case is anything
            else, zero initial conditions are assumed.
        """
        ret = self.__Model.LoadCases.ModalRitz.SetInitialCase(name,initialCase)
        return ret

    def SetLoads(self,name,NumberLoads,LoadType,LoadName,RitzMaxCyc=None,TargetPar=None):
        """
        ---This function sets the load data for the specified analysis case---
        inputs:
        name(str)-The name of an existing modal ritz load case.
        NumberLoads(int)-The number of loads assigned to the specified analysis case.
        LoadType(str list)-This is a str list that includes Load, Accel or Link, indicating the type of each
            load assigned to the load case.
        LoadName(str list)-This is a str list that includes the name of each load assigned to the load case.
            If the LoadType item is Load, this item is the name of a defined load pattern.
            If the LoadType item is Accel, this item is UX, UY, UZ, RX, RY or RZ, indicating the direction of the load.
            If the LoadType item is Link, this item is not used.
        RitzMaxCyc(int list)-This is a int list that includes the maximum number of generation cycles to be performed
            for the specified ritz starting vector. A value of 0 means there is no limit on the number of cycles.
        TargetPar(float list)-This is a float list that includes the target dynamic participation ratio.
        """
        if RitzMaxCyc==None:
            RitzMaxCyc=[0 for each in range(NumberLoads)]
        if TargetPar==None:
            TargetPar=[99 for each in range(NumberLoads)]
        ret = self.__Model.LoadCases.ModalRitz.SetLoads(name,NumberLoads,LoadType,LoadName,RitzMaxCyc,TargetPar)
        return ret

    def SetNumberModes(self,name,MaxModes=12,MinModes=1):
        """
        ---This function sets the number of modes requested for the specified load case---
        inputs:
        name(str)-The name of an existing modal ritz load case.
        MaxModes(int)-The maximum number of modes requested.
        MinModes(int)-The minimum number of modes requested.
        """
        ret = self.__Model.LoadCases.ModalRitz.SetNumberModes(name,MaxModes,MinModes)
        return ret

class load_ModalHistLinear:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model
        
    def SetCase(self,name):
        """
        ---This function initializes a linear modal history analysis case---
        name(str)-The name of an existing or new load case.
        """
        ret = self.__Model.LoadCases.ModHistLinear.SetCase(name)
        return ret

    def SetDampConstant(self,name,Damp):
        """
        ---This function sets constant modal damping for the specified load case---
        inputs:
        name(str)-The name of an existing linear modal history analysis case.
        Damp(float)-The constant damping for all modes (0 <= Damp < 1).
        """
        ret = self.__Model.LoadCases.ModHistLinear.SetDampConstant(name,Damp)
        return ret

    def SetDampInterpolated(self,name,DampType,NumberItems,Time,Damp):
        """
        ---This function sets interpolated modal damping data for the specified load case---
        inputs:
        name(str)-The name of an existing linear modal history analysis case.
        DampType(int)-This is 5 or 6, indicating the interpolated modal damping type.
            5 = Interpolated damping by period,6 = Interpolated damping by frequency
        NumberItems(int)-The number of Time and Damp pairs.
        Time(float list)-This is a float list that includes the period or the frequency, depending on the
            value of the DampType item. [s] for DampType = 5 and [cyc/s] for DampType = 6
        Damp(float list)-This is a float list that includes the damping for the specified period of frequency
            (0 <= Damp < 1).
        """
        ret = self.__Model.LoadCases.ModHistLinear.SetDampInterpolated(name,DampType,NumberItems,Time,Damp)
        return ret

    def SetDampProportional(self,name,DampType,Dampa,Dampb,Dampf1=0,Dampf2=0,
                                                            Dampd1=0,Dampd2=0):
        """
            ---This function sets proportional modal damping data for the specified load case---
            inputs:
            name(str)-The name of an existing linear direct integration time history load case.
            DampType(int)-This is 1, 2 or 3, indicating the proportional modal damping type.1 = Mass and stiffness
                proportional damping by direct specification,2 = Mass and stiffness proportional damping by period
                3 = Mass and stiffness proportional damping by frequency
            Dampa(float)-The mass proportional damping coefficient. This item applies only when DampType = 1.
            Dampb(float)-The stiffness proportional damping coefficient. This item applies only when DampType = 1.
            Dampf1(float)-This is the period or the frequency (depending on the value of the DampType item) for point 1.
                [s] for DampType = 2 and [cyc/s] for DampType = 3
            Dampf2(float)-This is either the period or the frequency (depending on the value of the DampType item)
                for point 2. [s] for DampType = 2 and [cyc/s] for DampType = 3
            Dampd1(float)-This is the damping at point 1 (0 <= Dampd1 < 1).This item applies only when DampType = 2 or 3.
            Dampd2(float)-This is the damping at point 2 (0 <= Dampd2 < 1).This item applies only when DampType = 2 or 3.
            """
        ret = self.__Model.LoadCases.ModHistLinear.SetDampProportional(name,DampType,Dampa,Dampb,Dampf1,Dampf2,Dampd1,Dampd2)
        return ret

    def SetLoads(self,name,NumberLoads,LoadType,LoadName,Func,SF=None,
                                                    TF=None,AT=None,CSys=None,Ang=None):
        """
        ---This function sets the load data for the specified analysis case---
        inputs:
        name(str)-The name of an existing nonlinear direct integration time history load case.
        NumberLoads(int)-The number of loads assigned to the specified analysis case.
        LoadType(str list)-This is a str list that includes Load or Accel, indicating the type of each load
            assigned to the load case.
        LoadName(str list)-This is a str list that includes the name of each load assigned to the load case.
            If the LoadType item is Load, this item is the name of a defined load pattern.
            If the LoadType item is Accel, this item is U1, U2, U3, R1, R2 or R3, indicating the direction of the load.
        Func(str list)-This is a str list that includes the name of the time history function associated with each load.
        SF(float list)-This is a str list that includes the scale factor of each load assigned to the load case.
            [L/s2] for U1 U2 and U3; otherwise unitless
        TF(float list)-This is a str list that includes the time scale factor of each load assigned to the load case.
        AT(float list)-This is a str list that includes the arrival time of each load assigned to the load case.
        CSys(str float)-This is a str list that includes the name of the coordinate system associated with each load.
            If this item is a blank string, the Global coordinate system is assumed.This item applies only when the
            LoadType item is Accel.
        Ang(float list)-This is a float list that includes the angle between the acceleration local 1 axis and
            the +X-axis of the coordinate system specified by the CSys item. The rotation is about the Z-axis
            of the specified coordinate system. [deg] This item applies only when the LoadType item is Accel.
        """
        if SF==None:
            SF=[1.0 for each in range(NumberLoads)]
        if TF==None:
            TF=[1.0 for each in range(NumberLoads)]
        if AT==None:
            AT=[0.0 for each in range(NumberLoads)]
        if CSys==None:
            CSys=["GLOBAL" for each in range(NumberLoads)]
        if Ang == None:
            Ang=[0.0 for each in range(NumberLoads)]
        ret = self.__Model.LoadCases.ModHistLinear.SetLoads(name,NumberLoads,LoadType,LoadName,Func,SF,TF,AT,CSys,Ang)
        return ret

    def SetModalCase(self,name,modalCase):
        """
        ---This function sets the modal case for the specified analysis case---
        inputs:
        name(str)-The name of an existing linear modal history analysis case.
        modalCase(str)-This is the name of an existing modal load case.
        """
        ret = self.__Model.LoadCases.ModHistLinear.SetModalCase(name,modalCase)
        return ret

    def SetTimeStep(self,name,nstep,DT):
        """
        ---This function sets the time step data for the specified load case---
        inputs:
        name(str)-The name of an existing linear modal history analysis case.
        nstep(int)-The number of output time steps.
        DT(float)-The output time step size.
        """
        ret = self.__Model.LoadCases.ModHistLinear.SetTimeStep(name,nstep,DT)
        return ret

class load_ModalHistNonlinear:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def SetCase(self,name):
        """
        ---This function initializes a nonlinear modal history analysis case.---
        inputs:
        name(str)-The name of an existing or new load case
        """
        ret = self.__Model.LoadCases.ModHistNonlinear.SetCase(name)
        return ret

    def SetDampConstant(self,name,damp):
        """
        ---This function sets constant modal damping for the specified load case---
        inputs:
        name(str)-The name of an existing nonlinear modal history analysis case.
        damp(float)-The constant damping for all modes (0 <= Damp < 1).
        """
        ret = self.__Model.LoadCases.ModHistNonlinear.SetDampConstant(name,damp)
        return ret

    def SetDampInterpolated(self,name,DampType,NumberItems,Time,Damp):
        """
        ---This function sets interpolated modal damping data for the specified load case---
        inputs:
        name(str)-The name of an existing linear modal history analysis case.
        DampType(int)-This is 5 or 6, indicating the interpolated modal damping type.
            5 = Interpolated damping by period,6 = Interpolated damping by frequency
        NumberItems(int)-The number of Time and Damp pairs.
        Time(float list)-This is a float list that includes the period or the frequency, depending on the
            value of the DampType item. [s] for DampType = 5 and [cyc/s] for DampType = 6
        Damp(float list)-This is a float list that includes the damping for the specified period of frequency
            (0 <= Damp < 1).
        """
        ret = self.__Model.LoadCases.ModHistNonlinear.SetDampInterpolated(name,DampType,NumberItems,Time,Damp)
        return ret

    def SetDampOverrides(self,name,NumberItems,Mode,Damp):
        """
        ---This function sets the modal damping overrides for the specified load case---
        inputs:
        name(str)-The name of an existing nonlinear modal history analysis case.
        NumberItems(int)-The number of Mode and Damp pairs.
        Mode(int list)-This is a int list that includes a mode number.
        Damp(float list)-This is a float list that includes the damping for the specified mode (0 <= Damp < 1).
        """
        ret = self.__Model.LoadCases.ModHistNonlinear.SetDampOverrides(name,NumberItems,Mode,Damp)
        return ret

    def SetDampProportional(self,name,DampType,Dampa,Dampb,Dampf1=0,
                                                            Dampf2=0,Dampd1=0,Dampd2=0):
        """
            ---This function sets proportional modal damping data for the specified load case---
            inputs:
            name(str)-The name of an existing linear direct integration time history load case.
            DampType(int)-This is 1, 2 or 3, indicating the proportional modal damping type.1 = Mass and stiffness
                proportional damping by direct specification,2 = Mass and stiffness proportional damping by period
                3 = Mass and stiffness proportional damping by frequency
            Dampa(float)-The mass proportional damping coefficient. This item applies only when DampType = 1.
            Dampb(float)-The stiffness proportional damping coefficient. This item applies only when DampType = 1.
            Dampf1(float)-This is the period or the frequency (depending on the value of the DampType item) for point 1.
                [s] for DampType = 2 and [cyc/s] for DampType = 3
            Dampf2(float)-This is either the period or the frequency (depending on the value of the DampType item)
                for point 2. [s] for DampType = 2 and [cyc/s] for DampType = 3
            Dampd1(float)-This is the damping at point 1 (0 <= Dampd1 < 1).This item applies only when DampType = 2 or 3.
            Dampd2(float)-This is the damping at point 2 (0 <= Dampd2 < 1).This item applies only when DampType = 2 or 3.
            """
        ret = self.__Model.LoadCases.ModHistNonlinear.SetDampProportional(name,DampType,Dampa,Dampb,Dampf1,Dampf2,Dampd1,Dampd2)
        return ret

    def SetInitialCase(self,name,initialCase=None):
        """
        ---This function sets the initial condition for the specified load case---
        inputs:
        name(str)-The name of an existing nonlinear modal history analysis case.
        initialCase-This is blank, None or the name of an existing analysis case. This item specifies if the
            load case starts from zero initial conditions, that is, an unstressed state, or if it continues
            from the end of another nonlinear modal time history load case.If the specified initial case is
            not a nonlinear modal time history load case, zero initial conditions are assumed
        """
        ret = self.__Model.LoadCases.ModHistNonlinear.SetInitialCase(name,initialCase)
        return ret

    def SetLoads(self,name,NumberLoads,LoadType,LoadName,Func,SF=None,
                                                    TF=None,AT=None,CSys=None,Ang=None):
        """
        ---This function sets the load data for the specified analysis case---
        inputs:
        name(str)-The name of an existing nonlinear direct integration time history load case.
        NumberLoads(int)-The number of loads assigned to the specified analysis case.
        LoadType(str list)-This is a str list that includes Load or Accel, indicating the type of each load
            assigned to the load case.
        LoadName(str list)-This is a str list that includes the name of each load assigned to the load case.
            If the LoadType item is Load, this item is the name of a defined load pattern.
            If the LoadType item is Accel, this item is U1, U2, U3, R1, R2 or R3, indicating the direction of the load.
        Func(str list)-This is a str list that includes the name of the time history function associated with each load.
        SF(float list)-This is a str list that includes the scale factor of each load assigned to the load case.
            [L/s2] for U1 U2 and U3; otherwise unitless
        TF(float list)-This is a str list that includes the time scale factor of each load assigned to the load case.
        AT(float list)-This is a str list that includes the arrival time of each load assigned to the load case.
        CSys(str float)-This is a str list that includes the name of the coordinate system associated with each load.
            If this item is a blank string, the Global coordinate system is assumed.This item applies only when the
            LoadType item is Accel.
        Ang(float list)-This is a float list that includes the angle between the acceleration local 1 axis and
            the +X-axis of the coordinate system specified by the CSys item. The rotation is about the Z-axis
            of the specified coordinate system. [deg] This item applies only when the LoadType item is Accel.
        """
        if SF==None:
            SF=[1.0 for each in range(NumberLoads)]
        if TF==None:
            TF=[1.0 for each in range(NumberLoads)]
        if AT==None:
            AT=[0.0 for each in range(NumberLoads)]
        if CSys==None:
            CSys=["GLOBAL" for each in range(NumberLoads)]
        if Ang == None:
            Ang=[0.0 for each in range(NumberLoads)]
        ret = self.__Model.LoadCases.ModHistNonlinear.SetLoads(name,NumberLoads,LoadType,LoadName,Func,SF,TF,AT,CSys,Ang)
        return ret

    def SetModalCase(self,name,modalCase):
        """
        ---This function sets the modal case for the specified analysis case---
        inputs:
        name(str)-The name of an existing nonlinear modal history analysis case.
        modalCase(str)-This is the name of an existing modal load case
        """
        ret = self.__Model.LoadCases.ModHistNonlinear.SetModalCase(name,modalCase)
        return ret

    def SetSolControlParameters(self,name,tstat=0,dtmax=0,dtmin=0,ftol=1e-5,
                                                                    etol=1e-5,itmax=100,itmin=2,Cf=1):
        """
        ---This function sets the solution control parameters for the specified load case---
        inputs:
        name(str)-The name of an existing nonlinear modal time history analysis case.
        tstat(float)-The static period.
        dtmax(float)-The maximum substep size.
        dtmin(float)-The minimum substep size.
        ftol(float)-The relative force convergence tolerance.
        etol(float)-The relative energy convergence tolerance
        itmax(int)-The maximum iteration limit.
        itmin(int)-The minimum iteration limit.
        Cf(float)-The convergence factor.
        """
        ret = self.__Model.LoadCases.ModHistNonlinear.SetSolControlParameters(name,tstat,dtmax,dtmin,ftol,etol,itmax,itmin,Cf)
        return ret

    def SetTimeStep(self,name:str,nstep:int,dt:float):
        """
        ---This function sets the time step data for the specified load case---
        inputs:
        name(str)-The name of an existing nonlinear modal history analysis case.
        nstep(int)-The number of output time steps.
        DT(float)-The output time step size.
        """
        ret = self.__Model.LoadCases.ModHistNonlinear.SetTimeStep(name,nstep,dt)
        return ret

class load_ResponseSpectrum:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def SetCase(self,name):
        """
        ---This function initializes a response spectrum analysis case---
        name(str)-The name of an existing or new load case.
        """
        ret = self.__Model.LoadCases.ResponseSpectrum.SetCase(name)
        return ret

    def SetDampConstant(self,name,damp):
        """
        ---This function sets constant modal damping for the specified load case---
        inputs:
        name(str)-The name of an existing response spectrum load case.
        damp(float)-The constant damping for all modes (0 <= Damp < 1).
        """
        ret = self.__Model.LoadCases.ResponseSpectrum.SetDampConstant(name,damp)
        return ret

    def SetDampInterpolated(self,name,DampType,NumberItems,Time,Damp):
        """
        ---This function sets interpolated modal damping data for the specified load case---
        inputs:
        name(str)-The name of an existing response spectrum load case.
        DampType(int)-This is either 5 or 6, indicating the interpolated modal damping type.
            5 = Interpolated damping by period,6 = Interpolated damping by frequency
        NumberItems(int)-The number of Time and Damp pairs
        Time(float list)-This is a float list that includes the period or the frequency depending on the value
            of the DampType item. [s] for DampType = 5 and [cyc/s] for DampType = 6
        Damp(float list)-This is a float list that includes the damping for the specified period of frequency
        (0 <= Damp < 1).
        """
        ret = self.__Model.LoadCases.ResponseSpectrum.SetDampInterpolated(name,DampType,NumberItems,Time,Damp)
        return ret

    def SetDampOverrides(self,name,NumberItems,Mode,Damp):
        """
        ---This function sets the modal damping overrides for the specified load case---
        inputs:
        name(str)-The name of an existing response spectrum load case.
        NumberItems(int)-The number of Mode and Damp pairs.
        Mode(int list)-This is a int list that includes a mode number.
        Damp(float list)-This is a float list that includes the damping for the specified mode (0 <= Damp < 1).
        """
        ret = self.__Model.LoadCases.ResponseSpectrum.SetDampOverrides(name,NumberItems,Mode,Damp)
        return ret

    def SetDampProportional(self,name,DampType,Dampa,Dampb,Dampf1=0,
                                                                Dampf2=0,Dampd1=0,Dampd2=0):
        """
        ---This function sets proportional modal damping data for the specified load case---
        inputs:
        name(str)-The name of an existing linear direct integration time history load case.
        DampType(int)-This is 1, 2 or 3, indicating the proportional modal damping type.1 = Mass and stiffness
            proportional damping by direct specification,2 = Mass and stiffness proportional damping by period
            3 = Mass and stiffness proportional damping by frequency
        Dampa(float)-The mass proportional damping coefficient. This item applies only when DampType = 1.
        Dampb(float)-The stiffness proportional damping coefficient. This item applies only when DampType = 1.
        Dampf1(float)-This is the period or the frequency (depending on the value of the DampType item) for point 1.
            [s] for DampType = 2 and [cyc/s] for DampType = 3
        Dampf2(float)-This is either the period or the frequency (depending on the value of the DampType item)
            for point 2. [s] for DampType = 2 and [cyc/s] for DampType = 3
        Dampd1(float)-This is the damping at point 1 (0 <= Dampd1 < 1).This item applies only when DampType = 2 or 3.
        Dampd2(float)-This is the damping at point 2 (0 <= Dampd2 < 1).This item applies only when DampType = 2 or 3.
        """
        ret = self.__Model.LoadCases.ResponseSpectrum.SetDampProportional(name,DampType,Dampa,Dampb,Dampf1,
                                                                Dampf2,Dampd1,Dampd2)
        return ret

    def SSetDiaphragmEccentricityOverride(self,name,Diaph,Eccen,Delete=False):
        """
        ---This function assigns diaphragm eccentricity overrides for response spectrum load cases---
        inputs:
        name(str)-The name of an existing response spectrum load case.
        Diaph(int)-The name of an existing special rigid diaphragm constraint, that is, a diaphragm constraint
            with the following features:1. The constraint type is CONSTRAINT_DIAPHRAGM = 2.2. The constraint
            coordinate system is Global.3. The constraint axis is Z.
        Eccen(float)-The eccentricity applied to the specified diaphragm. [L]
        Delete(bool)-If this item is True, the eccentricity override for the specified diaphragm is deleted.
        """
        ret = self.__Model.LoadCases.ResponseSpectrum.SetDiaphragmEccentricityOverride(name,Diaph,Eccen,Delete)
        return ret

    def SetDirComb(self,name,CombMethod = Literal['SRSS', 'ABS', 'CQC3'],SF=0):
        """
        ---This function sets the directional combination option for the specified load case---
        inputs:
        name(str)-The name of an existing response spectrum load case
        MyType(int)-This is 1, 2, or 3,  indicating the directional combination option.1 = SRSS,2 = ABS,3 = CQC3
        SF(float)-This item applies only when MyType = 2. It is the ABS scale factor.
        """
        mytype = {'SRSS':1,'ABS':2,'CQC3':3}[CombMethod]
        ret = self.__Model.LoadCases.ResponseSpectrum.SetDirComb(name,mytype,SF)
        return ret

    def SetEccentricity(self,name,Eccen):
        """
        ---This function sets the eccentricity ratio that applies to all diaphragms for the specified load case---
        inputs:
        name(str)-The name of an existing response spectrum load case.
        Eccen(float)-The eccentricity ratio that applies to all diaphragms.
        """
        ret = self.__Model.LoadCases.ResponseSpectrum.SetEccentricity(name,Eccen)
        return ret

    def SetLoads(self,name,NumberLoads,LoadName,Func,SF=None,
                                                    CSys=None,Ang=None):
        """
        ---This function sets the load data for the specified analysis case---
        inputs:
        name(str)-The name of an existing response spectrum load case.
        NumberLoads(int)-The number of loads assigned to the specified analysis case.
        LoadName(str list)-This is a str list that includes the name of each load assigned to the load case.
            If the LoadType item is Load, this item is the name of a defined load pattern.
            If the LoadType item is Accel, this item is U1, U2, U3, R1, R2 or R3, indicating the direction of the load.
        Func(str list)-This is a str list that includes the name of the response spectrum  function associated with each load.
        SF(float list)-This is a str list that includes the scale factor of each load assigned to the load case.
            [L/s2] for U1 U2 and U3; otherwise unitless
        CSys(str float)-This is a str list that includes the name of the coordinate system associated with each load.
            If this item is a blank string, the Global coordinate system is assumed.This item applies only when the
            LoadType item is Accel.
        Ang(float list)-This is a float list that includes the angle between the acceleration local 1 axis and
            the +X-axis of the coordinate system specified by the CSys item. The rotation is about the Z-axis
            of the specified coordinate system. [deg] This item applies only when the LoadType item is Accel.
        """
        if SF==None:
            SF=[1.0 for each in range(NumberLoads)]
        if CSys==None:
            CSys=["GLOBAL" for each in range(NumberLoads)]
        if Ang == None:
            Ang=[0.0 for each in range(NumberLoads)]
        ret = self.__Model.LoadCases.ResponseSpectrum.SetLoads(name,NumberLoads,LoadName,Func,SF,CSys,Ang)
        return ret

    def SetModalCase(self,name,ModalCase):
        """
        ---This function sets the modal case for the specified analysis case---
        inputs:
        name(str)-The name of an existing response spectrum load case.
        ModalCase(str)-This is the name of an existing modal load case. It specifies the modal load case on
            which any mode-type load assignments to the specified load case are based.
        """
        ret = self.__Model.LoadCases.ResponseSpectrum.SetModalCase(name,ModalCase)
        return ret

    def SetModalComb_1(self,name,MyType,F1=1,F2=0,PeriodicRigidCombType=1,td=60):
        """
        ---This function sets the modal combination option for the specified load case---
        inputs:
        name(str)-The name of an existing response spectrum load case.
        MyType(int)-This is 1, 2, 3, 4, 5 or 6, indicating the modal combination option.1 = CQC,2 = SRSS,3 = Absolute
            4 = GMC,5 = NRC 10 percent,6 = Double sum
        F1(float)-The GMC f1 factor. This item does not apply when MyType = 3. [cyc/s]
        F2(float)-The GMC f2 factor. This item does not apply when MyType = 3. [cyc/s]
        PeriodicRigidCombType(int)-This is 1 or 2, indicating the periodic plus rigid modal combination option.
            1 = SRSS,2 = Absolute
        td(float)-This item applies only when MyType = 6. It is the factor td. [s]
        """
        ret = self.__Model.LoadCases.ResponseSpectrum.SetModalComb_1(name,MyType,F1,F2,PeriodicRigidCombType,td)
        return ret

class SapLoadCases:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model
        self.StaticLinear = load_StaticLinear(Sapobj)
        self.StaticLinearMultistep = load_StaticLinearMultistep(Sapobj)
        self.StaticNonlinear = load_StaticNonlinear(Sapobj)
        self.Buckling = load_Buckling(Sapobj)
        self.DirHistLinear = load_DirHistLinear(Sapobj)
        self.DirHistNonlinear = load_DirHistNonlinear(Sapobj)
        self.ModalEigen = load_ModalEigen(Sapobj)
        self.ModalRitz = load_ModalRitz(Sapobj)
        self.ModalHistLinear = load_ModalHistLinear(Sapobj)
        self.ModalHistNonlinear = load_ModalHistNonlinear(Sapobj)
        self.ResponseSpectrum = load_ResponseSpectrum(Sapobj)
