

class SapMaterial():
    def __init__(self,Sapobj):
        """
        Translation: Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def SetSSCurve(self,matName,strainList,stressList):
        """
        ---sets the material stress-strain curve for existing material ---
        inputs:
        matName(str)-the name of the defined material
        strainList(float)-This is an array that includes the strain at each point on the
                        stress strain curve. The strains must increase monotonically.
        stressList(flaot)-This is an array that includes the stress at each point on
                        the stress strain curve. [F/L2]
        Points that have a negative strain must have a zero or negative stress. Similarly,
        points that have a positive strain must have a zero or positive stress.
        There must be one point defined that has zero strain and zero stress.
        """
        numPoint=len(strainList)
        pointID=[i1 for i1 in range(numPoint)]
        self.__Model.PropMaterial.SetSSCurve(matName,numPoint,pointID,strainList,stressList)

    def TendonUser(self,tendonName,weightPerV,E,temC):
        """
        ---user defined unixial tendon material  ---
        inputs:
        tendonName(str)-the name of the tendon material
        weightPerV(float)-The weight per unit volume for the material. [F/L3]
        E(float)-The modulus of elasticity. [F/L2]
        tempC(float)-The modulus of elasticity. [F/L2]
        """
        self.__Model.PropMaterial.SetMaterial(tendonName,7) #eMatType_Tendon = 7
        self.__Model.PropMaterial.SetWeightAndMass(tendonName, 1,weightPerV)#1 = Weight per unit volume
        self.__Model.PropMaterial.SetMPUniaxial(tendonName,E,temC)

    def AddMaterial(self,name,matType,region,standard,grade):
        """
        ---adds a new standard material property to the model---
        name(str)-the name of the added material
        matType(int)-the material type number.eMatType_Steel = 1,eMatType_Concrete = 2,eMatType_NoDesign = 3
                    eMatType_Aluminum = 4,eMatType_ColdFormed = 5,eMatType_Rebar = 6,eMatType_Tendon = 7
        region(str)-different countries or user ["China","Europe","India","Italy","New Zealand","Russia",
                    "Spain","United States","Vietnam","User"]
        standard(str)-the standard name, for China it includes ["GB","JTG","TB","User"]
        grade(str)-the grade name of the material property, For China steel JTG--["GB/T 714-2008 Q345q",--235--,
                    --370--,--420--,--460--,--500--,--550--,--620--,--690--]
                    For China Concrete JTG--["JTG D62-2004 C15",--20--,--25--,--30--,...,--80--]
        """
        self.__Model.PropMaterial.AddMaterial(name,matType,region,standard,grade)
        str_list = grade.split(" ")
        nameList=standard+"-"+str_list[-1]
        self.__Model.PropMaterial.ChangeName(nameList,name)

    def GetMPIsotropic(self,matName):
        """
        ---get the the mechanical properties for a material with an isotropic directional symmetry type---
        intput:
                matName(str)-the name of an existing material property
        return:[weightPerV,massPerV,E,v,tempC,G]
                weightPerV-The weight per unit volume for the material. [F/L3]
                massPerV-The mass per unit volume for the material. [M/L3]
                E-The modulus of elasticity. [F/L2]
                v-Poisson’s ratio.
                tempC-The thermal coefficient. [1/T]
                G-The shear modulus. For isotropic materials this value is program calculated
                    from the modulus of elasticity and poisson’s ratio. [F/L2]
        """
        weightAndMass=self.__Model.PropMaterial.GetWeightAndMass(matName)[1:]
        isoProperty=self.__Model.PropMaterial.GetMPIsotropic(matName)[1:]
        weightPerV,massPerV=weightAndMass
        E,v,tempC,G=isoProperty
        returnMatPro=[weightPerV,massPerV,E,v,tempC,G]
        return returnMatPro

    def SetMatrial(self,matName,matType):
        """
        ---This function initializes a material property.---
        inputs:
                matName(str)-The name of an existing or new material property
                matType(int)-This is one of the following items in the eMatType enumeration
                eMatType_Steel = 1,eMatType_Concrete = 2,eMatType_NoDesign = 3
                eMatType_Aluminum = 4,eMatType_ColdFormed = 5,eMatType_Rebar = 6,eMatType_Tendon = 7
        """
        self.__Model.PropMaterial.SetMaterial(matName,matType)

    def SetWeightAndMass(self,matName,weightPerV):
        """
        ---This function assigns weight per unit volume to a material property---
        inputs:
                matName(str)-The name of an existing material property.
                weightPerV(float)-This is the weight per unit volume,[F/L3]
        """
        # 1 = Weight per unit volume is specified,2 = Mass per unit volume is specified
        self.__Model.PropMaterial.SetWeightAndMass(matName, 1,weightPerV)

    def SetMPIsotropic(self,matName,E,v,temC):
        """
        ---set the the mechanical properties for a material with an isotropic directional symmetry type---
        inputs: [matName,matType,weightPerV,massPerV,E,v,tempC,G]
                matName(str)-the name of the defined material
                E(float)-The modulus of elasticity. [F/L2]
                v(float)-Poisson’s ratio.
                tempC(float)-The thermal coefficient. [1/T]
        """
        self.__Model.PropMaterial.SetMPIsotropic(matName,E,v,temC)

    def SetOSteel_1(self,matName,Fy,Fu,eFy,eFu,SSType,SSHysType=0,StrainAtHardening=0,
                                    StrainAtMaxStress=0,StrainAtRupture=0,FinalSlope=0):
        """
        ---This function sets the other material property data for steel materials---
        inputs:
                matName(str)-The name of an existing steel material property.
                Fy(flouat)-The minimum yield stress. [F/L2]
                Fu(float)-The minimum tensile stress. [F/L2]
                eFy(float)-The expected yield stress. [F/L2]
                eFu(float)-The expected tensile stress. [F/L2]
                SSType(int)-This is 0 or 1, indicating the stress-strain curve type.
                            0 = User defined,1 = Parametric - Simple
                SSHysType(int)-This is 0, 1 or 2, indicating the stress-strain hysteresis type.
                            0 = Elastic,1 = Kinematic,2 = Takeda
                StrainAtHardening(float)-This item applies only to parametric stress-strain curves.
                            It is the strain at the onset of strain hardening.
                StrainAtMaxStress(float)-This item applies only to parametric stress-strain curves.
                            It is the strain at maximum stress. This item must be larger than the
                            StrainAtHardening item.
                StrainAtRupture(float)-This item applies only to parametric stress-strain curves.
                            It is the strain at rupture. This item must be larger than the StrainAtMaxStress item
                FinalSlope(float)-This item applies only to parametric stress-strain curves. It is a multiplier on
                            the material modulus of elasticity, E. This value multiplied times E gives the final
                            slope of the curve.
        """
        self.__Model.PropMaterial.SetOSteel_1(matName, Fy,Fu,eFy,eFu,SSType,SSHysType,StrainAtHardening,
                                    StrainAtMaxStress,StrainAtRupture,FinalSlope)

    def SetOConcrete_1(self,matName,fc,IsLightweight,fcsfactor,SSType,SSHysType=0,StrainAtfc=0,
                                        StrainUltimate=0,FinalSlope=0,FrictionAngle=0,DilatationalAngle=0):
        """
        ---This function sets the other material property data for concrete materials.---
        inputs:
        matName(str)-The name of an existing concrete material property.
        fc(float)-The concrete compressive strength. [F/L2]
        IsLightweight(bool)-If this item is True, the concrete is assumed to be lightweight concrete.
        fcsfactor(float)-The shear strength reduction factor for lightweight concrete.
        SSType(int)-This is 0, 1 or 2, indicating the stress-strain curve type. 0 = User defined,
            1 = Parametric - Simple,2 = Parametric - Mander
        SSHysType(int)-This is 0, 1 or 2, indicating the stress-strain hysteresis type.0 = Elastic
            1 = Kinematic,2 = Takeda
        StrainAtfc(float)-This item applies only to parametric stress-strain curves. It is the strain at
            the unconfined compressive strength.
        StrainUltimate(float)-This item applies only to parametric stress-strain curves. It is the ultimate
            unconfined strain capacity. This item must be larger than the StrainAtfc item
        FinalSlope(float)-This item applies only to parametric stress-strain curves. It is a multiplier on
            the material modulus of elasticity, E. This value multiplied times E gives the final slope on the
            compression side of the curve.
        FrictionAngle(float)-The Drucker-Prager friction angle, 0 <= FrictionAngle < 90. [deg]
        DilatationalAngle(float)-The Drucker-Prager dilatational angle, 0 <= DilatationalAngle < 90. [deg]
        """
        self.__Model.PropMaterial.SetOConcrete_1(matName,fc,IsLightweight,fcsfactor,SSType,SSHysType,StrainAtfc,
                                        StrainUltimate,FinalSlope,FrictionAngle,DilatationalAngle)

    def SetORebar_1(self,matName,Fy,Fu,eFy,eFu,SSType,SSHysType=0,StrainAtHardening=0,
                                    StrainUltimate=0,FinalSlope=0,UseCaltransSSDefaults=False):
        """
        ---This function sets the other material property data for rebar materials..---
        inputs:
        matName(str)-The name of an existing rebar material property.
        Fy(float)-The minimum yield stress. [F/L2]
        Fu(float)-The minimum tensile stress. [F/L2]
        eFy(float)_The expected yield stress. [F/L2]
        eFu(float)-The expected tensile stress. [F/L2]
        SSType(int)-This is 0, 1 or 2, indicating the stress-strain curve type.0 = User defined
            1 = Parametric - Simple,2 = Parametric - Park
        SSHysType(int)-This is 0, 1 or 2, indicating the stress-strain hysteresis type.0 = Elastic
            1 = Kinematic,2 = Takeda
        StrainAtHardening(float)-This item applies only when parametric stress-strain curves are used and
            when UseCaltransSSDefaults is False. It is the strain at the onset of strain hardening
        StrainUltimate(float)-This item applies only when parametric stress-strain curves are used and when
            UseCaltransSSDefaults is False. It is the ultimate strain capacity. This item must be larger than the
            StrainAtHardening item.
        FinalSlope(float)-This item applies only to parametric stress-strain curves. It is a multiplier on the
            material modulus of elasticity, E. This value multiplied times E gives the final slope of the curve.
        UseCaltransSSDefaults(bool)-If this item is True, the program uses Caltrans default controlling strain
            values, which are bar size dependent.
        """
        self.__Model.PropMaterial.SetORebar_1(matName,Fy,Fu,eFy,eFu,SSType,SSHysType,StrainAtHardening,
                                    StrainUltimate,FinalSlope,UseCaltransSSDefaults)

    def SetOTendon_1(self,matName,Fy,Fu,SSType,SSHysType=1,FinalSlope=1):
        """
        ---This function sets the other material property data for tendon materials---
        inputs:
        matName(str)-The name of an existing tendon material property.
        Fy(float)-The minimum yield stress. [F/L2]
        Fu(float)-The minimum tensile stress. [F/L2]
        SSType(int)-This is 0, 1 or 2, indicating the stress-strain curve type.0 = User defined
            1 = Parametric – 250 ksi strand,2 = Parametric – 270 ksi strand
        SSHysType(int)-This is 0, 1 or 2, indicating the stress-strain hysteresis type.0 = Elastic
            1 = Kinematic,2 = Takeda
        FinalSlope(float)-This item applies only to parametric stress-strain curves. It is a multiplier
            on the material modulus of elasticity, E. This value multiplied times E gives the final slope of the curve.
        """
        self.__Model.PropMaterial.SetOTendon_1(matName,Fy,Fu,SSType,SSHysType,FinalSlope)

    def PropLink_SetMultiLinearPlastic(self,name,DOF,Fixed,Nonlinear,Ke={},Ce={},dj2=0,dj3=0):
        """
        ---This function initializes a multilinear plastic-type link property. If this function is
        called for an existing link property, all items for the property are reset to their default values.---
        inputs:
        name(str)-The name of an existing or new link property. If this is an existing property,
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
        self.__Model.PropLink.SetMultiLinearPlastic(name,DOFFinal,FixedFinal,nonlinearFinal,keInput,ceInput,dj2,dj3)
