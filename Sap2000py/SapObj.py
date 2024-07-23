
class SapPointObj_Get:
    def __init__(self, Sapobj):
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def CommonTo(self,name:str)->int:
        """
        ---This function returns the total number of objects (line, area, solid and link) that connect to the
        specified point object.---
        inputs:
        name(str)-The name of a point object or a group depending on the value selected for ItemType item.
        return:
        [numberItem,CommonTo]
        CommonTo(int)-The total number of objects (line, area, solid and link) that connect to the specified point object.
        """
        numbers=self.__Model.PointObj.GetCommonTo(name)
        return numbers

    def Connectivity(self,name:str)->list:
        """
        ---This function returns a list of objects connected to a specified point object---
        inputs:
        name(str)-The name of an existing point object.
        return:list
        [numberItem,totalObject,objectTypeList,objectNameList,_]

        """
        results=self.__Model.PointObj.GetConnectivity(name)
        return results

    def Constraint(self,name:str):
        """
        ---This function returns a list of constraint assignments made to one or more specified point objects.---
        inputs:
        name(str)-The name of an existing point object or group, depending on the value of the ItemType item.
        return:
        [numberItem,totalNumConstrait,pointNameturple,constraintNameTurple]
        """
        result=self.__Model.PointObj.GetConstraint(name)
        return result

    def CoordCartesian(self,name:str,Csys="Global"):
        """
        --- If successful, the function returns the x, y and z coordinates of the specified point object in the
        Present Units. The coordinates are reported in the coordinate system specified by Csys.---
        inputs:
        name(str)-The name of a defined point object.
        Csys(str)-The name of a defined coordinate system. If Csys is not specified, the Global coordinate s
            ystem is assumed.
        return:
        x,y,z(float)-The X,Y,Z-coordinate of the specified point object in the specified coordinate system. [L]
        [numItem,x,y,z]
        """
        x,y,z=0.0,0.0,0.0
        result=self.__Model.PointObj.GetCoordCartesian(name,x,y,z,Csys)
        return result

    def CoordCylindrical(self,name:str,Csys="Global"):
        """
        ---If successful, the function returns the r, theta and z coordinates of the specified point object in
        the Present Units. The coordinates are reported in the coordinate system specified by CSys.---
        inputs:
        name(str)-The name of a defined point object.
        Csys(str)-The name of a defined coordinate system. If Csys is not specified, the Global coordinate s
            ystem is assumed.
        return:
        [numItem,r,theta,z]
        r(float)-The radius for the specified point object in the specified coordinate system. [L]
        Theta(float)-The angle for the specified point object in the specified coordinate system. The angle is
            measured in the XY plane from the positive X axis. When looking in the XY plane with the positive
            Z axis pointing toward you, a positive Theta angle is counter clockwise [deg]
        z(float)-The Z-coordinate of the specified point object in the specified coordinate system. [L]
        """
        r,theta,z=0,0,0
        result=self.__Model.PointObj.GetCoordCylindrical(name,r,theta,z,Csys)
        return result

    def CoordSpherical(self,name:str,Csys="Global"):
        """
        ---If successful, the function returns the r, a and b coordinates of the specified point object in the
        Present Units. The coordinates are reported in the coordinate system specified by CSys.---
        inputs:
        name(str)-The name of an existing point object.
        Csys(str)-The name of a defined coordinate system. If Csys is not specified, the Global coordinate s
            ystem is assumed.
        return:
        [numItem,r,a,b]
        r(float)-The radius for the point object in the specified coordinate system. [L]
        a(float)-The plan angle for the point object in the specified coordinate system. This angle is measured
            in the XY plane from the positive global X axis. When looking in the XY plane with the positive Z axis
            pointing toward you, a positive a angle is counter clockwise. [deg]
        b(float)-The elevation angle for the point object in the specified coordinate system. This angle is measured
            in an X'Z plane that is perpendicular to the XY plane with the positive X' axis oriented at angle a from
            the positive global X axis. Angle b is measured from the positive global Z axis. When looking in the X’Z
            plane with the positive Y' axis pointing toward you, a positive b angle is counter clockwise. [deg]
        """
        r,a,b=0,0,0
        result =self.__Model.PointObj.GetCoordSpherical(name,r,a,b,Csys)
        return result

    def GroupAssign(self,name:str):
        """
        ---This function retrieves the names of the groups to which a specified point object is assigned---
        inputs:
        name(str)-The name of an existing point object.
        return:
        [numberItem,numberGroups,Groups]
        NumberGroups(int)-The number of group names retrieved.
        Groups(str)-The names of the groups to which the point object is assigned.
        """
        result=self.__Model.PointObj.GetGroupAssign(name)
        return result

    def LoadDispl(self,name:str,ItemType=0):
        """
        ---This function retrieves the ground displacement load assignments to point objects---
        inputs:
        name(str)-The name of an existing point object or group, depending on the value of the ItemType item.
        ItemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0
            Group = 1
            SelectedObjects = 2
            If this item is Object, the load assignments are retrieved for the point object specified by the Name item.
            If this item is Group, the assignments are retrieved for all point objects in the group specified by the
            Name item.
            If this item is SelectedObjects, the load assignments are retrieved for all selected point objects,
            and the Name item is ignored.
        return:
        [numberItem,NumberItems, PointName, LoadPat, LCStep, CSys, U1, U2, U3, R1, R2, R3]
        NumberItems(int)-This is the total number of joint ground displacement assignments returned.
        PointName(str list)-This is an array that includes the name of the point object to which the specified ground
            displacement assignment applies
        LoadPat(str list)-This is an array that includes the name of the load pattern for the ground displacement load
        LCStep(int list)-This is an array that includes the load pattern step for the ground displacement load. In most
            cases, this item does not apply and will be returned as 0
        CSys(str list)-This is an array that includes the name of the coordinate system for the ground displacement
            load. This is Local or the name of a defined coordinate system
        U1(float list)-This is an array that includes the assigned translational ground displacement in the local
            1-axis or coordinate system X-axis direction, depending on the specified CSys. [L]
        U2(float list)-This is an array that includes the assigned translational ground displacement in the local
            2-axis or coordinate system Y-axis direction, depending on the specified CSys. [L]
        U3(float list)-This is an array that includes the assigned translational ground displacement in the local
            3-axis or coordinate system Y-axis direction, depending on the specified CSys. [L]
        R1(float list)-This is an array that includes the assigned rotational ground displacement about the local
            1-axis or coordinate system X-axis, depending on the specified CSys. [rad]
        R2(float list)-This is an array that includes the assigned rotational ground displacement about the local
            2-axis or coordinate system X-axis, depending on the specified CSys. [rad]
        R3(float list)-This is an array that includes the assigned rotational ground displacement about the local
            3-axis or coordinate system X-axis, depending on the specified CSys. [rad]
        """
        NumberItems=0
        PointName=[]
        LoadPat=[]
        LCStep=[]
        CSys=[]
        U1,U2,U3,R1,R2,R3=[],[],[],[],[],[]

        result=self.__Model.PointObj.GetLoadDispl(name,NumberItems, PointName, LoadPat, LCStep, CSys,
                                                   U1, U2, U3, R1, R2, R3,ItemType)
        return result

    def LocalAxes(self,name:str):
        """
        ---This function retrieves the local axes angles for a point object.---
        inputs:
        name(str)-The name of an existing point object
        return:
        [numberItem,a,b,c,Advanced]
        a,b,c(float)-The local axes of the point are defined by first setting the positive local 1, 2 and 3 axes
            the same as the positive global X, Y and Z axes and then doing the following: [deg]
            1. Rotate about the 3 axis by angle a.
            2. Rotate about the resulting 2 axis by angle b.
            3. Rotate about the resulting 1 axis by angle c.
        Advanced(bool)-This item is True if the point object local axes orientation was obtained using advanced local
            axes parameters.
        """
        result=self.__Model.PointObj.GetLocalAxes(name)
        return result

    def Mass(self,name:str):
        """
        ---This function retrieves the point mass assignment values for a point object. The masses are always
        returned in the point local coordinate system.---
        inputs:
        name(str)-The name of an existing point object
        return:
        m(float list)-This is a foat list of six mass assignment values.
            Value(0) = U1 [M]
            Value(1) = U2 [M]
            Value(2) = U3 [M]
            Value(3) = R1 [ML2]
            Value(4) = R2 [ML2]
            Value(5) = R3 [ML2]
        """
        result=self.__Model.PointObj.GetMass(name)
        return result

    def NameList(self):
        """
        ---This function retrieves the names of all defined point objects---
        return:
        []
        NumberNames(int)-The number of point object names retrieved by the program.
        MyName(str list)-This is a one-dimensional list of point object names.
        """
        result=self.__Model.PointObj.GetNameList()
        return result

    def Restraint(self,name:str):
        """
        ---This function retrieves the restraint assignments for a point object. The restraint assignments
        are always returned in the point local coordinate system.---
        inputs:
        name(str)-The name of an existing point object.
        return:
        value
        """
        result=self.__Model.PointObj.GetRestraint(name)
        return result

    def Spring(self,name:str):
        """
        ---This function retrieves uncoupled spring stiffness assignments for a point object, that is,
        it retrieves the diagonal terms in the 6x6 spring matrix for the point object---
        inputs:
        name(str)-The name of an existing point object.
        return:
        [numberItem,k]
        k(float list)-This is a float list of six spring stiffness values.Value(0) = U1 [F/L],Value(1) = U2 [F/L],
            Value(2) = U3 [F/L],Value(3) = R1 [FL/rad],Value(4) = R2 [FL/rad],Value(5) = R3 [FL/rad]
        """
        k=[0,0,0,0,0,0]
        result=self.__Model.PointObj.GetSpring(name,k)
        return result

    def SpringCoupled(self,name:str):
        """
        ---This function retrieves coupled spring stiffness assignments for a point object.The spring stiffnesses
        reported are the sum of all springs assigned to the point object. The spring stiffness values are reported
        in the point local coordinate system.---
        input:
        name(str)-The name of an existing point object.
        return:

        k(float list)-This is an array of twenty one spring stiffness values.
            Value(0) = U1U1 [F/L]
            Value(1) = U1U2 [F/L]
            Value(2) = U2U2 [F/L]
            Value(3) = U1U3 [F/L]
            Value(4) = U2U3 [F/L]
            Value(5) = U3U3 [F/L]
            Value(6) = U1R1 [F/rad]
            Value(7) = U2R1 [F/rad]
            Value(8) = U3R1 [F/rad]
            Value(9) = R1R1 [FL/rad]
            Value(10) = U1R2 [F/rad]
            Value(11) = U2R2 [F/rad]
            Value(12) = U3R2 [F/rad]
            Value(13) = R1R2 [FL/rad]
            Value(14) = R2R2 [FL/rad]
            Value(15) = U1R3 [F/rad]
            Value(16) = U2R3 [F/rad]
            Value(17) = U3R3 [F/rad]
            Value(18) = R1R3 [FL/rad]
            Value(19) = R2R3 [FL/rad]
            Value(20) = R3R3 [FL/rad]
        """
        k=[0 for each in range(21)]
        result=self.__Model.PointObj.GetSpringCoupled(name,k)
        return result

class SapPointObj_Set:
    def __init__(self,Sapobj):
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model
        
    def Constraint(self,name:str,ConstraintName,ItemType=0,Replace=True):
        """
        ---This function makes joint constraint assignments to point objects.---
        inputs:
        name(str)-The name of an existing point object or group depending on the value of the ItemType item.
        ConstraintName(str)-The name of an existing joint constraint.
        ItemType(int)-This is one of the following items in the eItemType enumeration:Object = 0,Group = 1,
            SelectedObjects = 2,If this item is Object, the constraint assignment is made to the point object
            specified by the Name item.If this item is Group,  the constraint assignment is made to all point
            objects in the group specified by the Name item.If this item is SelectedObjects, the constraint
            assignment is made to all selected point objects and the Name item is ignored.
        Replace(bool)-If this item is True, all previous joint constraints, if any, assigned to the specified
            point object(s) are deleted before making the new assignment.
        """
        self.__Model.PointObj.SetConstraint(name,ConstraintName)

    def GroupAssign(self,name:str,GroupName,Remove=False,ItemType=0):
        """
        ---This function adds or removes point objects from a specified group.---
        inputs:
        name(str)-The name of an existing point object or group depending on the value of the ItemType item.
        GroupName(str)-The name of an existing group to which the assignment is made.
        Remove(bool)-If this item is False, the specified point objects are added to the group specified by the
            GroupName item. If it is True, the point objects are removed from the group.
        ItemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0
            Group = 1
            SelectedObjects = 2
            If this item is Object, the point object specified by the Name item is added or removed from the group
            specified by the GroupName item.If this item is Group, all point objects in the group specified by the
            Name item are added or removed from the group specified by the GroupName item.If this item is
            SelectedObjects, all selected point objects are added or removed from the group specified by the
            GroupName item and the Name item is ignored.
        """
        self.__Model.PointObj.SetGroupAssign(name,GroupName,Remove,ItemType)

    def LoadDispl(self,name:str,LoadPat,Value,Replace=False,CSys="Global",ItemType=0):
        """
        ---This function makes ground displacement load assignments to point objects.---
        inputs:
        name(str)-The name of an existing point object or group depending on the value of the ItemType item.
        LoadPat(str)-The name of the load pattern for the ground displacement load.
        Value(float list)-This is an array of six ground displacement load values.
            Value(0) = U1 [L]
            Value(1) = U2 [L]
            Value(2) = U3 [L]
            Value(3) = R1 [rad]
            Value(4) = R2 [rad]
            Value(5) = R3 [rad]
        Replace(bool)-If this item is True, all previous ground displacement loads, if any, assigned to the specified
            point object(s) in the specified load pattern are deleted before making the new assignment.
        CSys(str)-The name of the coordinate system for the considered ground displacement load. This is Local or
            the name of a defined coordinate system.
        ItemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0
            Group = 1
            SelectedObjects = 2
            If this item is Object, the load assignment is made to the point object specified by the Name item.
            If this item is Group, the load assignment is made to all point objects in the group specified by the Name item.
            If this item is SelectedObjects, the load assignment is made to all selected point objects and the Name
            item is ignored.
        """
        self.__Model.PointObj.SetLoadDispl(name,LoadPat,Value,Replace,CSys,ItemType)

    def LoadForce(self,name:str,loadPat,value,Replace=False,CSys="Global",ItemType=0):
        """
        ---This function makes point load assignments to point objects.---
        inputs:
        name(str)-The name of an existing point object or group depending on the value of the ItemType item.
        loadPat(str)-The name of the load pattern for the point load.
        value(float list)-This is an array of six point load values.
            Value(0) = F1 [F]
            Value(1) = F2 [F]
            Value(2) = F3 [F]
            Value(3) = M1 [FL]
            Value(4) = M2 [FL]
            Value(5) = M3 [FL]
        Replace(bool)-If this item is True, all previous ground displacement loads, if any, assigned to the specified
            point object(s) in the specified load pattern are deleted before making the new assignment.
        CSys(str)-The name of the coordinate system for the considered ground displacement load. This is Local or
            the name of a defined coordinate system.
        ItemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0
            Group = 1
            SelectedObjects = 2
            If this item is Object, the load assignment is made to the point object specified by the Name item.
            If this item is Group, the load assignment is made to all point objects in the group specified by the Name item.
            If this item is SelectedObjects, the load assignment is made to all selected point objects and the Name
            item is ignored.
        """
        self.__Model.PointObj.SetLoadForce(name,loadPat,value,Replace,CSys,ItemType)

    def LocalAxes(self,name:str,a,b,c,itemType=0):
        """
        ---This function sets the local axes angles for point objects.---
        inputs:
        name(str)-The name of an existing point object or group depending on the value of the ItemType item.
        a,b,c(float)-The local axes of the point are defined by first setting the positive local 1, 2 and 3 axes
            the same as the positive global X, Y and Z axes and then doing the following: [deg]
            1. Rotate about the 3 axis by angle a.
            2. Rotate about the resulting 2 axis by angle b.
            3. Rotate about the resulting 1 axis by angle c.
        ItemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0
            Group = 1
            SelectedObjects = 2
            If this item is Object, the load assignment is made to the point object specified by the Name item.
            If this item is Group, the load assignment is made to all point objects in the group specified by the Name item.
            If this item is SelectedObjects, the load assignment is made to all selected point objects and the Name
            item is ignored.
        """
        self.__Model.PointObj.SetLocalAxes(name,a,b,c,itemType)

    def Mass(self,name:str,m,itemType=0,isLocalCSys=True,Replace=False):
        """
        ---This function assigns point mass to a point object.---
        inputs:
        name(str)-The name of an existing point object or group depending on the value of the ItemType item.
        m(float list)-This is an array of six mass assignment values.
            Value(0) = U1 [M]
            Value(1) = U2 [M]
            Value(2) = U3 [M]
            Value(3) = R1 [ML2]
            Value(4) = R2 [ML2]
            Value(5) = R3 [ML2]
        ItemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0
            Group = 1
            SelectedObjects = 2
            If this item is Object, the load assignment is made to the point object specified by the Name item.
            If this item is Group, the load assignment is made to all point objects in the group specified by the Name item.
            If this item is SelectedObjects, the load assignment is made to all selected point objects and the Name
            item is ignored.
        isLocalCSys(bool)-If this item is True, the specified mass assignments are in the point object local coordinate
            system. If it is False, the assignments are in the Global coordinate system.
        Replace(bool)-If this item is True, all existing point mass assignments to the specified point object(s) are
            deleted prior to making the assignment. If it is False, the mass assignments are added to any existing assignments.
        """
        self.__Model.PointObj.SetMass(name,m,itemType,isLocalCSys,Replace)

    def Restraint(self,name:str,value,itemType=0):
        """
        ---This function assigns the restraint assignments for a point object. The restraint assignments are always
        set in the point local coordinate system.---
        inputs:
        name(str)-The name of an existing point object or group depending on the value of the ItemType item.
        value(bool list)-This is an array of six restraint values.
            Value(0) = U1
            Value(1) = U2
            Value(2) = U3
            Value(3) = R1
            Value(4) = R2
            Value(5) = R3
        ItemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0
            Group = 1
            SelectedObjects = 2
            If this item is Object, the load assignment is made to the point object specified by the Name item.
            If this item is Group, the load assignment is made to all point objects in the group specified by the Name item.
            If this item is SelectedObjects, the load assignment is made to all selected point objects and the Name
            item is ignored.
        """
        self.__Model.PointObj.SetRestraint(name,value,itemType)

    def Spring(self,name:str,k,ItemType=0,IsLocalCSys=False,Replace=False):
        """
        ---This function assigns uncoupled springs to a point object.---
        inputs:
        name(str)-The name of an existing point object or group depending on the value of the ItemType item.
        k(float list)-This is an array of six spring stiffness values.
            Value(0) = U1 [F/L]
            Value(1) = U2 [F/L]
            Value(2) = U3 [F/L]
            Value(3) = R1 [FL/rad]
            Value(4) = R2 [FL/rad]
            Value(5) = R3 [FL/rad]
        ItemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0
            Group = 1
            SelectedObjects = 2
            If this item is Object, the spring assignment is made to the point object specified by the Name item.
            If this item is Group, the spring assignment is made to all point objects in the group specified by the Name item.
            If this item is SelectedObjects, the spring assignment is made to all selected point objects and the Name
            item is ignored.
        IsLocalCSys(bool)-If this item is True, the specified spring assignments are in the point object local
            coordinate system. If it is False, the assignments are in the Global coordinate system.
        Replace(bool)-If this item is True, all existing point spring assignments to the specified point object(s)
            are deleted prior to making the assignment. If it is False, the spring assignments are added to any
            existing assignments.
        """
        self.__Model.PointObj.SetSpring(name,k,ItemType,IsLocalCSys,Replace)

    def SpringCoupled(self,name:str,k,ItemType=0,IsLocalCSys=False,Replace=False):
        """
        ---This function assigns coupled springs to a point object---
        inputs:
        name(str)-The name of an existing point object or group depending on the value of the ItemType item.
        k(float list)-This is an array of twenty one spring stiffness values.
            Value(0) = U1U1 [F/L]
            Value(1) = U1U2 [F/L]
            Value(2) = U2U2 [F/L]
            Value(3) = U1U3 [F/L]
            Value(4) = U2U3 [F/L]
            Value(5) = U3U3 [F/L]
            Value(6) = U1R1 [F/rad]
            Value(7) = U2R1 [F/rad]
            Value(8) = U3R1 [F/rad]
            Value(9) = R1R1 [FL/rad]
            Value(10) = U1R2 [F/rad]
            Value(11) = U2R2 [F/rad]
            Value(12) = U3R2 [F/rad]
            Value(13) = R1R2 [FL/rad]
            Value(14) = R2R2 [FL/rad]
            Value(15) = U1R3 [F/rad]
            Value(16) = U2R3 [F/rad]
            Value(17) = U3R3 [F/rad]
            Value(18) = R1R3 [FL/rad]
            Value(19) = R2R3 [FL/rad]
            Value(20) = R3R3 [FL/rad]
        ItemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0
            Group = 1
            SelectedObjects = 2
            If this item is Object, the spring assignment is made to the point object specified by the Name item.
            If this item is Group, the spring assignment is made to all point objects in the group specified by the Name item.
            If this item is SelectedObjects, the spring assignment is made to all selected point objects and the Name
            item is ignored.
        IsLocalCSys(bool)-If this item is True, the specified spring assignments are in the point object local
            coordinate system. If it is False, the assignments are in the Global coordinate system.
        Replace(bool)-If this item is True, all existing point spring assignments to the specified point object(s)
            are deleted prior to making the assignment. If it is False, the spring assignments are added to any
            existing assignments.
        """
        ret = self.__Model.PointObj.SetSpringCoupled(name,k,ItemType,IsLocalCSys,Replace)
        return ret

class SapPointObj:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model
        self.Get = SapPointObj_Get(Sapobj)
        self.Set = SapPointObj_Set(Sapobj)

    def AddCartesian(self,x,y,z,Name="",UserName="",CSys="Global",MergeOff=False,MergeNumber=0):
        """
        ---This function adds a point object to a model.The added point object will be tagged as a Special
        Point except if it was merged with another point object. Special points are allowed to exist in
        the model with no objects connected to them.---
        inputs:
        x,y,z-The X,Y,Z(float)-coordinates of the added point object in the specified coordinate system. [L]
        Name(str)-This is the name that the program ultimately assigns for the point object. If no UserName
            is specified, the program assigns a default name to the point object. If a UserName is specified
            and that name is not used for another point, the UserName is assigned to the point; otherwise a
            default name is assigned to the point.If a point is merged with another point, this will be the
            name of the point object with which it was merged.
        UserName(str)-This is an optional user specified name for the point object. If a UserName is specified
            and that name is already used for another point object, the program ignores the UserName.
        CSys(str)-The name of the coordinate system in which the joint coordinates are defined.
        MergeOff(bool)-If this item is False, a new point object that is added at the same location as an existing
            point object will be merged with the existing point object (assuming the two point objects have the
            same MergeNumber) and thus only one point object will exist at the location.If this item is True, the
            points will not merge and two point objects will exist at the same location.
        MergeNumber(int)-Two points objects in the same location will merge only if their merge number assignments
            are the same. By default all pointobjects have a merge number of zero.
        """
        self.__Model.PointObj.AddCartesian(x,y,z,Name,UserName,CSys,MergeOff,MergeNumber)

    def AddCylindrical(self,r,theta,z,Name="",UserName="",CSys="Global",MergeOff=False,MergeNumber=0):
        """
        ---This function adds a point object to a model. The added point object will be tagged as a Special Point
        except if it was merged with another point object. Special points are allowed to exist in the model with
        no objects connected to them---
        inputs:
        r(float)-The radius for the added point object in the specified coordinate system. [L]
        theta(float)-The angle for the added point object in the specified coordinate system. The angle is measured
            in the XY plane from the positive global X axis. When looking in the XY plane with the positive Z axis
            pointing toward you, a positive Theta angle is counter clockwise. [deg]
        z(float)-The Z-coordinate of the added point object in the specified coordinate system. [L]
        Name(str)-This is the name that the program ultimately assigns for the point object. If no UserName
            is specified, the program assigns a default name to the point object. If a UserName is specified
            and that name is not used for another point, the UserName is assigned to the point; otherwise a
            default name is assigned to the point.If a point is merged with another point, this will be the
            name of the point object with which it was merged.
        UserName(str)-This is an optional user specified name for the point object. If a UserName is specified
            and that name is already used for another point object, the program ignores the UserName.
        CSys(str)-The name of the coordinate system in which the joint coordinates are defined.
        MergeOff(bool)-If this item is False, a new point object that is added at the same location as an existing
            point object will be merged with the existing point object (assuming the two point objects have the
            same MergeNumber) and thus only one point object will exist at the location.If this item is True, the
            points will not merge and two point objects will exist at the same location.
        MergeNumber(int)-Two points objects in the same location will merge only if their merge number assignments
            are the same. By default all pointobjects have a merge number of zero.
        """
        self.__Model.PointObj.AddCartesian(r,theta,z,Name,UserName,CSys,MergeOff,MergeNumber)

    def AddSpherical(self,r,a,b,Name="",UserName="",CSys="Global",MergeOff=False,MergeNumber=0):
        """
        ---This function adds a point object to a model. The added point object will be tagged as a Special Point
        except if it was merged with another point object. Special points are allowed to exist in the model with
        no objects connected to them---
        inputs:
        r(float)-The radius for the added point object in the specified coordinate system. [L]
        a(float)-The plan angle for the added point object in the specified coordinate system. This angle is
            measured in the XY plane from the positive global X axis. When looking in the XY plane with the
            positive Z axis pointing toward you, a positive a angle is counterclockwise. [deg]
        b(float)-The elevation angle for the added point object in the specified coordinate system. This angle
            is measured in an X'Z plane that is perpendicular to the XY plane with the positive X' axis oriented
            at angle a from the positive global X axis. Angle b is measured from the positive global Z axis. When
            looking in the X’Z plane with the positive Y' axis pointing toward you, a positive b angle is counter
            clockwise. [deg]
        Name(str)-This is the name that the program ultimately assigns for the point object. If no UserName
            is specified, the program assigns a default name to the point object. If a UserName is specified
            and that name is not used for another point, the UserName is assigned to the point; otherwise a
            default name is assigned to the point.If a point is merged with another point, this will be the
            name of the point object with which it was merged.
        UserName(str)-This is an optional user specified name for the point object. If a UserName is specified
            and that name is already used for another point object, the program ignores the UserName.
        CSys(str)-The name of the coordinate system in which the joint coordinates are defined.
        MergeOff(bool)-If this item is False, a new point object that is added at the same location as an existing
            point object will be merged with the existing point object (assuming the two point objects have the
            same MergeNumber) and thus only one point object will exist at the location.If this item is True, the
            points will not merge and two point objects will exist at the same location.
        MergeNumber(int)-Two points objects in the same location will merge only if their merge number assignments
            are the same. By default all pointobjects have a merge number of zero.
        """
        self.__Model.PointObj.AddSpherical(r,a,b,Name,UserName,CSys,MergeOff,MergeNumber)

    def ChangeName(self,name:str,newName):
        """
        ---The function returns zero if the new name is successfully applied, otherwise it returns a nonzero value---
        inputs:
        name(str)-The existing name of a point object.
        newName(str)-The new name for the point object.
        """
        self.__Model.PointObj.ChangeName(name,newName)

    def Count(self):
        """
        ---This function returns the total number of point objects in the model---
        """
        pointNum=self.__Model.PointObj.Count()
        return pointNum

    def IsSpringCoupled(self,name:str):
        """
        ---This function indicates if the spring assignments to a point object are coupled, that is, if they have
        off-diagonal terms in the 6x6 spring matrix for the point object---
        inputs:
        name(str)-The name of an existing point object.
        return:
        [numberItem,IsCoupled]
        IsCoupled(bool)-This item is True if the spring assigned to the specified point object is coupled, otherwise
            it is False.
        """
        result=self.__Model.PointObj.IsSpringCoupled(name)
        return result


