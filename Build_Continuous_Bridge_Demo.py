from Sap2000py.Saproject import Saproject
from dataclasses import dataclass
from loguru import logger
from pathlib import Path
from collections import namedtuple
from extract_polygon_from_dxf import DXF2Polygons
from functools import lru_cache

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

# define a general frame section
H50sec = DXF2Polygons(file_path=r'Test\TongZhouSha_H_above_50.dxf', unit_of_dxf='cm', show_log=False)
H45sec = DXF2Polygons(file_path=r'Test\TongZhouSha_H_40_to_50.dxf', unit_of_dxf='cm', show_log=False)
H40sec = DXF2Polygons(file_path=r'Test\TongZhouSha_H_below_40.dxf', unit_of_dxf='cm', show_log=False)
solid_section = Section_General(
    name = "#468_pier_solid",
    material = "C40",
    Area = H50sec.outer_geometric_properties['area'],
    Depth = H50sec.outer_geometric_properties['height'],Width = H50sec.outer_geometric_properties['width'],
    As2=H50sec.outer_geometric_properties['Asy'],As3=H50sec.outer_geometric_properties['Asx'],
    I22=H50sec.outer_geometric_properties['Iyy'],I33=H50sec.outer_geometric_properties['Ixx'],J=H50sec.outer_geometric_properties['J'],
    notes = "#468_pier_top_solid_section")
ret = solid_section.define()
print(ret)
box_section = Section_General(
    name = "#468_pier_box",
    material = "C40",
    Area = H50sec.combine_geometric_properties['area'],
    Depth = H50sec.combine_geometric_properties['height'],Width = H50sec.combine_geometric_properties['width'],
    As2=H50sec.combine_geometric_properties['Asy'],As3=H50sec.combine_geometric_properties['Asx'],
    I22=H50sec.combine_geometric_properties['Iyy'],I33=H50sec.combine_geometric_properties['Ixx'],J=H50sec.combine_geometric_properties['J'],
    notes = "#468_pier_top_solid_section")
ret = box_section.define()
print(ret)

@dataclass
class SapPoint:
    x: float
    y: float
    z: float
    name: str = ""
    mass: float = 0.0
    
    def add(self):
        ret = Sap.Assign.PointObj.AddCartesian(self.x, self.y, self.z, UserName=self.name)
        if ret == 0:
            logger.success(f"Point {self.name} : ({self.x}, {self.y}, {self.z}) added successfully.")
        return ret
    
    def defineMass(self):
        ret = Sap.Assign.PointObj.Set.Mass(self.name, [self.mass for i in range(6)])
        if ret == 0:
            logger.success(f"Mass {self.mass} added to Point {self.name}")
        return ret

