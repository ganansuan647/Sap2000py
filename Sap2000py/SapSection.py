from typing import Literal
class SapSection:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model
        self.PropLink = PropLink(Sapobj)

    def PropFrame_SetGeneral(self,sectName,matName,t3,t2,Area,As2,As3,I22,I33,J,notes=""):
        """
        ---set a general frame section property---
        intput:
        sectName(str)-the name of the defined sections
        matName(str)-the name of the material used for current section
        Depth(t3)-The depth of the section. [L]
        Width(t2)-The width of the section. [L]
        Area(float)-The cross-sectional area. [L2]
        As2(float)-The shear area for forces in the section local 2-axis direction. [L2]
        As3(float)-The shear area for forces in the section local 3-axis direction. [L2]
        I22(float)-The moment of inertia for bending about the local 2 axis. [L4]
        I33(float)-The moment of inertia for bending about the local 3 axis. [L4]
        J(float)-The torsional constant. [L4]
        """
        ret = self.__Model.PropFrame.SetGeneral(sectName,matName,t3,t2,Area,As2,As3,J,I22,I33,1,1,1,1,1,1,-1, notes + "\nAdded by Sap2000py")
        return ret

    def PropFrame_SetSD(self,sectName,matName,DesignType=0,Color=-1,Notes="",GUID = ""):
        """
        ---set a SD(Section Designer) frame section property---
        This function initializes a section designer property.
        The function returns zero if the section property is successfully initialized; otherwise it returns a nonzero value.
        input:
        sectName(str)-the name of the defined sections
        matName(str)-the name of the material used for current section
        DesignType(long)-This is 0, 1, 2 or 3, indicating the design option for the section.
            0 = No design
            1 = Design as general steel section
            2 = Design as a concrete column; check the reinforcing
            3 = Design as a concrete column; design the reinforcing
        Color(long)-The display color assigned to the section. If Color is specified as -1, the program will automatically assign a color.
        Notes(str)-The notes, if any, assigned to the section.
        GUID(str)-The GUID (global unique identifier), if any, assigned to the section. If this item is input as Default, the program assigns a GUID to the section.
        """
        ret = self.__Model.PropFrame.SetSDSection(sectName, matName, DesignType, Color, Notes, GUID)
        return ret

    def Tendon_SetProp(self,tendonName,matName,modelOpt,Area):
        """
        ---set a tendon property---
        inputs:
        tendonName-The name of new tendon property
        matName-The name of the material property assigned to the tendon property.
        modelOpt-1 = Model tendon as loads,2 = Model tendon as elements
        area-The cross-sectional area of the tendon. [L2]
        """
        self.__Model.PropTendon.SetProp(tendonName,matName,modelOpt,Area)

    def Cable_SetPro(self,cableName,matName,Area):
        """
        ---set a cable property---
        intputs:
        cableName(str)-The name of  new cable property
        matName(str)-The name of the material property assigned to the cable property
        Area(float)-The cross-sectional area of the tendon. [L2]
        """
        self.__Model.PropCable.SetProp(cableName,matName,Area)

    def Area_SetPlane(self,areaName,MyType,MatProp,Thickness,MatAng=0,Incompatible=True):
        """
        ---This function initializes a plane-type area property. If this function is called for an existing area
        property, all items for the property are reset to their default value.---
        inputs:
        areaName(str)-The name of an existing or new area property. If this is an existing property,
                that property is modified; otherwise, a new property is added.
        MyType(int)-This is either 1 or 2, indicating the plane type.1 = Plane-stress,2 = Plane-strain
        MatProp(str)-The name of the material property for the area property.
        MatAng(float)-The material angle. [deg]
        Thickness(float)-The plane thickness. [L]
        Incompatible(bool)-If this item is True, incompatible bending modes are included in the stiffness
            formulation. In general, incompatible modes significantly improve the bending behavior of the object.
        """
        self.__Model.PropArea.SetPlane(areaName,MyType,MatProp,MatAng,Thickness,Incompatible)

    def Area_SetShell_1(self,name,ShellType,MatProp,Thickness,matAng=0):
        """
        ---This function initializes a shell-type area property. If this function is called for an existing
        area property, all items for the property are reset to their default value---
        inputs:
        name(str)-The name of an existing or new area property. If this is an existing property, that
            property is modified; otherwise, a new property is added.
        ShellType(int)-This is 1, 2, 3, 4, 5 or 6, indicating the shell type.1 = Shell - thin,2 = Shell - thick
            3 = Plate - thin,4 = Plate - thick,5 = Membrane6 = Shell layered/nonlinear
        MatProp(str)-The name of the material property for the area property. This item does not apply when
            ShellType = 6.
        Thickness(float)-The membrane thickness. [L],This item does not apply when ShellType = 6.
        matAng(float)-The material angle. [deg] This item does not apply when ShellType = 6.
        """
        self.__Model.PropArea.SetShell_1(name,ShellType,False,MatProp,matAng,Thickness,Thickness)

    def PropSolid_SetProp(self,name,matProp,a=0,b=0,c=0,incompatible=True):
        """
        ---This function defines a solid property---
        inputs:
        name(str)-The name of an existing or new solid property. If this is an existing property, that property
            is modified; otherwise, a new property is added
        MatProp(str)-The name of the material property assigned to the solid property.
        a,b,c(float)-The material angle A,B,C [deg]
        incompatible(bool)-If this item is True, incompatible bending modes are included in the stiffness
            formulation. In general, incompatible modes significantly improve the bending behavior of the object.
        """
        ret = self.__Model.PropSolid.SetProp(name,matProp,a,b,c,incompatible)
        return ret