class FrameObj_Set:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def AutoMesh(self,name,autoMesh,AutoMeshAtPoints,AutoMeshAtLines,
                                    umSegs,AutoMeshMaxLength,ItemType=0):
        """
        ---This function makes automatic meshing assignments to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        AutoMesh(bool)-This item is True if the frame object is to be automatically meshed by the program when
            the analysis model is created.
        AutoMeshAtPoints(bool)-This item is applicable only when the AutoMesh item is True. If this item is True,
            the frame object is automatically meshed at intermediate joints along its length
        AutoMeshAtLines(bool)-This item is applicable only when the AutoMesh item is True. If this item is True,
            the frame object is automatically meshed at intersections with other frames, area object edges and
            solid object edges.
        NumSegs(int)-This item is applicable only when the AutoMesh item is True. It is the minimum number of elements
            into which the frame object is automatically meshed. If this item is zero, the number of elements is not
            checked when the automatic meshing is done.
        AutoMeshMaxLength(float)-This item is applicable only when the AutoMesh item is True. It is the maximum length
            of auto meshed frame elements. If this item is zero, the element length is not checked when the automatic
            meshing is done. [L]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored.
        """
        self.__Model.FrameObj.SetAutoMesh(name,autoMesh,AutoMeshAtPoints,AutoMeshAtLines,
                                    umSegs,AutoMeshMaxLength,ItemType)

    def DesignProcedure(self,name,myType,itemType=0):
        """
        ---This function sets the design procedure for frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        myType(int)-This is 1 or 2, indicating the design procedure type desired for the specified frame object.
            1 = Default from material,2 = No design
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored.
        """
        self.__Model.FrameObj.SetDesignProcedure(name,myType,itemType)

    def EndLengthOffset(self,name,AutoOffset,Length1=0,Length2=0,rz=0,ItemType=0):
        """
        ---This function assigns frame object end offsets along the 1-axis of the object---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        AutoOffset(bool)-If this item is True, the end length offsets are automatically determined by the program
            from object connectivity, and the Length1, Length2 and rz items are ignored.
        Length1(float)-The offset length along the 1-axis of the frame object at the I-End of the frame object. [L]
        Length2(float)-The offset along the 1-axis of the frame object at the J-End of the frame object. [L]
        rz(float)-The rigid zone factor.  This is the fraction of the end offset length assumed to be rigid for
            bending and shear deformations.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored.
        """
        self.__Model.FrameObj.SetEndLengthOffset(name,AutoOffset,Length1,Length2,rz,ItemType)

    def EndSkew(self,name,skewI,skewJ,itemType=0):
        """
        ---This function assigns frame object end skew data. End skew data is used in the program to plot the
        extruded view of bridge objects that have been updated as spine models only.---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        skewI(float)-The angle in degrees measured counter clockwise from the positive local 3-axis to a line
            parallel to the I-End of the frame object (-90 < SkewI < 90). [deg]
        skewJ(float)-TThe angle in degrees measured counter clockwise from the positive local 3-axis to a line
            parallel to the J-End of the frame object (-90 < SkewJ < 90). [deg]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored.
        """
        self.__Model.FrameObj.SetEndSkew(name,skewI,skewJ,itemType)

    def GroupAssign(self,name,groupName,remove=False,itemType=0):
        """
        ---This function adds or removes frame objects from a specified group---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        groupName(str)-TThe name of an existing group to which the assignment is made.
        remove(bool)-If this item is False, the specified frame objects are added to the group specified by
            the GroupName item. If it is True, the frame objects are removed from the group.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored.
        """
        self.__Model.FrameObj.SetGroupAssign(name,groupName,remove,itemType)

    def InsertionPoint(self,name,CardinalPoint,Mirror2,StiffTransform,Offset1,Offset2,
                                          CSys="Local",itemType=0):
        """
        ---This function assigns frame object insertion point data. The assignments include the cardinal
            point and end joint offsets---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        CardinalPoint(int)-This is a numeric value from 1 to 11 that specifies the cardinal point for the frame
            object. The cardinal point specifies the relative position of the frame section on the line representing
            the frame object.
            1 = bottom left
            2 = bottom center
            3 = bottom right
            4 = middle left
            5 = middle center
            6 = middle right
            7 = top left
            8 = top center
            9 = top right
            10 = centroid
            11 = shear center
        Mirror2(bool)-If this item is True, the frame object section is assumed to be mirrored (flipped) about
            its local 2-axis.
        StiffTransform(bool)-If this item is True, the frame object stiffness is transformed for cardinal point
            and joint offsets from the frame section centroid.
        Offset1(float list)-This is an array of three joint offset distances, in the coordinate directions specified
            by CSys, at the I-End of the frame object. [L]
            Offset1(0) = Offset in the 1-axis or X-axis direction
            Offset1(1) = Offset in the 2-axis or Y-axis direction
            Offset1(2) = Offset in the 3-axis or Z-axis direction
        Offset2(float list)-This is an array of three joint offset distances, in the coordinate directions specified
            by CSys, at the J-End of the frame object. [L]
            Offset2(0) = Offset in the 1-axis or X-axis direction
            Offset2(1) = Offset in the 2-axis or Y-axis direction
            Offset2(2) = Offset in the 3-axis or Z-axis direction
        CSys(str)-This is Local or the name of a defined coordinate system. It is the coordinate system in which
            the Offset1 and Offset2 items are specified.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored.
        """
        self.__Model.FrameObj.SetInsertionPoint(name,CardinalPoint,Mirror2,StiffTransform,Offset1,Offset2,CSys,itemType)

    def LoadDeformation(self,name,loadPat,DOF,d,itemType=0):
        """
        ---This function assigns deformation loads to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        DOF(bool list)-This is a array of boolean values indicating if the considered degree of freedom has a deformation load.
            DOF(1) = U1,DOF(2) = U2,DOF(3) = U3,DOF(4) = R1,DOF(5) = R2,DOF(6) = R3
        d(float list)-This is a array of deformation load values. The deformations specified for a given degree of
            freedom are applied only if the corresponding DOF item for that degree of freedom is True.
                d(1) = U1 deformation [L]
                d(2) = U2 deformation [L]
                d(3) = U3 deformation [L]
                d(4) = R1 deformation [rad]
                d(5) = R2 deformation [rad]
                d(6) = R3 deformation [rad]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored.
        """
        self.__Model.FrameObj.SetLoadDeformation(name,loadPat,DOF,d,itemType)

    def LoadDistributed(self,name,loadPat,myType,Dir,Dist1,Dist2,Val1,Val2,
                                           CSys="Global",RelDist=True,Replace=True,ItemType=0):
        """
        ---This function assigns distributed loads to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        myType(int)-This is 1 or 2, indicating the type of distributed load.
            1 = Force per unit length,2 = Moment per unit length
        Dir(int)-This is an integer between 1 and 11, indicating the direction of the load.
            1 = Local 1 axis (only applies when CSys is Local)
            2 = Local 2 axis (only applies when CSys is Local)
            3 = Local 3 axis (only applies when CSys is Local)
            4 = X direction (does not apply when CSys is Local)
            5 = Y direction (does not apply when CSys is Local)
            6 = Z direction (does not apply when CSys is Local)
            7 = Projected X direction (does not apply when CSys is Local)
            8 = Projected Y direction (does not apply when CSys is Local)
            9 = Projected Z direction (does not apply when CSys is Local)
            10 = Gravity direction (only applies when CSys is Global)
            11 = Projected Gravity direction (only applies when CSys is Global)
            The positive gravity direction (see Dir = 10 and 11) is in the negative Global Z direction.
        Dist1(float)-This is the distance from the I-End of the frame object to the start of the distributed load.
            This may be a relative distance (0 <= Dist1 <= 1) or an actual distance, depending on the value of the
            RelDist item. [L] when RelDist is False
        Dist2(float)-This is the distance from the I-End of the frame object to the end of the distributed load.
            This may be a relative distance (0 <= Dist2 <= 1) or an actual distance, depending on the value of the
            RelDist item. [L] when RelDist is False
        Val1(float)-This is the load value at the start of the distributed load. [F/L] when MyType is 1 and [FL/L]
            when MyType is 2
        Val2(float)-This is the load value at the end of the distributed load. [F/L] when MyType is 1 and [FL/L]
            when MyType is 2
        CSys(str)-This is Local or the name of a defined coordinate system. It is the coordinate system in which
            the loads are specified.
        RelDist(bool)-If this item is True, the specified Dist item is a relative distance, otherwise it is an actual distance.
        Replace(bool)-If this item is True, all previous distributed loads, if any, assigned to the specified frame
            object(s), in the specified load pattern, are deleted before making the new assignment.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored.
        """
        self.__Model.FrameObj.SetLoadDistributed(name,loadPat,myType,Dir,Dist1,Dist2,Val1,Val2,CSys,RelDist,Replace,ItemType)

    def LoadGravity(self,name,loadPat,x,y,z,Replace=True,CSys="Global",itemType=0):
        """
        ---This function assigns gravity load multipliers to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        x,y,z(float)-These are the gravity load multipliers in the x, y and z directions of the specified coordinate system.
        Replace(bool)-If this item is True, all previous gravity loads, if any, assigned to the specified frame
            object(s), in the specified load pattern, are deleted before making the new assignment.
        CSys(str)-The coordinate system in which the x, y and z multipliers are specified
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored.
        """
        self.__Model.FrameObj.SetLoadGravity(name,loadPat,x,y,z,Replace,CSys,itemType)

    def LoadPoint(self,name,loadPat,myType,Dir,Dist,Val,
                                     CSys="Global",RelDist=True,Replace=True,itemType=0):
        """
        ---This function assigns point loads to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        myType(int)-This is 1 or 2, indicating the type of point load.
            1 = Force,2 = Moment
        Dir(int)-This is an integer between 1 and 11, indicating the direction of the load.
            1 = Local 1 axis (only applies when CSys is Local)
            2 = Local 2 axis (only applies when CSys is Local)
            3 = Local 3 axis (only applies when CSys is Local)
            4 = X direction (does not apply when CSys is Local)
            5 = Y direction (does not apply when CSys is Local)
            6 = Z direction (does not apply when CSys is Local)
            7 = Projected X direction (does not apply when CSys is Local)
            8 = Projected Y direction (does not apply when CSys is Local)
            9 = Projected Z direction (does not apply when CSys is Local)
            10 = Gravity direction (only applies when CSys is Global)
            11 = Projected Gravity direction (only applies when CSys is Global)
            The positive gravity direction (see Dir = 10 and 11) is in the negative Global Z direction.
        Dist(float)-This is the distance from the I-End of the frame object to the load location. This may
            be a relative distance (0 <= Dist <= 1) or an actual distance, depending on the value of the
            RelDist item. [L] when RelDist is False
        Val(float)-This is the value of the point load. [F] when MyType is 1 and [FL] when MyType is 2
        CSys(str)-This is Local or the name of a defined coordinate system. It is the coordinate system in
            which the loads are specified.
        RelDist(bool)-If this item is True, the specified Dist item is a relative distance, otherwise it is
            an actual distance.
        Replace(bool)-If this item is True, all previous loads, if any, assigned to the specified frame object(s),
            in the specified load pattern, are deleted before making the new assignment.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.FrameObj.SetLoadPoint(name,loadPat,myType,Dir,Dist,Val,CSys,RelDist,Replace,itemType)

    def LoadStrain(self,name,loadPat,DOF,Val,Replace=True,PatternName="",itemType=0):
        """
        ---This function assigns strain loads to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        DOF(int)-This is 1, 2, 3, 4, 5 or 6, indicating the degree of freedom to which the strain load is applied.
            1 = Strain11,2 = Strain12,3 = Strain13,4 = Curvature1,5 = Curvature2,6 = Curvature3
        Val(float)-This is the strain load value. [L/L] for DOF = 1, 2 and 3 and [1/L] for DOF = 4, 5 and 6
        Replace(bool)-If this item is True, all previous strain loads, if any, assigned to the specified frame object(s),
            in the specified load pattern, for the specified degree of freedom, are deleted before making the new assignment.
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the strain load for the
            frame object is uniform along the object at the value specified by Val.If PatternName is the name of a
            defined joint pattern, the strain load for the frame object is based on the specified strain value
            multiplied by the pattern value at the joints at each end of the frame object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.FrameObj.SetLoadStrain(name,loadPat,DOF,Val,Replace,PatternName,itemType)

    def LoadTargetForce(self,name,loadPat,DOF,f,RD,itemType=0):
        """
        ---This function assigns target forces to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        DOF(bool list)-This is a array of boolean values indicating if the considered degree of freedom has a target force.
            DOF(1) = P,DOF(2) = V2,DOF(3) = V3,DOF(4) = T,DOF(5) = M2,DOF(6) = M3
        f(float list)-This is a array of target force values. The target forces specified for a given degree of freedom
            are applied only if the corresponding DOF item for that degree of freedom is True.
            f(1) = P [F],f(2) = V2 [F],f(3) = V3 [F],f(4) = T [FL],f(5) = M2 [FL],f(6) = M3 [FL]
        RD(float list)-This is a array of relative distances along the frame objects where the target force values apply.
            The relative distances specified for a given degree of freedom are applicable only if the corresponding DOF
            item for that degree of freedom is True. The relative distance must be between 0 and 1, 0 <= RD <=1.
            RD(1) = relative location for P target force
            RD(2) = relative location for V2 target force
            RD(3) = relative location for V3 target force
            RD(4) = relative location for T target force
            RD(5) = relative location for M2 target force
            RD(6) = relative location for M3 target force
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.FrameObj.SetLoadTargetForce(name,loadPat,DOF,f,RD,itemType)

    def LoadTemperature(self,name,loadPat,myType,Val,PatternName="",Replace=True,itemType=0):
        """
        ---This function assigns temperature loads to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        myType(int)-This is 1, 2 or 3, indicating the type of temperature load.
            1 = Temperature,2 = Temperature gradient along local 2 axis,3 = Temperature gradient along local 3 axis
        Val(float)-This is the temperature change value. [T] for MyType = 1 and [T/L] for MyType = 2 and 3
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank the temperature load
            for the frame object is uniform along the object at the value specified by Val.If PatternName is the
            name of a defined joint pattern, the temperature load for the frame object is based on the specified
            temperature value multiplied by the pattern value at the joints at each end of the frame object.
        Replace(bool)-If this item is True, all previous temperature loads, if any, assigned to the specified frame
            object(s), in the specified load case, are deleted before making the new assignment.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.FrameObj.SetLoadTemperature(name,loadPat,myType,Val,PatternName,Replace,itemType)

    def LoadTransfer(self,name,Val,itemType=0):
        """
        ---This function returns the load transfer option for frame objects.  It indicates whether the frame
        receives load from an area object when the area object is loaded with a load of type uniform to frame---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        Val(bool)-This boolean value indicates if load is allowed to be transferred from area objects to this frame object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.FrameObj.SetLoadTransfer(name,Val,itemType)

    def LocalAxes(self,name,Ang,itemType=0):
        """
        ---This function assigns a local axis angle to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        Ang(float)-This is the angle that the local 2 and 3 axes are rotated about the positive local 1 axis,
            from the default orientation or, if the Advanced item is True, from the orientation determined by
            the plane reference vector. The rotation for a positive angle appears counter clockwise when the
            local +1 axis is pointing toward you. [deg]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.FrameObj.SetLocalAxes(name,Ang,itemType)

    def Mass(self,name,massOverL,Replace=False,itemType=0):
        """
        ---This function assigns mass per unit length to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        massOverL(float)-The mass per unit length assigned to the frame object. [M/L]
        Replace(bool)-If this item is True, all existing mass assignments to the frame object are removed before
            assigning the specified mas. If it is False, the specified mass is added to any existing mass already
            assigned to the frame object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.FrameObj.SetMass(name,massOverL,Replace,itemType)

    def MaterialOverwrite(self,name,proName,itemType=0):
        """
        ---This function sets the material overwrite assignment for frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        propName(str)-This is None or a blank string, indicating that any existing material overwrites assigned
            to the specified frame objects are to be removed, or it is the name of an existing material property.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.FrameObj.SetMaterialOverwrite(name,proName,itemType)

    def MatTemp(self,name,temp,patternName="",itemType=0):
        """
        ---This function assigns material temperatures to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        temp(float)-This is the material temperature value assigned to the frame object. [T]
        patternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the material temperature
            for the frame object is uniform along the object at the value specified by Temp.If PatternName is the name
            of a defined joint pattern, the material temperature for the frame object may vary from one end to the other.
            The material temperature at each end of the object is equal to the specified temperature multiplied by the
            pattern value at the joint at the end of the frame object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.FrameObj.SetMatTemp(name,temp,patternName,itemType)

    def Modifiers(self,name,value,itemType=0):
        """
        ---This function sets the frame modifier assignment for frame objects. The default value for all modifiers is one.---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        value(float list)-This is an array of eight unitless modifiers.
            Value(0) = Cross sectional area modifier
            Value(1) = Shear area in local 2 direction modifier
            Value(2) = Shear area in local 3 direction modifier
            Value(3) = Torsional constant modifier
            Value(4) = Moment of inertia about local 2 axis modifier
            Value(5) = Moment of inertia about local 3 axis modifier
            Value(6) = Mass modifier
            Value(7) = Weight modifier
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.FrameObj.SetModifiers(name,value,itemType)

    def NotionalSize(self,name,stype,value):
        """
        ---This function assigns the method to determine the notional size of a frame section for the creep and
            shrinkage calculations. This function is currently worked for the steel/aluminum sections - I/Wide
            Flange, Channel, Tee, Angle, Double Angle, Double Channel, Pipe and Tube sections, and all the concrete
            sections - Rectangular, Circular, Pipe, Tube, Precast I.---
        inputs:
        name(str)-The name of an existing frame section property.
        stype(str)-The type to define the notional size of a section. It can be:
            "Auto" = Program will determine the notional size based on the average thickness of an area element.
            "User" = The notional size is based on the user-defined value.
            "None" = Notional size will not be considered. In other words, the time-dependent effect of this section
                will not be considered.
        value(float)-For stype is "Auto", the Value represents for the scale factor to the program-determined notional
            size; for stype is “User”, the Value represents for the user-defined notional size [L]; for stype is “None”,
            the Value will not be used and can be set to 1.
        """
        self.__Model.PropFrame.SetNotionalSize(name,stype,value)

    def OutputStations(self,name,myType,settingValue,NoOutPutAndDesignAtElementEnds=False,
                                          NoOutPutAndDesignAtPointLoads=False,itemType=0):
        """
        ---This function assigns frame object output station data---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        myType(int)-This is 1 or 2, indicating how the output stations are specified.
            1 = maximum segment size, that is, maximum station spacing
            2 = minimum number of stations
        settingValue(float/int)-the corresponding value for myType
            The maximum segment size, that is, the maximum station spacing. This item applies only when MyType = 1. [L]
            The minimum number of stations. This item applies only when MyType = 2.
        NoOutPutAndDesignAtElementEnds(bool)-If this item is True, no additional output stations are added at the ends
            of line elements when the frame object is internally meshed.
        NoOutPutAndDesignAtPointLoads(bool)-If this item is True, no additional output stations are added at point load
            locations.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.FrameObj.SetOutputStations(name,myType,settingValue,NoOutPutAndDesignAtElementEnds,
                                          NoOutPutAndDesignAtPointLoads,itemType)

    def PDeltaForce(self,name,PDeltaForce,Dir,Replace,CSys="Global",itemType=0):
        """
        ---This function assigns P-Delta forces to straight frame objects. P-Delta force assignments do not apply to
            curved frames.---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        PDeltaForce(float)-The P-Delta force assigned to the frame object. [F]
        Dir(int)-This is 0, 1, 2 or 3, indicating the direction of the P-Delta force assignment.
            0 = Frame object local 1-axis direction
            1 = Projected X direction in CSys coordinate system
            2 = Projected Y direction in CSys coordinate system
            3 = Projected Z direction in CSys coordinate system
        Replace(bool)-If this item is True, all existing P-Delta force assignments to the frame object are removed
            before assigning the specified P-Delta force. If it is False, the specified P-Delta force is added to any
            existing P-Delta forces already assigned to the frame object.
        Csys(str)-This is the name of the coordinate system in which the projected X, Y or Z direction P-Delta forces
            are defined. This item does not apply if the Dir item is zero (frame object local 1-axis direction).
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.FrameObj.SetPDeltaForce(name,PDeltaForce,Dir,Replace,CSys,itemType)

    def Releases(self,name,ii,jj,startValue=[0,0,0,0,0,0],endValue=[0,0,0,0,0,0],itemType=0):
        """
        ---This function makes end release and partial fixity assignments to frame objects.The function returns zero
        if the assignments are successfully retrieved, otherwise it returns a nonzero value.Partial fixity assignments
        are made to degrees of freedom that have been released only.Some release assignments would cause instability
        in the model. An error is returned if this type of assignment is made. Unstable release assignments include
        the following:
        U1 released at both ends
        U2 released at both ends
        U3 released at both ends
        R1 released at both ends
        R2 released at both ends and U3 at either end
        R3 released at both ends and U2 at either end
        ---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        ii,jj(bool list)-These are arrays of six booleans indicating the I-End and J-End releases for the frame object.
            ii(0) and jj(0) = U1 release
            ii(1) and jj(1) = U2 release
            ii(2) and jj(2) = U3 release
            ii(3) and jj(3) = R1 release
            ii(4) and jj(4) = R2 release
            ii(5) and jj(5) = R3 release
        StartValue, EndValue(float list)-These are arrays of six values indicating the I-End and J-End partial fixity
            springs for the frame object.
            StartValue(0) and EndValue(0) = U1 partial fixity [F/L]
            StartValue(1) and EndValue(1) = U2 partial fixity [F/L]
            StartValue(2) and EndValue(2) = U3 partial fixity [F/L]
            StartValue(3) and EndValue(3) = R1 partial fixity [FL/rad]
            StartValue(4) and EndValue(4) = R2 partial fixity [FL/rad]
            StartValue(5) and EndValue(5) = R3 partial fixity [FL/rad]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.FrameObj.SetReleases(name,ii,jj,startValue,endValue,itemType)

    def Section(self,name,propName,itemType=0,sVarTotalLength=0,sVarRelStartLoc=0):
        """
        ---This function assigns a frame section property to a frame object---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        propName(str)-This is None or the name of a frame section property to be assigned to the specified frame object(s).
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        sVarTotalLength(float)-This is the total assumed length of the nonprismatic section. Enter 0 for this item to
            indicate that the section length is the same as the frame object length.This item is applicable only when
            the assigned frame section property is a nonprismatic section.
        sVarRelStartLoc(float)-This is the relative distance along the nonprismatic section to the I-End (start) of the
            frame object. This item is ignored when the sVarTotalLengthitem is 0.This item is applicable only when the
            assigned frame section property is a nonprismatic section, and the sVarTotalLengthitem is greater than zero.
        """
        self.__Model.FrameObj.SetSection(name,propName,itemType,sVarTotalLength,sVarRelStartLoc)

    def Spring(self,name,myType,s=0,simpleSpringType=1,LinkProp="",springLocalOneType=1,Dir=1,
                                  Plane23Angle=0,Vec=[1,0,0],Ang=0,Replace=False,CSys="Local",itemType=0):
        """
        ---This function makes spring assignments to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        myType(int)-This is 1 or 2, indicating the spring property type.1 = Simple spring,2 = Link property
        s(float)-The simple spring stiffness per unit length of the frame object. This item applies only when MyType = 1. [F/L2]
        simpleSpringType(int)-This is 1, 2 or 3, indicating the simple spring type. This item applies only when MyType = 1.
            1 = Spring resists tension and compression
            2 = Spring resists compression only
            3 = Spring resists tension only
        LinkProp(str)-The name of the link property assigned to the spring. This item applies only when MyType = 2.
        springLocalOneType(int)-This is 1, 2 or 3, indicating the method used to specify the spring positive local
            1-axis orientation.
            1 = Parallel to frame object local axis
            2 = In the frame object 2-3 plane
            3 = User specified direction vector
        Dir(int)-This is 1, 2, 3, -1, -2 or -3, indicating the frame object local axis that corresponds to the positive
            local 1-axis of the spring. This item applies only when SpringLocalOneType = 1.
        Plane23Angle(float)-This is the angle in the frame object 2-3 plane measured counter clockwise from the frame
            positive 2-axis to the spring positive 1-axis. This item applies only when SpringLocalOneType = 2. [deg]
        Vec(float list)-This is an array of three values that define the direction vector of the spring positive local
            1-axis. The direction vector is in the coordinate system specified by the CSys item. This item applies only
            when SpringLocalOneType = 3.
        Ang(float)-This is the angle that the link local 2-axis is rotated from its default orientation. This item
            applies only when MyType = 2. [deg]
        Replace(bool)-If this item is True, all existing spring assignments to the frame object are removed before
            assigning the specified spring. If it is False, the specified spring is added to any existing springs
            already assigned to the frame object.
        CSys(str)-This is Local (meaning the frame object local coordinate system) or the name of a defined coordinate
            system. This item is the coordinate system in which the user specified direction vector, Vec, is specified.
            This item applies only when SpringLocalOneType = 3.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.FrameObj.SetSpring(name,myType,s,simpleSpringType,LinkProp,springLocalOneType,Dir,
                                  Plane23Angle,Vec,Ang,Replace,CSys,itemType)

    def TCLimits(self,name,LimitCompressionExists,LimitCompression,LimitTensionExists,LimitTension,
                                    itemType=0):
        """
        ---This function makes tension/compression force limit assignments to frame objects.
        The function returns zero if the assignments are successfully applied, otherwise it returns a nonzero value.
        Note that the tension and compression limits are only used in nonlinear analyses
        ---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        LimitCompressionExists(bool)-This item is True if a compression force limit exists for the frame object.
        LimitCompression(float)-The compression force limit for the frame object. [F]
        LimitTensionExists(bool)-This item is True if a tension force limit exists for the frame object.
        LimitTension(float)-The tension force limit for the frame object. [F]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.FrameObj.SetTCLimits(name,LimitCompressionExists,LimitCompression,LimitTensionExists,LimitTension,
                                    itemType)

class FrameObj_Get:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def AutoMesh(self,name):
        """
        ---This function retrieves the automatic meshing assignments to frame objects---
        inputs:
        name(str)-The name of an existing frame object.
        return:[index,AutoMesh,AutoMeshAtPoints,AutoMeshAtLines,NumSegs,AutoMeshMaxLength]
        AutoMesh(bool)-This item is True if the frame object is to be automatically meshed by the program when the
            analysis model is created.
        AutoMeshAtPoints(bool)-This item is applicable only when the AutoMesh item is True. If this item is True, the
            frame object is automatically meshed at intermediate joints along its length.
        AutoMeshAtLines(bool)-This item is applicable only when the AutoMesh item is True. If this item is True, the
            frame object is automatically meshed at intersections with other frames, area object edges and solid object edges.
        NumSegs(int)-This item is applicable only when the AutoMesh item is True. It is the minimum number of elements
            into which the frame object is automatically meshed. If this item is zero, the number of elements is not
            checked when the automatic meshing is done.
        AutoMeshMaxLength(float)-This item is applicable only when the AutoMesh item is True. It is the maximum length
            of auto meshed frame elements. If this item is zero, the element length is not checked when the automatic
            meshing is done. [L]
        """
        result=self.__Model.FrameObj.GetAutoMesh(name)
        return result

    def GroupAssign(self,name):
        """
        ---This function retrieves the names of the groups to which a specified frame object is assigned---
        inputs:
        name(str)-The name of an existing frame object.
        return:[index,numberGroups,Groups]
        numberGroups(int)-The number of group names retrieved.
        Groups(str list)-The names of the groups to which the frame object is assigned.
        """
        result=self.__Model.FrameObj.GetGroupAssign(name)
        return result

    def LoadDeformation(self,name):
        """
        ---This function retrieves the deformation load assignments to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        return:[index,NumberItems,FrameName,LoadPat,dof1, dof2, dof3, dof4, dof5, dof6,U1, U2, U3, R1, R2, R3]
        NumberItems(int)-The total number of deformation loads retrieved for the specified frame objects.
        FrameName(str list)-This is an array that includes the name of the frame object associated with each deformation load.
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each deformation load.
        dof1,dof2,dof3,dof4,dof5,dof6(bool)-These are arrays of boolean values indicating if the considered degree of
            freedom has a deformation load.
            dof1 = U1,dof2 = U2,dof3 = U3,dof4 = R1,dof5 = R2,dof6 = R3
        U1, U2, U3, R1, R2, R3(float)-These are arrays of deformation load values. The deformations specified for a
            given degree of freedom are applicable only if the corresponding DOF item for that degree of freedom is True.
            U1 = U1 deformation [L]
            U2 = U2 deformation [L]
            U3 = U3 deformation [L]
            R1 = R1 deformation [rad]
            R2 = R2 deformation [rad]
            R3 = R3 deformation [rad]
        """
        result=self.__Model.FrameObj.GetLoadDeformation(name)
        return result

    def LoadDistributed(self,name):
        """
        ---This function retrieves the distributed load assignments to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        return:[index,NumberItems,FrameName,LoadPat,MyType,CSys,Dir,RD1,RD2,Dist1,Dist2,Val1,Val2]
        NumberItems(int)-The total number of distributed loads retrieved for the specified frame objects.
        FrameName(str list)-This is an array that includes the name of the frame object associated with each
            distributed load.
        LoadPat(str list)-This is an array that includes the name of the coordinate system in which the distributed
            loads are specified.
        MyType(int list)-This is an array that includes 1 or 2, indicating the type of distributed load.
            1 = Force,2 = Moment
        CSys(str list)-This is an array that includes the name of the coordinate system in which each distributed
            load is defined. It may be Local or the name of a defined coordinate system.
        Dir(int list)-This is an array that includes an integer between 1 and 11, indicating the direction of the load.
            1 = Local 1 axis (only applies when CSys is Local)
            2 = Local 2 axis (only applies when CSys is Local)
            3 = Local 3 axis (only applies when CSys is Local)
            4 = X direction (does not apply when CSys is Local)
            5 = Y direction (does not apply when CSys is Local)
            6 = Z direction (does not apply when CSys is Local)
            7 = Projected X direction (does not apply when CSys is Local)
            8 = Projected Y direction (does not apply when CSys is Local)
            9 = Projected Z direction (does not apply when CSys is Local)
            10 = Gravity direction (only applies when CSys is Global)
            11 = Projected Gravity direction (only applies when CSys is Global)
            The positive gravity direction (see Dir = 10 and 11) is in the negative Global Z direction.
        RD1(float list)-This is an array that includes the relative distance from the I-End of the frame object
            to the start of the distributed load.
        RD2(float list)-This is an array that includes the relative distance from the I-End of the frame object
            to the end of the distributed load.
        Dist1(float list)-This is an array that includes the actual distance from the I-End of the frame object
            to the start of the distributed load. [L]
        Dist2(float list)-This is an array that includes the actual distance from the I-End of the frame object
            to the end of the distributed load. [L]
        Val1(float list)-This is an array that includes the load value at the start of the distributed load.
            [F/L] when MyType is 1 and [FL/L] when MyType is 2
        Val2(float list)-This is an array that includes the load value at the end of the distributed load.
            [F/L] when MyType is 1 and [FL/L] when MyType is 2
        """
        result=self.__Model.FrameObj.GetLoadDistributed(name)
        return result

    def LoadGravity(self,name):
        """
        ---This function retrieves the gravity load assignments to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        return:[index,NumberItems,FrameName,LoadPat,CSys,x,y,z]
        NumberItems(int)-The total number of gravity loads retrieved for the specified frame objects.
        FrameName(str list)-This is an array that includes the name of the frame object associated with each gravity load.
        LoadPat(str list)-This is an array that includes the name of the coordinate system in which the gravity load
            multipliers are specified.
        CSys(str list)-This is an array that includes the name of the coordinate system associated with each gravity load.
        x,y,z(float)-These are arrays of gravity load multipliers in the x, y and z directions of the specified
            coordinate system.
        """
        result=self.__Model.FrameObj.GetLoadGravity(name)
        return result

    def LoadPoint(self,name):
        """
        ---This function retrieves the point load assignments to frame objects.---
        inputs:
        name(str)-The name of an existing frame object or group depending on the value of the ItemType item.
        return:
        [index,NumberItems,FrameName,LoadPat,MyType,CSys,Dir,RelDist,Dist,Val]

        NumberItems(int)-The total number of point loads retrieved for the specified frame objects.
        FrameName(str list)-This is an array that includes the name of the frame object associated with each point load.
        LoadPat(str list)-This is an array that includes the name of the coordinate system in which the point loads are
            specified.
        MyType(int list)-This is an array that includes 1 or 2, indicating the type of point load.
            1 = Force,2 = Moment
        CSys(str list)-This is an array that includes the name of the coordinate system in which each point load is
            defined. It may be Local or the name of a defined coordinate system.
        Dir(int list)-This is an array that includes an integer between 1 and 11 indicating the direction of the load.
            1 = Local 1 axis (only applies when CSys is Local)
            2 = Local 2 axis (only applies when CSys is Local)
            3 = Local 3 axis (only applies when CSys is Local)
            4 = X direction (does not apply when CSys is Local)
            5 = Y direction (does not apply when CSys is Local)
            6 = Z direction (does not apply when CSys is Local)
            7 = Projected X direction (does not apply when CSys is Local)
            8 = Projected Y direction (does not apply when CSys is Local)
            9 = Projected Z direction (does not apply when CSys is Local)
            10 = Gravity direction (only applies when CSys is Global)
            11 = Projected Gravity direction (only applies when CSys is Global)
            The positive gravity direction (see Dir = 10 and 11) is in the negative Global Z direction.
        RelDist(float list)-This is an array that includes the relative distance from the I-End of the frame
            object to the location where the point load is applied.
        Dist(float list)-This is an array that includes the actual distance from the I-End of the frame object
            to the location where the point load is applied. [L]
        Val(float list)-This is an array that includes the value of the point load. [F] when MyType is 1 and [FL]
            when MyType is 2
        """
        result=self.__Model.FrameObj.GetLoadPoint(name)
        return result

    def LoadStrain(self,name):
        """
        ---This function retrieves the strain load assignments to frame objects.---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        return:
        [NumberItems,FrameName,LoadPat,DOF,Val,PatternName]

        NumberItems(int)-The total number of strain loads retrieved for the specified frame objects.
        FrameName(str list)-This is an array that includes the name of the frame object associated with each strain load.
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each strain load.
        DOF(int)-This is an array that includes 1, 2, 3, 4, 5 or 6, indicating the degree of freedom associated with
            each strain load.
            1 = Strain11,2 = Strain12,3 = Strain13,4 = Curvature1,5 = Curvature2,6 = Curvature3
        Val(float list)-This is an array that includes the strain value. [L/L] for DOF = 1, 2 and 3 and [1/L] for
            DOF = 4, 5 and 6
        """
        result=self.__Model.FrameObj.GetLoadStrain(name)
        return result

    def LoadTargetForce(self,name):
        """
        ---This function retrieves the target force assignments to frame objects.---
        :param name:
        :return:
        [index,numberItems,FrameName,LoadPat,dof1, dof2, dof3, dof4, dof5, dof6,P, V2, V3, T, M2, M3,T1, T2, T3, T4, T5, T6]

        numberItems(int)-The total number of deformation loads retrieved for the specified frame objects.
        FrameName(str list)-This is an array that includes the name of the frame object associated with each target force.
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each target force.
        dof1, dof2, dof3, dof4, dof5, dof6(bool list)-These are arrays of boolean values indicating if the considered
            degree of freedom has a target force assignment.
            dof1 = P,dof2 = V2,dof3 = V3,dof4 = T,dof5 = M2,dof6 = M3
        P, V2, V3, T, M2, M3(float list)-These are arrays of target force values. The target forces specified for a
            given degree of freedom are applicable only if the corresponding DOF item for that degree of freedom is True.
            U1 = U1 deformation [L]
            U2 = U2 deformation [L]
            U3 = U3 deformation [L]
            R1 = R1 deformation [rad]
            R2 = R2 deformation [rad]
            R3 = R3 deformation [rad]
        T1, T2, T3, T4, T5, T6(float list)-These are arrays of the relative distances along the frame objects where the
            target force values apply. The relative distances specified for a given degree of freedom are applicable
            only if the corresponding dofn item for that degree of freedom is True.
            T1 = relative location for P target force
            T2 = relative location for V2 target force
            T3 = relative location for V3 target force
            T4 = relative location for T target force
            T5 = relative location for M2 target force
            T6 = relative location for M3 target force
        """
        result=self.__Model.FrameObj.GetLoadTargetForce(name)
        return result

    def LoadTemperature(self,name):
        """
        ---This function retrieves the temperature load assignments to frame objects---
        inputs:
        name(str)-The name of an existing frame object or group, depending on the value of the ItemType item.
        return:
        [index,NumberItems,FrameName,LoadPat,MyType,Val,PatternName]

        NumberItems(int)-The total number of temperature loads retrieved for the specified frame objects.
        FrameName(str list)-This is an array that includes the name of the frame object associated with each temperature load.
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each temperature load.
        MyType(int)-This is an array that includes 1, 2 or 3, indicating the type of temperature load.
            1 = Temperature
            2 = Temperature gradient along local 2 axis
            3 = Temperature gradient along local 3 axis
        Val(float list)-This is an array that includes the temperature load value. [T] for MyType= 1 and [T/L] for
            MyType= 2 and 3
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify the
            temperature load.
        """
        result=self.__Model.FrameObj.GetLoadTemperature(name)
        return result

    def LocalAxes(self,name):
        """
        ---This function retrieves the frame local axis angle assignment for frame objects---
        inputs:
        name(str)-The name of an existing frame object.
        return:
        [index Ang,Advanced]

        Ang(float)-This is the angle that the local 2 and 3 axes are rotated about the positive local 1 axis,
            from the default orientation or, if the Advanced item is True, from the orientation determined by
            the plane reference vector. The rotation for a positive angle appears counter clockwise when the
            local +1 axis is pointing toward you. [deg]
        Advanced(bool)-This item is True if the line object local axes orientation was obtained using advanced
            local axes parameters.
        """
        result=self.__Model.FrameObj.GetLocalAxes(name)
        return result

    def Mass(self,name):
        """
        ---This function retrieves the frame mass per unit length assignment for frame objects---
        inputs:
        name(str)-The name of an existing frame object.
        return:
        [index,MassOverL]
        MassOverL(float)-The mass per unit length assigned to the frame object. [M/L]
        """
        result=self.__Model.FrameObj.GetMass(name)
        return result

    def MatTemp(self,name):
        """
        ---This function retrieves the material temperature assignments to frame objects---
        inputs:
        name(str)-The name of an existing frame object
        return:
        [index,Temp,PatternName]
        Temp(float)-This is the material temperature value assigned to the frame object. [T]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the material temperature
            for the frame object is uniform along the object at the value specified by Temp.If PatternName is the name
            of a defined joint pattern, the material temperature for the frame object may vary from one end to the other.
            The material temperature at each end of the object is equal to the specified temperature multiplied by the
            pattern value at the joint at the end of the frame object.
        """
        result=self.__Model.FrameObj.GetMatTemp(name)
        print(result)

    def NameList(self):
        """
        ---This function retrieves the names of all defined frame objects---
        inputs:
        return:
        [index,NumberNames,MyName]
        NumberNames(int)-The number of frame object names retrieved by the program.
        MyName(str list)-This is a one-dimensional array of frame object names.
        """
        result=self.__Model.FrameObj.GetNameList()
        return result

    def PDeltaForce(self,name):
        """
        ---This function retrieves the P-Delta force assignments to frame objects. P-Delta forces do not apply to
        curved frame objects. If you request data for a curved frame, an error is returned.
        ---
        inputs:
        name(str)-The name of an existing straight frame object.
        return:
        [index,NumberForces,PDeltaForce,Dir,CSys]
        NumberForces(int)-The number of P-Delta forces assigned to the frame object.
        PDeltaForce(float list)-This is an array of the P-Delta force values assigned to the frame object. [F]
        Dir(int list)-This is an array that contains 0, 1, 2 or 3, indicating the direction of each P-Delta force assignment.
            0 = Frame object local 1-axis direction
            1 = Projected X direction in CSys coordinate system
            2 = Projected Y direction in CSys coordinate system
            3 = Projected Z direction in CSys coordinate system
        CSys(str list)-This is an array that contains the name of the coordinate system in which each projected P-Delta
            force is defined. This item is blank when the Dir item is zero, that is, when the P-Delta force is defined
            in the frame object local 1-axis direction.
        """
        result=self.__Model.FrameObj.GetPDeltaForce(name)
        return result

    def Points(self,name):
        """
        ---This function retrieves the names of the point objects at each end of a specified frame object---
        inputs:
        name(str)-The name of a defined frame object.
        return:
        [index,Point1,Point2]
        Point1(str)-The name of the point object at the I-End of the specified frame object.
        Point2(str)-The name of the point object at the J-End of the specified frame object.
        """
        result=self.__Model.FrameObj.GetPoints(name)
        return result

    def Releases(self,name):
        """
        ---This function retrieves the frame object end release and partial fixity assignments.---
        inputs:
        name(str)-The name of an existing frame object.
        return:
        [index,ii,jj,startValue,endValue]
        ii,jj(bool list)-These are arrays of six booleans indicating the I-End and J-End releases for the frame object.
            ii(0) and jj(0) = U1 release
            ii(1) and jj(1) = U2 release
            ii(2) and jj(2) = U3 release
            ii(3) and jj(3) = R1 release
            ii(4) and jj(4) = R2 release
            ii(5) and jj(5) = R3 release
        startValue,endValue(float list)-These are arrays of six values indicating the I-End and J-End partial fixity
            springs for the frame object.
            StartValue(0) and EndValue(0) = U1 partial fixity [F/L]
            StartValue(1) and EndValue(1) = U2 partial fixity [F/L]
            StartValue(2) and EndValue(2) = U3 partial fixity [F/L]
            StartValue(3) and EndValue(3) = R1 partial fixity [FL/rad]
            StartValue(4) and EndValue(4) = R2 partial fixity [FL/rad]
            StartValue(5) and EndValue(5) = R3 partial fixity [FL/rad]
        """
        result=self.__Model.FrameObj.GetReleases(name)
        return result

    def Section(self,name):
        """
        ---This function retrieves the frame section property assigned to a frame object---
        inputs:
        name(str)-The name of a defined frame object.
        return:
        [index,PropName,SAuto]
        PropName(str)-If no auto select list is assigned to the frame object, this is the name of the frame section
            property assigned to the frame object. If an auto select list is assigned to the frame object, this is
            the name of the frame section property, within the auto select list, which is currently being used as
            the analysis property for the frame object. If this item is None, no frame section property is assigned
            to the frame object.
        SAuto(str)-This is the name of the auto select list assigned to the frame object, if any. If this item is
            returned as a blank string, no auto select list is assigned to the frame object.
        """
        result=self.__Model.FrameObj.GetSection(name)
        return result

    def Spring(self,name):
        """
        ---This function retrieves the spring assignments to a frame object---
        inputs:
        name(str)-The name of an existing frame object.
        return:
        [index,NUmberSprings,MyType,s,SimpleSpringType,LinkProp,SpringLocalOneType,Dir,Plane23Angle,VecX,VecY,VecZ,
        CSys,Ang]
        NumberSprings(int)-The number of springs assignments made to the specified frame object.
        MyType(int list)-Each value in this array is either 1 or 2, indicating the spring property type.
            1 = Simple spring,2 = Link property
        s(float list)-Each value in this array is the simple spring stiffness per unit length of the frame object.
            This item applies only when the corresponding MyType = 1. [F/L2]
        SimpleSpringType(int list)-Each value in this array is 1, 2 or 3, indicating the simple spring type.
            This item applies only when the corresponding MyType = 1.
            1 = Spring resists tension and compression
            2 = Spring resists compression only
            3 = Spring resists tension only
        LinkProp(str list)-Each value in this array is the name of the link property assigned to the spring.
            This item applies only when the corresponding MyType = 2.
        SpringLocalOneType(int list)-Each value in this array is 1, 2 or 3, indicating the method used to specify
            the spring positive local 1-axis orientation.
            1 = Parallel to frame object local axis
            2 = In the frame object 2-3 plane
            3 = User specified direction vector
        Dir(int list)-Each value in this array is 1, 2, 3, -1, -2 or -3, indicating the frame object local axis that
            corresponds to the positive local 1-axis of the spring. This item applies only when the corresponding
            SpringLocalOneType = 1.
        Plane23Angle(float list)-Each value in this array is the angle in the frame object 2-3 plane measured counter
            clockwise from the frame positive 2-axis to the spring positive 1-axis. This item applies only when the
            corresponding SpringLocalOneType = 2. [deg]
        VecX(float list)-Each value in this array is the X-axis or frame local 1-axis component (depending on the
            CSys specified) of the user specified direction vector for the spring local 1-axis. The direction
            vector is in the coordinate system specified by the CSys item. This item applies only when the
            corresponding SpringLocalOneType = 3.
        VecY(float list)-Each value in this array is the Y-axis or frame local 2-axis component (depending on the
            CSys specified) of the user specified direction vector for the spring local 1-axis. The direction vector
            is in the coordinate system specified by the CSys item. This item applies only when the corresponding
            SpringLocalOneType = 3.
        VecZ(float list)-Each value in this array is the X-axis or frame local 3-axis component (depending on the
            CSys specified) of the user specified direction vector for the spring local 1-axis. The direction vector
            is in the coordinate system specified by the CSys item. This item applies only when the corresponding
            SpringLocalOneType = 3.
        CSys(str list)-Each value in this array is Local (meaning the frame object local coordinate system) or the
            name of a defined coordinate system. This item is the coordinate system in which the user specified
            direction vector, Vec, is specified. This item applies only when the corresponding SpringLocalOneType = 3.
        Ang(float list)-Each value in this array is the angle that the link local 2-axis is rotated from its default
            orientation. This item applies only when the corresponding MyType = 2. [deg]
        """
        result=self.__Model.FrameObj.GetSpring(name)
        return result

    def TCLimits(self,name):
        """
        ---This function retrieves the tension/compression force limit assignments to frame objects.The function
        returns zero if the assignments are successfully retrieved, otherwise it returns a nonzero value.Note that
        the tension and compression limits are used only in nonlinear analyses.
        ---
        inputs:
        name(str)-The name of an existing frame object.
        return:
        [index,LimitCompressionExists,LimitCompression,LimitTensionExists,LimitTension]
        LimitCompressionExists(bool)-This item is True if a compression force limit exists for the frame object.
        LimitCompression(float)-The compression force limit for the frame object. [F]
        LimitTensionExists(bool)-This item is True if a tension force limit exists for the frame object.
        LimitTension(float)-The tension force limit for the frame object. [F]
        """
        result=self.__Model.FrameObj.GetTCLimits(name)
        return result

    def TransformationMatrix(self,name):
        """
        ---The function returns zero if the frame object transformation matrix is successfully retrieved; otherwise
        it returns a nonzero value.
        ---
        inputs:
        name(str)-The name of an existing frame object.
        return:
        [index,value]
        value(float list)-Value is an array of nine direction cosines that define the transformation matrix.The following
            matrix equation shows how the transformation matrix is used to convert items from the frame object local
            coordinate system to the global coordinate system.
            In the equation, c0 through c8 are the nine values from the transformation array, (Local1, Local2, Local3)
            are an item (such as a load) in the object local coordinate system, and (GlobalX, GlobalY, GlobalZ) are
            the same item in the global coordinate system.The transformation from the local coordinate system to the
            present coordinate system is the same as that shown above for the global system if you substitute the
            present system for the global system.
        """
        result=self.__Model.FrameObj.GetTransformationMatrix(name)
        return result

class SapFrameObj:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model
        self.Set = FrameObj_Set(Sapobj)
        self.Get = FrameObj_Get(Sapobj)

    def AddByCoord(self,xi,yi,zi,xj,yj,zj,propName="Default",userName="",Csys="Global"):
        """
        ---This function adds a new frame object whose end points are at the specified coordinates---
        inputs:
        xi,yi,zi(float)-The coordinates of the I-End of the added frame object. The coordinates are in the
            coordinate system defined by the CSys item.
        xj,yj,zj(float)-The coordinates of the I-End of the added frame object. The coordinates are in
            the coordinate system defined by the CSys item.
        propName(str)-This is Default, None, or the name of a defined frame section property.If it is Default,
            the program assigns a default section property to the frame object. If it is None, no section
            property is assigned to the frame object. If it is the name of a defined frame section property,
            that property is assigned to the frame object.
        userName(str)-This is an optional user specified name for the frame object. If a UserName is specified
            and that name is already used for another frame object, the program ignores the UserName.
        Csys(str)-The name of the coordinate system in which the frame object end point coordinates are defined.
        """
        #name(str)-This is the name that the program ultimately assigns for the frame object. If no UserName is
        #specified, the program assigns a default name to the frame object. If a UserName is specified and
        #that name is not used for another frame, cable or tendon object, the UserName is assigned to the
        #frame object, otherwise a default name is assigned to the frame object.
        name=""
        self.__Model.FrameObj.AddByCoord(xi,yi,zi,xj,yj,zj,name,propName,userName,Csys)

    def AddByPoint(self,Point1,Point2,propName="Default",userName=""):
        """
        ---This function adds a new frame object whose end points are specified by name---
        inputs:
        Point1(str)-The name of a defined point object at the I-End of the added frame object.
        Point2(str)-The name of a defined point object at the J-End of the added frame object.
        propName(str)-This is Default, None, or the name of a defined frame section property.If it is Default,
            the program assigns a default section property to the frame object. If it is None, no section
            property is assigned to the frame object. If it is the name of a defined frame section property,
            that property is assigned to the frame object.
        userName(str)-This is an optional user specified name for the frame object. If a UserName is specified
            and that name is already used for another frame object, the program ignores the UserName.
        """
        # name(str)-This is the name that the program ultimately assigns for the frame object. If no UserName is
        # specified, the program assigns a default name to the frame object. If a UserName is specified and
        # that name is not used for another frame, cable or tendon object, the UserName is assigned to the
        # frame object, otherwise a default name is assigned to the frame object.
        name = ""
        self.__Model.FrameObj.AddByPoint(Point1,Point2,name,propName,userName)

    def ChangeName(self,name,newName):
        """
        ---The function returns zero if the new name is successfully applied, otherwise it returns a nonzero value---
        inputs:
        name(str)-The existing name of a defined frame object.
        newName(str)-The new name for the frame object.
        """
        self.__Model.FrameObj.ChangeName(name,newName)

    def Count(self,myType="All"):
        """
        ---This function returns a count of the frame objects in the model. Depending on the value of the MyType item,
            the count may be of all frame objects in the model, just the straight frame objects in the model or just
            the curved frame objects in the model---
        inputs:
        myType(str)-This is All, Straight, or Curved.
            All returns a count of all frame objects in the model, including both straight and curved frame objects.
            Straight returns a count of all straight frame objects in the model. Curved returns a count of all curved
            frame objects in the model.
        """
        countNum=self.__Model.FrameObj.Count(myType)
        return countNum

    def Delete(self,name,itemType=0):
        """
        ---The function deletes frame objects.---
        inputs:
        name(str)-The name of an existing frame object or group depending on the value of the ItemType item.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored.
        """
        self.__Model.FrameObj.Delete(name,itemType)



class CableObj_Set:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def CableData(self,name,CableType,NumSegs,Weight,ProjectedLoad,Value,UseDeformedGeom=False,
                                     ModelUsingFrames=False):
        """
        ---This function assigns the cable definition parameters to a cable object.---
        inputs:
        name(str)-The name of a defined cable object.
        CableType(int)-This is 1, 2, 3, 4, 5, 6, 7, 8, or 9, indicating the cable definition parameter.
            1 = Minimum tension at I-End
            2 = Minimum tension at J-End
            3 = Tension at I-End
            4 = Tension at J-End
            5 = Horizontal tension component
            6 = Maximum vertical sag
            7 = Low-point vertical sag
            8 = Undeformed length
            9 = Relative undeformed length
        NumSegs(int)-This is the number of segments into which the program internally divides the cable.
        Weight(float)-The added weight per unit length used when calculating the cable shape. [F/L]
        ProjectedLoad(float)-The projected uniform gravity load used when calculating the cable shape. [F/L]
        Value(float list)-This is the value of the parameter used to define the cable shape. The item that Value
            represents depends on the CableType item.
            CableType = 1: Not Used
            CableType = 2: Not Used
            CableType = 3: Tension at I-End [F]
            CableType = 4: Tension at J-End [F]
            CableType = 5: Horizontal tension component [F]
            CableType = 6: Maximum vertical sag [L]
            CableType = 7: Low-point vertical sag [L]
            CableType = 8: Undeformed length [L]
            CableType = 9: Relative undeformed length
        UseDeformedGeom(bool)-If this item is True, the program uses the deformed geometry for the cable object;
            otherwise it uses the undeformed geometry.
        ModelUsingFrames(bool)-If this item is True, the analysis model uses frame elements to model the cable
            instead of using cable elements.
        """
        self.__Model.CableObj.SetCableData(name,CableType,NumSegs,Weight,ProjectedLoad,Value,UseDeformedGeom,ModelUsingFrames)

    def GroupAssign(self,name,groupName,Remove=False,itemType=0):
        """
        ---This function adds or removes cable objects from a specified group---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        groupName(str)-The name of an existing group to which the assignment is made.
        Remove(bool)-If this item is False, the specified cable objects are added to the group specified by
            the GroupName item. If it is True, the cable objects are removed from the group.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.CableObj.SetGroupAssign(name,groupName,Remove,itemType)

    def LoadDeformation(self,name,loadPat,d,itemType=0):
        """
        ---This function assigns deformation loads to cable objects---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        d(float)-This is the axial deformation load value. [L]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.CableObj.SetLoadDeformation(name,loadPat,d,itemType)

    def LoadDistributed(self,name,loadPat,myType,Dir,Value,CSys="Global",Replace=True,itemType=0):
        """
        ---This function assigns uniform distributed loads over the full length of cable objects---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        myType(int)-This is 1 or 2, indicating the type of distributed load.
            1 = Force per unit length,2 = Moment per unit length
        Dir(int)-This is 1, 2, 3, 4, 5, 6 or 10, indicating the direction of the load.
            1 = Local 1 axis (only applies when CSys is Local)
            2 = Local 2 axis (only applies when CSys is Local)
            3 = Local 3 axis (only applies when CSys is Local)
            4 = X direction (does not apply when CSys is Local)
            5 = Y direction (does not apply when CSys is Local)
            6 = Z direction (does not apply when CSys is Local)
            10 = Gravity direction (only applies when CSys is Global)
            The positive gravity direction (see Dir = 10) is in the negative Global Z direction.
        Value(float)-This is the load value of the distributed load. The distributed load is applied over
            the full length of the cable. [F/L] when MyType is 1 and [FL/L] when MyType is 2
        CSys(str)-This is Local or the name of a defined coordinate system. It is the coordinate system
            in which the loads are specified.
        Replace(bool)-If this item is True, all previous loads, if any, assigned to the specified cable object(s),
            in the specified load pattern, are deleted before making the new assignment.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.CableObj.SetLoadDistributed(name,loadPat,myType,Dir,Value,CSys,Replace,itemType)

    def LoadGravity(self,name,loadPat,x,y,z,Replace=True,CSys="Global",itemType=0):
        """
        ---This function assigns gravity load multipliers to cable objects---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        x,y,z(float)-These are the gravity load multipliers in the x, y and z directions of the specified coordinate system.
        Replace(bool)-If this item is True, all previous gravity loads, if any, assigned to the specified cable object(s),
            in the specified load pattern, are deleted before making the new assignment.
        CSys(str)-The coordinate system in which the x, y and z multipliers are specified.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.CableObj.SetLoadGravity(name,loadPat,x,y,z,Replace,CSys,itemType)

    def LoadStrain(self,name,loadPat,Strain,Replace=True,PatternName="",itemType=0):
        """
        ---This function assigns strain loads to cable objects---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        Strain(float)-This is the axial strain load value. [L/L]
        Replace(bool)-If this item is True, all previous strain loads, if any, assigned to the specified cable
            object(s), in the specified load pattern, are deleted before making the new assignment.
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the strain load for
            the cable object is uniform along the object at the value specified by Strain.If PatternName is the
            name of a defined joint pattern, the strain load for the cable object is based on the specified
            strain value multiplied by the pattern value at the joints at each end of the cable object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.CableObj.SetLoadStrain(name,loadPat,Strain,Replace,PatternName,itemType)

    def LoadTargetForce(self,name,loadPat,P,RD,itemType=0):
        """
        ---This function assigns target forces to cable objects---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        P(float)-This is the axial target force value. [F]
        RD(float)-This is the relative distance along the cable object to the location where the target force
            value applies. The relative distance must be between 0 and 1, 0 <= RD <=1.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.CableObj.SetLoadTargetForce(name,loadPat,P,RD,itemType)

    def LoadTemperature(self,name,loadPat,Val,PatternName="",Replace=True,itemType=0):
        """
        ---This function assigns temperature loads to cable objects---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        Val(float)-This is the temperature change value. [T]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the temperature load
            for the cable object is uniform along the object at the value specified by Val.If PatternName is the name
            of a defined joint pattern, the temperature load for the cable object is based on the specified temperature
            value multiplied by the pattern value at the joints at each end of the cable object.
        Replace(bool)-If this item is True, all previous temperature loads, if any, assigned to the specified cable
            object(s), in the specified load case, are deleted before making the new assignment.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.CableObj.SetLoadTemperature(name,loadPat,Val,PatternName,Replace,itemType)

    def Mass(self,name,MassOverL,Replace=False,itemType=0):
        """
        ---This function assigns mass per unit length to cable objects---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        MassOverL(float)-The mass per unit length assigned to the cable object. [M/L]
        Replace(bool)-If this item is True, all existing mass assignments to the cable object are removed before
            assigning the specified mas. If it is False, the specified mass is added to any mass already assigned
            to the cable object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.CableObj.SetMass(name,MassOverL,Replace,itemType)

    def MatTemp(self,name,Temp,PatternName="",itemType=0):
        """
        ---This function assigns material temperatures to cable objects.---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        Temp(float)-This is the material temperature value assigned to the cable object. [T]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the material temperature
            for the cable object is uniform along the object at the value specified by Temp.If PatternName is the name
            of a defined joint pattern, the material temperature for the cable object may vary from one end to the
            other. The material temperature at each end of the object is equal to the specified temperature multiplied
            by the pattern value at the joint at the end of the cable object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.CableObj.SetMatTemp(name,Temp,PatternName,itemType)

    def Property(self,name,PropName,itemType=0):
        """
        ---This function assigns a cable property to a cable object---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        PropName(str)-The name of a cable property to be assigned to the specified cable object(s).
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.CableObj.SetProperty(name,PropName,itemType)

class CableObj_Get:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def CableData(self,name):
        """
        ---This function retrieves definition data for a specified cable object.---
        inputs:
        name(str)-The name of a defined cable object.
        retrurn:
        [index,CableType,NumSegs,Weight,ProjectedLoad,UseDeformedGeom,ModelUsingFrames,Parameter]
        CableType(int)-This is 1, 2, 3, 4, 5, 6, 7, 8, or 9, indicating the cable definition parameter.
            1 = Minimum tension at I-End
            2 = Minimum tension at J-End
            3 = Tension at I-End
            4 = Tension at J-End
            5 = Horizontal tension component
            6 = Maximum vertical sag
            7 = Low-point vertical sag
            8 = Undeformed length
            9 = Relative undeformed length
        NumSegs(int)-This is the number of segments into which the program internally divides the cable.
        Weight(float)-The added weight per unit length used when calculating the cable shape. [F/L]
        ProjectedLoad(float)-The projected uniform gravity load used when calculating the cable shape. [F/L]
        UseDeformedGeom(bool)-If this item is True, the program uses the deformed geometry for the cable object;
            otherwise it uses the undeformed geometry.
        ModelUsingFrames(bool)-If this item is True, the analysis model uses frame elements to model the cable
            instead of using cable elements.
        Parameter(float list)-This is an array of parameters related to the cable shape. The array is dimensioned by Sap2000.
            Parameter(0) = Tension at I-End [F]
            Parameter(1) = Tension at J-End [F]
            Parameter(2) = Horizontal tension component [F]
            Parameter(3) = Maximum deformed vertical sag [L]
            Parameter(4) = Deformed low-point vertical sag [L]
            Parameter(5) = Deformed length [L]
            Parameter(6) = Deformed relative length
            Parameter(7) = Maximum undeformed vertical sag [L]
            Parameter(8) = Undeformed low-point vertical sag [L]
            Parameter(9) = Undeformed length [L]
            Parameter(10) = Undeformed relative length
        """
        result=self.__Model.CableObj.GetCableData(name)
        return result

    def CableGeometry(self,name):
        """
        ---This function retrieves geometric data for a specified cable object---
        inputs:
        name(str)-The name of a defined cable object.
        return:
        [index,NumberPoints,x,y,z,sag,distance,RD]
        NumberPoints(int)-The number of points defining the cable geometry.
        x,y,z(float)-The x, y and z coordinates of the considered point on the cable in the coordinate system
            specified by the CSys item. [L]
        sag(float)-The cable vertical sag, measured from the chord, at the considered point. [L]
        Distance(float)-The distance along the cable, measured from the cable I-End, to the considered point. [L]
        RD(float)-The relative distance along the cable, measured from the cable I-End, to the considered point.
        """
        result=self.__Model.CableObj.GetCableGeometry(name)
        return result

    def GroupAssign(self,name):
        """
        ---This function retrieves the names of the groups to which a specified cable object is assigned---
        inputs:
        name(str)-The name of an existing cable object.
        return:
        [index,NumberGroups,Groups]
        NumberGroups(int)-The number of group names retrieved.
        Groups(str)-The names of the groups to which the cable object is assigned.
        """
        result=self.__Model.CableObj.GetGroupAssign(name)
        return result

    def LoadDeformation(self,name):
        """
        ---This function retrieves the deformation load assignments to cable objects.---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        return:
        [index,numberItems,CableName,LoadPat,U1]
        numberItems(int)-The total number of deformation loads retrieved for the specified cable objects.
        CableName(str list)-This is an array that includes the name of the cable object associated with each deformation load.
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each deformation load.
        U1(float list)-This is an array of axial deformation load values. [L]
        """
        result=self.__Model.CableObj.GetLoadDeformation(name)
        return result

    def LoadDistributed(self,name):
        """
        ---This function retrieves the distributed load assignments to cable objects. The loads are uniformly
        distributed over the full length of cable objects.
        ---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        return:
        [index,numberItems,CableName,loadPat,MyType,CSys,Dir,Value]
        numberItems(int)-The total number of distributed loads retrieved for the specified cable objects.
        cableName(str list)-This is an array that includes the name of the cable object associated with each distributed load.
        loadPat(str list)-This is an array that includes the name of the coordinate system in which the distributed
            loads are specified.
        myType(int list)-This is an array that includes 1 or 2, indicating the type of distributed load.
            1 = Force,2 = Moment
        CSys(str list)-This is an array that includes the name of the coordinate system in which each distributed
            load is defined. It may be Local or the name of a defined coordinate system.
        Dir(int)-This is 1, 2, 3, 4, 5, 6 or 10, indicating the direction of the load.
            1 = Local 1 axis (only applies when CSys is Local)
            2 = Local 2 axis (only applies when CSys is Local)
            3 = Local 3 axis (only applies when CSys is Local)
            4 = X direction (does not apply when CSys is Local)
            5 = Y direction (does not apply when CSys is Local)
            6 = Z direction (does not apply when CSys is Local)
            10 = Gravity direction (only applies when CSys is Global)
            The positive gravity direction (see Dir = 10) is in the negative Global Z direction.
        Value(float)-This is the load value of the distributed load. The distributed load is applied over the full
            length of the cable. [F/L] when MyType is 1 and [FL/L] when MyType is 2
        """
        result=self.__Model.CableObj.GetLoadDistributed(name)
        return result

    def LoadGravity(self,name):
        """
        ---This function retrieves the gravity load assignments to cable objects---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        return:
        [index,numberItems,cableName,loadPat,CSys,x,y,z]
        numberItems(int)-The total number of gravity loads retrieved for the specified cable objects.
        cableName(str list)-This is an array that includes the name of the cable object associated with each gravity load.
        loadPat(str list)-This is an array that includes the name of the coordinate system in which the gravity load
            multipliers are specified.
        CSys(str list)-This is an array that includes the name of the coordinate system associated with each gravity load.
        x,y,z(float list)-These are arrays of gravity load multipliers in the x, y and z directions of the specified
            coordinate system.
        """
        result=self.__Model.CableObj.GetLoadGravity(name)
        return result

    def LoadStrain(self,name):
        """
        ---This function retrieves the strain load assignments to cable objects---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        return:
        [index,numberItems,CableName,loadPat,Strain,PatternName]
        numberItems(int)-The total number of strain loads retrieved for the specified cable objects.
        CableName(str list)-This is an array that includes the name of the cable object associated with each strain load.
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each strain load.
        Strain(float list)-This is an array that includes the axial strain value. [L/L]
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify the strain load.
        """
        result=self.__Model.CableObj.GetLoadStrain(name)
        return result

    def LoadTargetForce(self,name):
        """
        ---This function retrieves the target force assignments to cable objects.---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        return:
        [index,numberItems,cableName,LoadPat,P,RD]
        numberItems(int)-The total number of deformation loads retrieved for the specified cable objects.
        cableName(str list)-This is an array that includes the name of the cable object associated with each target force.
        loadPat(str list)-This is an array that includes the name of the load pattern associated with each target force.
        P(float list)-This is an array of axial target force values. [F]
        RD(float list)-This is an array of the relative distances along the cable objects where the axial target force
            values apply.
        """
        result=self.__Model.CableObj.GetLoadTargetForce(name)
        return result

    def LoadTemperature(self,name):
        """
        ---This function retrieves the temperature load assignments to cable objects---
        inputs:
        name(str)-The name of an existing cable object or group, depending on the value of the ItemType item.
        return:
        [index,numberItems,cableName,loadPat,Val,PatternName]
        numberItems(int)-The total number of temperature loads retrieved for the specified cable objects.
        cableName(str list)-This is an array that includes the name of the cable object associated with each temperature load.
        loadPat(str list)-This is an array that includes the name of the load pattern associated with each temperature load.
        Val(float list)-This is an array that includes the temperature load value. [T]
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify the
            temperature load.
        """
        result=self.__Model.CableObj.GetLoadTemperature(name)
        return result

    def Mass(self,name):
        """
        ---This function retrieves the mass per unit length assignment for cable objects---
        inputs:
        name(str)-The name of an existing cable object.
        return:
        [index,massOverL]
        massOverL(float)-The mass per unit length assigned to the cable object. [M/L]
        """
        result=self.__Model.CableObj.GetMass(name)
        return result

    def MatTemp(self,name):
        """
        ---This function retrieves the material temperature assignments to cable objects.---
        inputs:
        name(str)-The name of an existing cable object.
        return:
        [index,Temp,PatternName]
        Temp(float)-This is the material temperature value assigned to the cable object. [T]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the material temperature
            for the cable object is uniform along the object at the value specified by Temp.If PatternName is the name
            of a defined joint pattern, the material temperature for the cable object may vary from one end to the other.
            The material temperature at each end of the object is equal to the specified temperature multiplied by the
            pattern value at the joint at the end of the cable object.
        """
        result=self.__Model.CableObj.GetMatTemp(name)
        return result

    def NameList(self):
        """
        ---This function retrieves the names of all defined cable objects---
        return:
        [index,numberNames,myName]
        numberNames(int)-The number of cable object names retrieved by the program.
        myName(str list)-This is a one-dimensional array of cable object names.
        """
        result=self.__Model.CableObj.GetNameList()
        return result

    def Points(self,name):
        """
        ---This function retrieves the names of the point objects at each end of a specified cable object.---
        inputs:
        name(str)-The name of a defined cable object.
        return:
        [index,Point1,Point2]
        Point1(str)-The name of the point object at the I-End of the specified cable object.
        Point2(str)-The name of the point object at the J-End of the specified cable object.
        """
        result=self.__Model.CableObj.GetPoints(name)
        return result

    def Property(self,name):
        """
        ---This function retrieves the cable property assigned to a cable object---
        inputs:
        name(str)-The name of a defined cable object.
        return:
        [index,PropName]
        PropName(str)-The name of the cable property assigned to the cable object.
        """
        result=self.__Model.CableObj.GetProperty(name)
        return result

    def TransformationMatrix(self,name):
            """
            ---The function returns zero if the cable object transformation matrix is successfully retrieved; otherwise
            it returns a nonzero value.
            ---
            inputs:
            name(str)-The name of an existing cable object.
            return:
            [index,value]
            value(float list)-Value is an array of nine direction cosines that define the transformation matrix.The following
                matrix equation shows how the transformation matrix is used to convert items from the cable object local
                coordinate system to the global coordinate system.In the equation, c0 through c8 are the nine values from the
                transformation array, (Local1, Local2, Local3) are an item (such as a load) in the object local coordinate
                system, and (GlobalX, GlobalY, GlobalZ) are the same item in the global coordinate system.The transformation
                from the local coordinate system to the present coordinate system is the same as that shown above for the
                global system if you substitute the present system for the global system.
            """
            result=self.__Model.CableObj.GetTransformationMatrix(name)
            return result

class SapCableObj:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model
        self.Set = CableObj_Set(Sapobj)
        self.Get = CableObj_Get(Sapobj)

    def AddByCoord(self,xi,yi,zi,xj,yj,zj,propName="Default",UserName="",CSys="Global"):
        """
        ---This function adds a new cable object whose end points are at the specified coordinates.---
        inputs:
        xi,yi,zi(float)-The coordinates of the I-End of the added cable object. The coordinates are in the coordinate
            system defined by the CSys item.
        xj,yj,zj(float)-The coordinates of the J-End of the added cable object. The coordinates are in the coordinate
            system defined by the CSys item.
        propName(str)-This is Default or the name of a defined cable property.If it is Default, the program assigns
            a default cable property to the cable object. If it is the name of a defined cable property, that property
            is assigned to the cable object.
        UserName(str):This is an optional user specified name for the cable object. If a UserName is specified and that
            name is already used for another cable object, the program ignores the UserName.
        CSys(str)-The name of the coordinate system in which the cable object end point coordinates are defined.
        """
        #This is the name that the program ultimately assigns for the cable object. If no UserName is specified,n
        # the program assigns a default name to the cable object. If a UserName is specified and that name is not
        # used for another frame, cable or tendon object, the UserName is assigned to the cable object; otherwise a
        # default name is assigned to the cable object.
        name=""
        self.__Model.CableObj.AddByCoord(xi,yi,zi,xj,yj,zj,name,propName,UserName,CSys)

    def AddByPoint(self,Point1,Point2,PropName="Default",UserName=""):
        """
        ---This function adds a new cable object whose end points are specified by name---
        inputs:
        Point1(str)-The name of a defined point object at the I-End of the added cable object.
        Point2(str)-The name of a defined point object at the J-End of the added cable object.
        PropName(str)-This is Default or the name of a defined cable property.If it is Default, the program assigns a
            default cable property to the cable object. If it is the name of a defined cable property, that property
            is assigned to the cable object.
        UserName(str)-This is an optional user specified name for the cable object. If a UserName is specified and that
        name is already used for another cable object, the program ignores the UserName.
        """
        # This is the name that the program ultimately assigns for the cable object. If no UserName is specified,n
        # the program assigns a default name to the cable object. If a UserName is specified and that name is not
        # used for another frame, cable or tendon object, the UserName is assigned to the cable object; otherwise a
        # default name is assigned to the cable object.
        name = ""
        self.__Model.CableObj.AddByPoint(Point1,Point2,name,PropName,UserName)

    def ChangeName(self,name,newName):
        """
        ---The function returns zero if the new name is successfully applied, otherwise it returns a nonzero value.---
        inputs:
        name(str)-The existing name of a defined cable object.
        newName(str)-The new name for the cable object.
        """
        self.__Model.CableObj.ChangeName(name,newName)

    def Count(self):
        """
        ---This function returns a count of the cable objects in the model.---
        """
        result=self.__Model.CableObj.Count()
        return result



class TendonObj_Set:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def Discretization(self,name,Value,itemType=0):
        """
        ---This function assigns a maximum discretization length to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        Value(float)-The maximum discretization length for the tendon. [L]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.TendonObj.SetDiscretization(name,Value,itemType)

    def GroupAssign(self,name,GroupName,Remove=False,itemType=0):
        """
        ---This function adds or removes tendon objects from a specified group.---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        GroupName(str)-The name of an existing group to which the assignment is made.
        Remove(bool)-If this item is False, the specified tendon objects are added to the group specified by the
            GroupName item. If it is True, the tendon objects are removed from the group.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.TendonObj.SetGroupAssign(name,GroupName,Remove,itemType)

    def LoadDeformation(self,name,LoadPat,d,itemType=0):
        """
        ---This function assigns deformation loads to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        LoadPat(str)-The name of a defined load pattern.
        d(float)-This is the axial deformation load value. [L]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.TendonObj.SetLoadDeformation(name,LoadPat,d,itemType)

    def LoadedGroup(self,name,GroupName,itemType=0):
        """
        ---This function makes the loaded group assignment to tendon objects. A tendon object transfers its load
        to any object that is in the specified group.
        ---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        GroupName(str)-This is the name of an existing group. All objects in the specified group can be loaded by the tendon.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignored
        """
        self.__Model.TendonObj.SetLoadedGroup(name,GroupName,itemType)

    def LoadForceStress(self,name,loadPat,JackFrom,LoadType,Value,CurvatureCoeff,WobbleCoeff,
                                            LossAnchorage,LossShortening,LossCreep,LossShrinkage,LossSteelRelax,
                                            Replace=True,itemType=0):
        """
        ---This function assigns force/stress loads to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        JackFrom(int)-This is 1, 2 or 3, indicating how the tendon is jacked.
            1 = Tendon jacked from I-End
            2 = Tendon jacked from J-End
            3 = Tendon jacked from both ends
        LoadType(int)-This is either 0 or 1, indicating how the type of load.
            0 = Force,1 = Stress
        Value(float)-This is the load value. [F] whenLoadType is 0, and [F/L2] when Loadtype is 1
        CurvatureCoeff(float)-The curvature coefficient used when calculating friction losses.
        WobbleCoeff(float)-The wobble coefficient used when calculating friction losses. [1/L]
        LossAnchorage(float)-The anchorage set slip. [L]
        LossShortening(float)-The tendon stress loss due to elastic shortening. [F/L2]
        LossCreep(float)-The tendon stress loss due to creep. [F/L2]
        LossShrinkage(float)-The tendon stress loss due to shrinkage. [F/L2]
        LossSteelRelax(float)-The tendon stress loss due to tendon steel relaxation. [F/L2]
        Replace(bool)-If this item is True, all previous force/stress loads, if any, assigned to the specified
            tendon object(s), in the specified load case, are deleted before making the new assignment.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.TendonObj.SetLoadForceStress(name,loadPat,JackFrom,LoadType,Value,CurvatureCoeff,WobbleCoeff,
                                            LossAnchorage,LossShortening,LossCreep,LossShrinkage,LossSteelRelax,
                                            Replace,itemType)

    def LoadGravity(self,name,loadPat,x,y,z,Replace=True,CSys="Global",itemType=0):
        """
        ---This function assigns gravity load multipliers to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        loadPat(str)-The name of a defined load pattern.
        x,y,z(float)-These are the gravity load multipliers in the x, y and z directions of the specified coordinate system.
        Replace(bool)-If this item is True, all previous gravity loads, if any, assigned to the specified tendon
            object(s), in the specified load pattern, are deleted before making the new assignment.
        CSys(str)-The coordinate system in which the x, y and z multipliers are specified.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.TendonObj.SetLoadGravity(name,loadPat,x,y,z,Replace,CSys,itemType)

    def LoadStrain(self,name,LoadPat,Strain,Replace=True,PatternName="",itemType=0):
        """
        ---This function assigns strain loads to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        LoadPat(str)-The name of a defined load pattern.
        Strain(float)-This is the axial strain load value. [L/L]
        Replace(bool)-If this item is True, all previous strain loads, if any, assigned to the specified tendon
            object(s), in the specified load pattern, are deleted before making the new assignment.
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the strain load for the
            tendon object is uniform along the object at the value specified by Strain.If PatternName is the name of
            a defined joint pattern, the strain load for the tendon object is based on the specified strain value
            multiplied by the pattern value at the joints at each end of the tendon object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.TendonObj.SetLoadStrain(name,LoadPat,Strain,Replace,PatternName,itemType)

    def LoadTemperature(self,name,LoadPat,Val,PatternName="",Replace=True,itemType=0):
        """
        ---This function assigns temperature loads to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group depending on the value of the ItemType item.
        LoadPat(str)-The name of a defined load pattern.
        Val(float)-This is the temperature change value. [T]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the temperature load
            for the tendon object is uniform along the object at the value specified by Val.If PatternName is the
            name of a defined joint pattern, the temperature load for the tendon object is based on the specified
            temperature value multiplied by the pattern value at the joints at each end of the tendon object.
        Replace(bool)-If this item is True, all previous temperature loads, if any, assigned to the specified tendon
            object(s), in the specified load case, are deleted before making the new assignment.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.TendonObj.SetLoadTemperature(name,LoadPat,Val,PatternName,Replace,itemType)

    def LocalAxes(self,name,Ang,itemType=0):
        """
        ---This function assigns a local axis angle to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        Ang(float)-This is the angle that the local 2 and 3 axes are rotated about the positive local 1 axis,
            from the default orientation. The rotation for a positive angle appears counter clockwise when the
            local +1 axis is pointing toward you. [deg]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.TendonObj.SetLocalAxes(name,Ang,itemType)

    def MatTemp(self,name,Temp,PatternName="",itemType=0):
        """
        ---This function assigns material temperatures to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        Temp(float)-This is the material temperature value assigned to the tendon object. [T]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the material temperature
            for the tendon object is uniform along the object at the value specified by Temp.If PatternName is the name
            of a defined joint pattern, the material temperature for the tendon object may vary from one end to the
            other. The material temperature at each end of the object is equal to the specified temperature multiplied
            by the pattern value at the joint at the end of the tendon object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.TendonObj.SetMatTemp(name,Temp,PatternName,itemType)

    def Property(self,name,PropName,itemType=0):
        """
        ---This function assigns a tendon property to a tendon object---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        PropName(str)-This is None or the name of a tendon property to be assigned to the specified tendon object(s).
            None means that no property is assigned to the tendon.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.TendonObj.SetProperty(name,PropName,itemType)

    def TCLimits(self,name,LimitCompressionExists,LimitCompression,
                                     LimitTensionExists,LimitTension,itemType=0):
        """
        ---This function makes tension/compression force limit assignments to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        LimitCompressionExists(bool)-This item is True if a compression force limit exists for the tendon object.
        LimitCompression(float)-The compression force limit for the tendon object. [F]
        LimitTensionExists(bool)-This item is True if a tension force limit exists for the tendon object.
        LimitTension(float)-The tension force limit for the tendon object. [F]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.TendonObj.SetTCLimits(name,LimitCompressionExists,LimitCompression,
                                     LimitTensionExists,LimitTension,itemType)

    def TendonData(self,name,NumberPoints,MyType,x,y,z,CSys="Global"):
        """
        ---This function assigns the tendon geometric definition parameters to a tendon object---
        inputs:
        name(str)-The name of a defined tendon object.
        NumberPoints(int)-The number of items used to define the tendon geometry.
        MyType(int)-This is an array of values that are 1, 3, 6, 7, 8, or 9, indicating the tendon geometry definition
            parameter for the specified point.
            1 = Start of tendon
            2 = The segment preceding the point is linear
            6 = The specified point is the end of a parabola
            7 = The specified point is an intermediate point on a parabola
            8 = The specified point is the end of a circle
            9 = The specified point is an intermediate point on a parabola
            The first point should always have a MyType value of 1. If it is not equal to 1, the program uses 1 anyway.
            MyType of 6 through 9 is based on using three points to calculate a parabolic or circular arc. MyType 6 and
            8 use the specified point and the two previous points as the three points. MyType 7 and 9 use the specified
            point and the points just before and after the specified point as the three points.
        x(float list)-This is an array of the X (or local 1) coordinate of each point in the coordinate system
            specified by CSys. [L]
        y(float list)-This is an array of the Y (or local 2) coordinate of each point in the coordinate system
            specified by CSys. [L]
        z(float list)-This is an array of the Z (or local 3) coordinate of each point in the coordinate system
            specified by CSys. [L]
        CSys(bool)-This is the coordinate system in which the x, y and z coordinate parameters are defined.
            It is Local or the name of a defined coordinate system.Local means that the point coordinates
            are in the local system of the specified tendon object with the origin assumed to be at the I-End of the tendon.
        """
        self.__Model.TendonObj.SetTendonData(name,NumberPoints,MyType,x,y,z,CSys)