@dataclass
class SapBase_6Spring():
    def __init__(self, point: SapPoint, pier_name, spring_data_name=None, **kwargs):
        self.point = point
        self.pier_name = pier_name
        self.name = self.pier_name + "_Base"
        self.point.name = self.name
        if not spring_data_name:
            self.spring_data_name = self.pier_name.split("_")[0].split("#")[-1]
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
    station: float  # station of the pier, like K100+000 -> 100000
    horizontal_pos: float
    Height_of_pier_bottom: float
    Height_of_pier: float
    Height_of_cap: float
    Mass_of_cap_in_ton: float
    bottom_solid_length: float
    top_solid_length: float
    Distance_between_bearings: float
    num_of_hollow_elements: int =1
    is_intermediate_pier: bool =False # whether the pier is an intermediate pier, if true, the pier will have 4 bearings otherwise 2
    offset: float =1.0 # the distance between the centerline of the support (bearing) and the centerline of the pier.
    
    def __post_init__(self):
        self.generate_points()
        self.generate_pier_elements()
        # self.add_body_constraint()
        self.add_mass()
        
        self.base.get_spring_data()
        self.base.add_spring()
    
    def add_mass(self):
        self.cap_point.defineMass()
    
    def generate_points(self):
        x,y = self.station,self.horizontal_pos
        points = []
        # base point
        self.base_point = SapPoint(x, y, self.Height_of_pier_bottom-self.Height_of_cap, f"{self.name}_Base")
        self.base = SapBase_6Spring(self.base_point, self.name)
        points.append(self.base_point)
        
        # cap points
        self.cap_point = SapPoint(x, y, self.Height_of_pier_bottom-self.Height_of_cap/2, f"{self.name}_Cap",mass=self.Mass_of_cap_in_ton)
        points.append(self.cap_point)
        
        # pier points
        self.pier_bottom_point = SapPoint(x, y, self.Height_of_pier_bottom, f"{self.name}_Bottom")
        points.append(self.pier_bottom_point)
        self.pier_hollow_bottom = SapPoint(x, y, self.Height_of_pier_bottom + self.bottom_solid_length, f"{self.name}_HollowBottom")
        points.append(self.pier_hollow_bottom)
        hollow_points = []
        for i,h in enumerate(self.__hollow_points_to_define()):
            middle_point = SapPoint(x, y, h, f"{self.name}_HollowMiddle_{i}")
            points.append(middle_point)
            hollow_points.append(middle_point)
        self.hollow_points=hollow_points
        self.pier_hollow_top = SapPoint(x, y, self.Height_of_pier_bottom + self.Height_of_pier - self.top_solid_length, f"{self.name}_HollowTop")
        points.append(self.pier_hollow_top)
        self.pier_top = SapPoint(x, y, self.Height_of_pier_bottom + self.Height_of_pier, f"{self.name}_Top")
        
        # bearing bottom points
        if y>0:
            y_outer = y + self.Distance_between_bearings/2
            y_inner = y - self.Distance_between_bearings/2
        else:
            y_outer = y - self.Distance_between_bearings/2
            y_inner = y + self.Distance_between_bearings/2
            
        if self.is_intermediate_pier:
            self.bearing_bottom_point_outer = [SapPoint(x-self.offset, y_outer, self.Height_of_pier_bottom, f"{self.name}_BearingBottom_outter_1"),
                                               SapPoint(x+self.offset, y_outer, self.Height_of_pier_bottom, f"{self.name}_BearingBottom_outter_2")]
            self.bearing_bottom_point_inner = [SapPoint(x-self.offset, y_inner, self.Height_of_pier_bottom, f"{self.name}_BearingBottom_inner_1"),
                                               SapPoint(x+self.offset, y_inner, self.Height_of_pier_bottom, f"{self.name}_BearingBottom_inner_2")]
            points.extend(self.bearing_bottom_point_outer)
            points.extend(self.bearing_bottom_point_inner)
        else: 
            self.bearing_bottom_point_outer = SapPoint(x, y_outer, self.Height_of_pier_bottom, f"{self.name}_BearingBottom_outter")
            self.bearing_bottom_point_inner = SapPoint(x, y_inner, self.Height_of_pier_bottom, f"{self.name}_BearingBottom_inner")
            points.append(self.bearing_bottom_point_outer)
            points.append(self.bearing_bottom_point_inner)
        
        self.points = points
        # Add points to SAP2000 model
        for point in self.points:
            point.add()

    def __hollow_points_to_define(self):
        coord_list = [self.Height_of_pier_bottom + self.bottom_solid_length, self.Height_of_pier_bottom + self.Height_of_pier - self.top_solid_length]
        if self.num_of_hollow_elements == 1:
            return []
        elif self.num_of_hollow_elements > 1:
            pass
        else:
            logger.error("Number of hollow elements is not valid.")
            return None

        result = []
        # interpolate the height of hollow points
        for i in range(1, self.num_of_hollow_elements):
            result.append(coord_list[0] + (coord_list[1] - coord_list[0]) * i / self.num_of_hollow_elements)
        return result

    # @lru_cache(maxsize=3)
    def get_solid_section(self):
        if self.Height_of_pier >= 50:
            sec = DXF2Polygons(file_path=r'Test\TongZhouSha_H_above_50.dxf', unit_of_dxf='cm', show_log=False)
        elif self.Height_of_pier >= 40:
            sec = DXF2Polygons(file_path=r'Test\TongZhouSha_H_40_to_50.dxf', unit_of_dxf='cm', show_log=False)
        elif self.Height_of_pier < 40 and self.Height_of_pier >= 0:
            sec = DXF2Polygons(file_path=r'Test\TongZhouSha_H_below_40.dxf', unit_of_dxf='cm', show_log=False)
        else:
            logger.error("Height of pier is not valid.")
            return None
        solid_section = Section_General(
            name = self.name+"_pier_solid",
            material = "C40",
            Area = sec.outer_geometric_properties['area'],
            Depth = sec.outer_geometric_properties['height'],Width = sec.outer_geometric_properties['width'],
            As2=sec.outer_geometric_properties['Asy'],As3=sec.outer_geometric_properties['Asx'],
            I22=sec.outer_geometric_properties['Iyy'],I33=sec.outer_geometric_properties['Ixx'],J=sec.outer_geometric_properties['J'],
            notes = self.name+"_pier_solid_section")
        return solid_section
    
    # @lru_cache(maxsize=3)
    def get_box_section(self):
        if self.Height_of_pier >= 50:
            sec = DXF2Polygons(file_path=r'Test\TongZhouSha_H_above_50.dxf', unit_of_dxf='cm', show_log=False)
        elif self.Height_of_pier >= 40:
            sec = DXF2Polygons(file_path=r'Test\TongZhouSha_H_40_to_50.dxf', unit_of_dxf='cm', show_log=False)
        elif self.Height_of_pier < 40 and self.Height_of_pier >= 0:
            sec = DXF2Polygons(file_path=r'Test\TongZhouSha_H_below_40.dxf', unit_of_dxf='cm', show_log=False)
        else:
            logger.error("Height of pier is not valid.")
            return None
        box_section = Section_General(
            name = self.name+"_pier_box",
            material = "C40",
            Area = sec.combine_geometric_properties['area'],
            Depth = sec.combine_geometric_properties['height'],Width = sec.combine_geometric_properties['width'],
            As2=sec.combine_geometric_properties['Asy'],As3=sec.combine_geometric_properties['Asx'],
            I22=sec.combine_geometric_properties['Iyy'],I33=sec.combine_geometric_properties['Ixx'],J=sec.combine_geometric_properties['J'],
            notes = self.name+"_pier_box_section")
        return box_section
    
    def get_cap_section(self):
        width = 12 if self.Height_of_pier >= 50 else 10.794
        depth = 18.625
        ret = Sap._Model.PropFrame.SetRectangle(self.name+"_Cap", "C30", width, depth)
        if ret == 0:
            logger.success(f"Cap section {self.name}_Cap added!")
        return self.name+"_Cap"
    
    def add_body_constraint(self):
        Sap.Define.jointConstraints.SetBody(self.pier_top.name, True, True, True, True, True, True)
        Sap.Define.jointConstraints.SetDiaphragm(self.pier_top.name, True, True, True)
        ret = Sap.Assign.PointObj.SetRestraint(self.base_point.name, [True, True, True, True, True, True])
        if ret[1] == 0:
            logger.success(f"Body constraint added to {self.base_point.name}")
        return ret
    
    def generate_pier_elements(self):
        solid_section = self.get_solid_section()
        box_section = self.get_box_section()
        solid_section.define()
        box_section.define()
        cap_section_name = self.get_cap_section()
        
        # define solid cap
        Sap.Assign.FrameObj.AddByPoint(self.base_point.name, self.cap_point.name, propName=cap_section_name, userName = self.name+"base2cap")
        Sap.Assign.FrameObj.AddByPoint(self.cap_point.name, self.pier_bottom_point.name, propName=cap_section_name, userName = self.name+"cap2bottom")
        
        # define pierpython
        Sap.Assign.FrameObj.AddByPoint(self.pier_bottom_point.name, self.pier_hollow_bottom.name, propName=solid_section.name, userName = self.name+"bottom2hollowBottom")
        for i,h in enumerate(self.hollow_points):
            if i == 0:
                Sap.Assign.FrameObj.AddByPoint(self.pier_hollow_bottom.name, h.name, propName=box_section.name, userName = self.name+f"hollow_{i+1}")
            else:
                Sap.Assign.FrameObj.AddByPoint(self.hollow_points[i-1].name, h.name, propName=box_section.name, userName = self.name+f"hollow_{i+1}")
        if len(self.hollow_points) == 0:
            Sap.Assign.FrameObj.AddByPoint(self.pier_hollow_bottom.name, self.pier_hollow_top.name, propName=box_section.name, userName = self.name+"hollowBottom2Top")
        else:
            Sap.Assign.FrameObj.AddByPoint(self.hollow_points[-1].name, self.pier_hollow_top.name, propName=box_section.name, userName = self.name+f"hollow_{i+1}")
        Sap.Assign.FrameObj.AddByPoint(self.pier_hollow_top.name, self.pier_top.name, propName=solid_section.name, userName = self.name+"hollowTop2Top")

sap_pier = SapPier_Box(
    name="#468",
    station=0,
    horizontal_pos=8.125,
    Height_of_pier_bottom=-3.1,
    Height_of_pier=40.0,
    Height_of_cap=3.0,
    Mass_of_cap_in_ton=1676.25,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=2,
    is_intermediate_pier = True,
    offset = 1.0
)
    
a=1

# point1 = SapPoint(*[1,0,0], "#468")
# base468 = SapBase_6Spring(point1, "#468")
# use auto_build to add point and spring or just do it step by step
# base468.add_point()
# base468.get_spring_data()
# base468.add_spring()
# base468.auto_build()

# ret = Sap.Assign.PointObj.Get.CoordCartesian(name)
# print(ret)
# ret = Sap._Model.PointObj.GetCoordCartesian(name)
# print(ret)
        
# Sap.File.Save(ModelPath)
# Sap.closeSap()