from Sap2000py.Saproject import Saproject
from dataclasses import dataclass
from loguru import logger

#full path to the model
ModelPath = 'F:\python\Sap2000\Models\Test.sdb'

# Create a Sap2000py obj (default: attatch to instance and create if not exist)
Sap = Saproject()

# Change Sap api settings if you want
# Sap.createSap(AttachToInstance = True,SpecifyPath = False,ProgramPath = "your sap2000 path")

# Open Sap2000program
Sap.openSap()

# Open Sap2000 sdb file (create if not exist, default: CurrentPath\\NewSapProj.sdb)
Sap.File.Open(ModelPath)
# And print the project information
Sap.getProjectInfo()

# Set Units to KN_m_C
Sap.setUnits("KN_m_C")

# Add China Common Material Set·
Sap.Scripts.AddCommonMaterialSet(standard = "JTG")

coords = [4,2,3]
name = "#273_Pier_1"
Sap.Assign.PointObj.AddCartesian(*coords, UserName=name)

ret = Sap.Assign.PointObj.Get.CoordCartesian(name)
print(ret)
ret = Sap._Model.PointObj.GetCoordCartesian(name)
print(ret)

    
@dataclass
class SapPoint:
    x: float
    y: float
    z: float
    name: str = ""
    
    def add(self):
        ret = Sap.Assign.PointObj.AddCartesian(self.x, self.y, self.z, UserName=self.name)
        if ret == 0:
            logger.success(f"Point {self.name} : ({self.x}, {self.y}, {self.z}) added successfully.")
        return ret

@dataclass
class BaseJoint:
    def __init__(self, point: SapPoint, pier_name, spring_data_name):
        self.point = SapPoint
        self.pier_name = pier_name
        self.name = self.pier_name + "_Base"
        self.point.name = self.name
        if not hasattr("spring_data_name"):
            spring_data_name = int(self.pier_name.split("#")[-1])
    
    def add(self):
        self.point.add()
        return ret
    
    def add_spring(self):
        ret = Sap.Assign.PointObj.Set.SpringCoupled(self.name, self.spring_data_name)
        if ret == 0:
            logger.success(f"Spring {self.spring_data_name} added to {self.name} successfully.")
        return ret

        
# Sap.File.Save(ModelPath)
# Sap.closeSap()