class TendonObj_Get:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def Discretization(self,name):
        """
        ---This function retrieves the maximum discretization length assignment for tendon objects---
        inputs:
        name(str)-The name of an existing tendon object
        return:
        [index,Value]
        Value(float)-The maximum discretization length for the tendon. [L]
        """
        result=self.__Model.TendonObj.GetDiscretization(name)
        return result

    def GroupAssign(self,name):
        """
        ---This function retrieves the names of the groups to which a specified tendon object is assigned---
        inputs:
        name(str)-The name of an existing tendon object
        return:
        [index,numberGroups,Groups]
        numberGroups(int)-The number of group names retrieved.
        Groups(str)-The names of the groups to which the tendon object is assigned
        """
        result=self.__Model.TendonObj.GetGroupAssign(name)
        return result

    def LoadDeformation(self,name):
        """
        ---This function retrieves the deformation load assignments to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        return:
        [index,NumberItems,TendonName,LoadPat,U1]
        NumberItems(int)-The total number of deformation loads retrieved for the specified tendon objects.
        TendonName(str list)-This is an array that includes the name of the tendon object associated with each deformation load.
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each deformation load
        U1(float list)-This is an array of axial deformation load values. [L]
        """
        result=self.__Model.TendonObj.GetLoadDeformation(name)
        return result

    def LoadedGroup(self,name):
        """
        ---This function retrieves the loaded group for tendon objects. A tendon object transfers its load to any
        object that is in the specified group.
        ---
        inputs:
        name(str)-The name of an existing tendon object
        return:
        [index,GroupName]
        GroupName(str)-This is the name of an existing group. All objects in the specified group can be loaded by the tendon.
        """
        result=self.__Model.TendonObj.GetLoadedGroup(name)
        return result

    def LoadForceStress(self,name):
        """
        ---This function retrieves the force/stress load assignments to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        return:
        [index,NumberItems,TendonName,LoadPat,JackFrom,LoadType,Value,CurvatureCoeff,WobbleCoeff,LossAnchorage,
        LossShortening,LossCreep,LossShrinkage,LossSteelRelax]
        NumberItems(int)-The total number of temperature loads retrieved for the specified tendon objects
        TendonName(str list)-This is an array that includes the name of the tendon object associated with each temperature load
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each temperature load
        JackFrom(int list)-This is an array that includes 1, 2 or 3, indicating how the tendon is jacked.
            1 = Tendon jacked from I-End
            2 = Tendon jacked from J-End
            3 = Tendon jacked from both ends
        LoadType(int list)-This is an array that includes either 0 or 1, indicating how the type of load.
            0 = Force,1 = Stress
        Value(float list)-This is an array that includes the load value. [F] when LoadType is 0, and [F/L2] when Loadtype is 1
        CurvatureCoeff(float list)-This is an array that includes the curvature coefficient used when calculating friction losses.
        WobbleCoeff(float list)-This is an array that includes the wobble coefficient used when calculating friction losses. [1/L]
        LossAnchorage(float list)-This is an array that includes the anchorage set slip. [L]
        LossShortening(float list)-This is an array that includes the tendon stress loss due to elastic shortening. [F/L2]
        LossCreep(float list)-This is an array that includes the tendon stress loss due to creep. [F/L2]
        LossShrinkage(float list)-This is an array that includes the tendon stress loss due to shrinkage. [F/L2]
        LossSteelRelax(float list)-This is an array that includes the tendon stress loss due to tendon steel relaxation. [F/L2]
        """
        result=self.__Model.TendonObj.GetLoadForceStress(name)
        return result

    def LoadGravity(self,name):
        """
        ---This function retrieves the gravity load assignments to tendon objects.---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        return:
        [index,NumberItems,TendonName,LoadPat,CSys,x,y,z]
        NumberItems(int)-The total number of gravity loads retrieved for the specified tendon objects.
        TendonName(str list)-This is an array that includes the name of the tendon object associated with each gravity load
        LoadPat(str list)-This is an array that includes the name of the coordinate system in which the gravity load
            multipliers are specified.
        CSys(str list)-This is an array that includes the name of the coordinate system associated with each gravity load
        x,y,z(float list)-These are arrays of gravity load multipliers in the x, y and z directions of the specified
            coordinate system.
        """
        result=self.__Model.TendonObj.GetLoadGravity(name)
        return result

    def LoadStrain(self,name):
        """
        ---This function retrieves the strain load assignments to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        return:
        [index,NumberItems,TendonName,LoadPat,Strain,PatternName]
        NumberItems(int)-The total number of strain loads retrieved for the specified tendon objects.
        TendonName(str list)-This is an array that includes the name of the tendon object associated with each strain load.
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each strain load.
        Strain(float)-This is an array that includes the axial strain value. [L/L]
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify the strain load.
        """
        result=self.__Model.TendonObj.GetLoadStrain(name)
        return result

    def LoadTemperature(self,name):
        """
        ---This function retrieves the temperature load assignments to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object or group, depending on the value of the ItemType item.
        return:
        [index,NumberItems,TendonName,LoadPat,Val,PatternName]
        NumberItems(int)-The total number of temperature loads retrieved for the specified tendon objects.
        TendonName(str list)-This is an array that includes the name of the tendon object associated with each
            temperature load.
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each temperature load.
        Val(float list)-This is an array that includes the temperature load value. [T]
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify the temperature load
        """
        result=self.__Model.TendonObj.GetLoadTemperature(name)
        return result

    def LocalAxes(self,name):
        """
        ---This function retrieves the tendon local axis angle assignment for tendon objects---
        inputs:
        name(str)-The name of an existing tendon object.
        return:
        [index,Ang]
        Ang(float)-This is the angle that the local 2 and 3 axes are rotated about the positive local 1 axis, from
            the default orientation. The rotation for a positive angle appears counter clockwise when the local +1
            axis is pointing toward you. [deg]
        """
        result=self.__Model.TendonObj.GetLocalAxes(name)
        return result

    def MatTemp(self,name):
        """
        ---This function retrieves the material temperature assignments to tendon objects---
        inputs:
        [index,Temp,PatternName]
        Temp(float)-This is the material temperature value assigned to the tendon object. [T]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the material temperature
            for the tendon object is uniform along the object at the value specified by Temp.If PatternName is the name
            of a defined joint pattern, the material temperature for the tendon object may vary from one end to the other.
            The material temperature at each end of the object is equal to the specified temperature multiplied by the
            pattern value at the joint at the end of the tendon object.
        """
        result=self.__Model.TendonObj.GetMatTemp(name)
        return result

    def NameList(self):
        """
        ---This function retrieves the names of all defined tendon objects---
        return:
        [index,NumberNames,MyName]
        NumberNames(int)-The number of tendon object names retrieved by the program.
        MyName(str list)-This is a one-dimensional array of tendon object names.
        """
        result=self.__Model.TendonObj.GetNameList()
        return result

    def Points(self,name):
        """
        ---This function retrieves the names of the point objects at each end of a specified tendon object---
        inputs:
        name(str)-The name of a defined tendon object
        return:
        [index,Point1,Point2]
        Point1(str)-The name of the point object at the I-End of the specified tendon object.
        Point2(str)-The name of the point object at the J-End of the specified tendon object.
        """
        result=self.__Model.TendonObj.GetPoints(name)
        return result

    def Property(self,name):
        """
        ---This function retrieves the tendon property assigned to a tendon object---
        inputs:
        name(str)-The name of a defined tendon object.
        return:
        [index,PropName]
        PropName(str)-The name of the tendon property assigned to the tendon object
        """
        result=self.__Model.TendonObj.GetProperty(name)
        return result

    def TCLimits(self,name):
        """
        ---This function retrieves the tension/compression force limit assignments to tendon objects---
        inputs:
        name(str)-The name of an existing tendon object
        return:
        [index,LimitCompressionExists,LimitCompression,LimitTensionExists,LimitTension]
        LimitCompressionExists(bool)-This item is True if a compression force limit exists for the tendon object
        LimitCompression(float)-The compression force limit for the tendon object. [F]
        LimitTensionExists(bool)-This item is True if a tension force limit exists for the tendon object.
        LimitTension(float)-The tension force limit for the tendon object. [F]
        """
        result=self.__Model.TendonObj.GetTCLimits(name)
        return result

    def TendonData(self,name):
        """
        ---This function retrieves the tendon geometric definition parameters for a tendon object---
        inputs:
        name(str)-The name of a defined tendon object
        return:
        [index,NumberItems,MyType,x,y,z]
        NumberItems(int)-The number of items used to define the tendon geometry
        MyType(int list)-This is an array of values that are 1, 3, 6, 7, 8, or 9, indicating the tendon geometry
            definition parameter for the specified point.
            1 = Start of tendon
            2 = The segment preceding the point is linear
            6 = The specified point is the end of a parabola
            7 = The specified point is an intermediate point on a parabola
            8 = The specified point is the end of a circle
            9 = The specified point is an intermediate point on a parabola
            The first point always has a MyType value of 1.MyType of 6 through 9 is based on using three points to
                calculate a parabolic or circular arc. MyType 6 and 8 use the specified point and the two previous
                points as the three points. MyType 7 and 9 use the specified point and the points just before and
                after the specified point as the three points.
        x(float list)-This is an array of the X (or local 1) coordinate of each point in the coordinate system
            specified by CSys. [L]
        y(float list)-This is an array of the Y (or local 2) coordinate of each point in the coordinate system
            specified by CSys. [L]
        z(float list)-This is an array of the Z (or local 3) coordinate of each point in the coordinate system
            specified by CSys. [L]
        """
        result=self.__Model.TendonObj.GetTendonData(name)
        return result

    def TendonGeometry(self,name):
        """
        ---The name of a defined tendon object.---
        inputs:
        name(str)-The name of a defined tendon object.
        return:
        [index,NumberPoints,x,y,z]
        NumberPoints(int)-The number of items used to define the discretized tendon geometry.
        x(float list)-This is an array of the X (or local 1) coordinate of each point in the coordinate system
            specified by CSys. [L]
        y(float list)-This is an array of the Y (or local 2) coordinate of each point in the coordinate system
            specified by CSys. [L]
        z(float list)-This is an array of the Z (or local 3) coordinate of each point in the coordinate system
            specified by CSys. [L]
        """
        result=self.__Model.TendonObj.GetTendonGeometry(name)
        return result

    def TransformationMatrix(self,name):
        """
        ---The function returns zero if the tendon object transformation matrix is successfully retrieved;
        otherwise it returns a nonzero value.
        ---
        inputs:
        name(str)-The name of an existing tendon object.
        return:
        [index,Value]
        Value(float list)-Value is an array of nine direction cosines that define the transformation matrix.The following
            matrix equation shows how the transformation matrix is used to convert items from the tendon object local
            coordinate system to the global coordinate system.In the equation, c0 through c8 are the nine values from
            the transformation array, (Local1, Local2, Local3) are an item (such as a load) in the object local coordinate
            system, and (GlobalX, GlobalY, GlobalZ) are the same item in the global coordinate system.The transformation
            from the local coordinate system to the present coordinate system is the same as that shown above for the global
            system if you substitute the present system for the global system.
        """
        result=self.__Model.TendonObj.GetTransformationMatrix(name)
        return result

