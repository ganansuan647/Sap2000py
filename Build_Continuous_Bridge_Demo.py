from Sap2000py.Saproject import Saproject
from dataclasses import dataclass
from loguru import logger
from pathlib import Path
from collections import namedtuple

#full path to the model
ModelPath = Path('.\Test\Test.sdb')

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

@dataclass
class Section_General:
    name: str
    material: str
    Area: float
    Depth: float
    Width: float
    As2: float
    As3: float
    I22: float
    I33: float
    J: float
    notes: str = ""
    
    @property
    def t3(self):
        return self.Depth
    
    @property
    def t2(self):
        return self.Width

    def define(self):
        ret = Sap.Define.section.PropFrame_SetGeneral(self.name, self.material, self.t3, self.t2, self.Area, self.As2, self.As3, self.I22, self.I33, self.J, notes=self.notes)
        if ret == 0:
            logger.opt(colors=True).success(f"Section <yellow>{self.name}</yellow> added!")
        return ret
    
    def get_elements_with_this_section(self):
        raise NotImplementedError

# boxsection = Section_General(
#     name = "#468_pier_top_solid",
#     material = "C40",
#     Area = 100,
#     Depth = 24,Width = 14,
#     As2=100,As3=100,
#     I22=80,I33=80,J=100,
#     notes = "#468_pier_top_solid_section")
# ret = boxsection.define()
# print(ret)

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
class SapBase_6Spring:
    def __init__(self, point: SapPoint, pier_name, spring_data_name=None, **kwargs):
        self.point = point
        self.pier_name = pier_name
        self.name = self.pier_name + "_Base"
        self.point.name = self.name
        if not spring_data_name:
            self.spring_data_name = self.pier_name.split("#")[-1]
        else:
            self.spring_data_name = spring_data_name
    
    def auto_build(self):
        self.add_point()
        self.get_spring_data()
        self.add_spring()
    
    def add_point(self):
        ret = self.point.add()
        return ret
    
    def get_spring_data(self,datapath = "spring.txt"):
        with open(datapath, "r") as f:
            lines = f.readlines()
            springs = [line.strip().split('\t') for line in lines]
            spring = [s for s in springs if s[0] == self.spring_data_name][0]
        klist = []
        for k in spring:
            if k != self.spring_data_name and k != 'GLOBAL':
                if k == '':
                    klist.append(0.0)
                else:
                    klist.append(float(k))
        if len(klist) != 21:
            print(f"spring data of {self.spring_data_name} is not right.")
        self.spring_data = klist
        return klist
    
    def add_spring(self, unit = "KN_m_C"):
        """
        Args:
            unit (str, optional): unit of coupled spring. Defaults to "KN_m_C".

        Returns:
            ret: return value of Sap2000 API, 0 for success, others for failure.
        """
        if not hasattr(self, "spring_data"):
            self.get_spring_data()
        if unit != Sap.Units:
            Sap.setUnits(unit)
        ret = Sap.Assign.PointObj.Set.SpringCoupled(self.name, self.spring_data, Replace=True)
        if ret[1] == 0:
            logger.opt(colors=True).success(f"Spring for Joint: <yellow>{self.name}</yellow> Added! K = <cyan>{self.spring_data}</cyan>")
        else:
            logger.opt(colors=True).success(f"Spring for Joint: <yellow>{self.name}</yellow> Failed to Add! K = {self.spring_data}")
        return ret

    def connect_with_pier(self):
        raise NotImplementedError

