

class jointConstraints:
    def __init__(self,Sapobj):
        """
        Translation: Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def SetBody(self,name,value,Csys="Global"):
        """
        ---This function defines a Body constraint.---
        inputs:
        name(str)-The name of an existing constraint.
        value(list)-indicate which joint degrees of freedom are included in the constraint. In order, the degrees of freedom
            addressed in the list are UX, UY, UZ, RX, RY and RZ.
        Csys(str)-The name of the coordinate system in which the constraint is defined.
        """
        valueDict = {"UX": 0, "UY": 1, "UZ": 2, "RX": 3, "RY": 4, "RZ": 5}
        valueFinal = [False, False, False, False, False, False]
        for each in value:
            indexNum = valueDict[each]
            valueFinal[indexNum] = True
        self.__Model.ConstraintDef.SetBody(name,valueFinal,Csys)

    def SetBeam(self,name,Axis=4,Csys="Global"):
        """
        ---This function defines a Beam constraint---
        inputs:
        name(str)-The name of a constraint.
        Axis(int)-This is one of the following items from the eConstraintAxis enumeration.
            It specifies the axis in the specified coordinate system that is parallel to the axis of the constraint.
            If AutoAxis is specified, the axis of the constraint is automatically determined from the joints assigned
            to the constraint.X = 1,Y = 2,Z = 3,AutoAxis = 4
        Csys(str)-The name of the coordinate system in which the constraint is defined.
        """
        self.__Model.ConstraintDef.SetBeam(name,Axis,Csys)

    def SetDiaphragm(self,name,Axis=4,Csys="Global"):
        """
        ---This function defines a Diaphragm constraint.---
        name(str)-The name of a constraint.
        Axis(int)-This is one of the following items from the eConstraintAxis enumeration.
            It specifies the axis in the specified coordinate system that is parallel to the axis of the constraint.
            If AutoAxis is specified, the axis of the constraint is automatically determined from the joints assigned
            to the constraint.X = 1,Y = 2,Z = 3,AutoAxis = 4
        Csys(str)-The name of the coordinate system in which the constraint is defined.
        """
        self.__Model.ConstraintDef.SetDiaphragm(name,Axis,Csys)

    def SetEqual(self,name,value,Csys="Global"):
        """
        ---This function defines an Equal constraint.---
        inputs:
        name(str)-The name of an existing constraint.
        value(list)-indicate which joint degrees of freedom are included in the constraint. In order, the degrees of freedom
            addressed in the list are UX, UY, UZ, RX, RY and RZ.
        Csys(str)-The name of the coordinate system in which the constraint is defined.
        """
        valueDict = {"UX": 0, "UY": 1, "UZ": 2, "RX": 3, "RY": 4, "RZ": 5}
        valueFinal = [False, False, False, False, False, False]
        for each in value:
            indexNum = valueDict[each]
            valueFinal[indexNum] = True
        self.__Model.ConstraintDef.SetEqual(name,valueFinal,Csys)

    def SetLine(self,name,value,Csys="Global"):
        """
        ---This function defines a Line constraint---
        inputs:
        name(str)-The name of an existing constraint.
        value(list)-indicate which joint degrees of freedom are included in the constraint. In order, the degrees of freedom
            addressed in the list are UX, UY, UZ, RX, RY and RZ.
        Csys(str)-The name of the coordinate system in which the constraint is defined.
        """
        valueDict = {"UX": 0, "UY": 1, "UZ": 2, "RX": 3, "RY": 4, "RZ": 5}
        valueFinal = [False, False, False, False, False, False]
        for each in value:
            indexNum = valueDict[each]
            valueFinal[indexNum] = True
        self.__Model.ConstraintDef.SetLine(name,valueFinal,Csys)

    def SetLocal(self,name,value):
        """
        ---This function defines a Local constraint---
        inputs:
        name(str)-The name of an existing constraint.
        value(list)-indicate which joint degrees of freedom are included in the constraint. In order, the degrees of freedom
            addressed in the list are U1, U2, U3, R1, R2 and R3.
        """
        valueDict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        valueFinal = [False, False, False, False, False, False]
        for each in value:
            indexNum = valueDict[each]
            valueFinal[indexNum] = True
        self.__Model.ConstraintDef.SetLocal(name,valueFinal)

    def SetPlate(self,name,Axis=4,Csys="Global"):
        """
        ---This function defines a Plate constraint---
        inputs:
        name(str)-The name of a constraint.
        Axis(int)-the eConstraintAxis enumeration. It specifies the axis in the specified coordinate system
            that is perpendicular to the plane of the constraint. If AutoAxis is specified, the axis of the
            constraint is automatically determined from the joints assigned to the constraint.X = 1,Y = 2,Z = 3
            AutoAxis = 4
        Csys(str)-The name of the coordinate system in which the constraint is defined.
        """
        self.__Model.ConstraintDef.SetPlate(name,Axis,Csys)

    def SetRod(self,name,Axis=4,Csys="Global"):
        """
        ---This function defines a Rod constraint---
        inputs:
        name(str)-The name of a constraint.
        Axis(int)-This is one of the following items from the eConstraintAxis enumeration. It specifies the axis
            in the specified coordinate system that is parallel to the axis of the constraint. If AutoAxis is
            specified, the axis of the constraint is automatically determined from the joints assigned to the
            constraint.X = 1,Y = 2,Z = 3,AutoAxis = 4
        Csys(str)-The name of the coordinate system in which the constraint is defined.
        """
        self.__Model.ConstraintDef.SetRod(name,Axis,Csys)

    def SetWeld(self,name,value,Tolerance,Csys="Global"):
        """
        ---This function defines a Weld constraint---
        inputs:
        name(str)-The name of an existing constraint.
        value(list)-indicate which joint degrees of freedom are included in the constraint. In order,
            the degrees of freedom addressed in the array are UX, UY, UZ, RX, RY and RZ.
        Tolerance(float)-Joints within this distance of each other are constrained together.
        Csys(str)-The name of the coordinate system in which the constraint is defined.
        """
        valueDict = {"UX": 0, "UY": 1, "UZ": 2, "RX": 3, "RY": 4, "RZ": 5}
        valueFinal = [False, False, False, False, False, False]
        for each in value:
            indexNum = valueDict[each]
            valueFinal[indexNum] = True
        self.__Model.ConstraintDef.SetWeld(name,valueFinal,Tolerance)