class PropLink_Set:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model 
        
    def SetLinear(self,name,DOF,Fixed,Ke={},Ce={},dj2=0,dj3=0,KeCoupled=False,CeCoupled=False):
        """
        ---This function initializes a linear-type link property. If this function is called for
        an existing link property, all items for the property are reset to their default value.---
        inputs:
        name(str)-The name of an existing or new link property. If this is an existing property,
            that property is modified; otherwise, a new property is added.
        DOF(list)-This is str list,indicating if properties exist for a specified degree of freedom.e.g. ["U1"]
        Fixed(list)-This is str list, indicating if the specified degree of freedom is fixed (restrained).e.g. ["R1"]
        Ke(dict)-This is a dictionary of stiffness terms for the link property,
            e.g., uncouple:{"U1":2000,"R1":5000},coupled: {"U1R2":400}
        Ce(dict)-This is a dictionary of damping terms for the link property,
            e.g., uncouple:{"U1":0.03,"R1":0.05},coupled: {"U1R2":0.05}
        dj2(float)-The distance from the J-End of the link to the U2 shear spring.
            This item applies only when DOF(1) = True. [L]
        dj3(float)-The distance from the J-End of the link to the U3 shear spring.
            This item applies only when DOF(2) = True. [L]
        KeCoupled(bool)-This item is True if the link stiffness, Ke, is coupled.
        CeCoupled(bool)-This item is True if the link damping, Ce, is coupled.
        """
        DOFDict={"U1":0,"U2":1,"U3":2,"R1":3,"R2":4,"R3":5}
        DOFFinal=[False,False,False,False,False,False]
        for each in DOF:
            indexNum=DOFDict[each]
            DOFFinal[indexNum]=True
        FixedFinal = [False, False, False, False, False, False]
        for each1 in Fixed:
            indexNum1=DOFDict[each1]
            FixedFinal[indexNum1]=True
        keDict={"U1":0,"U2":1,"U3":2,"R1":3,"R2":4,"R3":5}
        keCoupleDict={"U1U1":0,"U1U2":1,"U2U2":2,"U1U3":3,"U2U3":4,"U3U3":5,"U1R1":6,
                        "U2R1":7,"U3R1":8,"R1R1":9,"U1R2":10,"U2R2":11,"U3R2":12,"R1R2":13,
                        "R2R2":14,"U1R3":15,"U2R3":16,"U3R3":17,"R1R3":18,"R2R3":19,"R3R3":20}
        keFinal=[0 for each in range(6)]
        keCouple=[0 for each in range(21)]
        if not KeCoupled:
            keInput=keFinal
            key2=Ke.keys()
            for each2 in key2:
                indexNum2=keDict[each2]
                keInput[indexNum2]=Ke[each2]
        else:
            keInput = keCouple
            key3 = Ke.keys()
            for each3 in key3:
                indexNum3=keCoupleDict[each3]
                keInput[indexNum3]=Ke[each3]
        ceFinal = [0 for each in range(6)]
        ceCouple = [0 for each in range(21)]
        if not CeCoupled:
            ceInput=ceFinal
            key4=Ce.keys()
            for each4 in key4:
                indexNum4=keDict[each4]
                ceInput[indexNum4]=Ce[each4]
        else:
            ceInput = ceCouple
            key5 = Ce.keys()
            for each5 in key5:
                indexNum5=keCoupleDict[each5]
                ceInput[indexNum5]=Ce[each5]
        ret = self.__Model.PropLink.SetLinear(name,DOFFinal,FixedFinal,keInput,ceInput,dj2,dj3,KeCoupled,CeCoupled)
        return ret

    def MultiLinearElastic(self,name:str,
                           DOF:list[Literal['U1','U2','U3','R1','R2','R3']] = [],
                           Fixed:list[Literal['U1','U2','U3','R1','R2','R3']] = [],
                           Nonlinear:list[Literal['U1','U2','U3','R1','R2','R3']] = [],
                           Ke:dict[Literal['U1','U2','U3','R1','R2','R3'],float] = {},
                           Ce:dict[Literal['U1','U2','U3','R1','R2','R3'],float] = {},
                           dj2:float = 0.0,
                           dj3:float = 0.0,
                           notes:str = "",
                           GUID:str = ""):
        
        """
        ---This function initializes a multilinear elastic-type link property. If this function is called for an
        existing link property, all items for the property are reset to their default value.---
        inputs:
        name(str)-The name of an existing or new link property. If this is an existing property then.
            that property is modified; otherwise, a new property is added.
        DOF(list)-This is str list,indicating if properties exist for a specified degree of freedom.e.g. ["U1"]
        Fixed(list)-This is str list, indicating if the specified degree of freedom is fixed (restrained).e.g. ["R1"]
        Nonlinear(list)-This is str list, indicating if nonlinear properties exist for a specified degree of freedom.
            e.g. ["R1"]
        Ke(dict)-This is a dictionary of stiffness terms for the link property,e.g.,{"U1":2000,"R1":5000}
        Ce(dict)-This is a dictionary of damping terms for the link property,e.g.,{"U1":0.03,"R1":0.05}
        dj2(float)-The distance from the J-End of the link to the U2 shear spring.
            This item applies only when DOF(1) = True. [L]
        dj3(float)-The distance from the J-End of the link to the U3 shear spring.
            This item applies only when DOF(2) = True. [L]
        """
        DOFDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        DOFFinal = [False, False, False, False, False, False]
        for each in DOF:
            indexNum = DOFDict[each]
            DOFFinal[indexNum] = True
        FixedFinal = [False, False, False, False, False, False]
        for each1 in Fixed:
            indexNum1 = DOFDict[each1]
            FixedFinal[indexNum1] = True
        nonlinearFinal = [False, False, False, False, False, False]
        for each2 in Nonlinear:
            indexNum2=DOFDict[each2]
            nonlinearFinal[indexNum2]=True
        keDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        keInput = [0 for each in range(6)]
        key2 = Ke.keys()
        for each2 in key2:
            indexNum2 = keDict[each2]
            keInput[indexNum2] = Ke[each2]
        ceInput = [0 for each in range(6)]
        key3 = Ce.keys()
        for each3 in key3:
            indexNum3 = keDict[each3]
            ceInput[indexNum3] = Ce[each3]
        ret = self.__Model.PropLink.SetMultiLinearElastic(name,DOFFinal,FixedFinal,nonlinearFinal,keInput,ceInput,dj2,dj3,notes,GUID)
        return ret

    def MultiLinearPoints(self,name,DOF:Literal['U1','U2','U3','R1','R2','R3'],forceList:list[float],dispList:list[float],Type:Literal['Isotropic','Kinematic','Takeda','Pivot']='Isotropic',a1=0,a2=0,b1=0,b2=0,eta=0):
        """
        ---This function sets the force-deformation data for a specified degree of freedom in multilinear
        elastic and multilinear plastic link properties.---
        inputs:
        name(str)-The name of an existing multilinear elastic or multilinear plastic link property.
        DOF(int)-This is 1, 2, 3, 4, 5 or 6, indicating the degree of freedom to which the multilinear points apply.
            1 = U1,2 = U2,3 = U3,4 = R1,5 = R2,6 = R3
        forceList(float list)-that includes the force at each point. When DOF is U1, U2 or U3, this is a force.
            When DOF is R1, R2 or R3. this is a moment. [F] if DOF <= 3, and [FL} if DOF > 3
        dispList(float list)-that includes the displacement at each point. When DOF is U1, U2 or U3, this is
            a translation. When DOF is R1, R2 or R3, this is a rotation. [L] if DOF <= 3, and [rad] if DOF > 3
        myType(int)-This item applies only to multilinear plastic link properties. It is 1, 2 or 3, indicating
            the hysteresis type.0=Isotropic,1 = Kinematic,2 = Takeda,3 = Pivot
        a1,a2,b1,b2,eta(float)-This item applies only to multilinear plastic link properties that have a pivot
        hysteresis type (MyType = Pivot).
        """
        DOFDict = {"U1": 1, "U2": 2, "U3": 3, "R1": 4, "R2": 5, "R3": 6}
        dof = DOFDict[DOF]
        TypeDict = {"Isotropic": 0, "Kinematic": 1, "Takeda": 2, "Pivot": 3}
        Typeid = TypeDict[Type]
        numberPoints=len(forceList)
        TypeDict={"Isotropic":0,"Kinematic":1,"Takeda":2,"Pivot":3}
        myType=TypeDict[Type]
        self.__Model.PropLink.SetMultiLinearPoints(name,DOF,numberPoints,forceList,dispList,myType,a1,a2,b1,b2,eta)

    def Damper(self,name,DOF,Fixed,Nonliear,Ke={},Ce={},k={},c={},cexp={},dj2=0,dj3=0):
        """
        ---This function initializes an exponential damper-type link property---
        inputs:
        name(str)-The name of an existing or new link property. If this is an existing property, that property
            is modified; otherwise, a new property is added.
        DOF(list)-This is str list,indicating if properties exist for a specified degree of freedom.e.g. ["U1"]
        Fixed(list)-This is str list, indicating if the specified degree of freedom is fixed (restrained).e.g. ["R1"]
        Nonlinear(list)-This is str list, indicating if nonlinear properties exist for a specified degree of freedom.
            e.g. ["R1"]
        Ke(dict)-This is a dictionary of stiffness terms for the link property,e.g.,{"U1":2000,"R1":5000}
        Ce(dict)-This is a dictionary of damping terms for the link property,e.g.,{"U1":0.03,"R1":0.05}
        k(dict)-The initial stiffness applies for nonlinear analyses.e.g.,{"U1":10000}
        c(dict)-The nonlinear damping coefficient applies for nonlinear analyses.{"U1":2000}
        cexp(dict)-The nonlinear damping exponent applies for nonlinear analyses. It is applied to the velocity
            across the damper in the equation of motion.{"U1":0.3}
        dj2(float)-The distance from the J-End of the link to the U2 shear spring.
            This item applies only when DOF(1) = True. [L]
        dj3(float)-The distance from the J-End of the link to the U3 shear spring.
            This item applies only when DOF(2) = True. [L]
        """
        DOFDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        DOFFinal = [False, False, False, False, False, False]
        for each in DOF:
            indexNum = DOFDict[each]
            DOFFinal[indexNum] = True
        FixedFinal = [False, False, False, False, False, False]
        for each1 in Fixed:
            indexNum1 = DOFDict[each1]
            FixedFinal[indexNum1] = True
        nonlinearFinal = [False, False, False, False, False, False]
        for each2 in Nonliear:
            indexNum2 = DOFDict[each2]
            nonlinearFinal[indexNum2] = True
        keDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        keInput = [0 for each in range(6)]
        key2 = Ke.keys()
        for each2 in key2:
            indexNum2 = keDict[each2]
            keInput[indexNum2] = Ke[each2]
        ceInput = [0 for each in range(6)]
        key3 = Ce.keys()
        for each3 in key3:
            indexNum3 = keDict[each3]
            ceInput[indexNum3] = Ce[each3]
        kInput=[0 for each in range(6)]
        key4=k.keys()
        for each4 in key4:
            indexNum4 = keDict[each4]
            kInput[indexNum4] = k[each4]
        cInput = [0 for each in range(6)]
        key5 = c.keys()
        for each5 in key5:
            indexNum5 = keDict[each5]
            cInput[indexNum5] = c[each5]
        cexpInput = [0 for each in range(6)]
        key6 = cexp.keys()
        for each6 in key6:
            indexNum6 = keDict[each6]
            cexpInput[indexNum6] = cexp[each6]
        self.__Model.PropLink.SetDamper(name,DOFFinal,FixedFinal,nonlinearFinal,keInput,ceInput,kInput,cInput,
                                            cexpInput,dj2,dj3)

    def DamperBilinear(self,name,DOF,Fixed,Nonliear,Ke={},Ce={},k={},c={},
                                                    cy={},ForceLimit={},dj2=0,dj3=0):
        """
        ---This function initializes a bilinear damper-type link property---
        inputs:
        name(str)-The name of an existing or new link property. If this is an existing property, that property
            is modified; otherwise, a new property is added.
        DOF(list)-This is str list,indicating if properties exist for a specified degree of freedom.e.g. ["U1"]
        Fixed(list)-This is str list, indicating if the specified degree of freedom is fixed (restrained).e.g. ["R1"]
        Nonlinear(list)-This is str list, indicating if nonlinear properties exist for a specified degree of freedom.
            e.g. ["R1"]
        Ke(dict)-This is a dictionary of stiffness terms for the link property,e.g.,{"U1":2000,"R1":5000}
        Ce(dict)-This is a dictionary of damping terms for the link property,e.g.,{"U1":0.03,"R1":0.05}
        k(dict)-The initial stiffness applies for nonlinear analyses.e.g.,{"U1":10000}
        c(dict)-The nonlinear initial damping coefficient applies for nonlinear analyses.{"U1":2000}
        cy(dict)-The nonlinear yielded damping coefficient applies for nonlinear analyses.
        ForceLimit(dict)-nonlinear linear force limit terms for the link property. The linear force limit
            applies for nonlinear analyses.
        dj2(float)-The distance from the J-End of the link to the U2 shear spring.
            This item applies only when DOF(1) = True. [L]
        dj3(float)-The distance from the J-End of the link to the U3 shear spring.
            This item applies only when DOF(2) = True. [L]
        """
        DOFDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        DOFFinal = [False, False, False, False, False, False]
        for each in DOF:
            indexNum = DOFDict[each]
            DOFFinal[indexNum] = True
        FixedFinal = [False, False, False, False, False, False]
        for each1 in Fixed:
            indexNum1 = DOFDict[each1]
            FixedFinal[indexNum1] = True
        nonlinearFinal = [False, False, False, False, False, False]
        for each2 in Nonliear:
            indexNum2 = DOFDict[each2]
            nonlinearFinal[indexNum2] = True
        keDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        keInput = [0 for each in range(6)]
        key2 = Ke.keys()
        for each2 in key2:
            indexNum2 = keDict[each2]
            keInput[indexNum2] = Ke[each2]
        ceInput = [0 for each in range(6)]
        key3 = Ce.keys()
        for each3 in key3:
            indexNum3 = keDict[each3]
            ceInput[indexNum3] = Ce[each3]
        kInput = [0 for each in range(6)]
        key4 = k.keys()
        for each4 in key4:
            indexNum4 = keDict[each4]
            kInput[indexNum4] = k[each4]
        cInput = [0 for each in range(6)]
        key5 = c.keys()
        for each5 in key5:
            indexNum5 = keDict[each5]
            cInput[indexNum5] = c[each5]
        cyInput = [0 for each in range(6)]
        key6 = cy.keys()
        for each6 in key6:
            indexNum6 = keDict[each6]
            cyInput[indexNum6] = cy[each6]
        forceLimitInput = [0 for each in range(6)]
        key7 = ForceLimit.keys()
        for each7 in key7:
            indexNum7 = keDict[each7]
            forceLimitInput[indexNum7] = ForceLimit[each7]
        ret = self.__Model.PropLink.SetDamperBilinear(name,DOFFinal,FixedFinal,nonlinearFinal,keInput,ceInput,kInput,cInput,
                                                    cyInput,forceLimitInput,dj2,dj3)
        return ret

    def Gap(self,name,DOF,Fixed,NonLinear,Ke={},Ce={},k={},disp={},dj2=0,dj3=0):
        """
        ---This function initializes a gap-type link property---
        inputs:
        name(str)-The name of an existing or new link property
        DOF(list)-This is str list,indicating if properties exist for a specified degree of freedom.e.g. ["U1"]
        Fixed(list)-This is str list, indicating if the specified degree of freedom is fixed (restrained).e.g. ["R1"]
        Nonlinear(list)-This is str list, indicating if nonlinear properties exist for a specified degree of freedom.
            e.g. ["R1"]
        Ke(dict)-This is a dictionary of stiffness terms for the link property,e.g.,{"U1":2000,"R1":5000}
        Ce(dict)-This is a dictionary of damping terms for the link property,e.g.,{"U1":0.03,"R1":0.05}
        k(dict)-The initial stiffness applies for nonlinear analyses.e.g.,{"U1":10000}
        disp(dict)-initial gap opening terms for the link property. The initial gap opening applies
            for nonlinear analyses.{"U1":1.2}
        dj2(float)-The distance from the J-End of the link to the U2 shear spring.
            This item applies only when DOF(1) = True. [L]
        dj3(float)-The distance from the J-End of the link to the U3 shear spring.
            This item applies only when DOF(2) = True. [L]
        """
        DOFDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        DOFFinal = [False, False, False, False, False, False]
        for each in DOF:
            indexNum = DOFDict[each]
            DOFFinal[indexNum] = True
        FixedFinal = [False, False, False, False, False, False]
        for each1 in Fixed:
            indexNum1 = DOFDict[each1]
            FixedFinal[indexNum1] = True
        nonlinearFinal = [False, False, False, False, False, False]
        for each2 in NonLinear:
            indexNum2 = DOFDict[each2]
            nonlinearFinal[indexNum2] = True
        keDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        keInput = [0 for each in range(6)]
        key2 = Ke.keys()
        for each2 in key2:
            indexNum2 = keDict[each2]
            keInput[indexNum2] = Ke[each2]
        ceInput = [0 for each in range(6)]
        key3 = Ce.keys()
        for each3 in key3:
            indexNum3 = keDict[each3]
            ceInput[indexNum3] = Ce[each3]
        kInput = [0 for each in range(6)]
        key4 = k.keys()
        for each4 in key4:
            indexNum4 = keDict[each4]
            kInput[indexNum4] = k[each4]
        dispInput = [0 for each in range(6)]
        key5 = disp.keys()
        for each5 in key5:
            indexNum5 = keDict[each5]
            dispInput[indexNum5] = disp[each5]
        ret = self.__Model.PropLink.SetGap(name,DOFFinal,FixedFinal,nonlinearFinal,keInput,ceInput,kInput,dispInput,dj2,dj3)
        return ret

    def Hook(self,name,DOF,Fixed,NonLinear,Ke={},Ce={},k={},disp={},dj2=0,dj3=0):
        """
        ---This function initializes a hook-type link property---
        inputs:
        name(str)-The name of an existing or new link property
        DOF(list)-This is str list,indicating if properties exist for a specified degree of freedom.e.g. ["U1"]
        Fixed(list)-This is str list, indicating if the specified degree of freedom is fixed (restrained).e.g. ["R1"]
        Nonlinear(list)-This is str list, indicating if nonlinear properties exist for a specified degree of freedom.
            e.g. ["R1"]
        Ke(dict)-This is a dictionary of stiffness terms for the link property,e.g.,{"U1":2000,"R1":5000}
        Ce(dict)-This is a dictionary of damping terms for the link property,e.g.,{"U1":0.03,"R1":0.05}
        k(dict)-The initial stiffness applies for nonlinear analyses.e.g.,{"U1":10000}
        disp(dict)-initial hook opening terms for the link property. The initial gap opening applies
            for nonlinear analyses.{"U1":1.2}
        dj2(float)-The distance from the J-End of the link to the U2 shear spring.
            This item applies only when DOF(1) = True. [L]
        dj3(float)-The distance from the J-End of the link to the U3 shear spring.
            This item applies only when DOF(2) = True. [L]
        """
        DOFDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        DOFFinal = [False, False, False, False, False, False]
        for each in DOF:
            indexNum = DOFDict[each]
            DOFFinal[indexNum] = True
        FixedFinal = [False, False, False, False, False, False]
        for each1 in Fixed:
            indexNum1 = DOFDict[each1]
            FixedFinal[indexNum1] = True
        nonlinearFinal = [False, False, False, False, False, False]
        for each2 in NonLinear:
            indexNum2 = DOFDict[each2]
            nonlinearFinal[indexNum2] = True
        keDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        keInput = [0 for each in range(6)]
        key2 = Ke.keys()
        for each2 in key2:
            indexNum2 = keDict[each2]
            keInput[indexNum2] = Ke[each2]
        ceInput = [0 for each in range(6)]
        key3 = Ce.keys()
        for each3 in key3:
            indexNum3 = keDict[each3]
            ceInput[indexNum3] = Ce[each3]
        kInput = [0 for each in range(6)]
        key4 = k.keys()
        for each4 in key4:
            indexNum4 = keDict[each4]
            kInput[indexNum4] = k[each4]
        dispInput = [0 for each in range(6)]
        key5 = disp.keys()
        for each5 in key5:
            indexNum5 = keDict[each5]
            dispInput[indexNum5] = disp[each5]
        ret = self.__Model.PropLink.SetHook(name,DOFFinal,FixedFinal,nonlinearFinal,keInput,ceInput,kInput,dispInput,dj2,dj3)
        return ret

    def PlasticWen(self,name,DOF,Fixed,NonLinear,Ke={},Ce={},k={},yieldF={},Ratio={},
                                                exp={},dj2=0,dj3=0):
        """
        ---This function initializes a plastic Wen-type link property---
        inputs:
        name(str)-The name of an existing or new link property
        DOF(list)-This is str list,indicating if properties exist for a specified degree of freedom.e.g. ["U1"]
        Fixed(list)-This is str list, indicating if the specified degree of freedom is fixed (restrained).e.g. ["R1"]
        Nonlinear(list)-This is str list, indicating if nonlinear properties exist for a specified degree of freedom.
            e.g. ["R1"]
        Ke(dict)-This is a dictionary of stiffness terms for the link property,e.g.,{"U1":2000,"R1":5000}
        Ce(dict)-This is a dictionary of damping terms for the link property,e.g.,{"U1":0.03,"R1":0.05}
        k(dict)-The initial stiffness applies for nonlinear analyses.e.g.,{"U1":10000}
        yieldF(dict)-yield force terms for the link property. The yield force applies for nonlinear analyses.
        Ratio(dict)-post-yield stiffness ratio terms for the link property. The post-yield stiffness ratio
            applies for nonlinear analyses. It is the post-yield stiffness divided by the initial stiffness.
        exp(dict)-yield exponent terms for the link property. The yield exponent applies for nonlinear analyses.
            The yielding exponent that controls the sharpness of the transition from the initial stiffness to the
            yielded stiffness.
        dj2(float)-The distance from the J-End of the link to the U2 shear spring.
            This item applies only when DOF(1) = True. [L]
        dj3(float)-The distance from the J-End of the link to the U3 shear spring.
            This item applies only when DOF(2) = True. [L]
        """
        DOFDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        DOFFinal = [False, False, False, False, False, False]
        for each in DOF:
            indexNum = DOFDict[each]
            DOFFinal[indexNum] = True
        FixedFinal = [False, False, False, False, False, False]
        for each1 in Fixed:
            indexNum1 = DOFDict[each1]
            FixedFinal[indexNum1] = True
        nonlinearFinal = [False, False, False, False, False, False]
        for each2 in NonLinear:
            indexNum2 = DOFDict[each2]
            nonlinearFinal[indexNum2] = True
        keDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        keInput = [0 for each in range(6)]
        key2 = Ke.keys()
        for each2 in key2:
            indexNum2 = keDict[each2]
            keInput[indexNum2] = Ke[each2]
        ceInput = [0 for each in range(6)]
        key3 = Ce.keys()
        for each3 in key3:
            indexNum3 = keDict[each3]
            ceInput[indexNum3] = Ce[each3]
        kInput = [0 for each in range(6)]
        key4 = k.keys()
        for each4 in key4:
            indexNum4 = keDict[each4]
            kInput[indexNum4] = k[each4]
        yieldFInput = [0 for each in range(6)]
        key5 = yieldF.keys()
        for each5 in key5:
            indexNum5 = keDict[each5]
            yieldFInput[indexNum5] = yieldF[each4]
        RatioInput = [0 for each in range(6)]
        key6 = Ratio.keys()
        for each6 in key6:
            indexNum6 = keDict[each6]
            RatioInput[indexNum6] = Ratio[each6]
        expInput = [0 for each in range(6)]
        key7 = exp.keys()
        for each7 in key7:
            indexNum7 = keDict[each7]
            expInput[indexNum7] = exp[each7]
        ret = self.__Model.PropLink.SetPlasticWen(name,DOFFinal,FixedFinal,nonlinearFinal,keInput,ceInput,kInput,
                                                yieldFInput,RatioInput,expInput,dj2,dj3)
        return ret

    def RubberIsolator(self,name,DOF,Fixed,NonLinear,Ke={},Ce={},k={},YieldF={},
                                                    Ratio={},dj2=0,dj3=0):
        """
        ---This function initializes a rubber isolator-type link property---
        inputs:
        name(str)-The name of an existing or new link property
        DOF(list)-This is str list,indicating if properties exist for a specified degree of freedom.e.g. ["U1"]
        Fixed(list)-This is str list, indicating if the specified degree of freedom is fixed (restrained).e.g. ["R1"]
        Nonlinear(list)-This is str list, indicating if nonlinear properties exist for a specified degree of freedom.
            e.g. ["R1"]
        Ke(dict)-This is a dictionary of stiffness terms for the link property,e.g.,{"U1":2000,"R1":5000}
        Ce(dict)-This is a dictionary of damping terms for the link property,e.g.,{"U1":0.03,"R1":0.05}
        k(dict)-The initial stiffness applies for nonlinear analyses.e.g.,{"U1":10000}
            k(0) = U1, Not Used,k(1) = U2 [F/L],k(2) = U3 [F/L],k(3) = R1, Not Used,k(4) = R2, Not Used
            k(5) = R3, Not Used
        yieldF(dict)-yield force terms for the link property. The yield force applies for nonlinear analyses.
            k(0) = U1, Not Used,k(1) = U2 [F/L],k(2) = U3 [F/L],k(3) = R1, Not Used,k(4) = R2, Not Used
            k(5) = R3, Not Used
        Ratio(dict)-post-yield stiffness ratio terms for the link property. The post-yield stiffness ratio
            applies for nonlinear analyses. It is the post-yield stiffness divided by the initial stiffness.
            k(0) = U1, Not Used,k(1) = U2 [F/L],k(2) = U3 [F/L],k(3) = R1, Not Used,k(4) = R2, Not Used
            k(5) = R3, Not Used
        dj2(float)-The distance from the J-End of the link to the U2 shear spring.
            This item applies only when DOF(1) = True. [L]
        dj3(float)-The distance from the J-End of the link to the U3 shear spring.
            This item applies only when DOF(2) = True. [L]
        """
        DOFDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        DOFFinal = [False, False, False, False, False, False]
        for each in DOF:
            indexNum = DOFDict[each]
            DOFFinal[indexNum] = True
        FixedFinal = [False, False, False, False, False, False]
        for each1 in Fixed:
            indexNum1 = DOFDict[each1]
            FixedFinal[indexNum1] = True
        nonlinearFinal = [False, False, False, False, False, False]
        for each2 in NonLinear:
            indexNum2 = DOFDict[each2]
            nonlinearFinal[indexNum2] = True
        keDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        keInput = [0 for each in range(6)]
        key2 = Ke.keys()
        for each2 in key2:
            indexNum2 = keDict[each2]
            keInput[indexNum2] = Ke[each2]
        ceInput = [0 for each in range(6)]
        key3 = Ce.keys()
        for each3 in key3:
            indexNum3 = keDict[each3]
            ceInput[indexNum3] = Ce[each3]
        kInput = [0 for each in range(6)]
        key4 = k.keys()
        for each4 in key4:
            indexNum4 = keDict[each4]
            kInput[indexNum4] = k[each4]
        yieldFInput = [0 for each in range(6)]
        key5 = YieldF.keys()
        for each5 in key5:
            indexNum5 = keDict[each5]
            yieldFInput[indexNum5] = YieldF[each4]
        RatioInput = [0 for each in range(6)]
        key6 = Ratio.keys()
        for each6 in key6:
            indexNum6 = keDict[each6]
            RatioInput[indexNum6] = Ratio[each6]
        ret = self.__Model.PropLink.SetRubberIsolator(name,DOFFinal,FixedFinal,nonlinearFinal,keInput,ceInput,kInput,
                                                yieldFInput,RatioInput,dj2,dj3)
        return ret

    def FrictionIsolator(self,name,DOF,Fixed,Nonlinear,Ke={},Ce={},k={},slow={},fast={},
                                                    Rate={},Radius={},damping=0,dj2=0,dj3=0):
        """
        ---This function initializes a friction isolator-type link proper---
        inputs:
        name(str)-The name of an existing or new link property
        DOF(list)-This is str list,indicating if properties exist for a specified degree of freedom.e.g. ["U1"]
        Fixed(list)-This is str list, indicating if the specified degree of freedom is fixed (restrained).e.g. ["R1"]
        Nonlinear(list)-This is str list, indicating if nonlinear properties exist for a specified degree of freedom.
            e.g. ["R1"]
        Ke(dict)-This is a dictionary of stiffness terms for the link property,e.g.,{"U1":2000,"R1":5000}
        Ce(dict)-This is a dictionary of damping terms for the link property,e.g.,{"U1":0.03,"R1":0.05}
        k(dict)-The initial stiffness applies for nonlinear analyses.e.g.,{"U1":10000}
            k(0) = U1 [F/L],k(1) = U2 [F/L],k(2) = U3 [F/L],k(3) = R1, Not Used,k(4) = R2, Not Used,k(5) = R3, Not Used
        slow(dict)- the friction coefficient at zero velocity terms for the link property. This coefficient applies
            for nonlinear analyses.Slow(0) = U1, Not Used,Slow(1) = U2,Slow(2) = U3,Slow(3) = R1, Not Used,
            Slow(4) = R2, Not Used,Slow(5) = R3, Not Used
        fast(dict)-the friction coefficient at fast velocity terms for the link property. This coefficient applies
            for nonlinear analyses.Slow(0) = U1, Not Used,Slow(1) = U2,Slow(2) = U3,Slow(3) = R1, Not Used,
            Slow(4) = R2, Not Used,Slow(5) = R3, Not Used
        Rate(dict)-the inverse of the characteristic sliding velocity terms for the link property. This item applies
            for nonlinear analyses.Slow(0) = U1, Not Used,Slow(1) = U2,Slow(2) = U3,Slow(3) = R1, Not Used,
            Slow(4) = R2, Not Used,Slow(5) = R3, Not Used
        Radius(dict)-the radius of the sliding contact surface terms for the link property. Inputting 0 means
            there is an infinite radius, that is, the slider is flat. This item applies for nonlinear analyses.
            Slow(0) = U1, Not Used,Slow(1) = U2,Slow(2) = U3,Slow(3) = R1, Not Used,
            Slow(4) = R2, Not Used,Slow(5) = R3, Not Used
        damping(float)-the nonlinear damping coefficient used for the axial translational degree of freedom,
            U1. This item applies for nonlinear analyses. [F/L]
        dj2(float)-The distance from the J-End of the link to the U2 shear spring.
            This item applies only when DOF(1) = True. [L]
        dj3(float)-The distance from the J-End of the link to the U3 shear spring.
            This item applies only when DOF(2) = True. [L]
        """
        DOFDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        DOFFinal = [False, False, False, False, False, False]
        for each in DOF:
            indexNum = DOFDict[each]
            DOFFinal[indexNum] = True
        FixedFinal = [False, False, False, False, False, False]
        for each1 in Fixed:
            indexNum1 = DOFDict[each1]
            FixedFinal[indexNum1] = True
        nonlinearFinal = [False, False, False, False, False, False]
        for each2 in Nonlinear:
            indexNum2 = DOFDict[each2]
            nonlinearFinal[indexNum2] = True
        keDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        keInput = [0 for each in range(6)]
        key2 = Ke.keys()
        for each2 in key2:
            indexNum2 = keDict[each2]
            keInput[indexNum2] = Ke[each2]
        ceInput = [0 for each in range(6)]
        key3 = Ce.keys()
        for each3 in key3:
            indexNum3 = keDict[each3]
            ceInput[indexNum3] = Ce[each3]
        kInput = [0 for each in range(6)]
        key4 = k.keys()
        for each4 in key4:
            indexNum4 = keDict[each4]
            kInput[indexNum4] = k[each4]
        slowInput = [0 for each in range(6)]
        key5 = slow.keys()
        for each5 in key5:
            indexNum5 = keDict[each5]
            slowInput[indexNum5] = slow[each5]
        fastInput = [0 for each in range(6)]
        key6 = fast.keys()
        for each6 in key6:
            indexNum6 = keDict[each6]
            fastInput[indexNum6] = fast[each6]
        rateInput = [0 for each in range(6)]
        key7 = Rate.keys()
        for each7 in key7:
            indexNum7 = keDict[each7]
            rateInput[indexNum7] = Rate[each7]
        radiusInput = [0 for each in range(6)]
        key8 = Radius.keys()
        for each8 in key8:
            indexNum8 = keDict[each8]
            radiusInput[indexNum8] = Radius[each8]
        ret = self.__Model.PropLink.SetFrictionIsolator(name,DOFFinal,FixedFinal,nonlinearFinal,keInput,ceInput,kInput,
                                                    slowInput,fastInput,rateInput,radiusInput,damping,dj2,dj3)
        return ret

    def WeightAndMass(self,name,w,mass=0,R1=0,R2=0,R3=0):
        """
        ---This function assigns weight and mass values to a link property.---
        inputs:
        name(str)-The name of an existing link property.
        w(float)-The weight of the link. [F]
        mass(float)-The translational mass of the link. [M]
        R1,R2,R3(float)-The rotational inertia of the link about its local 1,2,3 axis. [ML2]
        """
        ret = self.__Model.PropLink.SetWeightAndMass(name)
        return ret