class SapTendonObj:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model
        self.Set = TendonObj_Set(Sapobj)
        self.Get = TendonObj_Get(Sapobj)

    def AddByCoord(self,xi,yi,zi,xj,yj,zj,PropName="Default",UserName="",CSsy="Global"):
        """
        ---This function adds a new tendon object whose end points are at the specified coordinates---
        inputs:
        xi,yi,zi(float)-The coordinates of the I-End of the added tendon object. The coordinates are in the coordinate
            system defined by the CSys item.
        xj,yj,zj(float)-The coordinates of the J-End of the added tendon object. The coordinates are in the coordinate
            system defined by the CSys item.
        PropName(str)-This is Default, None or the name of a defined tendon property.If it is Default, the program
            assigns a default tendon property to the tendon object. If it is None, no tendon property is assigned to
            the tendon object. If it is the name of a defined tendon property, that property is assigned to the tendon object.
        UserName(str)-This is an optional user specified name for the tendon object. If a UserName is specified and that
            name is already used for another tendon object, the program ignores the UserName.
        CSys(str)-The name of the coordinate system in which the tendon object end point coordinates are defined.
        """
        # This is the name that the program ultimately assigns for the tendon object. If no UserName is specified,
        # the program assigns a default name to the tendon object. If a UserName is specified and that name is not
        # used for another frame, cable or tendon object, the UserName is assigned to the tendon object; otherwise
        # a default name is assigned to the tendon object.
        name = ""
        self.__Model.TendonObj.AddByCoord(xi,yi,zi,xj,yj,zj,name,PropName,UserName,CSsy)

    def AddByPoint(self,Point1,Point2,PropName="Default",UserName=""):
        """
        ---This function adds a new tendon object whose end points are specified by name---
        inputs:
        Point1(str)-The name of a defined point object at the I-End of the added tendon object.
        Point2(str)-The name of a defined point object at the J-End of the added tendon object.
        PropName(str)-This is Default, None or the name of a defined tendon property.If it is Default, the program
            assigns a default tendon property to the tendon object. If it is None, no tendon property is assigned
            to the tendon object. If it is the name of a defined tendon property, that property is assigned to the
            tendon object.
        UserName(str)-This is an optional user specified name for the tendon object. If a UserName is specified and
            that name is already used for another tendon object, the program ignores the UserName.
        """
        # This is the name that the program ultimately assigns for the tendon object. If no UserName is specified,
        # the program assigns a default name to the tendon object. If a UserName is specified and that name is not
        # used for another frame, cable or tendon object, the UserName is assigned to the tendon object; otherwise
        # a default name is assigned to the tendon object.
        name = ""
        self.__Model.TendonObj.AddByPoint(Point1,Point2,name,PropName,UserName)

    def Count(self):
        """
        ---This function returns a count of the tendon objects in the model---
        """
        result=self.__Model.TendonObj.Count()
        return result