@dataclass
class SapPier_Box:
    name: str
    Height_of_pier_bottom: float
    Height_of_pier: float
    bottom_solid_length: float
    bottom_solid_section: tuple
    top_solid_length: float
    top_solid_section: tuple
    hollow_excavation: tuple
    num_of_hollow: int
    
    def __post_init__(self):
        self.generate_points()
        self.generate_elements()
    
    def generate_points(self):
        try:
            self.pier_hollow_bottom = SapPoint(self.pier_bottom.x, self.pier_bottom.y, self.Height_of_pier_bottom + self.bottom_solid_length, f"{self.name}_HollowBottom")
            self.pier_hollow_top = SapPoint(self.pier_bottom.x, self.pier_bottom.y, self.Height_of_pier_bottom + self.Height_of_pier - self.top_solid_length, f"{self.name}_HollowTop")
            self.pier_top = SapPoint(self.pier_bottom.x, self.pier_bottom.y, self.Height_of_pier_bottom + self.Height_of_pier, f"{self.name}_Top")
            self.pier_hollow_points = [SapPoint(self.pier_bottom.x, self.pier_bottom.y, self.Height_of_pier_bottom + self.bottom_solid_length + i*(self.Height_of_pier - self.bottom_solid_length - self.top_solid_length)/self.num_of_hollow, f"{self.name}_Hollow_{i+1}") for i in range(self.num_of_hollow)]
            
            # Add points to SAP2000 model
            self.pier_bottom.add()
            self.pier_hollow_bottom.add()
            self.pier_hollow_top.add()
            self.pier_top.add()
            for point in self.pier_hollow_points:
                point.add()
        except Exception as e:
            logger.error(f"Error in generating points for {self.name}: {e}")

    def generate_elements(self):
        try:
            # Generate bottom solid section element
            Sap.Assign.FrameObj.AddByCoord(self.pier_bottom.x, self.pier_bottom.y, self.pier_bottom.z, self.pier_hollow_bottom.x, self.pier_hollow_bottom.y, self.pier_hollow_bottom.z, f"{self.name}_BottomSolid")
            Sap.PropFrame.SetRectangle(f"{self.name}_BottomSolid", "Concrete", self.bottom_solid_section[0], self.bottom_solid_section[1])

            # Generate top solid section element
            Sap.Assign.FrameObj.AddByCoord(self.pier_hollow_top.x, self.pier_hollow_top.y, self.pier_hollow_top.z, self.pier_top.x, self.pier_top.y, self.pier_top.z, f"{self.name}_TopSolid")
            Sap.PropFrame.SetRectangle(f"{self.name}_TopSolid", "Concrete", self.top_solid_section[0], self.top_solid_section[1])

            # Generate hollow section elements
            for i in range(len(self.pier_hollow_points) - 1):
                Sap.Assign.FrameObj.AddByCoord(self.pier_hollow_points[i].x, self.pier_hollow_points[i].y, self.pier_hollow_points[i].z, self.pier_hollow_points[i + 1].x, self.pier_hollow_points[i + 1].y, self.pier_hollow_points[i + 1].z, f"{self.name}_Hollow_{i+1}")
                Sap.PropFrame.SetCircle(f"{self.name}_Hollow_{i+1}", "Concrete", self.hollow_excavation[0], self.hollow_excavation[1])

        except Exception as e:
            logger.error(f"Error in generating elements for {self.name}: {e}")


sap_pier = SapPier_Box(
    name="#468",
    Height_of_pier_bottom=-3.1,
    Height_of_pier=40.0,
    bottom_solid_length=2.0,
    bottom_solid_section_shape=(9.0,4.0),
    top_solid_length=3.0,
    top_solid_section_shape=(10.6, 4.0),
    hollow_excavation=(1.5, 1.5),
    num_of_hollow=2,
    bottom_solid_section_prop=(9.0, 4.0),
    top_solid_section_prop=(10.6, 4.0),
)
    
    

point1 = SapPoint(*[1,0,0], "#468")
base468 = SapBase_6Spring(point1, "#468")
# use auto_build to add point and spring or just do it step by step
# base468.add_point()
# base468.get_spring_data()
# base468.add_spring()
base468.auto_build()

# ret = Sap.Assign.PointObj.Get.CoordCartesian(name)
# print(ret)
# ret = Sap._Model.PointObj.GetCoordCartesian(name)
# print(ret)
        
# Sap.File.Save(ModelPath)
# Sap.closeSap()