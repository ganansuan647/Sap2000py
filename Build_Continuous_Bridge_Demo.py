from Sap2000py.Saproject import Saproject
from dataclasses import dataclass
from loguru import logger
from pathlib import Path
from collections import namedtuple
from extract_polygon_from_dxf import DXF2Polygons
from functools import lru_cache
from typing import Literal
from itertools import chain

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

@dataclass
class SapPoint:
    x: float
    y: float
    z: float
    name: str = ""
    mass: float = 0.0
    
    def add(self):
        ret = Sap.Assign.PointObj.AddCartesian(self.x, self.y, self.z, UserName=self.name)
        if ret[1] == 0:
            logger.opt(colors=True).success(f"Point <yellow>{self.name}</yellow> : <cyan>({self.x}, {self.y}, {self.z})</cyan> added.")
        else:
            logger.opt(colors=True).error(f"Point <yellow>{self.name}</yellow> : <cyan>({self.x}, {self.y}, {self.z})</cyan> failed to add.")
        return ret
    
    def defineMass(self):
        ret = Sap.Assign.PointObj.Set.Mass(self.name, [self.mass for i in range(6)])
        if ret == 0:
            logger.success(f"Mass {self.mass} added to Point {self.name}")
        else:
            logger.error(f"Mass {self.mass} failed to add to Point {self.name}")
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
            logger.opt(colors=True).error(f"Spring for Joint: <yellow>{self.name}</yellow> Failed to Add! K = {self.spring_data}")
        return ret

    def connect_with_pier(self):
        raise NotImplementedError