class AreaObj_Set:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def AutoMesh(self,name,MeshType,n1=2,n2=2,MaxSize1=0,MaxSize2=0,PointOnEdgeFromLine=False,
                                   PointOnEdgeFromPoint=False,ExtendCookieCutLines=False,
                                   Rotation=0,MaxSizeGeneral=0,LocalAxesOnEdge=False,LocalAxesOnFace=False,
                                   ResTraintsOnEdge=False,RestraintsOnFace=False,Group="ALL",SubMesh=False,SubMeshSize=0,
                                   itemType=0):
        """
        ---This function makes automatic meshing assignments to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item.
        MeshType(int)-This item is 0, 1, 2, 3, 4, 5 or 6, indicating the automatic mesh type for the area object.
            0 = No automatic meshing
            1 = Mesh area into a specified number of objects
            2 = Mesh area into objects of a specified maximum size
            3 = Mesh area based on points on area edges
            4 = Cookie cut mesh area based on lines intersecting edges
            5 = Cookie cut mesh area based on points
            6 = Mesh area using General Divide Tool
            Mesh options 1, 2 and 3 apply to quadrilaterals and triangles only.
        n1(int)-This item applies when MeshType = 1. It is the number of objects created along the edge of the
            meshed area object that runs from point 1 to point 2.
        n2(int)-This item applies when MeshType = 1. It is the number of objects created along the edge of the
            meshed area object that runs from point 1 to point 3.
        MaxSize1(float)-This item applies when MeshType = 2. It is the maximum size of objects created along the
            edge of the meshed area object that runs from point 1 to point 2. [L]If this item is input as 0, the
            default value is used. The default value is 48 inches if the database units are English or 120 centimeters
            if the database units are metric.
        MaxSize2(float)-This item applies when MeshType = 2. It is the maximum size of objects created along the edge
            of the meshed area object that runs from point 1 to point 3. [L]If this item is input as 0, the default
            value is used. The default value is 48 inches if the database units are English or 120 centimeters if the
            database units are metric.
        PointOnEdgeFromLine(bool)-This item applies when MeshType = 3. If it is True, points on the area object edges
            are determined from intersections of straight line objects included in the group specified by the Group
            item with the area object edges.
        PointOnEdgeFromPoint(bool)-This item applies when MeshType = 3. If it is True, points on the area object edges
            are determined from point objects included in the group specified by the Group item that lie on the area object edges
        ExtendCookieCutLines(bool)-This item applies when MeshType = 4. MeshType = 4 provides cookie cut meshing based
            on straight line objects included in the group specified by the Group item that intersect the area object
            edges. If the ExtendCookieCutLines item is True, all straight line objects included in the group specified
            by the Group item are extended to intersect the area object edges for the purpose of meshing the area object.
        Rotation(float)-This item applies when MeshType = 5. MeshType = 5 provides cookie cut meshing based on two
            perpendicular lines passing through point objects included in the group specified by the Group item.
            By default these lines align with the area object local 1 and 2 axes. The Rotation item is an angle in
            degrees that the meshing lines are rotated from their default orientation. [deg]
        MaxSizeGeneral(float)-This item applies when MeshType = 6. It is the maximum size of objects created by the
            General Divide Tool.If this item is input as 0, the default value is used. The default value is 48 inches
            if the database units are English or 120 centimeters if the database units are metric.
        LocalAxesOnEdge(bool)-If this item is True, and if both points along an edge of the original area object
            have the same local axes, then the program makes the local axes for added points along the edge the
            same as the edge end points.
        LoalAxesOnFace(bool)-If this item is True, and if all points around the perimeter of the original area object
            have the same local axes, the program makes the local axes for all added points the same as the perimeter points.
        RestraintsOnEdge(bool)-If this item is True, and if both points along an edge of the original area object have
            the same restraint/constraint, then, if the added point and the adjacent corner points have the same local
            axes definition, the program includes the restraint/constraint for added points along the edge.
        RestraintsOnFace(bool)-If this item is True, and if all points around the perimeter of the original area object
            have the same restraint/constraint, then, if an added point and the perimeter points have the same local
            axes definition, the program includes the restraint/constraint for the added point.
        Group(str)-The name of a defined group. Some of the meshing options make use of point and line objects
            included in this group.
        SubMesh(bool)-If this item is True, after initial meshing, the program further meshes any area objects that
            have an edge longer than the length specified by the SubMeshSize item.
        SubMeshSize(bool)-This item applies when the SubMesh item is True. It is the maximum size of area objects to
            remain when the auto meshing is complete. [L]If this item is input as 0, the default value is used.
            The default value is 12 inches if the database units are English or 30 centimeters if the database units are metric.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.AreaObj.SetAutoMesh(name,MeshType,n1,n2,MaxSize1,MaxSize2,PointOnEdgeFromLine,
                                   PointOnEdgeFromPoint,ExtendCookieCutLines,Rotation,MaxSizeGeneral,LocalAxesOnEdge,
                                    LocalAxesOnFace,ResTraintsOnEdge,RestraintsOnFace,Group,SubMesh,SubMeshSize,itemType)

    def EdgeConstraint(self,name,ConstraintExists,itemType=0):
        """
        ---This function makes generated edge constraint assignments to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        ConstraintExists(bool)-This item is True if an automatic edge constraint is generated by the program
            for the area object in the analysis model.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.AreaObj.SetEdgeConstraint(name,ConstraintExists,itemType)

    def GroupAssign(self,name,GroupName,Remove=False,itemType=0):
        """
        ---This function adds or removes area objects from a specified group---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item.
        GroupName(str)-The name of an existing group to which the assignment is made.
        Remove(bool)-If this item is False, the specified area objects are added to the group specified by the
            GroupName item. If it is True, the area objects are removed from the group.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.AreaObj.SetGroupAssign(name,GroupName,Remove,itemType)

    def LoadGravity(self,name,LoadPat,x,y,z,Replace=True,CSys="Global",itemType=0):
        """
        ---This function assigns gravity load multipliers to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item.
        LoadPat(str)-The name of a defined load pattern
        x,y,z(float)-These are the gravity load multipliers in the x, y and z directions of the specified coordinate system
        Replace(bool)-If this item is True, all previous gravity loads, if any, assigned to the specified area object(s),
            in the specified load pattern, are deleted before making the new assignment
        CSys(str)-The coordinate system in which the x, y and z multipliers are specified
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.AreaObj.SetLoadGravity(name,LoadPat,x,y,z,Replace,CSys,itemType)

    def LoadPorePressure(self,name,LoadPat,Value,PatternName="",Replace=True,itemType=0):
        """
        ---This function assigns pore pressure loads to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        LoadPat(str(str)-The name of a defined load pattern
        Value(float)-This is the pore pressure value. [F/L2]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the pore pressure
            load for the area object is uniform over the object at the value specified by Value.If PatternName is
            the name of a defined joint pattern, the pore pressure load for the area object is based on the specified
            pore pressure value multiplied by the pattern value at the point objects that define the area object.
        Replace(bool)-If this item is True, all previous pore pressure loads, if any, assigned to the specified area
            object(s), in the specified load case, are deleted before making the new assignment.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.AreaObj.SetLoadPorePressure(name,LoadPat,Value,PatternName,Replace,itemType)

    def LoadRotate(self,name,loadPat,Value,itemType=0):
        """
        ---This function assigns rotate loads to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        loadPat(str)-The name of a defined load pattern
        Value(float)-This is the angular velocity. [Cyc/T]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.AreaObj.SetLoadRotate(name,loadPat,Value,itemType)

    def LoadStrain(self,name,LoadPat,component,Value,Replace=True,PatternName="",itemType=0):
        """
        ---This function assigns strain loads to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        LoadPat(str)-The name of a defined load pattern
        component(int)-This is 1, 2, 3, 4, 5, 6, 7, 8, or 9, indicating the component to which the strain load is applied.
            1 = Strain11,2 = Strain22,3 = Strain12,4 = Curvature11,5 = Curvature22,6 = Curvature12,7 = Strain13
            8 = Strain23,9 = Strain33
        Value(float)-This is the strain load value. [L/L] for Component = 1, 2, 3, 7, 8, and 9 and [1/L] for Component = 4, 5 and 6
        Replace(bool)-If this item is True, all previous strain loads, if any, assigned to the specified area object(s),
            in the specified load pattern, for the specified degree of freedom, are deleted before making the new assignment
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the strain load for the
            area object is uniform over the object at the value specified by Value.If PatternName is the name of a
            defined joint pattern, the strain load for the area object is based on the specified strain value
            multiplied by the pattern value at the corner points of the area object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.AreaObj.SetLoadStrain(name,LoadPat,component,Value,Replace,PatternName,itemType)

    def LoadSurfacePressure(self,name,LoadPat,Face,Value,PatternName="",Replace=True,itemType=0):
        """
        ---This function assigns surface pressure loads to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        LoadPat(str)-The name of a defined load pattern
        Face(int)-This is -1, -2 or a nonzero, positive integer, indicating the area object face to which the
            specified load assignment applies.
            -1 = Bottom face,-2 = Top face,>0 = Edge face
            Note that edge face n is from area object point n to area object point n + 1. For example, edge face
            2 is from area object point 2 to area object point 3.
        Value(float)-This is the surface pressure value. [F/L2]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the surface pressure
            load for the area object face is uniform over the face at the value specified by Value.If PatternName
            is the name of a defined joint pattern, the surface pressure load for the area object face is based on
            the specified surface pressure value multiplied by the pattern value at the point objects that are part of the face.
        Replace(bool)-If this item is True, all previous surface pressure loads, if any, assigned to the specified
            area object(s), in the specified load case, are deleted before making the new assignment.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.AreaObj.SetLoadSurfacePressure(name,LoadPat,Face,Value,PatternName,Replace,itemType)

    def LoadTemperature(self,name,LoadPat,MyType,Value,PatternName="",Replace=True,itemType=0):
        """
        ---This function assigns temperature loads to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        LoadPat(str)-The name of a defined load pattern
        MyType(int)-This is either 1 or 3, indicating the type of temperature load.
            1 = Temperature,3 = Temperature gradient along local 3 axis
        Value(float)-This is the temperature change value. [T] for MyType = 1 and [T/L] for MyType = 3
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the temperature
            load for the area object is uniform over the object at the value specified by Value.If PatternName
            is the name of a defined joint pattern the temperature load for the area object is based on the
            specified temperature value multiplied by the pattern value at the joints that define the area object.
        Replace(bool)-If this item is True, all previous temperature loads, if any, assigned to the specified area
            object(s), in the specified load case, are deleted before making the new assignment
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.AreaObj.SetLoadTemperature(name,LoadPat,MyType,Value,PatternName,Replace,itemType)

    def LoadUniform(self,name,LoadPat,Value,Dir,Replace=True,CSys="Global",itemType=0):
        """
        ---This function assigns uniform loads to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        LoadPat(str)-The name of a defined load pattern
        Value(float)-The uniform load value. [F/L2]
        Dir(int)-This is an integer between 1 and 11, indicating the direction of the load.
            1 = Local 1 axis (only applies when CSys is Local)
            2 = Local 2 axis (only applies when CSys is Local)
            3 = Local 3 axis (only applies when CSys is Local)
            4 = X direction (does not apply when CSys is Local)
            5 = Y direction (does not apply when CSys is Local)
            6 = Z direction (does not apply when CSys is Local)
            7 = Projected X direction (does not apply when CSys is Local)
            8 = Projected Y direction (does not apply when CSys is Local)
            9 = Projected Z direction (does not apply when CSys is Local)
            10 = Gravity direction (only applies when CSys is Global)
            11 = Projected Gravity direction (only applies when CSys is Global)
            The positive gravity direction (see Dir = 10 and 11) is in the negative Global Z direction.
        Replace(bool)-If this item is True, all previous uniform loads, if any, assigned to the specified area
            object(s), in the specified load pattern, are deleted before making the new assignment
        CSys(str)-This is Local or the name of a defined coordinate system, indicating the coordinate system
            in which the uniform load is specified
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.AreaObj.SetLoadUniform(name,LoadPat,Value,Dir,Replace,CSys,itemType)

    def LoadUniformToFrame(self,name,LoadPat,Value,Dir,DistType,Replace=True,CSys="Global",itemType=0):
        """
        ---This function assigns uniform to frame loads to area objects---
        name(str)-The name of an existing area object or group depending on the value of the ItemType item
        LoadPat(str)-The name of a defined load pattern
        Value(float)-The uniform load value. [F/L2]
        Dir(int)-This is an integer between 1 and 11, indicating the direction of the load.
            1 = Local 1 axis (only applies when CSys is Local)
            2 = Local 2 axis (only applies when CSys is Local)
            3 = Local 3 axis (only applies when CSys is Local)
            4 = X direction (does not apply when CSys is Local)
            5 = Y direction (does not apply when CSys is Local)
            6 = Z direction (does not apply when CSys is Local)
            7 = Projected X direction (does not apply when CSys is Local)
            8 = Projected Y direction (does not apply when CSys is Local)
            9 = Projected Z direction (does not apply when CSys is Local)
            10 = Gravity direction (only applies when CSys is Global)
            11 = Projected Gravity direction (only applies when CSys is Global)
            The positive gravity direction (see Dir = 10 and 11) is in the negative Global Z direction.
        DistType(int)-This is either 1 or 2, indicating the load distribution type.
            1 = One-way load distribution
            2 = Two-way load distribution
            One-way distribution is parallel to the area object local 1 axis. Two-way distribution is parallel to
                the area object local 1 and 2 axes.
        Replace(bool)-If this item is True, all previous uniform loads, if any, assigned to the specified area
            object(s), in the specified load pattern, are deleted before making the new assignment
        CSys(str)-This is Local or the name of a defined coordinate system, indicating the coordinate system in
            which the uniform load is specified
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.AreaObj.SetLoadUniformToFrame(name,LoadPat,Value,Dir,DistType,Replace,CSys,itemType)

    def LoadWindPressure_1(self,name,LoadPat,MyType,Cp,DistributionType,itemType=0):
        """
        ---This function assigns wind pressure loads to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item.
        LoadPat(str)-The name of a defined load pattern
        MyType(int)-This is either 1 or 2, indicating the wind pressure type.
            1 = Windward, pressure varies over height
            2 = Other, pressure is constant over height
        Cp(float)-This is the wind pressure coefficient
        DistributionType(int)-This is either 1 or 2, indicating the distribution type.
            1 = To Joints,2 = To Frames – One-way,3 = To Frames – Two-way
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.AreaObj.SetLoadWindPressure_1(name,LoadPat,MyType,Cp,DistributionType,itemType)

    def LocalAxes(self,name,Ang,itemType=0):
        """
        ---This function assigns a local axis angle to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        Ang(float)-This is the angle that the local 1 and 2 axes are rotated about the positive local 3 axis
            from the default orientation. The rotation for a positive angle appears counter clockwise when
            the local +3 axis is pointing toward you. [deg]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.AreaObj.SetLocalAxes(name,Ang,itemType)

    def Mass(self,name,MassOverL,Replace=False,itemType=0):
        """
        ---This function assigns mass per unit area to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        MassOverL(float)-The mass per unit area assigned to the area object. [M/L2]
        Replace(bool)-If this item is True, all existing mass assignments to the area object are removed before
            assigning the specified mas. If it is False, the specified mass is added to any existing mass already
            assigned to the area object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.AreaObj.SetMass(name,MassOverL,Replace,itemType)

    def MatTemp(self,name,Temp,PatternName="",itemType=0):
        """
        ---This function assigns material temperatures to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        Temp(float)-This is the material temperature value assigned to the area object. [T]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the material temperature
            for the area object is uniform over the object at the value specified by Temp.If PatternName is the name
            of a defined joint pattern, the material temperature for the area object may vary. The material temperature
            at each corner point around the area object perimeter is equal to the specified temperature multiplied by
            the pattern value at the associated point object. The material temperature at other points in the area
            object is calculated by interpolation from the corner points.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.AreaObj.SetMatTemp(name,Temp,PatternName,itemType)

    def Modifiers(self,name,Value,itemType=0):
        """
        ---This function sets the modifier assignment for area objects. The default value for all modifiers is one---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        Value(float)-This is an array of ten unitless modifiers.
            Value(0) = Membrane f11 modifier
            Value(1) = Membrane f22 modifier
            Value(2) = Membrane f12 modifier
            Value(3) = Bending m11 modifier
            Value(4) = Bending m22 modifier
            Value(5) = Bending m12 modifier
            Value(6) = Shear v13 modifier
            Value(7) = Shear v23 modifier
            Value(8) = Mass modifier
            Value(9) = Weight modifier
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.AreaObj.SetModifiers(name,Value,itemType)

    def NotionalSize(self,name,style,Value):
        """
        ---This function assigns the method to determine the notional size of an area section for the creep and
        shrinkage calculations. This function is currently worked for shell type area section
        ---
        inputs:
        name(str)-The name of an existing shell-type area section property
        style(str)-The type to define the notional size of a section. It can be:
            "Auto" = Program will determine the notional size based on the average thickness of an area element.
            "User" = The notional size is based on the user-defined value.
            "None" = Notional size will not be considered. In other words, the time-dependent effect of this
            section will not be considered.
        Value(float)-For stype is "Auto", the Value represents for the scale factor to the program-determined notional
            size; for stype is “User”, the Value represents for the user-defined notional size [L]; for stype is “None”,
            the Value will not be used and can be set to 1.
        """
        self.__Model.PropArea.SetNotionalSize(name,style,Value)

    def Offsets(self,name,OffsetType,OffsetPattern,OffsetPatternSF,Offset,itemType=0):
        """
        ---This function sets the joint offset assignments for area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        OffsetType(int)-This is 0, 1 or 2, indicating the joint offset type.
            0 = No joint offsets
            1 = User defined joint offsets specified by joint pattern
            2 = User defined joint offsets specified by point
        OffsetPattern(str)-This item applies only when OffsetType = 1. It is the name of the defined
            joint pattern that is used to calculate the joint offsets
        OffesetPatternSF(float)-This item applies only when OffsetType = 1. It is the scale factor applied to
            the joint pattern when calculating the joint offsets. [L]
        Offset(float)-This item applies only when OffsetType = 2. It is an array of joint offsets for each of
            the points that define the area object. [L]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.AreaObj.SetOffsets(name,OffsetType,OffsetPattern,OffsetPatternSF,Offset,itemType)

    def Property(self,name,PropName,itemType=0):
        """
        ---This function assigns an area property to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        PropName(str)-This is None or the name of a area property to be assigned to the specified area object(s).
            None means that no property is assigned to the area object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.AreaObj.SetProperty(name,PropName,itemType)

    def Spring(self,name,myType,s,simpleSpringType,LinkProp,Face,SpringLocalOneType,Dir,
                                 OutWard,Vec,Ang,Replace,CSys="Local",itemType=0):
        """
        ---This function makes spring assignments to area objects. The springs are assigned to a specified area object face---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        MyType(int)-This is either 1 or 2, indicating the spring property type.
            1 = Simple spring,2 = Link property
        s(float)-The simple spring stiffness per unit area of the specified area object face. This item applies
            only when MyType = 1. [F/L3]
        SimpleSpringType(int)-This is 1, 2 or 3, indicating the simple spring type. This item applies only when MyType = 1.
            1 = Spring resists tension and compression
            2 = Spring resists compression only
            3 = Spring resists tension only
        LinkProp(str)-The name of the link property assigned to the spring. This item applies only when MyType = 2.
        Face(int)-This is -1, -2 or a nonzero, positive integer indicating the area object face to which the specified
            spring assignment applies.
            -1 = Bottom face,-2 = Top face,>0 = Edge face
            Note that edge face n is from area object point n to area object point n + 1. For example, edge face 2 is
            from area object point 2 to area object point 3.
        SpringLocalOneType(int)-This is 1, 2 or 3, indicating the method used to specify the spring positive local
            1-axis orientation.
            1 = Parallel to area object local axis
            2 = Normal to specified area object face
            3 = User specified direction vector
        Dir(int)-This is 1, 2, 3, -1, -2 or -3, indicating the area object local axis that corresponds to the positive
            local 1-axis of the spring. This item applies only when SpringLocalOneType = 1
        Outward(bool)-This item is True if the spring positive local 1 axis is outward from the specified area object
            face. This item applies only when SpringLocalOneType = 2.
        Vec(float list)-This is an array of three values that define the direction vector of the spring positive local
            1-axis. The direction vector is in the coordinate system specified by the CSys item. This item applies only
            when SpringLocalOneType = 3.
        Ang(float)-This is the angle that the link local 2-axis is rotated from its default orientation. This item
            applies only when MyType = 2. [deg]
        Replace(bool)-If this item is True, all existing spring assignments to the area object are removed before
            assigning the specified spring. If it is False, the specified spring is added to any existing springs
            already assigned to the area object.
        CSys(str)-This is Local (meaning the area object local coordinate system) or the name of a defined coordinate
            system. This item is the coordinate system in which the user specified direction vector, Vec, is specified.
            This item applies only when SpringLocalOneType = 3.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignor
        """
        self.__Model.AreaObj.SetSpring(name,myType,s,simpleSpringType,LinkProp,Face,SpringLocalOneType,Dir,
                                 OutWard,Vec,Ang,Replace,CSys,itemType)

    def Thickness(self,name,ThinknessType,ThinknessPattern,ThicknessPatternSF,Thickness,itemType=0):
        """
        ---This function sets the thickness overwrite assignments for area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item.
        ThinknessType(int)-This is 0, 1 or 2, indicating the thickness overwrite type.
            0 = No thickness overwrites
            1 = User defined thickness overwrites specified by joint pattern
            2 = User defined thickness overwrites specified by point
        ThinknessPattern(str)-This item applies only when ThicknessType = 1. It is the name of the defined joint
            pattern that is used to calculate the thicknesses
        ThicknessPatternSF(float)-This item applies only when ThicknessType = 1. It is the scale factor applied
            to the joint pattern when calculating the thicknesses. [L]
        Thickness(float)-This item applies only when ThicknessType = 2. It is an array of thicknesses at each
            of the points that define the area object. [L]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignor
        """
        self.__Model.AreaObj.SetThickness(name,ThinknessType,ThinknessPattern,ThicknessPatternSF,Thickness,itemType)

