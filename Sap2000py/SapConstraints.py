
from typing import Literal


class JointConstraints:
    """Constraint class."""

    def __init__(self, sap_obj):
        """
        Initialize the constraint class.

        Passing in the parent class object directly is to avoid
        getting only the last opened SAP2000 window when initializing the
        parent class instance to get the model pointer in the subclass.

        Args:
            sap_obj: SAP2000 object.
        """
        self.__object = sap_obj._Object
        self.__model = sap_obj._Model
        self.Set = JointConstraintsSet(sap_obj)
        self.Get = JointConstraintsGet(sap_obj)

class JointConstraintsSet:
    """Constraint setting class."""

    def __init__(self, sap_obj):
        """
        Initialize the constraint setting class.

        Passing in the parent class object directly is to avoid
        getting only the last opened SAP2000 window when initializing the
        parent class instance to get the model pointer in the subclass.

        Args:
            sap_obj: SAP2000 object.
        """
        self.__object = sap_obj._Object
        self.__model = sap_obj._Model

    def Body(self, name: str, value: list[Literal["UX", "UY", "UZ", "RX", "RY", "RZ"]], csys: str = "Global"):
        """
        Define a Body constraint.

        Args:
            name: The name of an existing constraint.
            value: Indicate which joint degrees of freedom are included in the constraint.
                   In order, the degrees of freedom addressed in the list are UX, UY, UZ, RX, RY and RZ.
            csys: The name of the coordinate system in which the constraint is defined.

        Returns:
            ret (int): Returns 0 if successful, otherwise returns a nonzero value.
        """
        value_dict = {"UX": 0, "UY": 1, "UZ": 2, "RX": 3, "RY": 4, "RZ": 5}
        value_final = [False] * 6
        for each in value:
            index_num = value_dict[each]
            value_final[index_num] = True
        return self.__model.ConstraintDef.SetBody(name, value_final, csys)

    def Beam(self, name: str, axis: Literal["X", "Y", "Z", "AutoAxis"] = "AutoAxis", csys: str = "Global"):
        """
        Define a Beam constraint.

        Args:
            name: The name of a constraint.
            axis: This is one of the items from the eConstraintAxis enumeration.
                  It specifies the axis in the specified coordinate system that is parallel to the axis of the constraint.
                  If AutoAxis is specified, the axis of the constraint is automatically determined from the joints assigned
                  to the constraint. X = 1, Y = 2, Z = 3, AutoAxis = 4
            csys: The name of the coordinate system in which the constraint is defined.

        Returns:
            ret (int): Returns 0 if successful, otherwise returns a nonzero value.
        """
        axis_dict = {"X": 1, "Y": 2, "Z": 3, "AutoAxis": 4}
        axis_value = axis_dict[axis]
        return self.__model.ConstraintDef.SetBeam(name, axis_value, csys)

    def Diaphragm(self, name: str, axis: Literal["X", "Y", "Z", "AutoAxis"] = "AutoAxis", csys: str = "Global"):
        """
        Define a Diaphragm constraint.

        Args:
            name: The name of a constraint.
            axis: This is one of the items from the eConstraintAxis enumeration.
                  It specifies the axis in the specified coordinate system that is parallel to the axis of the constraint.
                  If AutoAxis is specified, the axis of the constraint is automatically determined from the joints assigned
                  to the constraint. X = 1, Y = 2, Z = 3, AutoAxis = 4
            csys: The name of the coordinate system in which the constraint is defined.

        Returns:
            ret (int): Returns 0 if successful, otherwise returns a nonzero value.
        """
        axis_dict = {"X": 1, "Y": 2, "Z": 3, "AutoAxis": 4}
        axis_value = axis_dict[axis]
        return self.__model.ConstraintDef.SetDiaphragm(name, axis_value, csys)

    def Equal(self, name: str, value: list[Literal["UX", "UY", "UZ", "RX", "RY", "RZ"]], csys: str = "Global"):
        """
        Define an Equal constraint.

        Args:
            name: The name of an existing constraint.
            value: Indicate which joint degrees of freedom are included in the constraint.
                   In order, the degrees of freedom addressed in the list are UX, UY, UZ, RX, RY and RZ.
            csys: The name of the coordinate system in which the constraint is defined.

        Returns:
            ret (int): Returns 0 if successful, otherwise returns a nonzero value.
        """
        value_dict = {"UX": 0, "UY": 1, "UZ": 2, "RX": 3, "RY": 4, "RZ": 5}
        value_final = [False] * 6
        for each in value:
            index_num = value_dict[each]
            value_final[index_num] = True
        return self.__model.ConstraintDef.SetEqual(name, value_final, csys)

    def Pine(self, name: str, value: list[Literal["UX", "UY", "UZ", "RX", "RY", "RZ"]], csys: str = "Global"):
        """
        Define a Line constraint.

        Args:
            name: The name of an existing constraint.
            value: Indicate which joint degrees of freedom are included in the constraint.
                   In order, the degrees of freedom addressed in the list are UX, UY, UZ, RX, RY and RZ.
            csys: The name of the coordinate system in which the constraint is defined.

        Returns:
            ret (int): Returns 0 if successful, otherwise returns a nonzero value.
        """
        value_dict = {"UX": 0, "UY": 1, "UZ": 2, "RX": 3, "RY": 4, "RZ": 5}
        value_final = [False] * 6
        for each in value:
            index_num = value_dict[each]
            value_final[index_num] = True
        return self.__model.ConstraintDef.SetLine(name, value_final, csys)

    def Pocal(self, name: str, value: list[Literal["U1", "U2", "U3", "R1", "R2", "R3"]]):
        """
        Define a Local constraint.

        Args:
            name: The name of an existing constraint.
            value: Indicate which joint degrees of freedom are included in the constraint.
                   In order, the degrees of freedom addressed in the list are U1, U2, U3, R1, R2 and R3.

        Returns:
            ret (int): Returns 0 if successful, otherwise returns a nonzero value.
        """
        value_dict = {"U1": 0, "U2": 1, "U3": 2, "R1": 3, "R2": 4, "R3": 5}
        value_final = [False] * 6
        for each in value:
            index_num = value_dict[each]
            value_final[index_num] = True
        return self.__model.ConstraintDef.SetLocal(name, value_final)

    def Plate(self, name: str, axis: Literal["X", "Y", "Z", "AutoAxis"] = "AutoAxis", csys: str = "Global"):
        """
        Define a Plate constraint.

        Args:
            name: The name of a constraint.
            axis: The eConstraintAxis enumeration. It specifies the axis in the specified coordinate system
                  that is perpendicular to the plane of the constraint. If AutoAxis is specified, the axis of the
                  constraint is automatically determined from the joints assigned to the constraint.
                  X = 1, Y = 2, Z = 3, AutoAxis = 4
            csys: The name of the coordinate system in which the constraint is defined.

        Returns:
            ret (int): Returns 0 if successful, otherwise returns a nonzero value.
        """
        axis_dict = {"X": 1, "Y": 2, "Z": 3, "AutoAxis": 4}
        axis_value = axis_dict[axis]
        return self.__model.ConstraintDef.SetPlate(name, axis_value, csys)

    def Rod(self, name: str, axis: Literal["X", "Y", "Z", "AutoAxis"] = "AutoAxis", csys: str = "Global"):
        """
        Define a Rod constraint.

        Args:
            name: The name of a constraint.
            axis: This is one of the items from the eConstraintAxis enumeration. It specifies the axis
                  in the specified coordinate system that is parallel to the axis of the constraint. If AutoAxis is
                  specified, the axis of the constraint is automatically determined from the joints assigned to the
                  constraint. X = 1, Y = 2, Z = 3, AutoAxis = 4
            csys: The name of the coordinate system in which the constraint is defined.

        Returns:
            ret (int): Returns 0 if successful, otherwise returns a nonzero value.
        """
        axis_dict = {"X": 1, "Y": 2, "Z": 3, "AutoAxis": 4}
        axis_value = axis_dict[axis]
        return self.__model.ConstraintDef.SetRod(name, axis_value, csys)

    def Weld(self, name: str, value: list[Literal["UX", "UY", "UZ", "RX", "RY", "RZ"]], tolerance: float, csys: str = "Global"):
        """
        Define a Weld constraint.

        Args:
            name: The name of an existing constraint.
            value: Indicate which joint degrees of freedom are included in the constraint. In order,
                   the degrees of freedom addressed in the array are UX, UY, UZ, RX, RY and RZ.
            tolerance: Joints within this distance of each other are constrained together.
            csys: The name of the coordinate system in which the constraint is defined.

        Returns:
            ret (int): Returns 0 if successful, otherwise returns a nonzero value.
        """
        value_dict = {"UX": 0, "UY": 1, "UZ": 2, "RX": 3, "RY": 4, "RZ": 5}
        value_final = [False] * 6
        for each in value:
            index_num = value_dict[each]
            value_final[index_num] = True
        return self.__model.ConstraintDef.SetWeld(name, value_final, tolerance, csys)