@dataclass
class Sap_Double_Box_Pier:
    name: str
    station: float  # station of the pier, like K100+000 -> 100000
    Height_of_pier_bottom: float
    Height_of_pier: float
    bottom_solid_length: float
    top_solid_length: float
    Distance_between_bearings: float
    Height_of_cap: float = 3.0 if Height_of_pier >= 50 else 2.8 if 40<=Height_of_pier<50 else 2.7
    Distance_between_piers: float = 20.75
    num_of_hollow_elements: int =1
    is_intermediate_pier: bool =False # whether the pier is an intermediate pier, if true, the pier will have 4 bearings otherwise 2
    offset: float =1.0 # the distance between the centerline of the support (bearing) and the centerline of the pier.
    
    def __post_init__(self):
        self.addsome_empty_attr()
        
        self.generate_pier_points(side = 'both')
        self.generate_pier_elements(side = 'both')
        
        self.generate_base_points()
        self.generate_cap_elements()
        self.base.get_spring_data()
        self.base.add_spring()
        
        self.add_body_constraint()
        # self.add_mass()
        
    def add_mass(self):
        # if cap section is defined properly, mass of cap should not be added to cap point
        # self.cap_point.defineMass()
        pass
    
    def generate_base_points(self):
        x = self.station
        y = 0
        # base point
        self.base_point = SapPoint(x, y, self.Height_of_pier_bottom-self.Height_of_cap, f"{self.name}_Base")
        self.base = SapBase_6Spring(self.base_point, self.name)
        
        # cap points
        if not hasattr(self, "Mass_of_cap_in_ton"):
            self.get_cap_section()
        self.cap_point = SapPoint(x, y, self.Height_of_pier_bottom-self.Height_of_cap/2, f"{self.name}_Cap",mass=self.Mass_of_cap_in_ton)
        
        # cap top points
        self.cap_top_point = SapPoint(x, y, self.Height_of_pier_bottom, f"{self.name}_CapTop")
        
        self.base_points = [self.base_point, self.cap_point, self.cap_top_point]
        for point in self.base_points:
            point.add()
    
    def addsome_empty_attr(self):
        self.pier_bottom_point:dict = {}
        self.pier_hollow_bottom:dict = {}
        self.hollow_points:dict = {}
        self.pier_hollow_top:dict = {}
        self.pier_top:dict = {}
        self.bearing_bottom_point_outer:dict = {}
        self.bearing_bottom_point_inner:dict = {}
        self.points:dict = {}
    
    def generate_pier_points(self,side = Literal['left','right','both']):
        x = self.station
        if side == 'left':
            y = - self.Distance_between_piers/2
        elif side == 'right':
            y = self.Distance_between_piers/2
        elif side == 'both':
            self.generate_pier_points('left')
            self.generate_pier_points('right')
            return

        points = []
        # pier points
        self.pier_bottom_point[side] = SapPoint(x, y, self.Height_of_pier_bottom, f"{self.name+'_'+side}_Bottom")
        points.append(self.pier_bottom_point[side])
        
        self.pier_hollow_bottom[side] = SapPoint(x, y, self.Height_of_pier_bottom + self.bottom_solid_length, f"{self.name+'_'+side}_HollowBottom")
        points.append(self.pier_hollow_bottom[side])
        
        hollow_points = []
        for i,h in enumerate(self.__hollow_points_to_define()):
            middle_point = SapPoint(x, y, h, f"{self.name+'_'+side}_HollowMiddle_{i}")
            points.append(middle_point)
            hollow_points.append(middle_point)
        self.hollow_points[side] = hollow_points
        
        h_piertop = self.Height_of_pier_bottom + self.Height_of_pier
        
        self.pier_hollow_top[side] = SapPoint(x, y, h_piertop - self.top_solid_length, f"{self.name+'_'+side}_HollowTop")
        points.append(self.pier_hollow_top[side])
        
        self.pier_top[side] = SapPoint(x, y, h_piertop, f"{self.name+'_'+side}_Top")
        points.append(self.pier_top[side])

        # bearing bottom points
        if y>0:
            y_outer = y + self.Distance_between_bearings/2
            y_inner = y - self.Distance_between_bearings/2
        else:
            y_outer = y - self.Distance_between_bearings/2
            y_inner = y + self.Distance_between_bearings/2
        if self.is_intermediate_pier:
            self.bearing_bottom_point_outer[side] = [SapPoint(x-self.offset, y_outer, h_piertop, f"{self.name+'_'+side}_BearingBottom_outter_1"),
                                               SapPoint(x+self.offset, y_outer, h_piertop, f"{self.name+'_'+side}_BearingBottom_outter_2")]
            self.bearing_bottom_point_inner[side] = [SapPoint(x-self.offset, y_inner, h_piertop, f"{self.name+'_'+side}_BearingBottom_inner_1"),
                                               SapPoint(x+self.offset, y_inner, h_piertop, f"{self.name+'_'+side}_BearingBottom_inner_2")]
            points.extend(self.bearing_bottom_point_outer[side])
            points.extend(self.bearing_bottom_point_inner[side])
        else: 
            self.bearing_bottom_point_outer[side] = SapPoint(x, y_outer, h_piertop, f"{self.name+'_'+side}_BearingBottom_outter")
            self.bearing_bottom_point_inner[side] = SapPoint(x, y_inner, h_piertop, f"{self.name+'_'+side}_BearingBottom_inner")
            points.append(self.bearing_bottom_point_outer[side])
            points.append(self.bearing_bottom_point_inner[side])
        
        self.points[side] = points
        # Add points to SAP2000 model (only add once)
        for point in points:
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
        depth = 37.25
        self.Mass_of_cap_in_ton = width * depth * self.Height_of_cap * 2.5
        ret = Sap._Model.PropFrame.SetRectangle(self.name+"_Cap", "C30", width, depth)
        if ret == 0:
            logger.success(f"Cap section {self.name}_Cap added!")
        return self.name+"_Cap"
    
    def __add_body_constraints_for_points(self,constraint_name:str, points : list):
        for point in points:
            ret = Sap.Assign.PointObj.Set.Constraint(point.name,constraint_name,ItemType = 0)
            if ret[1] == 0:
                logger.opt(colors=True).success(f"<yellow>{point.name}</yellow> added to Body constraint : <yellow>{constraint_name}</yellow>")
            else:
                logger.opt(colors=True).error(f"<yellow>{point.name}</yellow> failed to add to Body constraint : <yellow>{constraint_name}</yellow>")
    
    def add_body_constraint(self):
        body_dof = ["UX", "UY", "UZ", "RX", "RY", "RZ"]
        flatten = lambda l: list(chain.from_iterable(map(lambda x: flatten(x) if isinstance(x, list) else [x], l)))
        
        # add body constraint between capTop and pier
        
        Sap.Define.jointConstraints.SetBody(self.name+"_Cap_Pier", body_dof)
        self.__add_body_constraints_for_points(self.name+"_Cap_Pier", flatten([self.cap_top_point, self.pier_bottom_point['left'],self.pier_bottom_point['right']]))
        
        # add body constraint between pier top and bearing bottom
        left_points = flatten([self.pier_top['left'], self.bearing_bottom_point_outer['left'], self.bearing_bottom_point_inner['left']])
        right_points = flatten([self.pier_top['right'], self.bearing_bottom_point_outer['right'], self.bearing_bottom_point_inner['right']])
        # left
        Sap.Define.jointConstraints.SetBody(self.name+"_left_Pier_Bearing", body_dof)
        self.__add_body_constraints_for_points(self.name+"_left_Pier_Bearing", left_points)
        # right
        Sap.Define.jointConstraints.SetBody(self.name+"_right_Pier_Bearing", body_dof)
        self.__add_body_constraints_for_points(self.name+"_right_Pier_Bearing", right_points)
        
    def generate_cap_elements(self):
        cap_section_name = self.get_cap_section()
        
        # define solid cap
        Sap.Assign.FrameObj.AddByPoint(self.base_point.name, self.cap_point.name, propName=cap_section_name, userName = self.name+"base2cap")
        Sap.Assign.FrameObj.AddByPoint(self.cap_point.name, self.cap_top_point.name, propName=cap_section_name, userName = self.name+"cap2bottom")
    
    def generate_pier_elements(self,side = Literal['left','right','both']):
        if side == 'both':
            self.generate_pier_elements('left')
            self.generate_pier_elements('right')
            return
                  
        solid_section = self.get_solid_section()
        box_section = self.get_box_section()
        solid_section.define()
        box_section.define()
        
        # define pier
        Sap.Assign.FrameObj.AddByPoint(self.pier_bottom_point[side].name, self.pier_hollow_bottom[side].name, propName=solid_section.name, userName = self.name+'_'+side+"bottom2hollowBottom")
        for i,h in enumerate(self.hollow_points[side]):
            if i == 0:
                Sap.Assign.FrameObj.AddByPoint(self.pier_hollow_bottom[side].name, h.name, propName=box_section.name, userName = self.name+'_'+side+f"hollow_{i+1}")
            else:
                Sap.Assign.FrameObj.AddByPoint(self.hollow_points[side][i-1].name, h.name, propName=box_section.name, userName = self.name+'_'+side+f"hollow_{i+1}")
        if len(self.hollow_points[side]) == 0:
            Sap.Assign.FrameObj.AddByPoint(self.pier_hollow_bottom[side].name, self.pier_hollow_top[side].name, propName=box_section.name, userName = self.name+'_'+side+"hollowBottom2Top")
        else:
            Sap.Assign.FrameObj.AddByPoint(self.hollow_points[side][-1].name, self.pier_hollow_top[side].name, propName=box_section.name, userName = self.name+'_'+side+f"hollow_{i+1}")
        Sap.Assign.FrameObj.AddByPoint(self.pier_hollow_top[side].name, self.pier_top[side].name, propName=solid_section.name, userName = self.name+'_'+side+"hollowTop2Top")

