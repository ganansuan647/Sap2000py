import os
class CommonMaterialSet_China:
    def __init__(self,Sapobj,standard):
        """
        Add Common Material Set for China with your desired standard,
        for China it includes ["GB","JTG","TB","User"]
        """
        self.__Object = Sapobj._Object
        self.__Model = Sapobj._Model
        if standard !=  "User":
            print('Adding Chinese '+standard +' Materials...')
            # Add commonly used materials
            Steel = 1
            Concrete = 2
            Rebar = 6
            Tendon = 7
            # Delete initial materials in Sap2000
            Sapobj._Model.PropMaterial.Delete("A992Fy50")
            Sapobj._Model.PropMaterial.Delete("4000Psi") # this one can't be erased
            Sapobj._Model.PropMaterial.Delete("A416Gr270")
            # Steel
            if standard == "GB":
                # GB Steel
                Sapobj.Define.material.AddMaterial("Q235",Steel,"China","GB","Q235")
                Sapobj.Define.material.AddMaterial("Q345",Steel,"China","GB","Q345")
                Sapobj.Define.material.AddMaterial("Q390",Steel,"China","GB","Q390")
                Sapobj.Define.material.AddMaterial("Q420",Steel,"China","GB","Q420")
                Sapobj.Define.material.AddMaterial("Q460",Steel,"China","GB","Q460")
            elif standard == "JTG" or "TB":
                # JTG/T Steel
                Sapobj.Define.material.AddMaterial("Q235q",Steel,"China","JTG","GB/T 714-2008 Q235q")
                Sapobj.Define.material.AddMaterial("Q345q",Steel,"China","JTG","GB/T 714-2008 Q345q")
                Sapobj.Define.material.AddMaterial("Q370q",Steel,"China","JTG","GB/T 714-2008 Q370q")
                Sapobj.Define.material.AddMaterial("Q420q",Steel,"China","JTG","GB/T 714-2008 Q420q")
                Sapobj.Define.material.AddMaterial("Q460q",Steel,"China","JTG","GB/T 714-2008 Q460q")
                Sapobj.Define.material.AddMaterial("Q500q",Steel,"China","JTG","GB/T 714-2008 Q500q")
                Sapobj.Define.material.AddMaterial("Q550q",Steel,"China","JTG","GB/T 714-2008 Q550q")
                Sapobj.Define.material.AddMaterial("Q620q",Steel,"China","JTG","GB/T 714-2008 Q620q")
                Sapobj.Define.material.AddMaterial("Q690q",Steel,"China","JTG","GB/T 714-2008 Q690q")

            # Concrete
            if standard == "GB":
                # GB Concrete
                Sapobj.Define.material.AddMaterial("C30",Concrete,"China","GB","GB 50010 C30")
                Sapobj.Define.material.AddMaterial("C35",Concrete,"China","GB","GB 50010 C35")
                Sapobj.Define.material.AddMaterial("C40",Concrete,"China","GB","GB 50010 C40")
                Sapobj.Define.material.AddMaterial("C45",Concrete,"China","GB","GB 50010 C45")
                Sapobj.Define.material.AddMaterial("C50",Concrete,"China","GB","GB 50010 C50")
                Sapobj.Define.material.AddMaterial("C55",Concrete,"China","GB","GB 50010 C55")
                Sapobj.Define.material.AddMaterial("C60",Concrete,"China","GB","GB 50010 C60")
            elif standard == "JTG":
                # JTG Concrete
                Sapobj.Define.material.AddMaterial("C30",Concrete,"China","JTG","JTG D62-2004 C30")
                Sapobj.Define.material.AddMaterial("C35",Concrete,"China","JTG","JTG D62-2004 C35")
                Sapobj.Define.material.AddMaterial("C40",Concrete,"China","JTG","JTG D62-2004 C40")
                Sapobj.Define.material.AddMaterial("C45",Concrete,"China","JTG","JTG D62-2004 C45")
                Sapobj.Define.material.AddMaterial("C50",Concrete,"China","JTG","JTG D62-2004 C50")
                Sapobj.Define.material.AddMaterial("C55",Concrete,"China","JTG","JTG D62-2004 C55")
                Sapobj.Define.material.AddMaterial("C60",Concrete,"China","JTG","JTG D62-2004 C60")
            elif standard == "TB":
                # TB Concrete
                Sapobj.Define.material.AddMaterial("C30",Concrete,"China","TB","TB10002.3 C30")
                Sapobj.Define.material.AddMaterial("C35",Concrete,"China","TB","TB10002.3 C35")
                Sapobj.Define.material.AddMaterial("C40",Concrete,"China","TB","TB10002.3 C40")
                Sapobj.Define.material.AddMaterial("C45",Concrete,"China","TB","TB10002.3 C45")
                Sapobj.Define.material.AddMaterial("C50",Concrete,"China","TB","TB10002.3 C50")
                Sapobj.Define.material.AddMaterial("C55",Concrete,"China","TB","TB10002.3 C55")
                Sapobj.Define.material.AddMaterial("C60",Concrete,"China","TB","TB10002.3 C60")
            # Rebar
            if standard == "GB":
                # GB Rebar
                Sapobj.Define.material.AddMaterial("HPB300",Rebar,"China","GB","GB50010 HPB300")
                Sapobj.Define.material.AddMaterial("HPB335",Rebar,"China","GB","GB50010 HPB335")
                Sapobj.Define.material.AddMaterial("HPB400",Rebar,"China","GB","GB50010 HPB400")
                Sapobj.Define.material.AddMaterial("HPB500",Rebar,"China","GB","GB50010 HPB500")
            elif standard == "JTG":
                # JTG Rebar
                Sapobj.Define.material.AddMaterial("HRB335",Rebar,"China","JTG","JTG D62-2004 HRB335")
                Sapobj.Define.material.AddMaterial("HRB400",Rebar,"China","JTG","JTG D62-2004 HRB400")
            elif standard == "TB":
                # TB Rebar
                Sapobj.Define.material.AddMaterial("Q235",Rebar,"China","JTG","TB Q235")
                Sapobj.Define.material.AddMaterial("HRB335",Rebar,"China","JTG","TB HRB335")
                Sapobj.Define.material.AddMaterial("PSB830",Rebar,"China","JTG","TB PSB830")

            # Tendon
            if standard == "JTG":
                # JTG Tendon
                Sapobj.Define.material.AddMaterial("fpk1470",Tendon,"China","JTG","JTGD62 fpk1470")
                Sapobj.Define.material.AddMaterial("fpk1570",Tendon,"China","JTG","JTGD62 fpk1570")
                Sapobj.Define.material.AddMaterial("fpk1720",Tendon,"China","JTG","JTGD62 fpk1720")
                Sapobj.Define.material.AddMaterial("fpk1860",Tendon,"China","JTG","JTGD62 fpk1860")
            elif standard == "TB":
                # TB Tendon
                Sapobj.Define.material.AddMaterial("fpk1470",Tendon,"China","TB","TB fpk1470")
                Sapobj.Define.material.AddMaterial("fpk1570",Tendon,"China","TB","TB fpk1570")
                Sapobj.Define.material.AddMaterial("fpk1670",Tendon,"China","TB","TB fpk1670")
                Sapobj.Define.material.AddMaterial("fpk1720",Tendon,"China","TB","TB fpk1720")
                Sapobj.Define.material.AddMaterial("fpk1770",Tendon,"China","TB","TB fpk1770")
                Sapobj.Define.material.AddMaterial("fpk1860",Tendon,"China","TB","TB fpk1860")
                Sapobj.Define.material.AddMaterial("fpk1960",Tendon,"China","TB","TB fpk1960")
            
            print(standard +' Material Set Added!')
            # get material names
            MaterialList = Sapobj.MaterialList
            print(len(MaterialList),' Materials are Defined:\n',MaterialList)
            print('Edit '+__file__+' to modify the materials you need!')
            print('Material names are stored in Saproject().MaterialList')
        # User defined
        if standard == "User":
            # define your materials here
            pass

            # print materials you defined
            print('User defined Material Set Added!')
            # get material names
            MaterialList = Sapobj.MaterialList
            print(len(MaterialList),' Materials are Defined:\n',MaterialList)
            print('Edit '+__file__+' to modify the materials you need!')
            print('Material names are stored in Saproject().MaterialList')