class PropLink_Get:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model 
    
    def GetDamper(self, name: str) -> list:
        """
        Retrieves link property data for an exponential damper-type link property.
        
        Parameters:
        name (str): The name of an existing exponential damper-type link property.
        
        Returns:
        List: [ret, DOF, Fixed, NonLinear, Ke, Ce, k, c, cexp, dj2, dj3, Notes, GUID]
            - ret (int): Returns zero if the property data is successfully retrieved; otherwise returns a nonzero value.
            - DOF (list of bool): A boolean array, dimensioned to 5, indicating if properties exist for a specified degree of freedom.
            - Fixed (list of bool): A boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed (restrained).
            - NonLinear (list of bool): A boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified degree of freedom.
            - Ke (list of float): An array of effective stiffness terms for the link property. The effective stiffness applies for linear analyses.
            - Ce (list of float): An array of effective damping terms for the link property. The effective damping applies for linear analyses.
            - k (list of float): An array of initial stiffness terms for the link property. The initial stiffness applies for nonlinear analyses.
            - c (list of float): An array of nonlinear damping coefficient terms for the link property. The nonlinear damping coefficient applies for nonlinear analyses.
            - cexp (list of float): An array of the nonlinear damping exponent terms. The nonlinear damping exponent applies for nonlinear analyses.
            - dj2 (float): The distance from the J-End of the link to the U2 shear spring.
            - dj3 (float): The distance from the J-End of the link to the U3 shear spring.
            - Notes (str): The notes, if any, assigned to the property.
            - GUID (str): The GUID (global unique identifier), if any, assigned to the property.
        """
        ret = self.__Model.PropLink.GetDamper(name)
        return ret

    def GetDamperBilinear(self, name: str) -> list:
        """
        Retrieves link property data for a bilinear damper-type link property.
        
        Parameters:
        name (str): The name of an existing bilinear damper-type link property.
        
        Returns:
        List: [ret, DOF, Fixed, NonLinear, Ke, Ce, k, c, cy, ForceLimit, dj2, dj3, Notes, GUID]
            - ret (int): Returns zero if the property data is successfully retrieved; otherwise returns a nonzero value.
            - DOF (list of bool): A boolean array, dimensioned to 5, indicating if properties exist for a specified degree of freedom.
            - Fixed (list of bool): A boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed (restrained).
            - NonLinear (list of bool): A boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified degree of freedom.
            - Ke (list of float): An array of effective stiffness terms for the link property. The effective stiffness applies for linear analyses.
            - Ce (list of float): An array of effective damping terms for the link property. The effective damping applies for linear analyses.
            - k (list of float): An array of initial stiffness terms for the link property. The initial stiffness applies for nonlinear analyses.
            - c (list of float): An array of nonlinear initial damping coefficient terms for the link property. The nonlinear initial damping coefficient applies for nonlinear analyses.
            - cy (list of float): An array of nonlinear yielded damping coefficient terms for the link property. The nonlinear yielded damping coefficient applies for nonlinear analyses.
            - ForceLimit (list of float): An array of nonlinear linear force limit terms for the link property. The linear force limit applies for nonlinear analyses.
            - dj2 (float): The distance from the J-End of the link to the U2 shear spring.
            - dj3 (float): The distance from the J-End of the link to the U3 shear spring.
            - Notes (str): The notes, if any, assigned to the property.
            - GUID (str): The GUID (global unique identifier), if any, assigned to the property.
        """
        ret = self.__Model.PropLink.GetDamperBilinear(name)
        return ret

    def GetDamperFrictionSpring(self, name: str) -> list:
        """
        Retrieves link property data for a friction spring damper-type link property.
        
        Parameters:
        name (str): The name of an existing friction spring damper-type link property.
        
        Returns:
        List: [ret, DOF, Fixed, NonLinear, Ke, Ce, k, k1, k2, u0, us, dj2, dj3, Notes, GUID]
            - ret (int): Returns zero if the property data is successfully retrieved; otherwise returns a nonzero value.
            - DOF (list of bool): A boolean array, dimensioned to 5, indicating if properties exist for a specified degree of freedom.
            - Fixed (list of bool): A boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed (restrained).
            - NonLinear (list of bool): A boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified degree of freedom.
            - Ke (list of float): An array of effective stiffness terms for the link property. The effective stiffness applies for linear analyses.
            - Ce (list of float): An array of effective damping terms for the link property. The effective damping applies for linear analyses.
            - k (list of float): An array of initial (nonslipping) stiffness terms for the link property. The initial stiffness applies for nonlinear analyses.
            - k1 (list of float): An array of slipping stiffness when loading terms for the link property. The slipping stiffness when loading applies for nonlinear analyses.
            - k2 (list of float): An array of slipping stiffness when unloading terms for the link property. The slipping stiffness when unloading applies for nonlinear analyses.
            - u0 (list of float): An array of precompression displacement terms for the link property. The nonlinear precompression displacement applies for nonlinear analyses.
            - us (list of float): An array of stop displacement terms for the link property. The nonlinear stop displacement applies for nonlinear analyses.
            - dj2 (float): The distance from the J-End of the link to the U2 shear spring.
            - dj3 (float): The distance from the J-End of the link to the U3 shear spring.
            - Notes (str): The notes, if any, assigned to the property.
            - GUID (str): The GUID (global unique identifier), if any, assigned to the property.
        """
        ret = self.__Model.PropLink.GetDamperFrictionSpring(name)
        return ret

    def GetDamperLinearExponential(self, name: str) -> list:
        """
        Retrieves link property data for a linear exponential damper-type link property.
        
        Parameters:
        name (str): The name of an existing linear exponential damper-type link property.
        
        Returns:
        List: [ret, DOF, Fixed, NonLinear, Ke, Ce, k, c, cexp, ForceLimit, dj2, dj3, Notes, GUID]
            - ret (int): Returns zero if the property data is successfully retrieved; otherwise returns a nonzero value.
            - DOF (list of bool): A boolean array, dimensioned to 5, indicating if properties exist for a specified degree of freedom.
            - Fixed (list of bool): A boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed (restrained).
            - NonLinear (list of bool): A boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified degree of freedom.
            - Ke (list of float): An array of effective stiffness terms for the link property. The effective stiffness applies for linear analyses.
            - Ce (list of float): An array of effective damping terms for the link property. The effective damping applies for linear analyses.
            - k (list of float): An array of initial stiffness terms for the link property. The initial stiffness applies for nonlinear analyses.
            - c (list of float): An array of nonlinear damping coefficient terms for the link property. The nonlinear damping coefficient applies for nonlinear analyses.
            - cexp (list of float): An array of the nonlinear damping exponent terms. The nonlinear damping exponent applies for nonlinear analyses.
            - ForceLimit (list of float): An array of nonlinear linear force limit terms for the link property. The linear force limit applies for nonlinear analyses.
            - dj2 (float): The distance from the J-End of the link to the U2 shear spring.
            - dj3 (float): The distance from the J-End of the link to the U3 shear spring.
            - Notes (str): The notes, if any, assigned to the property.
            - GUID (str): The GUID (global unique identifier), if any, assigned to the property.
        """
        ret = self.__Model.PropLink.GetDamperLinearExponential(name)
        return ret

    def GetFrictionIsolator(self, name: str) -> list:
        """
        Retrieves link property data for a friction isolator-type link property.
        
        Parameters:
        name (str): The name of an existing friction isolator-type link property.
        
        Returns:
        List: [ret, DOF, Fixed, NonLinear, Ke, Ce, k, Slow, Fast, Rate, Radius, Damping, dj2, dj3, Notes, GUID]
            - ret (int): Returns zero if the property data is successfully retrieved; otherwise returns a nonzero value.
            - DOF (list of bool): A boolean array, dimensioned to 5, indicating if properties exist for a specified degree of freedom.
            - Fixed (list of bool): A boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed (restrained).
            - NonLinear (list of bool): A boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified degree of freedom.
            - Ke (list of float): An array of effective stiffness terms for the link property. The effective stiffness applies for linear analyses.
            - Ce (list of float): An array of effective damping terms for the link property. The effective damping applies for linear analyses.
            - k (list of float): An array of initial stiffness terms for the link property. The initial stiffness applies for nonlinear analyses.
            - Slow (list of float): An array of the friction coefficient at zero velocity terms for the link property. This coefficient applies for nonlinear analyses.
            - Fast (list of float): An array of the friction coefficient at fast velocity terms for the link property. This coefficient applies for nonlinear analyses.
            - Rate (list of float): An array of the inverse of the characteristic sliding velocity terms for the link property. This item applies for nonlinear analyses.
            - Radius (list of float): An array of the radius of the sliding contact surface terms for the link property. Inputting 0 means there is an infinite radius, that is, the slider is flat. This item applies for nonlinear analyses.
            - Damping (float): The nonlinear damping coefficient used for the axial translational degree of freedom, U1. This item applies for nonlinear analyses.
            - dj2 (float): The distance from the J-End of the link to the U2 shear spring.
            - dj3 (float): The distance from the J-End of the link to the U3 shear spring.
            - Notes (str): The notes, if any, assigned to the property.
            - GUID (str): The GUID (global unique identifier), if any, assigned to the property.
        """
        ret = self.__Model.PropLink.GetFrictionIsolator(name)
        return ret

    def GetGap(self, name: str) -> list:
        """
        Retrieves link property data for a gap-type link property.
        
        Parameters:
        name (str): The name of an existing gap-type link property.
        
        Returns:
        List: [ret, DOF, Fixed, NonLinear, Ke, Ce, k, dis, dj2, dj3, Notes, GUID]
            - ret (int): Returns zero if the property data is successfully retrieved; otherwise returns a nonzero value.
            - DOF (list of bool): A boolean array, dimensioned to 5, indicating if properties exist for a specified degree of freedom.
            - Fixed (list of bool): A boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed (restrained).
            - NonLinear (list of bool): A boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified degree of freedom.
            - Ke (list of float): An array of effective stiffness terms for the link property. The effective stiffness applies for linear analyses.
            - Ce (list of float): An array of effective damping terms for the link property. The effective damping applies for linear analyses.
            - k (list of float): An array of initial stiffness terms for the link property. The initial stiffness applies for nonlinear analyses.
            - dis (list of float): An array of initial gap opening terms for the link property. The initial gap opening applies for nonlinear analyses.
            - dj2 (float): The distance from the J-End of the link to the U2 shear spring.
            - dj3 (float): The distance from the J-End of the link to the U3 shear spring.
            - Notes (str): The notes, if any, assigned to the property.
            - GUID (str): The GUID (global unique identifier), if any, assigned to the property.
        """
        ret = self.__Model.PropLink.GetGap(name)
        return ret

    def GetHook(self, name: str) -> list:
        """
        Retrieves link property data for a hook-type link property.
        
        Parameters:
        name (str): The name of an existing hook-type link property.
        
        Returns:
        List: [ret, DOF, Fixed, NonLinear, Ke, Ce, k, dis, dj2, dj3, Notes, GUID]
            - ret (int): Returns zero if the property data is successfully retrieved; otherwise returns a nonzero value.
            - DOF (list of bool): A boolean array, dimensioned to 5, indicating if properties exist for a specified degree of freedom.
            - Fixed (list of bool): A boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed (restrained).
            - NonLinear (list of bool): A boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified degree of freedom.
            - Ke (list of float): An array of effective stiffness terms for the link property. The effective stiffness applies for linear analyses.
            - Ce (list of float): An array of effective damping terms for the link property. The effective damping applies for linear analyses.
            - k (list of float): An array of initial stiffness terms for the link property. The initial stiffness applies for nonlinear analyses.
            - dis (list of float): An array of initial hook opening terms for the link property. The initial hook opening applies for nonlinear analyses.
            - dj2 (float): The distance from the J-End of the link to the U2 shear spring.
            - dj3 (float): The distance from the J-End of the link to the U3 shear spring.
            - Notes (str): The notes, if any, assigned to the property.
            - GUID (str): The GUID (global unique identifier), if any, assigned to the property.
        """
        ret = self.__Model.PropLink.GetHook(name)
        return ret

    def GetLinear(self, name: str) -> list:
        """
        Retrieves link property data for a linear-type link property.
        
        Parameters:
        name (str): The name of an existing linear-type link property.
        
        Returns:
        List: [ret, DOF, Fixed, Ke, Ce, dj2, dj3, KeCoupled, CeCoupled, Notes, GUID]
            - ret (int): Returns zero if the property data is successfully retrieved; otherwise returns a nonzero value.
            - DOF (list of bool): A boolean array, dimensioned to 5, indicating if properties exist for a specified degree of freedom.
            - Fixed (list of bool): A boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed (restrained).
            - Ke (list of float): An array of stiffness terms for the link property. There are 6 terms if the stiffness is uncoupled and 21 if it is coupled.
            - Ce (list of float): An array of damping terms for the link property. There are 6 terms if the damping is uncoupled and 21 if it is coupled.
            - dj2 (float): The distance from the J-End of the link to the U2 shear spring.
            - dj3 (float): The distance from the J-End of the link to the U3 shear spring.
            - KeCoupled (bool): Indicates if the link stiffness, Ke, is coupled.
            - CeCoupled (bool): Indicates if the link damping, Ce, is coupled.
            - Notes (str): The notes, if any, assigned to the property.
            - GUID (str): The GUID (global unique identifier), if any, assigned to the property.
        """
        ret = self.__Model.PropLink.GetLinear(name)
        return ret

    def GetMultiLinearElastic(self, name: str) -> list:
        """
        Retrieves link property data for a multilinear elastic-type link property.
        
        Parameters:
        name (str): The name of an existing multilinear elastic-type link property.
        
        Returns:
        List: [ret, DOF, Fixed, NonLinear, Ke, Ce, dj2, dj3, Notes, GUID]
            - ret (int): Returns zero if the property data is successfully retrieved; otherwise returns a nonzero value.
            - DOF (list of bool): A boolean array, dimensioned to 5, indicating if properties exist for a specified degree of freedom.
            - Fixed (list of bool): A boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed (restrained).
            - NonLinear (list of bool): A boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified degree of freedom.
            - Ke (list of float): An array of effective stiffness terms for the link property. The effective stiffness applies for linear analyses.
            - Ce (list of float): An array of effective damping terms for the link property. The effective damping applies for linear analyses.
            - dj2 (float): The distance from the J-End of the link to the U2 shear spring.
            - dj3 (float): The distance from the J-End of the link to the U3 shear spring.
            - Notes (str): The notes, if any, assigned to the property.
            - GUID (str): The GUID (global unique identifier), if any, assigned to the property.
        """
        ret = self.__Model.PropLink.GetMultiLinearElastic(name)
        return ret

    def GetMultiLinearPlastic(self, name: str) -> list:
        """
        Retrieves link property data for a multilinear plastic-type link property.
        
        Parameters:
        name (str): The name of an existing multilinear plastic-type link property.
        
        Returns:
        List: [ret, DOF, Fixed, NonLinear, Ke, Ce, dj2, dj3, Notes, GUID]
            - ret (int): Returns zero if the property data is successfully retrieved; otherwise returns a nonzero value.
            - DOF (list of bool): A boolean array, dimensioned to 5, indicating if properties exist for a specified degree of freedom.
            - Fixed (list of bool): A boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed (restrained).
            - NonLinear (list of bool): A boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified degree of freedom.
            - Ke (list of float): An array of effective stiffness terms for the link property. The effective stiffness applies for linear analyses.
            - Ce (list of float): An array of effective damping terms for the link property. The effective damping applies for linear analyses.
            - dj2 (float): The distance from the J-End of the link to the U2 shear spring.
            - dj3 (float): The distance from the J-End of the link to the U3 shear spring.
            - Notes (str): The notes, if any, assigned to the property.
            - GUID (str): The GUID (global unique identifier), if any, assigned to the property.
        """
        ret = self.__Model.PropLink.GetMultiLinearPlastic(name)
        return ret

    def GetMultiLinearPoints(self, name: str) -> list:
        """
        Retrieves the force-deformation data for a specified degree of freedom in multilinear elastic and multilinear plastic link properties.
        
        Parameters:
        name (str): The name of an existing multilinear elastic or multilinear plastic link property.
        
        Returns:
        List: [ret, DOF, NumberPoints, F, D, MyType, a1, a2, b1, b2, eta]
            - ret (int): Returns zero if the data is successfully retrieved; otherwise returns a nonzero value.
            - DOF (int): 1, 2, 3, 4, 5, or 6, indicating the degree of freedom to which the multilinear points apply.
            - NumberPoints (int): The number of force-deformation points for the specified degree of freedom.
            - F (list of float): An array, dimensioned to NumberPoints - 1, that includes the force at each point.
            - D (list of float): An array, dimensioned to NumberPoints - 1, that includes the displacement at each point.
            - MyType (int): This item applies only to multilinear plastic link properties. It is 1, 2, or 3, indicating the hysteresis type.
            - a1 (float): This item only applies to multilinear plastic link properties that have a pivot hysteresis type (MyType = 3). It is the Alpha1 hysteresis parameter.
            - a2 (float): This item applies only to multilinear plastic link properties that have a pivot hysteresis type (MyType = 3). It is the Alpha2 hysteresis parameter.
            - b1 (float): This item applies only to multilinear plastic link properties that have a pivot hysteresis type (MyType = 3). It is the Beta1 hysteresis parameter.
            - b2 (float): This item applies only to multilinear plastic link properties that have a pivot hysteresis type (MyType = 3). It is the Beta2 hysteresis parameter.
            - eta (float): This item applies only to multilinear plastic link properties that have a pivot hysteresis type (MyType = 3). It is the Eta hysteresis parameter.
        """
        ret = self.__Model.PropLink.GetMultiLinearPoints(name)
        return ret

    def GetNameList(self) -> list:
        """
        Retrieves the names of all defined link properties of the specified type.
        
        Parameters:
        None
        
        Returns:
        List: [ret, NumberNames, MyName]
            - ret (int): Returns zero if the names are successfully retrieved; otherwise returns a nonzero value.
            - NumberNames (int): The number of link property names retrieved by the program.
            - MyName (list of str): A one-dimensional array of link property names.
        """
        ret = self.__Model.PropLink.GetNameList()
        return ret

    def GetPDelta(self, name: str) -> list:
        """
        Retrieves P-delta parameters for a link property.
        
        Parameters:
        name (str): The name of an existing link property.
        
        Returns:
        List: [Value, ret]
            - Value (list of float): An array of P-delta parameters.
                - Value[0] = M2 P-delta to I-end of link as moment, M2I
                - Value[1] = M2 P-delta to J-end of link as moment, M2J
                - Value[2] = M3 P-delta to I-end of link as moment, M3I
                - Value[3] = M3 P-delta to J-end of link as moment, M3J
            - ret (int): Returns zero if the data is successfully retrieved; otherwise returns a nonzero value.
        """
        ret = self.__Model.PropLink.GetPDelta(name)
        return ret

    def GetPlasticWen(self, name: str) -> list:
        """
        Retrieves link property data for a plastic Wen-type link property.
        
        Parameters:
        name (str): The name of an existing plastic Wen-type link property.
        
        Returns:
        List: [DOF, Fixed, NonLinear, Ke, Ce, k, Yield, Ratio, exp, dj2, dj3, Notes, GUID, ret]
            - DOF (list of bool): A boolean array, dimensioned to 5, indicating if properties exist for a specified degree of freedom.
            - Fixed (list of bool): A boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed (restrained).
            - NonLinear (list of bool): A boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified degree of freedom.
            - Ke (list of float): An array of effective stiffness terms for the link property. The effective stiffness applies for linear analyses.
            - Ce (list of float): An array of effective damping terms for the link property. The effective damping applies for linear analyses.
            - k (list of float): An array of initial stiffness terms for the link property. The initial stiffness applies for nonlinear analyses.
            - Yield (list of float): An array of yield force terms for the link property. The yield force applies for nonlinear analyses.
            - Ratio (list of float): An array of post-yield stiffness ratio terms for the link property. The post-yield stiffness ratio applies for nonlinear analyses.
            - exp (list of float): An array of yield exponent terms for the link property. The yield exponent applies for nonlinear analyses.
            - dj2 (float): The distance from the J-End of the link to the U2 shear spring.
            - dj3 (float): The distance from the J-End of the link to the U3 shear spring.
            - Notes (str): The notes, if any, assigned to the property.
            - GUID (str): The GUID (global unique identifier), if any, assigned to the property.
            - ret (int): Returns zero if the property data is successfully retrieved; otherwise returns a nonzero value.
        """
        ret = self.__Model.PropLink.GetPlasticWen(name,)
        return ret

    def GetRubberIsolator(self, name: str) -> list:
        """
        Retrieves link property data for a rubber isolator-type link property.
        
        Parameters:
        name (str): The name of an existing rubber isolator-type link property.
        
        Returns:
        List: [DOF, Fixed, NonLinear, Ke, Ce, k, Yield, Ratio, dj2, dj3, Notes, GUID, ret]
            - DOF (list of bool): A boolean array, dimensioned to 5, indicating if properties exist for a specified degree of freedom.
            - Fixed (list of bool): A boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed (restrained).
            - NonLinear (list of bool): A boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified degree of freedom.
            - Ke (list of float): An array of effective stiffness terms for the link property. The effective stiffness applies for linear analyses.
            - Ce (list of float): An array of effective damping terms for the link property. The effective damping applies for linear analyses.
            - k (list of float): An array of initial stiffness terms for the link property. The initial stiffness applies for nonlinear analyses.
            - Yield (list of float): An array of yield force terms for the link property. The yield force applies for nonlinear analyses.
            - Ratio (list of float): An array of post-yield stiffness ratio terms for the link property. The post-yield stiffness ratio applies for nonlinear analyses.
            - dj2 (float): The distance from the J-End of the link to the U2 shear spring.
            - dj3 (float): The distance from the J-End of the link to the U3 shear spring.
            - Notes (str): The notes, if any, assigned to the property.
            - GUID (str): The GUID (global unique identifier), if any, assigned to the property.
            - ret (int): Returns zero if the property data is successfully retrieved; otherwise returns a nonzero value.
        """
        ret = self.__Model.PropLink.GetRubberIsolator(name)
        return ret

    def GetSpringData(self, name: str) -> list:
        """
        Retrieves length and area values for a link property that are used if the link property is specified in line and area spring assignments.
        
        Parameters:
        name (str): The name of an existing link property.
        
        Returns:
        List: [DefinedForThisLength, DefinedForThisArea, ret]
            - DefinedForThisLength (float): The link property is defined for this length in a line (frame) spring. [L]
            - DefinedForThisArea (float): The link property is defined for this area in an area spring. [L2]
            - ret (int): Returns zero if the data is successfully retrieved; otherwise returns a nonzero value.
        """
        ret = self.__Model.PropLink.GetSpringData(name)
        return ret

    def GetTCFrictionIsolator(self, name: str) -> list:
        """
        Retrieves link property data for a T/C friction isolator-type link property.
        
        Parameters:
        name (str): The name of an existing T/C friction isolator-type link property.
        
        Returns:
        List: [DOF, Fixed, NonLinear, Ke, Ce, k, Slow, Fast, Rate, Radius, SlowT, FastT, RateT, kt, dis, dist, Damping, dj2, dj3, Notes, GUID, ret]
            - DOF (list of bool): A boolean array, dimensioned to 5, indicating if properties exist for a specified degree of freedom.
            - Fixed (list of bool): A boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed (restrained).
            - NonLinear (list of bool): A boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified degree of freedom.
            - Ke (list of float): An array of effective stiffness terms for the link property. The effective stiffness applies for linear analyses.
            - Ce (list of float): An array of effective damping terms for the link property. The effective damping applies for linear analyses.
            - k (list of float): An array of initial stiffness terms for the link property. The initial stiffness applies for nonlinear analyses.
            - Slow (list of float): An array of the friction coefficient at zero velocity terms when U1 is in compression for the link property. This coefficient applies for nonlinear analyses.
            - Fast (list of float): An array of the friction coefficient at fast velocity terms when U1 is in compression for the link property. This coefficient applies for nonlinear analyses.
            - Rate (list of float): An array of the inverse of the characteristic sliding velocity terms when U1 is in compression for the link property. This item applies for nonlinear analyses.
            - Radius (list of float): An array of the radius of the sliding contact surface terms for the link property. Inputting 0 means there is an infinite radius, that is, the slider is flat. This item applies for nonlinear analyses.
            - SlowT (list of float): An array of the friction coefficient at zero velocity terms when U1 is in tension for the link property. This coefficient applies for nonlinear analyses.
            - FastT (list of float): An array of the friction coefficient at fast velocity terms when U1 is in tension for the link property. This coefficient applies for nonlinear analyses.
            - RateT (list of float): An array of the inverse of the characteristic sliding velocity terms when U1 is in tension for the link property. This item applies for nonlinear analyses.
            - kt (float): The axial translational tension stiffness for the U1 degree of freedom. This item applies for nonlinear analyses.
            - dis (float): The U1 degree of freedom gap opening for compression. This item applies for nonlinear analyses.
            - dist (float): The U1 degree of freedom gap opening for tension. This item applies for nonlinear analyses.
            - Damping (float): The nonlinear damping coefficient used for the axial translational degree of freedom, U1. This item applies for nonlinear analyses.
            - dj2 (float): The distance from the J-End of the link to the U2 shear spring.
            - dj3 (float): The distance from the J-End of the link to the U3 shear spring.
            - Notes (str): The notes, if any, assigned to the property.
            - GUID (str): The GUID (global unique identifier), if any, assigned to the property.
            - ret (int): Returns zero if the property data is successfully retrieved; otherwise returns a nonzero value.
        """
        ret = self.__Model.PropLink.GetTCFrictionIsolator(name)
        return ret

    def GetTriplePendulumIsolator(self, name: str) -> list:
        """
        Retrieves link property data for a Triple Pendulum Isolator type link property.
        
        Parameters:
        name (str): The name of an existing Triple Pendulum Isolator type link property.
        
        Returns:
        List: [DOF, Fixed, NonLinear, Ke, Ce, K1, Damping, K, Slow, Fast, Rate, Radius, StopDist, HeightOut, HeightIn, dj2, dj3, Notes, GUID, ret]
            - DOF (list of bool): A boolean array, dimensioned to 5, indicating if properties exist for a specified degree of freedom.
            - Fixed (list of bool): A boolean array, dimensioned to 5, indicating if the specified degree of freedom is fixed (restrained).
            - NonLinear (list of bool): A boolean array, dimensioned to 5, indicating if nonlinear properties exist for a specified degree of freedom.
            - Ke (list of float): An array of effective stiffness terms for the link property. The effective stiffness applies for linear analyses, and also for nonlinear analysis for those DOF for which NonLinear(n) = False.
            - Ce (list of float): An array of effective damping terms for the link property. The effective damping applies for linear analyses.
            - K1 (float): The axial compression stiffness for the U1 degree of freedom. This item applies for nonlinear analyses.
            - Damping (float): The nonlinear damping coefficient for the axial degree of freedom, U1, when it is in compression. This item applies for nonlinear analyses.
            - K (list of float): An array, dimensioned to 3, of initial nonlinear stiffness (before sliding) for each sliding surface.
            - Slow (list of float): An array, dimensioned to 3, of the friction coefficient at zero velocity for each sliding surface when U1 is in compression.
            - Fast (list of float): An array, dimensioned to 3, of the friction coefficient at fast velocity for each sliding surface when U1 is in compression.
            - Rate (list of float): An array, dimensioned to 3, of the inverse of the characteristic sliding velocity for the Slow and Fast friction coefficients for each sliding surface.
            - Radius (list of float): An array, dimensioned to 3, of the radius for each sliding surface. Inputting 0 means there is an infinite radius, that is, the slider is flat.
            - StopDist (list of float): An array, dimensioned to 3, of the amount of displacement allowed before hitting a stiff limit for each sliding surface. Inputting 0 means there is no stop.
            - HeightOut (float): The height (distance) between the outer sliding surfaces at zero displacement.
            - HeightIn (float): The height (distance) between the inner sliding surfaces.
            - dj2 (float): The distance from the J-End of the link to the U2 shear spring, that is, the center of the isolator.
            - dj3 (float): The distance from the J-End of the link to the U3 shear spring, that is, the center of the isolator.
            - Notes (str): The notes, if any, assigned to the property.
            - GUID (str): The GUID (global unique identifier), if any, assigned to the property.
            - ret (int): Returns zero if the property data is successfully retrieved; otherwise returns a nonzero value.
        """
        ret = self.__Model.PropLink.GetTriplePendulumIsolator(name)
        return ret

    def GetTypeOAPI(self, name: str) -> list:
        """
        Retrieves the property type for the specified link property.
        
        Parameters:
        name (str): The name of an existing link property.
        
        Returns:
        List: [PropType, ret]
            - PropType (str): The type of the link property as defined in the eLinkPropType enumeration.
                'Linear' = 1
                'Damper' = 2
                'Gap' = 3
                'Hook' = 4
                'PlasticWen' = 5
                'RubberIsolator' = 6
                'FrictionIsolator' = 7
                'MultiLinearElastic' = 8
                'MultiLinearPlastic' = 9
                'TCFrictionIsolator' = 10
                'NotFound' = 0
            - ret (int): Returns zero if the type is successfully retrieved; otherwise returns a nonzero value.
        """
        TypeDict = {0:None, 1:'Linear', 2:'Damper', 3:'Gap', 4:'Hook', 5:'PlasticWen', 6:'RubberIsolator', 7:'FrictionIsolator', 8:'MultiLinearElastic', 9:'MultiLinearPlastic', 10:'TCFrictionIsolator'}
        PropType,ret = self.__Model.PropLink.GetTypeOAPI(name)
        if PropType in TypeDict:
            return [TypeDict[PropType],ret]
        else:
            return [PropType,ret]

    def GetWeightAndMass(self, name: str) -> list:
        """
        Retrieves weight and mass data for a link property.
        
        Parameters:
        name (str): The name of an existing link property.
        
        Returns:
        List: [w, m, R1, R2, R3, ret]
            - w (float): The weight of the link. [F]
            - m (float): The translational mass of the link. [M]
            - R1 (float): The rotational inertia of the link about its local 1 axis. [ML2]
            - R2 (float): The rotational inertia of the link about its local 2 axis. [ML2]
            - R3 (float): The rotational inertia of the link about its local 3 axis. [ML2]
            - ret (int): Returns zero if the data is successfully retrieved; otherwise returns a nonzero value.
        """
        ret = self.__Model.PropLink.GetWeightAndMass(name)
        return ret

class PropLink:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model
        self.Set = PropLink_Set(Sapobj)
        self.Get = PropLink_Get(Sapobj)

    