pier466 = Sap_Double_Box_Pier(
    name="#466",
    station=0,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=-3.1,
    Height_of_pier=40.0,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=2,
    is_intermediate_pier = True,
    offset = 1.0
)

pier467 = Sap_Double_Box_Pier(
    name="#467",
    station=90,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=-4.5,
    Height_of_pier=45.0,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=2,
    is_intermediate_pier = False,
)

pier468 = Sap_Double_Box_Pier(
    name="#468",
    station=180,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=-5.9,
    Height_of_pier=47.0,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=2,
    is_intermediate_pier = False,
)

pier469 = Sap_Double_Box_Pier(
    name="#469",
    station=270,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=-5.9,
    Height_of_pier=47.0,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=2,
    is_intermediate_pier = False,
)

pier470 = Sap_Double_Box_Pier(
    name="#470",
    station=360,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=-5.9,
    Height_of_pier=47.0,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=2,
    is_intermediate_pier = False,
)

pier471 = Sap_Double_Box_Pier(
    name="#471",
    station=450,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=-5.9,
    Height_of_pier=47.0,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=2,
    is_intermediate_pier = True,
    offset=1.0
)
    
@dataclass
class Sap_Box_Girder:
    pierlist: list[Sap_Double_Box_Pier]
    num_of_ele_foreach_girder: int = 6
    
    
    
        

    
    
Sap.RefreshView()
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