class AreaObj_Get:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def AutoMesh(self,name):
        """
        ---This function retrieves the automatic meshing assignments to area objects---
        inputs:
        name(str)-The name of an existing area object
        return:
        [index,MeshType,n1,n2,MaxSize1,MaxSize2,PointOnEdgeFromLine,PointOnEdgeFromPoint,ExtendCookieCutLines,
        Rotation,MaxSizeGeneral,LocalAxesOnEdge,LocalAxesOnFace,RestraintsOnEdge,RestraintsOnFace,Group,SubMesh,
        SubMeshSize]
        MeshType(int)-This item is 0, 1, 2, 3, 4, 5 or 6, indicating the automatic mesh type for the area object.
            0 = No automatic meshing
            1 = Mesh area into a specified number of objects
            2 = Mesh area into objects of a specified maximum size
            3 = Mesh area based on points on area edges
            4 = Cookie cut mesh area based on lines intersecting edges
            5 = Cookie cut mesh area based on points
            6 = Mesh area using General Divide Tool
            Mesh options 1, 2 and 3 apply to quadrilaterals and triangles only.
        n1(int)-This item applies when MeshType = 1. It is the number of objects created along the edge of the
            meshed area object that runs from point 1 to point 2.
        n2(int)-This item applies when MeshType = 1. It is the number of objects created along the edge of the
            meshed area object that runs from point 1 to point 3.
        MaxSize1(float)-This item applies when MeshType = 2. It is the maximum size of objects created along the
            edge of the meshed area object that runs from point 1 to point 2. [L]If this item is input as 0, the
            default value is used. The default value is 48 inches if the database units are English or 120 centimeters
            if the database units are metric.
        MaxSize2(float)-This item applies when MeshType = 2. It is the maximum size of objects created along the edge
            of the meshed area object that runs from point 1 to point 3. [L]If this item is input as 0, the default
            value is used. The default value is 48 inches if the database units are English or 120 centimeters if the
            database units are metric.
        PointOnEdgeFromLine(bool)-This item applies when MeshType = 3. If it is True, points on the area object edges
            are determined from intersections of straight line objects included in the group specified by the Group
            item with the area object edges.
        PointOnEdgeFromPoint(bool)-This item applies when MeshType = 3. If it is True, points on the area object edges
            are determined from point objects included in the group specified by the Group item that lie on the area object edges
        ExtendCookieCutLines(bool)-This item applies when MeshType = 4. MeshType = 4 provides cookie cut meshing based
            on straight line objects included in the group specified by the Group item that intersect the area object
            edges. If the ExtendCookieCutLines item is True, all straight line objects included in the group specified
            by the Group item are extended to intersect the area object edges for the purpose of meshing the area object.
        Rotation(float)-This item applies when MeshType = 5. MeshType = 5 provides cookie cut meshing based on two
            perpendicular lines passing through point objects included in the group specified by the Group item.
            By default these lines align with the area object local 1 and 2 axes. The Rotation item is an angle in
            degrees that the meshing lines are rotated from their default orientation. [deg]
        MaxSizeGeneral(float)-This item applies when MeshType = 6. It is the maximum size of objects created by the
            General Divide Tool.If this item is input as 0, the default value is used. The default value is 48 inches
            if the database units are English or 120 centimeters if the database units are metric.
        LocalAxesOnEdge(bool)-If this item is True, and if both points along an edge of the original area object
            have the same local axes, then the program makes the local axes for added points along the edge the
            same as the edge end points.
        LoalAxesOnFace(bool)-If this item is True, and if all points around the perimeter of the original area object
            have the same local axes, the program makes the local axes for all added points the same as the perimeter points.
        RestraintsOnEdge(bool)-If this item is True, and if both points along an edge of the original area object have
            the same restraint/constraint, then, if the added point and the adjacent corner points have the same local
            axes definition, the program includes the restraint/constraint for added points along the edge.
        RestraintsOnFace(bool)-If this item is True, and if all points around the perimeter of the original area object
            have the same restraint/constraint, then, if an added point and the perimeter points have the same local
            axes definition, the program includes the restraint/constraint for the added point.
        Group(str)-The name of a defined group. Some of the meshing options make use of point and line objects
            included in this group.
        SubMesh(bool)-If this item is True, after initial meshing, the program further meshes any area objects that
            have an edge longer than the length specified by the SubMeshSize item.
        SubMeshSize(bool)-This item applies when the SubMesh item is True. It is the maximum size of area objects to
            remain when the auto meshing is complete. [L]If this item is input as 0, the default value is used.
            The default value is 12 inches if the database units are English or 30 centimeters if the database units are metric.
        """
        result=self.__Model.AreaObj.GetAutoMesh(name)
        return result

    def EdgeConstraint(self,name):
        """
        ---This function retrieves the generated edge constraint assignments to area objects---
        inputs:
        name(str)-The name of an existing area object
        return:
        [index,ConstraintExists]
        ConstraintExists(bool)-This item is True if an automatic edge constraint is generated by the program for
            the area object in the analysis model.
        """
        result=self.__Model.AreaObj.GetEdgeConstraint(name)
        return result

    def Elm(self,name):
        """
        ---This function retrieves the names of the area elements (analysis model area) associated with a specified
        area object in the object-based model
        ---
        inputs:
        name(str)-The name of an existing area object
        return:
        [index,nelm,Elm]
        nelm(int)-The number of area elements created from the specified area object
        Elm(str list)-An array that includes the name of a area element created from the specified area object.
        """
        result=self.__Model.AreaObj.GetElm(name)
        return result

    def GroupAssign(self,name):
        """
        ---This function retrieves the names of the groups to which a specified area object is assigned---
        inputs:
        name(str)-The name of an existing area object.
        return:
        [index,NumberGroups,Groups]
        NumberGroups(int)-The number of group names retrieved.
        Groups(str list)-The names of the groups to which the area object is assigned
        """
        result=self.__Model.AreaObj.GetGroupAssign(name)
        return result

    def LoadGravity(self,name):
        """
        ---This function retrieves the gravity load assignments to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,AreaName,LoadPat,CSys,x,y,z]
        NumberItems(int)-The total number of gravity loads retrieved for the specified area objects
        AreaName(str)-This is an array that includes the name of the area object associated with each gravity load
        LoadPat(str list)-This is an array that includes the name of the coordinate system in which the gravity
            load multipliers are specified
        CSys(str list)-This is an array that includes the name of the coordinate system associated with each gravity load
        x,y,z(float list)-These are arrays of gravity load multipliers in the x, y and z directions of the specified
            coordinate system
        """
        result=self.__Model.AreaObj.GetLoadGravity(name)
        return result

    def LoadPorePressure(self,name):
        """
        ---This function retrieves the pore pressure load assignments to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,AreaName,LoadPat,Value,PatternName]
        NumberItems(int)-The total number of pore pressure loads retrieved for the specified area objects
        AreaName(str list)-This is an array that includes the name of the area object associated with each pore pressure load
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each pore pressure load
        Value(float list)-This is an array that includes the pore pressure load value. [F/L2]
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify the pore
            pressure load
        """
        result=self.__Model.AreaObj.GetLoadPorePressure(name)
        return result

    def LoadRotate(self,name):
        """
        ---This function retrieves the rotate load assignments to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,AreaName,LoadPat,Value]
        NumberItems(int)-The total number of rotate loads retrieved for the specified area objects.
        AreaName(str list)-This is an array that includes the name of the area object associated with each rotate load
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each rotate load
        Value(float list)-This is an array that includes the angular velocity value. [Cyc/T]
        """
        result=self.__Model.AreaObj.GetLoadRotate(name)
        return result

    def LoadStrain(self,name):
        """
        ---This function retrieves the strain load assignments to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,AreaName,LoadPat,component,Value,PatternName]
        NumberItems(int)-The total number of strain loads retrieved for the specified area objects
        AreaName(str list)-This is an array that includes the name of the area object associated with each strain load
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each strain load
        Component(int)-This is an array that includes 1, 2, 3, 4, 5, 6, 7, 8, or 9, indicating the component associated
            with each strain load.
            1 = Strain11,2 = Strain22,3 = Strain12,4 = Curvature11,5 = Curvature22,6 = Curvature12,7 = Strain13
            8 = Strain23,9 = Strain33
        Value(float list)-This is an array that includes the strain value. [L/L] for Component = 1, 2, 3, 7, 8, and 9,
            and [1/L] for Component = 4, 5 and 6
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify the strain load.
        """
        result=self.__Model.AreaObj.GetLoadStrain(name)
        return result

    def LoadSurfacePressure(self,name):
        """
        ---This function retrieves the surface pressure load assignments to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,AreaName,LoadPat,Face,Value,PatternName]
        NumberItems(int)-The total number of surface pressure loads retrieved for the specified area objects
        AreaName(str list)-This is an array that includes the name of the area object associated with each surface pressure load
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each surface pressure load
        Face(int)-This is an array that includes either -1, -2 or a nonzero, positive integer, indicating the area
            object face to which the specified load assignment applies.
            -1 = Bottom face,-2 = Top face,>0 = Edge face
            Note that edge face n is from area object point n to area object point n + 1. For example, edge face 2 is
            from area object point 2 to area object point 3.
        Value(float list)-This is an array that includes the surface pressure load value. [F/L2]
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify
            the surface pressure load.
        """
        result=self.__Model.AreaObj.GetLoadSurfacePressure(name)
        return result

    def LoadTemperature(self,name):
        """
        ---This function retrieves the temperature load assignments to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,AreaName,LoadPat,MyType,Value,PatternName]
        NumberItems(int)-The total number of temperature loads retrieved for the specified area objects
        AreaName(str list)-This is an array that includes the name of the area object associated with each temperature load
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each temperature load
        MyType(int)-This is an array that includes either 1 or 3, indicating the type of temperature load.
            1 = Temperature,3 = Temperature gradient along local 3 axis
        Value(float list)-This is an array that includes the temperature load value. [T] for MyType= 1 and [T/L] for MyType= 3
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify the temperature load.
        """
        result=self.__Model.AreaObj.GetLoadTemperature(name)
        return result

    def LoadUniform(self,name):
        """
        ---This function retrieves the uniform load assignments to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,AreaName,LoadPat,CSys,Dir,Value]
        NumberItems(int)-The total number of uniform loads retrieved for the specified area objects.
        AreaName(str list)-This is an array that includes the name of the area object associated with each uniform load
        LoadPat(str list)-This is an array that includes the name of the coordinate system in which the uniform load
            is specified.
        CSys(str list)-This is an array that includes the name of the coordinate system associated with each uniform load.
        Dir(int)-This is an integer between 1 and 11, indicating the direction of the load.
            1 = Local 1 axis (only applies when CSys is Local)
            2 = Local 2 axis (only applies when CSys is Local)
            3 = Local 3 axis (only applies when CSys is Local)
            4 = X direction (does not apply when CSys is Local)
            5 = Y direction (does not apply when CSys is Local)
            6 = Z direction (does not apply when CSys is Local)
            7 = Projected X direction (does not apply when CSys is Local)
            8 = Projected Y direction (does not apply when CSys is Local)
            9 = Projected Z direction (does not apply when CSys is Local)
            10 = Gravity direction (only applies when CSys is Global)
            11 = Projected Gravity direction (only applies when CSys is Global)
            The positive gravity direction (see Dir = 10 and 11) is in the negative Global Z direction.
        Value(float)-The uniform load value. [F/L2]
        """
        result=self.__Model.AreaObj.GetLoadUniform(name)
        return result

    def LoadUniformToFrame(self,name):
        """
        ---This function retrieves the uniform to frame load assignments to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,AreaName,LoadPat,CSys,Dir,Value,DistType]
        NumberItems(int)-The total number of uniform loads retrieved for the specified area objects
        AreaName(str list)-This is an array that includes the name of the area object associated with each uniform load.
        LoadPat(str list)-This is an array that includes the name of the coordinate system in which the uniform load is specified
        CSys(str list)-This is an array that includes the name of the coordinate system associated with each uniform load
        Dir(int)-This is an integer between 1 and 11, indicating the direction of the load.
            1 = Local 1 axis (only applies when CSys is Local)
            2 = Local 2 axis (only applies when CSys is Local)
            3 = Local 3 axis (only applies when CSys is Local)
            4 = X direction (does not apply when CSys is Local)
            5 = Y direction (does not apply when CSys is Local)
            6 = Z direction (does not apply when CSys is Local)
            7 = Projected X direction (does not apply when CSys is Local)
            8 = Projected Y direction (does not apply when CSys is Local)
            9 = Projected Z direction (does not apply when CSys is Local)
            10 = Gravity direction (only applies when CSys is Global)
            11 = Projected Gravity direction (only applies when CSys is Global)
            The positive gravity direction (see Dir = 10 and 11) is in the negative Global Z direction
        Value(float)-The uniform load value. [F/L2]
        DistType(int)-This is either 1 or 2, indicating the load distribution type.
            1 = One-way load distribution,2 = Two-way load distribution
            One-way distribution is parallel to the area object local 1 axis. Two-way distribution is parallel
            to the area object local 1 and 2 axes.
        """
        result=self.__Model.AreaObj.GetLoadUniformToFrame(name)
        return result

    def LoadWindPressure_1(self,name):
        """
        ---This function retrieves the wind pressure load assignments to area objects---
        inputs:
        name(str)-The name of an existing area object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,AreaName,LoadPat,MyType,Cp,DistributionType]
        NumberItems(int)-The total number of wind pressure loads retrieved for the specified area objects.
        AreaName(str list)-This is an array that includes the name of the area object associated with each wind pressure load
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each wind pressure load
        MyType(int)-This is an array that includes either 1 or 2, indicating the wind pressure type.
            1 = Windward, pressure varies over height
            2 = Other, pressure is constant over height
        Cp(float list)-This is an array that includes the wind pressure coefficient value
        DistributionType(int)-This is either 1 or 2, indicating the distribution type.
            1 = To Joints
            2 = To Frames – One-way
            3 = To Frames – Two-way
        """
        result=self.__Model.AreaObj.GetLoadWindPressure_1(name)
        return result

    def LocalAxes(self,name):
        """
        ---This function retrieves the local axis angle assignment for area objects---
        inputs:
        name(str)-The name of an existing area object
        return:
        [index,Ang,Advanced]
        Ang(float)-This is the angle that the local 1 and 2 axes are rotated about the positive local 3 axis from
            the default orientation. The rotation for a positive angle appears counter clockwise when the local
            +3 axis is pointing toward you. [deg]
        Advanced(bool)-This item is True if the area object local axes orientation was obtained using advanced
            local axes parameters.
        """
        result=self.__Model.AreaObj.GetLocalAxes(name)
        return result

    def Mass(self,name):
        """
        ---This function retrieves the mass per unit area assignment for area objects---
        inputs:
        name(str)-The name of an existing area object
        return:
        [index,MassOverL2]
        MassOverL2(float)-The mass per unit area assigned to the area object. [M/L2]
        """
        result=self.__Model.AreaObj.GetMass(name)
        return result

    def MatTemp(self,name):
        """
        ---This function retrieves the material temperature assignments to area objects---
        inputs:
        name(str)-The name of an existing area object
        return:
        [index,Temp,PatternName]
        Temp(float)-This is the material temperature value assigned to the area object. [T]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the material
            temperature for the area object is uniform over the object at the value specified by Temp.If PatternName
            is the name of a defined joint pattern, the material temperature for the area object may vary. The material
            temperature at each corner point around the area object perimeter is equal to the specified temperature
            multiplied by the pattern value at the associated point object. The material temperature at other points
            in the area object is calculated by interpolation from the corner points.
        """
        result=self.__Model.AreaObj.GetMatTemp(name)
        return result

    def Modifiers(self,name):
        """
        ---This function retrieves the modifier assignment for area objects. The default value for all modifiers is one---
        inputs:
        name(str)-The name of an existing area object
        return:
        [index,Value]
        Value(float list)-This is an array of ten unitless modifiers.
            Value(0) = Membrane f11 modifier
            Value(1) = Membrane f22 modifier
            Value(2) = Membrane f12 modifier
            Value(3) = Bending m11 modifier
            Value(4) = Bending m22 modifier
            Value(5) = Bending m12 modifier
            Value(6) = Shear v13 modifier
            Value(7) = Shear v23 modifier
            Value(8) = Mass modifier
            Value(9) = Weight modifier
        """
        result=self.__Model.AreaObj.GetModifiers(name)
        return result

    def NameList(self):
        """
        ---This function retrieves the names of all defined area objects---
        return:
        [index,NumberNames,MyName]
        NumberNames(int)-The number of area object names retrieved by the program
        MyName(str list)-This is a one-dimensional array of area object names
        """
        result=self.__Model.AreaObj.GetNameList()
        return result

    def NotionalSize(self,name):
        """
        ---This function retrieves the method to determine the notional size of an area section for the creep
        and shrinkage calculations. This function is currently worked for shell type area section.
        ---
        inputs:
        name(str)-The name of an existing shell-type area section property
        return:
        [index,stype,Value]
        stype(str)-The type to define the notional size of a section. It can be:
            "Auto" = Program will determine the notional size based on the average thickness of an area element.
            "User" = The notional size is based on the user-defined value.
            "None" = Notional size will not be considered. In other words, the time-dependent effect of this section
            will not be considered.
        Value(float)-For stype is "Auto", the Value represents for the scale factor to the program-determined
            notional size; for stype is “User”, the Value represents for the user-defined notional size [L];
            for stype is “None”, the Value will not be used and can be set to 1.
        """
        result=self.__Model.PropArea.GetNotionalSize(name)
        return result

    def Offsets(self,name):
        """
        ---This function retrieves the joint offset assignments for area objects---
        inputs:
        name(str)-The name of an existing area object
        return:
        [index,OffsetType,OffsetPattern,OffsetPatternSF,Offset]
        OffsetType(int)-This is 0, 1 or 2, indicating the joint offset type.
            0 = No joint offsets
            1 = User defined joint offsets specified by joint pattern
            2 = User defined joint offsets specified by point
        OffsetPattern(str)-This item applies only when OffsetType = 1. It is the name of the defined joint
            pattern that is used to calculate the joint offsets
        OffsetPatternSF(float)-This item applies only when OffsetType = 1. It is the scale factor applied to
            the joint pattern when calculating the joint offsets. [L]
        Offset(float list)-This item applies only when OffsetType = 2. It is an array of joint offsets for
            each of the points that define the area object. [L]
        """
        result=self.__Model.AreaObj.GetOffsets(name)
        return result

    def Points(self,name):
        """
        ---This function retrieves the names of the point objects that define an area object---
        inputs:
        name(str)-The name of a defined area object
        return:
        [index,NumberPoints,Point]
        NumberPoints(int)-The number of point objects that define the area object
        Point(str list)-This is an array containing the names of the point objects that define the area object.
            The point names are in order around the area object
        """
        result=self.__Model.AreaObj.GetPoints(name)
        return result

    def Property(self,name):
        """
        ---This function retrieves the area property assigned to an area object---
        inputs:
        name(str)-The name of a defined area object
        return:
        [index,PropName]
        PropName(str)-The name of the area property assigned to the area object. This item is None if no area
            property is assigned to the area object.
        """
        result=self.__Model.AreaObj.GetProperty(name)
        return result

    def Spring(self,name):
        """
        ---This function retrieves the spring assignments to an area object face---
        inputs:
        name(str)-The name of an existing area object
        return:
        [index,NumberSprings,MyType,s,SimpleSpringType,LinkProp,Face,SpringLocalOneType,Dir,Outward,VecX,
        VecY,VecZ,CSys,Ang]
        NumberSprings(str)-The number of spring assignments made to the specified area object
        MyType(int)-This is either 1 or 2, indicating the spring property type.
            1 = Simple spring,2 = Link property
        s(float)-The simple spring stiffness per unit area of the specified area object face. This item applies
            only when MyType = 1. [F/L3]
        SimpleSpringType(int)-This is 1, 2 or 3, indicating the simple spring type. This item applies only when MyType = 1.
            1 = Spring resists tension and compression
            2 = Spring resists compression only
            3 = Spring resists tension only
        LinkProp(str)-The name of the link property assigned to the spring. This item applies only when MyType = 2.
        Face(int)-This is -1, -2 or a nonzero, positive integer indicating the area object face to which the specified
            spring assignment applies.
            -1 = Bottom face,-2 = Top face,>0 = Edge face
            Note that edge face n is from area object point n to area object point n + 1. For example, edge face 2 is
            from area object point 2 to area object point 3.
        SpringLocalOneType(int)-This is 1, 2 or 3, indicating the method used to specify the spring positive local
            1-axis orientation.
            1 = Parallel to area object local axis
            2 = Normal to specified area object face
            3 = User specified direction vector
        Dir(int)-This is 1, 2, 3, -1, -2 or -3, indicating the area object local axis that corresponds to the positive
            local 1-axis of the spring. This item applies only when SpringLocalOneType = 1
        Outward(bool)-This item is True if the spring positive local 1 axis is outward from the specified area object
            face. This item applies only when SpringLocalOneType = 2.
        Vec(float list)-This is an array of three values that define the direction vector of the spring positive local
            1-axis. The direction vector is in the coordinate system specified by the CSys item. This item applies only
            when SpringLocalOneType = 3.
        CSys(str)-This is Local (meaning the area object local coordinate system) or the name of a defined coordinate
            system. This item is the coordinate system in which the user specified direction vector, Vec, is specified.
            This item applies only when SpringLocalOneType = 3.
        Ang(float)-This is the angle that the link local 2-axis is rotated from its default orientation. This item
            applies only when MyType = 2. [deg]
        """
        result=self.__Model.AreaObj.GetSpring(name)
        return result

    def Thickness(self,name):
        """
        ---This function retrieves the thickness overwrite assignments for area objects---
        inputs:
        name(str)-The name of an existing area object
        return:
        [index,ThinknessType,ThinknessPattern,ThicknessPatternSF,Thickness]
        ThinknessType(int)-This is 0, 1 or 2, indicating the thickness overwrite type.
            0 = No thickness overwrites
            1 = User defined thickness overwrites specified by joint pattern
            2 = User defined thickness overwrites specified by point
        ThicknessPattern(str)-This item applies only when ThicknessType = 1. It is the name of the defined joint
            that is used to calculate the thicknesses
        ThicknessPatternSF(float)-This item applies only when ThicknessType = 1. It is the scale factor applied
            to the joint pattern when calculating the thicknesses. [L]
        Thickness(float list)-This item applies only when ThicknessType = 2. It is an array of thicknesses at each
            of the points that define the area object. [L]
        """
        result=self.__Model.AreaObj.GetThickness(name)
        return result

    def TransformationMatrix(self,name):
        """
        ---The function returns zero if the area object transformation matrix is successfully retrieved---
        inputs:
        name(str)-The name of an existing area object
        return:
        [index,Value]
        Value(float list)-Value is an array of nine direction cosines that define the transformation matrix.The
            following matrix equation shows how the transformation matrix is used to convert items from the area
            object local coordinate system to the global coordinate system.
        """
        result=self.__Model.AreaObj.GetTransformationMatrix(name)
        return result