class JointConstraintsGet:
    """Constraint retrieval class."""

    def __init__(self, sap_obj):
        """
        Initialize the constraint retrieval class.

        Passing in the parent class object directly is to avoid
        getting only the last opened SAP2000 window when initializing the
        parent class instance to get the model pointer in the subclass.

        Args:
            sap_obj: SAP2000 object.
        """
        self.__object = sap_obj._Object
        self.__model = sap_obj._Model

    def Body(self, name: str) -> tuple[list[bool], str, int]:
        """
        Retrieve the definition of a Body constraint.

        Args:
            name: The name of an existing constraint.

        Returns:
            A tuple containing:
            - value: A list of six booleans that indicate which joint degrees of freedom are included in the constraint.
                     In order, the degrees of freedom addressed in the list are UX, UY, UZ, RX, RY and RZ.
            - csys: The name of the coordinate system in which the constraint is defined.
            - ret: 0 if the constraint data is successfully retrieved, otherwise it returns a nonzero value.
        """
        return self.__model.ConstraintDef.GetBody(name)
    
    def Beam(self, name: str) -> tuple[int, str, int]:
        """
        Retrieve the definition of a Beam constraint.

        Args:
            name: The name of an existing constraint.

        Returns:
            A tuple containing:
            - axis: An integer from the eConstraintAxis enumeration specifying the axis of the constraint.
                    1 = X, 2 = Y, 3 = Z, 4 = AutoAxis
            - csys: The name of the coordinate system in which the constraint is defined.
            - ret: 0 if the constraint data is successfully retrieved, otherwise it returns a nonzero value.
        """
        return self.__model.ConstraintDef.GetBeam(name)
    
    def ConstraintType(self, name: str) -> tuple[int, int]:
        """
        Retrieve the constraint type for the specified constraint.

        Args:
            name: The name of an existing constraint.

        Returns:
            A tuple containing:
            - constraint_type: An integer from the eConstraintType enumeration specifying the constraint type.
              Possible values include:
              1 = CONSTRAINT_BODY
              2 = CONSTRAINT_DIAPHRAGM
              3 = CONSTRAINT_PLATE
              4 = CONSTRAINT_ROD
              5 = CONSTRAINT_BEAM
              6 = CONSTRAINT_EQUAL
              7 = CONSTRAINT_LOCAL
              8 = CONSTRAINT_WELD
              13 = CONSTRAINT_LINE
            - ret: 0 if the constraint type is successfully obtained, otherwise it returns a nonzero value.
        """
        return self.__model.ConstraintDef.GetConstraintType(name)
    
    def Diaphragm(self, name: str) -> tuple[int, str, int]:
        """
        Retrieve the definition of a Diaphragm constraint.

        Args:
            name: The name of an existing constraint.

        Returns:
            A tuple containing:
            - axis: An integer from the eConstraintAxis enumeration specifying the axis of the constraint.
                    1 = X, 2 = Y, 3 = Z, 4 = AutoAxis
            - csys: The name of the coordinate system in which the constraint is defined.
            - ret: 0 if the constraint data is successfully retrieved, otherwise it returns a nonzero value.

        Remarks:
            This function returns the definition for the specified Diaphragm constraint.
        """
        return self.__model.ConstraintDef.GetDiaphragm(name)
    
    def Equal(self, name: str) -> tuple[list[bool], str, int]:
        """
        Retrieve the definition of an Equal constraint.

        Args:
            name: The name of an existing constraint.

        Returns:
            A tuple containing:
            - value: A list of six booleans indicating which joint degrees of freedom are included in the constraint.
                     In order, the degrees of freedom are UX, UY, UZ, RX, RY, and RZ.
            - csys: The name of the coordinate system in which the constraint is defined.
            - ret: 0 if the constraint data is successfully obtained, otherwise it returns a nonzero value.

        Remarks:
            This function returns the definition for the specified Equal constraint.
        """
        return self.__model.ConstraintDef.GetEqual(name)
    
    def Line(self, name: str) -> tuple[list[bool], str, int]:
        """
        Retrieve the definition of a Line constraint.

        Args:
            name: The name of an existing constraint.

        Returns:
            A tuple containing:
            - value: A list of six booleans indicating which joint degrees of freedom are included in the constraint.
                     In order, the degrees of freedom are UX, UY, UZ, RX, RY, and RZ.
            - csys: The name of the coordinate system in which the constraint is defined.
            - ret: 0 if the constraint data is successfully obtained, otherwise it returns a nonzero value.

        Remarks:
            This function returns the definition for the specified Line constraint.
        """
        return self.__model.ConstraintDef.GetLine(name)
    
    def Local(self, name: str) -> tuple[list[bool], int]:
        """
        Retrieve the definition of a Local constraint.

        Args:
            name: The name of an existing constraint.

        Returns:
            A tuple containing:
            - value: A list of six booleans indicating which joint degrees of freedom are included in the constraint.
                     In order, the degrees of freedom are U1, U2, U3, R1, R2, and R3.
            - ret: 0 if the constraint data is successfully obtained, otherwise it returns a nonzero value.

        Remarks:
            This function returns the definition for the specified Local constraint.
        """
        return self.__model.ConstraintDef.GetLocal(name)
    
    def NameList(self) -> tuple[int, list[str]]:
        """
        Retrieve the names of all defined joint constraints.

        Returns:
            A tuple containing:
            - NumberNames: The number of joint constraint names retrieved.
            - MyName: A list of strings containing the names of all defined joint constraints.

        Remarks:
            This function retrieves the names of all defined joint constraints.
            It returns 0 if the names are successfully retrieved, otherwise it returns a nonzero value.
        """
        return self.__model.ConstraintDef.GetNameList()
    
    def Plate(self, name: str) -> tuple[int, str, int]:
        """
        Retrieve the definition of a Plate constraint.

        Args:
            name: The name of an existing constraint.

        Returns:
            A tuple containing:
            - axis: An integer representing the axis perpendicular to the plane of the constraint.
                    1 = X, 2 = Y, 3 = Z, 4 = AutoAxis
            - csys: The name of the coordinate system in which the constraint is defined.
            - ret: 0 if the constraint data is successfully obtained, otherwise it returns a nonzero value.

        Remarks:
            This function returns the definition for the specified Plate constraint.
        """
        return self.__model.ConstraintDef.GetPlate(name)

    def Rod(self, name: str) -> tuple[int, str, int]:
        """
        Retrieve the definition of a Rod constraint.

        Args:
            name: The name of an existing constraint.

        Returns:
            A tuple containing:
            - axis: An integer representing the axis parallel to the axis of the constraint.
                    1 = X, 2 = Y, 3 = Z, 4 = AutoAxis
            - csys: The name of the coordinate system in which the constraint is defined.
            - ret: 0 if the constraint data is successfully obtained, otherwise it returns a nonzero value.

        Remarks:
            This function returns the definition for the specified Rod constraint.
        """
        return self.__model.ConstraintDef.GetRod(name)
    
    def SpecialRigidDiaphragmList(self) -> tuple[int, list[str]]:
        """
        Retrieve the list of special rigid diaphragm constraint names.

        Returns:
            A tuple containing:
            - Num: The number of special rigid diaphragm constraints.
            - Diaph: A list of strings containing the names of each special rigid diaphragm constraint.

        Remarks:
            This function retrieves the list of names for each special rigid diaphragm constraint.
            A special rigid diaphragm constraint is required for:
            1. Assignment of auto seismic load diaphragm eccentricity overwrites.
            2. Calculation of auto wind loads whose exposure widths are determined from the extents of rigid diaphragms.

            A special rigid diaphragm constraint has the following characteristics:
            1. The constraint type is CONSTRAINT_DIAPHRAGM = 2.
            2. The constraint coordinate system is Global.
            3. The constraint axis is Z.

            The function returns 0 if the name list is successfully retrieved, otherwise it returns a nonzero value.
        """
        return self.__model.ConstraintDef.GetSpecialRigidDiaphragmList()

    def Weld(self, name: str) -> tuple[list[bool], float, str, int]:
        """
        Retrieve the definition of a Weld constraint.

        Args:
            name: The name of an existing constraint.

        Returns:
            A tuple containing:
            - value: A list of six booleans indicating which joint degrees of freedom are included in the constraint.
                     The order is UX, UY, UZ, RX, RY, RZ.
            - tolerance: The distance within which joints are constrained together.
            - csys: The name of the coordinate system in which the constraint is defined.
            - ret: 0 if the constraint data is successfully obtained, otherwise it returns a nonzero value.

        Remarks:
            This function returns the definition for the specified Weld constraint.
        """
        return self.__model.ConstraintDef.GetWeld(name)
