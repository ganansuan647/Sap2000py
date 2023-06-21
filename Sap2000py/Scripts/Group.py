
class SapGroup:
    def __init__(self,Sapobj):
        """
        Choose cases to run and Analyze model
        """
        self.__Object = Sapobj._Object
        self.__Model = Sapobj._Model
        self._Sapobj = Sapobj

    def GetGroupNames(self):
        """
        Get group names,return NameList.
        """
        NumberNames, NameList,ret = self.__Model.GroupDef.GetNameList()
        return NameList
    
    def Select(self,GroupName):
        """
        Select group by GroupName
        input:
            GroupName(str/list):group name
        """
        # Change type to list
        if type(GroupName)==str:
            GroupName = [GroupName]

        nonameflag = False
        for Name in GroupName:
            if Name not in self.GetGroupNames():
                print('GroupName "{}"dosen\'t exist!'.format(Name))
                nonameflag = True
            else:
                self.__Model.SelectObj.Group(GroupName)

        if nonameflag:
            print('You have entered the wrong GroupName, please check in the Caselist below:')
            print(self.GetGroupNames())

    def GetElements(self,GroupName:str):
        """
        Get elements in group
        input:
            GroupName(str|list):group name
        output:
        ElementList(dict):
            element id : type(Point:1,Frame:2,Cable:3,
                        Tendon:4,Area:5,Solid:6,Link:7)
        Warning: It should be noted that dict can only pair one value to one key,
                So please makesure Your Group don't have two elements with 
                different type but the same id!!
        """
        # Change type to list
        if type(GroupName)==str:
            GroupName = [GroupName]
        nonameflag = False
        ElementList = {}
        for Name in GroupName:
            if Name not in self.GetGroupNames():
                print('GroupName "{}"dosen\'t exist!'.format(Name))
                nonameflag = True
            else:
                NumberElements,typelist,elementList,ret = self.__Model.GroupDef.GetAssignments(Name)
                # Change typelist to typestr_list
                typestr_list = []
                for types in typelist:
                    typestr = self._Sapobj.Scripts.lookup(self._Sapobj.ObjDict,types)
                    typestr_list.append(typestr)
                ElementList.update(dict(zip(elementList,typestr_list)))

        if nonameflag:
            print('You have entered the wrong GroupName, please check in the Caselist below:')
            print(self.GetGroupNames())
        return ElementList

    def AddtoGroup(self,GroupName:str,idlist,typeStr:str):
        """
        Add elements to group
        input:
            GroupName(str):group name
            idlist(list):element id list
            typeStr(str):{'Point':1,'Frame':2,'Cable':3,
                        'Tendon':4,'Area':5,'Solid':6,'Link':7}
        """
        Objstr = typeStr+'Obj'
        SapModel = self.__Model

        # check if this group exists
        allgroups = self.GetGroupNames()
        if GroupName not in allgroups:
            SapModel.GroupDef.SetGroup(GroupName)

        # Change type to list
        if type(idlist)==str:
            idlist = [idlist]

        for id in idlist:
            eval('SapModel.{}.SetGroupAssign(id, GroupName)'.format(Objstr))

    def RemovefromGroup(self,GroupName:str,dellist,typeStr:str):
        """
        Remove elements from group
        input:
            GroupName(str):group name
            dellist(list):element id list to be deleted
            typeStr(str):{'Point':1,'Frame':2,'Cable':3,
                        'Tendon':4,'Area':5,'Solid':6,'Link':7}
        """
        Objstr = typeStr+'Obj'
        # Delete from existing elements
        EleList = self.GetElements(GroupName)
        for id2del in dellist:
            if id2del in EleList:
                if EleList[id2del] == typeStr:
                    del EleList[id2del]
                else:
                    print('The element {} is not {}!'.format(id2del,typeStr))
            else:
                print('The element {} is not in group {}!'.format(id2del,GroupName))
        
        # clear current group
        self.__Model.GroupDef.Clear(GroupName)

        # create the group again
        for ele in EleList.keys():
            typestr = EleList[ele]
            self.AddtoGroup(GroupName,ele,typestr)

        