class SapAreaObj:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model
        self.Set = AreaObj_Set(Sapobj)
        self.Get = AreaObj_Get(Sapobj)

    def AddByCoord(self,NumberPoints,x,y,z,PropName="Default",UserName="",CSys="Global"):
        """
        ---This function adds a new area object, defining points at the specified coordinates---
        inputs:
        NumberPoints(int)-The number of points in the area abject.
        x,y,z(float list)-These are arrays of x, y and z coordinates, respectively, for the corner points of the
            area object. The coordinates are in the coordinate system defined by the CSys item. The coordinates
            should be ordered to run clockwise or counter clockwise around the area object.
        PropName(str)-This is Default, None or the name of a defined area property.If it is Default, the program
            assigns a default area property to the area object. If it is None, no area property is assigned to the
            area object. If it is the name of a defined area property, that property is assigned to the area object.
        UserName(str)-This is an optional user specified name for the area object. If a UserName is specified and
            that name is already used for another area object, the program ignores the UserName.
        CSys(str)-The name of the coordinate system in which the area object point coordinates are defined.
        """
        # This is the name that the program ultimately assigns to the area object. If no UserName is specified,
        # the program assigns a default name to the area object. If a UserName is specified and that name is not
        # used for another area object, the UserName is assigned to the area object; otherwise a default name is
        # assigned to the area object.
        name = ""
        self.__Model.AreaObj.AddByCoord(NumberPoints,x,y,z,name,PropName,UserName,CSys)

    def AddByPoint(self,NumberPoints,Point,PropName="Default",UserName=""):
        """
        ---This function adds a new area object whose defining points are specified by name---
        inputs:
        NumberPoints(int)-The number of points in the area abject.
        Point(str list)-This is an array containing the names of the point objects that define the added area object.
            The point object names should be ordered to run clockwise or counter clockwise around the area object.
        PropName(str)-This is Default, None or the name of a defined area property.If it is Default, the program
            assigns a default area property to the area object. If it is None, no area property is assigned to the
            area object. If it is the name of a defined area property, that property is assigned to the area object.
        UserName(str)-This is an optional user specified name for the area object. If a UserName is specified and
            that name is already used for another area object, the program ignores the UserName.
        """
        # This is the name that the program ultimately assigns to the area object. If no UserName is specified,
        # the program assigns a default name to the area object. If a UserName is specified and that name is not
        # used for another area object, the UserName is assigned to the area object; otherwise a default name is
        # assigned to the area object.
        name = ""
        self.__Model.AreaObj.AddByPoint(NumberPoints,Point,name,PropName,UserName)

    def ChangeName(self,name,NewName):
        """
        ---This function applies a new name to an area object---
        inputs:
        name(str)-The existing name of a defined area object.
        NewName(str)-The new name for the area object.
        """
        self.__Model.AreaObj.ChangeName(name,NewName)

    def Count(self):
        """
        ---This function returns a count of the area objects in the model---
        """
        result=self.__Model.AreaObj.Count()
        return result


class SolidObj_Set:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def AutoMesh(self,name,MeshType,n1=2,n2=2,n3=2,MaxSize1=0,MaxSize2=0,MaxSize3=0,RestraintsOnEdge=False,
                                    RestraintOnFace=False):
        """
        ---This function makes automatic meshing assignments to solid objects---
        inputs:
        name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        MeshType(int)-This item is 0, 1 or 2, indicating the automatic mesh type for the solid object.
            0 = No automatic meshing
            1 = Mesh solid into a specified number of objects
            2 = Mesh solid into objects of a specified maximum size
        n1(int)-This item applies when MeshType = 1. It is the number of objects created along the edge of the
            meshed solid object that runs from point 1 to point 2
        n2(int)-This item applies when MeshType = 1. It is the number of objects created along the edge of the
            meshed solid object that runs from point 1 to point 3
        n3(int)-This item applies when MeshType = 1. It is the number of objects created along the edge of the
            meshed solid object that runs from point 1 to point 5
        MaxSize1(float)-This item applies when MeshType = 2. It is the maximum size of objects created along the
            edge of the meshed solid object that runs from point 1 to point 2. [L] If this item is input as 0, the
            default value is used. The default value is 48 inches if the database units are English or 120 centimeters
            if the database units are metric
        MaxSize2(float)-This item applies when MeshType = 2. It is the maximum size of objects created along the edge
            of the meshed solid object that runs from point 1 to point 3. [L] If this item is input as 0, the default
            value is used. The default value is 48 inches if the database units are English or 120 centimeters if the
            database units are metric.
        MaxSize3(float)-This item applies when MeshType = 2. It is the maximum size of objects created along the edge
            of the meshed solid object that runs from point 1 to point 5. [L] If this item is input as 0, the default
            value is used. The default value is 48 inches if the database units are English or 120 centimeters if the
            database units are metric.
        RestraintsOnEdge(bool)-If this item is True, and if both points along an edge of the original solid object have
            the same restraint/constraint, then, if the an added point on that edge and the original corner points have
            the same local axes definition, the program assigns the restraint/constraint to the added point
        RestraintsOnFace(bool)-If this item is True, and if all corner points on an solid object face have the same
            restraint/constraint, then, if an added point on that face and the original corner points for the face
            have the same local axes definition, the program assigns the restraint/constraint to the added point.
        """
        self.__Model.SolidObj.SetAutoMesh(name,MeshType,n1,n2,n3,MaxSize1,MaxSize2,MaxSize3,RestraintsOnEdge,RestraintOnFace)

    def EdgeConstraint(self,Name,ConstraintExists,itemType=0):
        """
        ---This function makes generated edge constraint assignments to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        ConstraintExists(bool)-This item is True if an automatic edge constraint is generated by the program for
            the solid object in the analysis model
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.SolidObj.SetEdgeConstraint(Name,ConstraintExists,itemType)

    def GroupAssign(self,Name,GroupName,Remove=False,itemType=0):
        """
        ---This function adds or removes solid objects from a specified group---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        GroupName(str)-The name of an existing group to which the assignment is made
        Remove(bool)-If this item is False, the specified solid objects are added to the group specified by the
            GroupName item. If it is True, the solid objects are removed from the group
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.SolidObj.SetGroupAssign(Name,GroupName,Remove,itemType)

    def LoadGravity(self,Name,LoadPat,x,y,z,Replace=True,CSys="Global",itemType=0):
        """
        ---This function assigns gravity load multipliers to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        LoadPat(str)-The name of a defined load pattern
        x,y,z(float)-These are the gravity load multipliers in the x, y and z directions of the specified coordinate system
        Replace(bool)-If this item is True, all previous gravity loads, if any, assigned to the specified
            solid object(s), in the specified load pattern, are deleted before making the new assignment
        CSys(str)-The coordinate system in which the x, y and z multipliers are specified
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.SolidObj.SetLoadGravity(Name,LoadPat,x,y,z,Replace,CSys,itemType)

    def LoadPorePressure(self,Name,LoadPat,Value,PatternName="",Replace=True,itemType=0):
        """
        ---This function assigns pore pressure loads to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        LoadPat(str)-The name of a defined load pattern
        Value(float)-This is the pore pressure value. [F/L2]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the pore pressure
            load for the solid object is uniform over the object at the value specified by Value.If PatternName
            is the name of a defined joint pattern, the pore pressure load for the solid object is based on the
            specified pore pressure value multiplied by the pattern value at the corner point objects of the solid object.
        Replace(bool)-If this item is True, all previous pore pressure loads, if any, assigned to the specified solid
            object(s), in the specified load case, are deleted before making the new assignment.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.SolidObj.SetLoadPorePressure(Name,LoadPat,Value,PatternName,Replace,itemType)

    def LoadStrain(self,Name,LoadPat,Component,Value,Replace=True,PatternName="",itemType=0):
        """
        ---This function assigns strain loads to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        LoadPat(str)-The name of a defined load pattern
        Component(int)-This is 1, 2, 3, 4, 5 or 6, indicating the component to which the strain load is applied.
            1 = Strain11
            2 = Strain22
            3 = Strain33
            4 = Strain12
            5 = Strain13
            6 = Strain23
        Value(float)-This is the strain load value. [L/L]
        Replace(bool)-If this item is True, all previous strain loads, if any, assigned to the specified solid object(s),
            in the specified load pattern, for the specified degree of freedom, are deleted before making the new assignment.
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the strain load for the
            solid object is uniform over the object at the value specified by Value.If PatternName is the name of a
            defined joint pattern, the strain load for the solid object is based on the specified strain value multiplied
            by the pattern value at the corner point objects of the solid object.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.SolidObj.SetLoadStrain(Name,LoadPat,Component,Value,Replace,PatternName,itemType)

    def LoadSurfacePressure(self,Name,LoadPat,Face,Value,PatternName="",Replace=True,itemType=0):
        """
        ---This function assigns surface pressure loads to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        LoadPat(str)-The name of a defined load pattern
        Face(str)-This is 1, 2, 3, 4, 5 or 6, indicating the solid object face to which the specified load assignment applies.
        Value(float)-This is the surface pressure value. [F/L2]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the surface pressure
            load for the solid object is uniform over the object at the value specified by Value.If PatternName is
            the name of a defined joint pattern, the surface pressure load for the solid object is based on the
            specified surface pressure value multiplied by the pattern value at the corner point objects of the solid object.
        Replace(bool)-If this item is True, all previous surface pressure loads, if any, assigned to the specified solid
            object(s), on the specified face, in the specified load pattern, are deleted before making the new assignment.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.SolidObj.SetLoadSurfacePressure(Name,LoadPat,Face,Value,PatternName,Replace,itemType)

    def LoadTemperature(self,Name,LoadPat,Value,PatternName="",Replace=True,itemType=0):
        """
        ---This function assigns temperature loads to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        LoadPat(str)-The name of a defined load pattern
        Value(float)-This is the temperature change value. [T]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the temperature load
            for the solid object is uniform over the object at the value specified by Value.If PatternName is the
            name of a defined joint pattern, the temperature load for the solid object is based on the specified
            temperature value multiplied by the pattern value at the corner point objects of the solid object.
        Replace(bool)-If this item is True, all previous temperature loads, if any, assigned to the specified solid
            object(s), in the specified load case, are deleted before making the new assignment
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.SolidObj.SetLoadTemperature(Name,LoadPat,Value,PatternName,Replace,itemType)

    def LocalAxes(self,Name,a,b,c,itemType=0):
        """
        ---This function sets the local axes angles for solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        a,b,c(float)-The local axes of the solid object are defined by first setting the positive local 1, 2 and 3
            axes the same as the positive global X, Y and Z axes and then doing the following: [deg]
                1.Rotate about the 3 axis by angle a.
                2.Rotate about the resulting 2 axis by angle b.
                3.Rotate about the resulting 1 axis by angle c.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.SolidObj.SetLocalAxes(Name,a,b,c,itemType)

    def MatTemp(self,Name,Temp,PatternName="",itemType=0):
        """
        ---This function assigns material temperatures to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        Temp(float)-This is the material temperature value assigned to the solid object. [T]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the material
            temperature for the solid object is uniform over the object at the value specified by Temp.If
            PatternName is the name of a defined joint pattern, the material temperature for the solid object
            may vary. The material temperature at each corner point of the solid object is equal to the specified
            temperature multiplied by the pattern value at the associated point object. The material temperature
            at other points in the solid object is calculated by interpolation from the corner points.
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.SolidObj.SetMatTemp(Name,Temp,PatternName,itemType)

    def Property(self,Name,PropName,itemType=0):
        """
        ---This function assigns a solid property to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        PropName(str)-This is the name of a solid property to be assigned to the specified solid object(s).
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.SolidObj.SetProperty(Name,PropName,itemType)

    def Spring(self,Name,MyType,s,SimpleSpringType,LinkProp,Face,SpringLocalOneType,Dir,
                                  Outward,Vec,Ang,Replace,CSys="Local",itemType=0):
        """
        ---This function makes spring assignments to solid objects. The springs are assigned to a specified solid object face---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        MyType(int)-This is either 1 or 2, indicating the spring property type.
            1 = Simple spring,2 = Link property
        s(float)-The simple spring stiffness per unit area of the specified solid object face. This item applies
            only when MyType = 1. [F/L3]
        SimpleSpringType(int)-This is 1, 2 or 3, indicating the simple spring type. This item applies only when MyType = 1.
            1 = Spring resists tension and compression
            2 = Spring resists compression only
            3 = Spring resists tension only
        LinkProp(str)-The name of the link property assigned to the spring. This item applies only when MyType = 2
        Face(int)-This is 1, 2, 3, 4, 5 or 6, indicating the solid object face to which the specified spring assignment applies
        SpringLocalOneType(int)-This is 1, 2 or 3, indicating the method used to specify the spring positive local 1-axis
            orientation.
            1 = Parallel to solid object local axis
            2 = Normal to specified solid object face
            3 = User specified direction vector
        Dir(int)-This is 1, 2, 3, -1, -2 or -3, indicating the solid object local axis that corresponds to the
            positive local 1-axis of the spring. This item applies only when SpringLocalOneType = 1.
        Outward(bool)-This item is True if the spring positive local 1 axis is outward from the specified solid object
            face. This item applies only when SpringLocalOneType = 2.
        Vec(float list)-This is an array of three values that define the direction vector of the spring positive local
            1-axis. The direction vector is in the coordinate system specified by the CSys item. This item applies only
            when SpringLocalOneType = 3
        Ang(float)-This is the angle that the link local 2-axis is rotated from its default orientation.
            This item applies only when MyType = 2. [deg]
        Replace(bool)-If this item is True, all existing spring assignments to the solid object are removed before
            assigning the specified spring. If it is False, the specified spring is added to any existing springs
            already assigned to the solid object
        CSys(str)-This is Local (meaning the solid object local coordinate system) or the name of a defined coordinate
            system. This item is the coordinate system in which the user specified direction vector, Vec, is specified.
            This item applies only when SpringLocalOneType = 3
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.SolidObj.SetSpring(Name,MyType,s,SimpleSpringType,LinkProp,Face,SpringLocalOneType,Dir,
                                  Outward,Vec,Ang,Replace,CSys,itemType)

class SolidObj_Get:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def AutoMesh(self,name):
        """
        ---The name of an existing solid object---
        inputs:
        name(str)-The name of an existing solid object
        return:
        [index,MeshType,n1,n2,n3,MaxSize1,MaxSize2,MaxSize3,RestraintsOnEdge,RestraintsOnFace]

        MeshType(int)-This item is 0, 1 or 2, indicating the automatic mesh type for the solid object.
            0 = No automatic meshing
            1 = Mesh solid into a specified number of objects
            2 = Mesh solid into objects of a specified maximum size
        n1(int)-This item applies when MeshType = 1. It is the number of objects created along the edge of the
            meshed solid object that runs from point 1 to point 2
        n2(int)-This item applies when MeshType = 1. It is the number of objects created along the edge of the
            meshed solid object that runs from point 1 to point 3
        n3(int)-This item applies when MeshType = 1. It is the number of objects created along the edge of the
            meshed solid object that runs from point 1 to point 5
        MaxSize1(float)-This item applies when MeshType = 2. It is the maximum size of objects created along the
            edge of the meshed solid object that runs from point 1 to point 2. [L] If this item is input as 0, the
            default value is used. The default value is 48 inches if the database units are English or 120 centimeters
            if the database units are metric
        MaxSize2(float)-This item applies when MeshType = 2. It is the maximum size of objects created along the edge
            of the meshed solid object that runs from point 1 to point 3. [L] If this item is input as 0, the default
            value is used. The default value is 48 inches if the database units are English or 120 centimeters if the
            database units are metric.
        MaxSize3(float)-This item applies when MeshType = 2. It is the maximum size of objects created along the edge
            of the meshed solid object that runs from point 1 to point 5. [L] If this item is input as 0, the default
            value is used. The default value is 48 inches if the database units are English or 120 centimeters if the
            database units are metric.
        RestraintsOnEdge(bool)-If this item is True, and if both points along an edge of the original solid object have
            the same restraint/constraint, then, if the an added point on that edge and the original corner points have
            the same local axes definition, the program assigns the restraint/constraint to the added point
        RestraintsOnFace(bool)-If this item is True, and if all corner points on an solid object face have the same
            restraint/constraint, then, if an added point on that face and the original corner points for the face
            have the same local axes definition, the program assigns the restraint/constraint to the added point.
        """
        result=self.__Model.SolidObj.GetAutoMesh(name)
        return result

    def EdgeConstraint(self,name):
        """
        ---This function retrieves the generated edge constraint assignments to solid objects---
        inputs:
        name(str)-The name of an existing solid object
        return:
        [index,ConstraintExists]

        ConstraintExists(bool)-This item is True if an automatic edge constraint is generated by the
            program for the solid object in the analysis model
        """
        result=self.__Model.SolidObj.GetEdgeConstraint(name)
        return result

    def Elm(self,Name):
        """
        ---This function retrieves the names of the solid elements (analysis model solid) associated with a
        specified solid object in the object-based model
        ---
        inputs:
        Name(str)-The name of an existing solid object
        return:
        [index,nelm,Elm]

        nelm(int)-The number of solid elements created from the specified solid object
        Elm(str list)-An array that includes the name of a solid element created from the specified solid object
        """
        result=self.__Model.SolidObj.GetElm(Name)
        return result

    def GroupAssign(self,Name):
        """
        ---This function retrieves the names of the groups to which a specified solid object is assigned---
        inputs:
        Name(str)-The name of an existing solid object
        return:
        [index,NumberGroups,Groups]

        NumberGroups(int)-The number of group names retrieved
        Groups(str list)-The names of the groups to which the solid object is assigned
        """
        result=self.__Model.SolidObj.GetGroupAssign(Name)
        return result

    def LoadGravity(self,Name):
        """
        ---This function retrieves the gravity load assignments to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,SolidName,LoadPat,CSys,x,y,z]

        NumberItems(int)-The total number of gravity loads retrieved for the specified solid objects
        SolidName(str list)-This is an array that includes the name of the solid object associated with each gravity load
        LoadPat(str list)-This is an array that includes the name of the coordinate system in which the gravity load
            multipliers are specified
        CSys(str list)-This is an array that includes the name of the coordinate system associated with each gravity load
        x,y,z(float list)-These are arrays of gravity load multipliers in the x, y and z directions of the specified
            coordinate system
        """
        result=self.__Model.SolidObj.GetLoadGravity(Name)
        return result

    def LoadPorePressure(self,Name):
        """
        ---This function retrieves the pore pressure load assignments to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,SolidName,LoadPat,Value,PatternName]

        NumberItems(int)-The total number of pore pressure loads retrieved for the specified solid objects
        SolidName(str list)-This is an array that includes the name of the solid object associated with each pore pressure load
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each pore pressure load
        Value(float list)-This is an array that includes the pore pressure load value. [F/L2]
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify the pore
            pressure load
        """
        result=self.__Model.SolidObj.GetLoadPorePressure(Name)
        return result

    def LoadStrain(self,Name):
        """
        ---This function retrieves the strain load assignments to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,SolidName,LoadPat,Component,Value,PatternName]

        NumberItems(int)-The total number of strain loads retrieved for the specified solid objects
        SolidName(str list)-This is an array that includes the name of the solid object associated with each strain load
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each strain load
        Component(int)-This is 1, 2, 3, 4, 5 or 6, indicating the component to which the strain load is applied.
            1 = Strain11,2 = Strain22,3 = Strain33,4 = Strain12,5 = Strain13,6 = Strain23
        Value(float list)-This is an array that includes the strain value. [L/L]
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify the strain load
        """
        result=self.__Model.SolidObj.GetLoadStrain(Name)
        return result

    def LoadSurfacePressure(self,Name):
        """
        ---This function retrieves the surface pressure load assignments to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,SolidName,LoadPat,Face,Value,PatternName]

        NumberItems(int)-The total number of surface pressure loads retrieved for the specified solid objects
        SolidName(str list)-This is an array that includes the name of the solid object associated with each surface pressure load.
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each surface pressure load
        Face(int list)-This is an array that includes 1, 2, 3, 4, 5 or 6, indicating the solid object face to which the
            specified load assignment applies
        Value(float list)-This is an array that includes the surface pressure load value. [F/L2]
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify the
            surface pressure load
        """
        result=self.__Model.SolidObj.GetLoadSurfacePressure(Name)
        return result

    def LoadTemperature(self,Name):
        """
        ---This function retrieves the temperature load assignments to solid objects---
        inputs:
        Name(str)-The name of an existing solid object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,SolidName,LoadPat,Value,PatternName]

        NumberItems(int)-The total number of temperature loads retrieved for the specified solid objects
        SolidName(str list)-This is an array that includes the name of the solid object associated with each temperature load
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each temperature load
        Value(float list)-This is an array that includes the temperature load value. [T]
        PatternName(str list)-This is an array that includes the joint pattern name, if any, used to specify the temperature load
        """
        result=self.__Model.SolidObj.GetLoadTemperature(Name)
        return result

    def LocalAxes(self,Name):
        """
        ---This function retrieves the local axes angles for a solid object---
        inputs:
        Name(str)-The name of an existing solid object
        return:
        [index,a,b,c,Advanced]

        a,b,c(float)-The local axes of the solid object are defined by first setting the positive local 1, 2 and 3
            axes the same as the positive global X, Y and Z axes and then doing the following: [deg]
            1.Rotate about the 3 axis by angle a.
            2.Rotate about the resulting 2 axis by angle b.
            3.Rotate about the resulting 1 axis by angle c.
        Advanced(bool)-This item is True if the solid object local axes orientation was obtained using advanced
            local axes parameters
        """
        result=self.__Model.SolidObj.GetLocalAxes(Name)
        return result

    def MatTemp(self,Name):
        """
        ---This function retrieves the material temperature assignments to solid objects---
        inputs:
        Name(str)-The name of an existing solid object
        return:
        [index,Temp,PatternName]

        Temp(float)-This is the material temperature value assigned to the solid object. [T]
        PatternName(str)-This is blank or the name of a defined joint pattern. If it is blank, the material temperature
            for the solid object is uniform over the object at the value specified by Temp.If PatternName is the name
            of a defined joint pattern, the material temperature for the solid object may vary. The material temperature
            at each corner point of the solid object is equal to the specified temperature multiplied by the pattern value
            at the associated point object. The material temperature at other points in the solid object is calculated by
            interpolation from the corner points.
        """
        result=self.__Model.SolidObj.GetMatTemp(Name)
        return result

    def NameList(self):
        """
        ---This function retrieves the names of all defined solid objects---
        return:
        [index,NumberNames,MyName]

        NumberNames(int)-The number of solid object names retrieved by the program
        MyName(str list)-This is a one-dimensional array of solid object names
        """
        result=self.__Model.SolidObj.GetNameList()
        return result

    def Points(self,Name):
        """
        ---This function retrieves the names of the corner point objects of a solid object---
        inputs:
        Name(str)-The name of a defined solid object
        return:
        [index,Point]

        Point(str list)-This is an array containing the names of the corner point objects of the solid object
        """
        result=self.__Model.SolidObj.GetPoints(Name)
        return result

    def Property(self,Name):
        """
        ---This function retrieves the solid property assigned to a solid object---
        inputs:
        Name(str)-The name of a defined solid object
        return:
        [index,PropName]

        PropName(str)-The name of the solid property assigned to the solid object
        """
        result=self.__Model.SolidObj.GetProperty(Name)
        return result

    def Spring(self,Name):
        """
        ---This function retrieves the spring assignments to a solid object face---
        inputs:
        Name(str)-The name of an existing solid object
        return:
        [index,NumberSprings,MyType,s,SimpleSpringType,LinkProp,Face,SpringLocalOneType,Dir,Outward,VecX,
        VecY,VecZ,CSys,Ang]

        NumberSprings(int)-The number of springs assignments made to the specified solid object
        MyType(int)-This is either 1 or 2, indicating the spring property type.
            1 = Simple spring,2 = Link property
        s(float)-The simple spring stiffness per unit area of the specified solid object face. This item applies
            only when MyType = 1. [F/L3]
        SimpleSpringType(int)-This is 1, 2 or 3, indicating the simple spring type. This item applies only when MyType = 1.
            1 = Spring resists tension and compression
            2 = Spring resists compression only
            3 = Spring resists tension only
        LinkProp(str)-The name of the link property assigned to the spring. This item applies only when MyType = 2
        Face(int)-This is 1, 2, 3, 4, 5 or 6, indicating the solid object face to which the specified spring assignment applies
        SpringLocalOneType(int)-This is 1, 2 or 3, indicating the method used to specify the spring positive local 1-axis
            orientation.
            1 = Parallel to solid object local axis
            2 = Normal to specified solid object face
            3 = User specified direction vector
        Dir(int)-This is 1, 2, 3, -1, -2 or -3, indicating the solid object local axis that corresponds to the
            positive local 1-axis of the spring. This item applies only when SpringLocalOneType = 1.
        Outward(bool)-This item is True if the spring positive local 1 axis is outward from the specified solid object
            face. This item applies only when SpringLocalOneType = 2.
        VecX(float list)-Each value in this array is the X-axis or solid object local 1-axis component (depending on
            the CSys specified) of the user specified direction vector for the spring local 1-axis. The direction
            vector is in the coordinate system specified by the CSys item. This item applies only when the corresponding
            SpringLocalOneType = 3.
        VecY(float list)-Each value in this array is the Y-axis or solid object local 2-axis component (depending on
            the CSys specified) of the user specified direction vector for the spring local 1-axis. The direction
            vector is in the coordinate system specified by the CSys item. This item applies only when the corresponding
            SpringLocalOneType = 3.
        VecZ(float list)-Each value in this array is the X-axis or solid object local 3-axis component (depending on the
            CSys specified) of the user specified direction vector for the spring local 1-axis. The direction vector is
            in the coordinate system specified by the CSys item. This item applies only when the corresponding SpringLocalOneType = 3.
        CSys(str)-This is Local (meaning the solid object local coordinate system) or the name of a defined coordinate
            system. This item is the coordinate system in which the user specified direction vector, Vec, is specified.
            This item applies only when SpringLocalOneType = 3
        Ang(float)-This is the angle that the link local 2-axis is rotated from its default orientation.
            This item applies only when MyType = 2. [deg]
        """
        result=self.__Model.SolidObj.GetSpring(Name)
        return result

    def TransformationMatrix(self,Name):
        """
        ---The function returns zero if the solid object transformation matrix is successfully retrieved---
        inputs:
        Name(str)-The name of an existing solid object
        return:
        [index,Value]

        Value(float list)-Value is an array of nine direction cosines that define the transformation matrix.The following
            matrix equation shows how the transformation matrix is used to convert items from the solid object local
            coordinate system to the global coordinate system.In the equation, c0 through c8 are the nine values from
            the transformation array, (Local1, Local2, Local3) are an item (such as a load) in the object local coordinate
            system, and (GlobalX, GlobalY, GlobalZ) are the same item in the global coordinate system.The transformation
            from the local coordinate system to the present coordinate system is the same as that shown above for the global
            system if you substitute the present system for the global system.
        """
        result=self.__Model.SolidObj.GetTransformationMatrix(Name)
        return result

class SapSolidObj:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model
        self.Set = SolidObj_Set(Sapobj)
        self.Get = SolidObj_Get(Sapobj)

    def AddByCoord(self,x,y,z,PropName="Default",UserName="",CSys="Global"):
        """
        ---This function adds a new solid object whose corner points are at the specified coordinates. Note that
        solid objects always are defined with eight corner points
        ---
        inputs:
        x,y,z(float list)-These are arrays of x, y and z coordinates, respectively, for the corner points of the
            solid object. The coordinates are in the coordinate system defined by the CSys item.
        PropName(str)-This is either Default or the name of a defined solid property.If it is Default, the program
            assigns a default solid property to the solid object. If it is the name of a defined solid property,
            that property is assigned to the solid object
        UserName(str)-This is an optional user specified name for the solid object. If a UserName is specified and
            that name is already used for another solid object, the program ignores the UserName
        CSys(str)-The name of the coordinate system in which the solid object point coordinates are defined
        """
        # This is the name that the program ultimately assigns for the solid object. If no UserName is specified,
        # the program assigns a default name to the solid object. If a UserName is specified and that name is not
        # used for another solid object, the UserName is assigned to the solid object; otherwise a default name is
        # assigned to the solid object.
        name = ""
        self.__Model.SolidObj.AddByCoord(x,y,z,name,PropName,UserName,CSys)

    def AddByPoint(self,Point,PropName="Default",UserName=""):
        """
        ---This function adds a new solid object whose corner points are specified by name---
        inputs:
        Point(str list)-This is an array containing the names of the eight point objects that define
            the corner points of the added solid object
        PropName(str)-This is either Default or the name of a defined solid property
        UserName(str)-This is an optional user specified name for the solid object. If a UserName is specified
            and that name is already used for another solid object, the program ignores the UserName
        """
        # This is the name that the program ultimately assigns for the solid object. If no UserName is specified,
        # the program assigns a default name to the solid object. If a UserName is specified and that name is not
        # used for another solid object, the UserName is assigned to the solid object; otherwise a default name is
        # assigned to the solid object.
        name = ""
        self.__Model.SolidObj.AddByPoint(Point,name,PropName,UserName)

    def Count(self):
        """
        ---This function returns a count of the solid objects in the model---
        """
        result=self.__Model.SolidObj.Count()
        return result


class LinkObj_Set:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def GroupAssign(self,Name,GroupName,Remove=False,itemType=0):
        """
        ---This function adds or removes link objects from a specified group---
        inputs:
        Name(str)-The name of an existing link object or group, depending on the value of the ItemType item
        GroupName(str)-The name of an existing group to which the assignment is made
        Remove(bool)-If this item is False, the specified link objects are added to the group specified by the
            GroupName item. If it is True, the link objects are removed from the group
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.LinkObj.SetGroupAssign(Name,GroupName,Remove,itemType)

    def LoadDeformation(self,Name,LoadPat,DOF,d,itemType=0):
        """
        ---This function assigns deformation loads to link objects---
        inputs:
        Name(str)-The name of an existing link object or group, depending on the value of the ItemType item
        LoadPat(int)-This is one(str)-The name of a defined load pattern
        DOF(bool list)-This is a array of boolean values indicating if the considered degree of freedom has a deformation load.
            DOF(1) = U1,DOF(2) = U2,DOF(3) = U3,DOF(4) = R1,DOF(5) = R2,DOF(6) = R3
        d(float list)-This is a array of deformation load values. The deformations specified for a given degree of
            freedom are applied only if the corresponding DOF item for that degree of freedom is True.
            d(1) = U1 deformation [L]
            d(2) = U2 deformation [L]
            d(3) = U3 deformation [L]
            d(4) = R1 deformation [rad]
            d(5) = R2 deformation [rad]
            d(6) = R3 deformation [rad]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.LinkObj.SetLoadDeformation(Name,LoadPat,DOF,d,itemType)

    def LoadGravity(self,Name,LoadPat,x,y,z,Replace=True,CSys="Global",itemType=0):
        """
        ---This function assigns gravity load multipliers to link objects---
        inputs:
        Name(str)-The name of an existing link object or group, depending on the value of the ItemType item
        LoadPat(str)-The name of a defined load pattern
        x,y,z(float)-These are the gravity load multipliers in the x, y and z directions of the specified coordinate system
        Replace(bool)-If this item is True, all previous gravity loads, if any, assigned to the specified link object(s),
            in the specified load pattern, are deleted before making the new assignment
        CSys(str)-The coordinate system in which the x, y and z multipliers are specified
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.LinkObj.SetLoadGravity(Name,LoadPat,x,y,z,Replace,CSys,itemType)

    def LoadTargetForce(self,Name,LoadPat,DOF,f,RD,itemType=0):
        """
        ---This function assigns target forces to frame objects---
        inputs:
        Name(str)-The name of an existing link object or group, depending on the value of the ItemType item
        LoadPat(str)-The name of a defined load pattern
        DOF(float list)-This is a array of boolean values indicating if the considered degree of freedom has a target force.
            DOF(1) = P,DOF(2) = V2,DOF(3) = V3,DOF(4) = T,DOF(5) = M2,DOF(6) = M3
        f(float list)-This is a array of target force values. The target forces specified for a given degree of freedom
            are applied only if the corresponding DOF item for that degree of freedom is True.
            f(1) = P [F]
            f(2) = V2 [F]
            f(3) = V3 [F]
            f(4) = T [FL]
            f(5) = M2 [FL]
            f(6) = M3 [FL]
        RD(float list)-This is a array of relative distances along the link objects where the target force values apply.
            The relative distances specified for a given degree of freedom are applicable only if the corresponding DOF
            item for that degree of freedom is True. The relative distance must be between 0 and 1, 0 <= RD <=1.
            RD(1) = relative location for P target force
            RD(2) = relative location for V2 target force
            RD(3) = relative location for V3 target force
            RD(4) = relative location for T target force
            RD(5) = relative location for M2 target force
            RD(6) = relative location for M3 target force
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.LinkObj.SetLoadTargetForce(Name,LoadPat,DOF,f,RD,itemType)

    def LocalAxes(self,Name,Ang,itemType=0):
        """
        ---This function assigns a local axis angle to link objects---
        inputs:
        Name(str)-The name of an existing link object or group, depending on the value of the ItemType item
        Ang(float)-This is the angle that the local 2 and 3 axes are rotated about the positive local 1 axis,
            from the default orientation or, if the Advanced item is True, from the orientation determined
            by the plane reference vector. The rotation for a positive angle appears counter clockwise when
            the local +1 axis is pointing toward you. [deg]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.LinkObj.SetLocalAxes(Name,Ang,itemType)

    def Property(self,Name,PropName,itemType=0):
        """
        ---This function assigns a link property to link objects---
        inputs:
        Name(str)-The name of an existing link object or group, depending on the value of the ItemType item
        PropName(str)-This is the name of a link property to be assigned to the specified link object(s).
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.LinkObj.SetProperty(Name,PropName,itemType)

    def PropertyFD(self,Name,PropName,itemType=0):
        """
        ---This function assigns a frequency dependent link property to link objects---
        inputs:
        Name(str)-The name of an existing link object or group, depending on the value of the ItemType item
        PropName(str)-This is either None or the name of a frequency dependent link property to be assigned to the
            specified link object(s). None means that no frequency dependent link property is assigned to the link object
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        self.__Model.LinkObj.SetPropertyFD(Name,PropName,itemType)

class LinkObj_Get:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def Elm(self,Name):
        """
        ---This function retrieves the name of the link element (analysis model link) associated with a specified
        link object in the object-based model
        ---
        inputs:
        Name(str)-The name of an existing link object
        return:
        [index,Elm]

        Elm(str)-The name of the link element created from the specified link object
        """
        result=self.__Model.LinkObj.GetElm(Name)
        return result

    def GroupAssign(self,Name):
        """
        ---This function retrieves the names of the groups to which a specified link object is assigned---
        inputs:
        Name(str)-The name of an existing link object
        return:
        [index,NumberGroups,Groups]

        NumberGroups(int)-The number of group names retrieved
        Groups(str list)-The names of the groups to which the link object is assigned
        """
        result=self.__Model.LinkObj.GetGroupAssign(Name)
        return result

    def LoadDeformation(self,Name):
        """
        ---This function retrieves the deformation load assignments to link objects---
        inputs:
        Name(str)-The name of an existing link object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,LinkName,LoadPat,dof1,dof2,dof3,dof4,dof5,dof6,U1,U2,U3,R1,R2,R3,itemType=0]

        NumberItems(int)-The total number of deformation loads retrieved for the specified link objects
        LinkName(str list)-This is an array that includes the name of the link object associated with each deformation load
        LoadPat(str list)-This is an array that includes the name of the load pattern associated with each deformation load
        dof1,dof2,dof3,dof4,dof5,dof6(bool)-These are arrays of boolean values, indicating if the considered degree of
            freedom has a deformation load.
            dof1 = U1
            dof2 = U2
            dof3 = U3
            dof4 = R1
            dof5 = R2
            dof6 = R3
        U1,U2,U3,R1,R2,R3(float)-These are arrays of deformation load values. The deformations specified for a given
            degree of freedom are applicable only if the corresponding DOF item for that degree of freedom is True.
            U1 = U1 deformation [L]
            U2 = U2 deformation [L]
            U3 = U3 deformation [L]
            R1 = R1 deformation [rad]
            R2 = R2 deformation [rad]
            R3 = R3 deformation [rad]
        itemType(int)-This is one of the following items in the eItemType enumeration:
            Object = 0,Group = 1,SelectedObjects = 2
            If this item is Object, the frame object specified by the Name item is deleted.
            If this item is Group, all of the frame objects in the group specified by the Name item are deleted.
            If this item is SelectedObjects, all selected frame objects are deleted, and the Name item is ignore
        """
        result=self.__Model.LinkObj.GetLoadDeformation(Name)
        return result

    def LoadGravity(self,Name):
        """
        ---This function retrieves the gravity load assignments to link objects---
        inputs:
        Name(str)-The name of an existing link object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,LinkName,LoadPat,CSys,x,y,z]

        NumberItems(int)-The total number of gravity loads retrieved for the specified link objects
        LinkName(str list)-This is an array that includes the name of the link object associated with each gravity load.
        LoadPat(str list)-This is an array that includes the name of the coordinate system in which the gravity load
            multipliers are specified
        CSys(str list)-This is an array that includes the name of the coordinate system associated with each gravity load
        x,y,z(float)-These are arrays of gravity load multipliers in the x, y and z directions of the specified coordinate system
        """
        result=self.__Model.LinkObj.GetLoadGravity(Name)
        return result

    def LoadTargetForce(self,Name):
        """
        ---This function retrieves the target force assignments to link objects---
        inputs:
        Name(str)-The name of an existing link object or group, depending on the value of the ItemType item
        return:
        [index,NumberItems,LinkName,LoadPat,dof1,dof2,dof3,dof4,dof5,dof6,P,V2,V3,T,M2,M3,T1,T2,T3,T4,T5,T6]

        NumberItems(int)-The total number of deformation loads retrieved for the specified link objects
        LinkName(str)-This is an array that includes the name of the link object associated with each target force
        LoadPat(str)-This is an array that includes the name of the load pattern associated with each target force
        dof1,dof2,dof3,dof4,dof5,dof6(bool)-These are arrays of boolean values indicating if the considered degree of
            freedom has a target force assignment.
            dof1 = P
            dof2 = V2
            dof3 = V3
            dof4 = T
            dof5 = M2
            dof6 = M3
        P,V2,V3,T,M2,M3(float)-These are arrays of target force values. The target forces specified for a given
            degree of freedom are applicable only if the corresponding DOF item for that degree of freedom is True.
            U1 = U1 deformation [L]
            U2 = U2 deformation [L]
            U3 = U3 deformation [L]
            R1 = R1 deformation [rad]
            R2 = R2 deformation [rad]
            R3 = R3 deformation [rad]
        T1,T2,T3,T4,T5,T6(float)-These are arrays of the relative distances along the link objects where the target
            force values apply. The relative distances specified for a given degree of freedom are applicable only
            if the corresponding dofn item for that degree of freedom is True.
            T1 = relative location for P target force
            T2 = relative location for V2 target force
            T3 = relative location for V3 target force
            T4 = relative location for T target force
            T5 = relative location for M2 target force
            T6 = relative location for M3 target force
        """
        result=self.__Model.LinkObj.GetLoadTargetForce(Name)
        return result

    def LocalAxes(self,Name):
        """
        ---This function retrieves the local axis angle assignment for link objects---
        inputs:
        Name(str)-The name of an existing link object
        return:
        [index,Ang,Advanced]

        Ang(float)-This is the angle that the local 2 and 3 axes are rotated about the positive local 1 axis, from the
            default orientation or, if the Advanced item is True, from the orientation determined by the plane reference
            vector. The rotation for a positive angle appears counter clockwise when the local +1 axis is pointing toward
            you. [deg]
        Advanced(bool)-This item is True if the link object local axes orientation was obtained using advanced local axes parameters
        """
        result=self.__Model.LinkObj.GetLocalAxes(Name)
        return result

    def NameList(self):
        """
        ---This function retrieves the names of all defined link objects---
        return:
        [index,NumberNames,MyName]

        NumberNames(int)-The number of link object names retrieved by the program
        MyName(str list)-This is a one-dimensional array of link object names
        """
        result=self.__Model.LinkObj.GetNameList()
        return result

    def Points(self,Name):
        """
        ---This function retrieves the names of the point objects at each end of a specified link object---
        inputs:
        Name(str)-The name of a defined link object
        return:
        [index,Point1,Point2]

        Point1(str)-The name of the point object at the I-End of the specified link object
        Point2(str)-The name of the point object at the J-End of the specified link object
        """
        result=self.__Model.LinkObj.GetPoints(Name)
        return result

    def Property(self,Name):
        """
        ---This function retrieves the link property assigned to a link object---
        inputs:
        Name(str)-The name of a defined link object
        return:
        [index,PropName]

        PropName(str)-The name of the link property assigned to the link object
        """
        result=self.__Model.LinkObj.GetProperty(Name)
        return result

    def PropertyFD(self,Name):
        """
        ---This function retrieves the frequency dependent link property assigned to a link object---
        inputs:
        Name(str)-The name of a defined link object
        return:
        [index,PropName]

        PropName(str)-The name of the frequency dependent link property assigned to the link object. This item is
            None if there is no frequency dependent link property assigned to the link object
        """
        result=self.__Model.LinkObj.GetPropertyFD(Name)
        return result

    def TransformationMatrix(self,Name):
        """
        ---The function returns zero if the link object transformation matrix is successfully retrieved;
        otherwise it returns a nonzero value
        ---
        inputs:
        Name(str)-The name of an existing link object
        return:
        [index,Value]

        Value(float list)-Value is an array of nine direction cosines that define the transformation matrix.The following
            matrix equation shows how the transformation matrix is used to convert items from the link object local
            coordinate system to the global coordinate system.In the equation, c0 through c8 are the nine values from
            the transformation array, (Local1, Local2, Local3) are an item (such as a load) in the object local coordinate
            system, and (GlobalX, GlobalY, GlobalZ) are the same item in the global coordinate system.The transformation
            from the local coordinate system to the present coordinate system is the same as that shown above for the global
            system if you substitute the present system for the global system.
        """
        result=self.__Model.LinkObj.GetTransformationMatrix(Name)
        return result

class SapLinkObj:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model
        self.Set = LinkObj_Set(Sapobj)
        self.Get = LinkObj_Get(Sapobj)

    def AddByCoord(self,xi,yi,zi,xj,yj,zj,IsSingleJoint=False,PropName="Default",
                                  UserName="",CSys="Global"):
        """
        ---This function adds a new link object whose end points are at the specified coordinates---
        inputs:
        xi,yi,zi(float)-The coordinates of the I-End of the added link object. The coordinates are in the coordinate
            system defined by the CSys item
        xj,yj,zj(float)-The coordinates of the J-End of the added link object. The coordinates are in the coordinate
            system defined by the CSys item
        IsSingleJoint(bool)-This item is True if a one-joint link is added and False if a two-joint link is added
        PropName(str)-This is either Default or the name of a defined link property.If it is Default the program
            assigns a default link property to the link object. If it is the name of a defined link property, that
            property is assigned to the link object
        UserName(str)-This is an optional user specified name for the link object. If a UserName is specified and
            that name is already used for another link object, the program ignores the UserName
        CSys(str)-The name of the coordinate system in which the link object end point coordinates are defined
        """
        #This is the name that the program ultimately assigns for the link object. If no UserName is specified,
        # the program assigns a default name to the link object. If a UserName is specified and that name is not
        # used for another link object, the UserName is assigned to the link object; otherwise a default name is
        # assigned to the link object
        Name=""
        self.__Model.LinkObj.AddByCoord(xi,yi,zi,xj,yj,zj,Name,IsSingleJoint,PropName,UserName,CSys)

    def AddByPoint(self,Point1,Point2,IsSingleJoint=False,PropName="Default",UserName=""):
        """
        ---This function adds a new link object whose end points are specified by name---
        inputs:
        Point1(str)-The name of a defined point object at the I-End of the added link object
        Point2(str)-The name of a defined point object at the J-End of the added link object.
            This item is ignored if the IsSingleJoint item is True
        IsSingleJoint(bool)-This item is True if a one-joint link is added and False if a two-joint link is added
        PropName(str)-This is either Default or the name of a defined link property.If it is Default the program
            assigns a default link property to the link object. If it is the name of a defined link property, that
            property is assigned to the link object
        UserName(str)-This is an optional user specified name for the link object. If a UserName is specified and
            that name is already used for another link object, the program ignores the UserName
        """
        # This is the name that the program ultimately assigns for the link object. If no UserName is specified,
        # the program assigns a default name to the link object. If a UserName is specified and that name is not
        # used for another link object, the UserName is assigned to the link object; otherwise a default name is
        # assigned to the link object
        Name = ""
        self.__Model.LinkObj.AddByPoint(Point1,Point2,Name,IsSingleJoint,PropName,UserName)

    def Count(self):
        """
        ---This function returns a count of the link objects in the model---
        """
        result=self.__Model.LinkObj.Count()
        return result
