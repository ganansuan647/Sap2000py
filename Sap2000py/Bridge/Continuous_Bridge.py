import math
import weakref
from dataclasses import dataclass, field
from itertools import chain
from pathlib import Path
from typing import ClassVar, Dict, List, Literal, Union

import numpy as np
from loguru import logger
from sectionproperties.analysis import Section
from sectionproperties.pre import Geometry
from shapely import Polygon

from Sap2000py import Saproject


class ShouldNotInstantiateError(Exception):
    pass

@dataclass
class Section_General:
    name:str
    material:str
    Area:float
    Depth:float
    Width:float
    As2:float
    As3:float
    I22:float
    I33:float
    I23:float
    J:float=1e10
    geom:Geometry = None
    sec: Section = None
    unit_of_sec:Literal['mm','cm','m'] = 'm'
    notes:str=""
    
    @property
    def t3(self):
        return self.Depth
    
    @property
    def t2(self):
        return self.Width

    def define(self):
        if self.unit_of_sec == 'mm':
            Saproject().setUnits("KN_mm_C")
        elif self.unit_of_sec == 'cm':
            Saproject().setUnits("KN_cm_C")
        elif self.unit_of_sec == 'm':
            Saproject().setUnits("KN_m_C")
        ret = Saproject().Define.section.PropFrame_SetGeneral(self.name, self.material, self.t3, self.t2, self.Area, self.As2, self.As3, self.I22, self.I33, self.J, notes=self.notes)
        if ret == 0:
            logger.opt(colors=True).success(f"Section <yellow>{self.name}</yellow> added!")
        Saproject().setUnits("KN_m_C")
        return ret
    
    def ignore_mass_effect(self):
        # Set mass and weight modifiers to 0
        ret = Saproject()._Model.PropFrame.SetModifiers(self.name,[1,1,1,1,1,1,0,0])
        if ret[-1] == 0:
            logger.opt(colors=True).success(f"Mass effect ignored for Section <yellow>{self.name}</yellow>!")
        else:
            logger.opt(colors=True).error(f"Failed to ignore mass effect for Section <yellow>{self.name}</yellow>!")
    
    def plot_geometry(self):
        if self.geom:
            self.geom.plot_geometry()
        else:
            logger.error("No geometry to plot.")
            
    def plot_mesh(self):
        if self.sec:
            self.sec.plot_mesh(materials=False)
        else:
            logger.error("No mesh to plot.")
    
    def print_all_properties(self):
        if self.sec:
            self.sec.calculate_geometric_properties()
            self.sec.display_results(fmt=".0f")
        else:
            logger.error("No section to calculate properties.")
    
    def get_elements_with_this_section(self):
        raise NotImplementedError

@dataclass
class Section_NonPrismatic:
    """
    
    VaryingRules(list[float,Literal['Variable','Absolute'],str,str,Literal['Linear','Parabolic','Cubic']],Literal['Linear','Parabolic','Cubic']):
        [0]:list of the length type for each segment.1 = Variable (relative length),2 = Absolute
        [1]:the length of each segment
        [2]:start section property name
        [3]:end section property name
        [4]:the type of the varying rule for EI33.1 = Linear,2 = Parabolic,3 = Cubic
        [5]:the type of the varying rule for EI22.1 = Linear,2 = Parabolic,3 = Cubic

    CardinalPoint:Literal['Centroid','Shear Center','Bottom Left','Bottom Center','Bottom Right','Middle Left','Middle Center','Middle Right','Top Left','Top Center','Top Right'] = 'Top Center'

    
    """
    name:str
    VaryingRules:list[Literal['Variable','Absolute'],float,str,str,Literal['Linear','Parabolic','Cubic'],Literal['Linear','Parabolic','Cubic']]
    notes:str=""
    
    def define(self):
        NumberItems:int = len(self.VaryingRules)
        lengthTypeList:List = [segment[0] for segment in self.VaryingRules]
        lengthlist:List = [segment[1] for segment in self.VaryingRules]
        startSecList:List = [segment[2] for segment in self.VaryingRules]
        endSecList:List = [segment[3] for segment in self.VaryingRules]
        EI33Variation = [segment[4] for segment in self.VaryingRules]
        EI22Variation = [segment[5] for segment in self.VaryingRules]
        ret = Saproject().Define.section.PropFrame_SetNonPrismatic(self.name, NumberItems, startSecList, endSecList, lengthlist, lengthTypeList, EI33Variation, EI22Variation)
        if ret[-1] == 0:
            logger.opt(colors=True).success(f"Section <yellow>{self.name}</yellow> added!")
        return ret

   

@dataclass
class SapPoint:
    x:float
    y:float
    z:float
    name:str=""
    mass: List[float] = field(default_factory=lambda: [0.0 for _ in range(6)])
    restraints:list[Literal['Ux','Uy','Uz','Rx','Ry','Rz']] = field(default_factory=list)

    def add(self):
        ret = Saproject().Assign.PointObj.AddCartesian(self.x, self.y, self.z, UserName=self.name)
        if ret[1] == 0:
            logger.opt(colors=True).success(f"Point <yellow>{self.name}</yellow> : <cyan>({self.x}, {self.y}, {self.z})</cyan> added.")
        else:
            logger.opt(colors=True).error(f"Point <yellow>{self.name}</yellow> : <cyan>({self.x}, {self.y}, {self.z})</cyan> failed to add.")
        return ret
    
    def defineMass(self, mass: Union[float, List[float]] = None, dof: List[Literal['Ux','Uy','Uz','Rx','Ry','Rz']] = ['Ux', 'Uy', 'Uz']):
        # 如果 mass 是一个值，应用于指定的 dof
        if isinstance(mass, (int, float)):
            dof_index_map = {'Ux': 0, 'Uy': 1, 'Uz': 2, 'Rx': 3, 'Ry': 4, 'Rz': 5}
            # 更新对应的自由度
            for d in dof:
                self.mass[dof_index_map[d]] = mass
        
        # 如果 mass 是一个列表，与 dof 一一对应
        elif isinstance(mass, list) and len(mass) == len(dof):
            dof_index_map = {'Ux': 0, 'Uy': 1, 'Uz': 2, 'Rx': 3, 'Ry': 4, 'Rz': 5}
            for m, d in zip(mass, dof):
                self.mass[dof_index_map[d]] = m
        
        else:
            raise ValueError("The mass must be either a single float value or a list matching the length of dof.")
        
        # 调用外部接口设置质量
        ret = Saproject().Assign.PointObj.Set.Mass(self.name, self.mass)
        
        # 检查返回值并记录日志
        if ret[-1] == 0:
            logger.success(f"Mass {self.mass} added to Point {self.name}")
        else:
            logger.error(f"Mass {self.mass} failed to add at Point {self.name}")
        
        return ret

    def exists(self):
        return Saproject().Assign.PointObj.Get.CoordCartesian(self.name)[-1] == 0

    def fix(self,DOF=list[Literal['Ux','Uy','Uz','Rx','Ry','Rz']]):
        if DOF is not None:
            self.restraints = DOF
        ret = Saproject().Assign.PointObj.Set.Restraint(self.name,self.restraints)
        if ret[-1] == 0:
            logger.success(f"Restraints at DOF:[{self.restraints}] added to Point {self.name}")
        else:
            logger.error(f"Restraints at DOF:[{self.restraints}] failed to added at Point {self.name}")
        return ret

@dataclass
class SapFrame:
    node1:Union[SapPoint,str]
    node2:Union[SapPoint,str]
    section:Union[str,Section_General,Section_NonPrismatic]
    
    name:str = ""
    CardinalPoint:Literal['Centroid','Shear Center','Bottom Left','Bottom Center','Bottom Right','Middle Left','Middle Center','Middle Right','Top Left','Top Center','Top Right'] = 'Centroid'
    
    def define(self):
        if isinstance(self.node1, SapPoint):
            namei = self.node1.name
        else:
            namei = self.node1
        if isinstance(self.node2, SapPoint):
            namej = self.node2.name
        else:
            namej = self.node2
        if isinstance(self.section, str):
            section_name = self.section
        else:
            section_name = self.section.name
        ret = Saproject().Assign.FrameObj.AddByPoint(namei, namej,propName=section_name, userName = self.name)
        if ret[-1] == 0:
            logger.opt(colors=True).success(f"Frame element <yellow>{self.name}</yellow> added!")
        else:
            logger.opt(colors=True).error(f"Frame element <yellow>{self.name}</yellow> failed to add!")

    def add_line_mass(self, disLoad:float = 0.0, Replace:bool = True):
        """add frame line mass

        Args:
            disLoad (float, optional): mass per unit length under unit kN_m . Defaults to 0.0.
            Replace (bool, optional): replace line mass or not. Defaults to True.
        """
        # add line mass manually instead(一期+二期恒载)
        ret = Saproject().Assign.FrameObj.Set.Mass(self.name,disLoad,Replace=Replace)
        if ret == 0:
            if Replace:
                logger.opt(colors=True).success(f"element <yellow>{self.name}</yellow> line mass set as {disLoad} ton/m (kN/m/g)!")
            else:
                logger.opt(colors=True).success(f"element <yellow>{self.name}</yellow> line mass set as {disLoad} ton/m (kN/m/g)!")
        else:
            logger.opt(colors=True).error(f"element <yellow>{self.name}</yellow> mass failed to set as {disLoad} ton/m (kN/m/g)!")

    def get_section_name(self):
        ret = Saproject()._Model.FrameObj.GetSection(self.name)
        if ret[-1] == 0:
            return ret[0]
        else:
            logger.error(f"Failed to get section name of Frame {self.name}")
     
    def define_Cardinal_Point(self,CardinalPoint:Literal['Centroid','Shear Center','Bottom Left','Bottom Center','Bottom Right','Middle Left','Middle Center','Middle Right','Top Left','Top Center','Top Right'] = None):
        if CardinalPoint is not None:
            newCardinalPoint = CardinalPoint
        else:
            newCardinalPoint = self.CardinalPoint
        ret = Saproject().Assign.FrameObj.Set.InsertionPoint(self.name, newCardinalPoint, False, False, [0,0,0], [0,0,0], "Local")
        if ret[-1] == 0:
            logger.opt(colors=True).success(f"Cardinal Point of Element <yellow>{self.name}</yellow> set as <yellow>{self.CardinalPoint}</yellow>!")
            self.CardinalPoint = CardinalPoint
        else:
            logger.opt(colors=True).error(f"Cardinal Point of Element <yellow>{self.name}</yellow> failed to set as <yellow>{self.CardinalPoint}</yellow>!")
        return ret

    def set_varying_sec_params(self,VarTotalLength:float = 0.0, RelStartLoc: float = 0.0):
        """_summary_

        Args:
            VarTotalLength (float, optional): This is the total assumed length of the nonprismatic section. Enter 0 for this item to indicate that the section length is the same as the frame object length. Defaults to 0.0. This item is applicable only when the assigned frame section property is a nonprismatic section. 
            RelStartLoc (float, optional): This is the relative distance along the nonprismatic section to the I-End (start) of the frame object. This item is ignored when the sVarTotalLengthitem is 0.0. Defaults to 0.0. This item is applicable only when the assigned frame section property is a nonprismatic section, and the sVarTotalLengthitem is greater than zero.
        """
        if isinstance(self.section, str):
                secname = self.section
        else:
            secname = self.section.name
                
        if not isinstance(self.section, Section_NonPrismatic):
            ret = Saproject()._Model.FrameObj.GetSectionNonPrismatic(self.name)
            if ret[-1] != 0:
                logger.warning(f"Section {self.section} is not nonprismatic.")
            raise ValueError(f"Section {self.section} is not nonprismatic.")
        ret = Saproject().Assign.FrameObj.Set.Section(name=self.name,
                                                propName=secname,
                                                sVarTotalLength=float(VarTotalLength),
                                                sVarRelStartLoc=float(RelStartLoc))
        if ret == 0:
            logger.opt(colors=True).success(f"Frame with nonprismatic section: <yellow>{secname}</yellow> now set as total length of <yellow>{VarTotalLength}</yellow> and relative start location at <yellow>{RelStartLoc}</yellow>!")
        else:
            logger.opt(colors=True).error(f"Failed to set Frame with nonprismatic section: <yellow>{secname}</yellow> as total length of <yellow>{VarTotalLength}</yellow> and relative start location at <yellow>{RelStartLoc}</yellow>!")
            
        

class SapBase_6Spring:
    def __init__(self, point: SapPoint, pier_name, spring_data_name=None,spring_file_path:Path = Path(".\Examples\ContinuousBridge6spring.txt")):
        self.point = point
        self.pier_name = pier_name
        self.name = self.pier_name + "_Base"
        self.point.name = self.name
        self.spring_file_path = spring_file_path
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
    
    def get_spring_data(self,datapath:Path = None):
        if not datapath:
            datapath = self.spring_file_path
        with open(datapath, "r") as f:
            lines = f.readlines()
            springs = [line.strip().split('\t') for line in lines]
            spring = [s for s in springs if s[0].split('#')[-1] == self.spring_data_name][0]
        klist = []
        for k in spring:
            if k != self.spring_data_name and k.split('#')[-1] != self.spring_data_name and k != 'GLOBAL':
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
        if unit != Saproject().Units:
            Saproject().setUnits(unit)
        ret = Saproject().Assign.PointObj.Set.SpringCoupled(self.name, self.spring_data, Replace=True)
        if ret[1] == 0:
            logger.opt(colors=True).success(f"Spring for Joint: <yellow>{self.name}</yellow> Added! K = <cyan>{self.spring_data}</cyan>")
        else:
            logger.opt(colors=True).error(f"Spring for Joint: <yellow>{self.name}</yellow> Failed to Add! K = {self.spring_data}")
        return ret

    def connect_with_pier(self):
        raise NotImplementedError

@dataclass
class Sap_Double_Box_Pier:
    name:str
    station:float
    Height_of_pier_bottom:float
    Height_of_pier:float
    bottom_solid_length:float
    top_solid_length:float
    Distance_between_bearings:float
    Distance_between_piers:float
    Height_of_cap:float=None
    num_of_hollow_elements:int =1
    is_intermediate_pier:bool =False
    offset:float =1.0
        
    def __post_init__(self):
        self.addsome_empty_attr()
        
        self.generate_pier_points(side = 'both')
        self.generate_pier_elements(side = 'both')
        
        self.generate_base_points()
        self.generate_cap_elements()
        
        self.add_body_constraint()
        # self.add_mass()
        Saproject().RefreshView()
    
    def connect_with_base(self,baseobj:Literal['SapBase_6Spring']):
        self.base = baseobj
        self.base.get_spring_data()
        self.base.add_spring()
    
    def generate_base_points(self):
        x = self.station
        y = 0
        # base point
        self.base_point = SapPoint(x, y, self.Height_of_pier_bottom-self.Height_of_cap, f"{self.name}_Base")
        
        # cap points
        if not hasattr(self, "Mass_of_cap_in_ton"):
            self.get_cap_section()
        self.cap_point = SapPoint(x, y, self.Height_of_pier_bottom-self.Height_of_cap/2, f"{self.name}_Cap",mass=[self.Mass_of_cap_in_ton for _ in range(3)] + [0, 0, 0])
        
        # cap top points
        self.cap_top_point = SapPoint(x, y, self.Height_of_pier_bottom, f"{self.name}_CapTop")
        
        self.base_points = [self.base_point, self.cap_point, self.cap_top_point]
        for point in self.base_points:
            point.add()
    
    def addsome_empty_attr(self):
        if self.Height_of_cap ==None:
            self.Height_of_cap: float = 3.0 if self.Height_of_pier >= 50 else 2.8 if 40<=self.Height_of_pier<50 else 2.7
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
            y = self.Distance_between_piers/2
        elif side == 'right':
            y = - self.Distance_between_piers/2
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
    
    def __box_section_geoms(self):
        # 合并截面
        # 可修改的值
        if self.Height_of_pier >= 50:
            height = 400
        elif self.Height_of_pier >= 40:
            height = 350
        elif self.Height_of_pier < 40 and self.Height_of_pier >= 0:
            height = 300
        else:
            logger.error("Height of pier is not valid.")
            return None
        # 不变的值
        width = 900
        d_width_concrete = 105
        chamfer_width,chamfer_height = 120,60
        d_height_concrete = 70
        R = height/2
        # clockwise(八边形)
        inner_points = [
            (-width/2+d_width_concrete+chamfer_width, height/2-d_height_concrete),
            (width/2-d_width_concrete-chamfer_width, height/2-d_height_concrete),
            (width/2-d_width_concrete, height/2-d_height_concrete-chamfer_height),
            (width/2-d_width_concrete, -height/2+d_height_concrete+chamfer_height),
            (width/2-d_width_concrete-chamfer_width, -height/2+d_height_concrete),
            (-width/2+d_width_concrete+chamfer_width, -height/2+d_height_concrete),
            (-width/2+d_width_concrete, -height/2+d_height_concrete+chamfer_height),
            (-width/2+d_width_concrete, height/2-d_height_concrete-chamfer_height)]

        def create_arc(center, radius, start_angle, end_angle, num_points=20):
            """
            Create a half-circle arc.
            
            :param center: Tuple (x, y) representing the center of the circle.
            :param radius: Radius of the circle.
            :param start_angle: Starting angle of the arc in degrees.
            :param end_angle: Ending angle of the arc in degrees.
            :param num_points: Number of points to generate the arc.
            :return: Shapely LineString representing the half-circle arc.
            """
            angles = [np.radians(start_angle + i * (end_angle - start_angle) / (num_points - 1))
                    for i in range(num_points)]
            points = [(center[0] + radius * np.cos(angle), center[1] + radius * np.sin(angle))
                    for angle in angles]

            return points

        outer_points = []
        outer_points.append((-width/2+R,R))
        outer_points.append((width/2-R,R))
        outer_points.extend(create_arc((width/2-R,0),R,90,-90))
        outer_points.append((width/2-R,-R))
        outer_points.append((-width/2+R,-R))
        outer_points.extend(create_arc((-width/2+R,0),R,270,90))
        # 实心截面需内开小洞，否则翘曲常数计算会存在问题
        innerpoly = Polygon(inner_points)
        inner_circle = Polygon(create_arc((0,0),1,0,360))
        outerpoly = Polygon(outer_points)
        
        innergeom = Geometry(geom=innerpoly)
        inner_circle_geom = Geometry(geom=inner_circle)
        outergeom = Geometry(geom=outerpoly)-inner_circle_geom
        outergeom.create_mesh(mesh_sizes=[(outerpoly.area)/100])
        combinedgeom = outergeom - innergeom
        combinedgeom.create_mesh(mesh_sizes=[(outerpoly.area-innerpoly.area)/100])
        return combinedgeom,outergeom
    
    def get_solid_section(self,plot:bool = False,plottype:Literal['geometry','mesh']='mesh'):
        material = "C40"
        unit_of_sec = 'cm'
        _,solidgeom = self.__box_section_geoms()
        sec = Section(geometry=solidgeom)
        if plot:
            if plottype == 'geometry':
                sec.plot_geometry()
            elif plottype == 'mesh':
                sec.plot_mesh(materials=False)
        # 计算截面特性
        # 几何特性
        sec.calculate_frame_properties()
        sec.calculate_geometric_properties()
        # warpping properties like shear area As2,As3, torsion constant J
        sec.calculate_warping_properties()
        bounds = solidgeom.geom.bounds  # (minx, miny, maxx, maxy)
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]

        ixx_c, iyy_c, ixy_c = sec.get_ic()
        J = sec.get_j() if sec.get_j() != math.nan else ixx_c + iyy_c
        asx, asy = sec.get_as()

        self.solid_section = Section_General(
            name=self.name+"_pier_box",
            material="C40",
            Area=sec.get_area(),
            Depth=height,Width=width,
            As2=asy,As3=asx,
            I22=iyy_c,I33=ixx_c,I23=ixy_c,J=J,
            geom=solidgeom,sec=sec,
            unit_of_sec=unit_of_sec,
            notes=self.name+"_pier_box_section"
        )
        return self.solid_section
    
    def get_box_section(self,plot:bool = False,plottype:Literal['geometry','mesh']='mesh'):
        material = "C40"
        unit_of_sec = 'cm'
        combinedgeom,_ = self.__box_section_geoms()        

        sec = Section(geometry=combinedgeom)
        if plot:
            if plottype == 'geometry':
                sec.plot_geometry()
            elif plottype == 'mesh':
                sec.plot_mesh(materials=False)
        # 计算截面特性
        # 几何特性
        sec.calculate_frame_properties()
        sec.calculate_geometric_properties()
        # warpping properties like shear area As2,As3, torsion constant J
        sec.calculate_warping_properties()
        bounds = combinedgeom.geom.bounds  # (minx, miny, maxx, maxy)
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        
        ixx_c, iyy_c, ixy_c = sec.get_ic()
        asx,asy = sec.get_as()

        self.box_section = Section_General(
            name = self.name+"_pier_box",
            material = "C40",
            Area = sec.get_area(),
            Depth = height,Width = width,
            As2=asy,As3=asx,
            I22=iyy_c,I33=ixx_c,I23=ixy_c,J=sec.get_j(),
            geom = combinedgeom, sec = sec,
            unit_of_sec = unit_of_sec,
            notes = self.name+"_pier_box_section")
        return self.box_section
    
    def get_cap_section(self):
        width = 12 if self.Height_of_pier >= 50 else 10.794
        depth = 37.25
        self.Mass_of_cap_in_ton = width * depth * self.Height_of_cap * 2.5
        ret = Saproject()._Model.PropFrame.SetRectangle(self.name+"_Cap", "C30", width, depth)
        if ret == 0:
            logger.success(f"Cap section {self.name}_Cap added!")
        self.cap_section = self.name+"_Cap"
        return self.cap_section
    
    def _add_body_constraints_for_points(self,constraint_name:str, points : list):
        for point in points:
            if not point.exists():
                logger.opt(colors=True).warning(f"<yellow>{point.name}</yellow> Accidentally does not exist!")
                point.add()
            ret = Saproject().Assign.PointObj.Set.Constraint(point.name,constraint_name,ItemType = 0)
            if ret[1] == 0:
                logger.opt(colors=True).success(f"<yellow>{point.name}</yellow> added to Body constraint : <yellow>{constraint_name}</yellow>")
            else:
                logger.opt(colors=True).error(f"<yellow>{point.name}</yellow> failed to add to Body constraint : <yellow>{constraint_name}</yellow>")
    
    def add_body_constraint(self):
        body_dof = ["UX", "UY", "UZ", "RX", "RY", "RZ"]
        flatten = lambda l: list(chain.from_iterable(map(lambda x: flatten(x) if isinstance(x, list) else [x], l)))
        
        # add body constraint between capTop and pier
        
        Saproject().Define.jointConstraints.SetBody(self.name+"_Cap_Pier", body_dof)
        self._add_body_constraints_for_points(self.name+"_Cap_Pier", flatten([self.cap_top_point, self.pier_bottom_point['left'],self.pier_bottom_point['right']]))
        
        # add body constraint between pier top and bearing bottom
        left_points = flatten([self.pier_top['left'], self.bearing_bottom_point_outer['left'], self.bearing_bottom_point_inner['left']])
        right_points = flatten([self.pier_top['right'], self.bearing_bottom_point_outer['right'], self.bearing_bottom_point_inner['right']])
        # left
        Saproject().Define.jointConstraints.SetBody(self.name+"_left_Pier_Bearing", body_dof)
        self._add_body_constraints_for_points(self.name+"_left_Pier_Bearing", left_points)
        # right
        Saproject().Define.jointConstraints.SetBody(self.name+"_right_Pier_Bearing", body_dof)
        self._add_body_constraints_for_points(self.name+"_right_Pier_Bearing", right_points)
        
    def generate_cap_elements(self):
        cap_section_name = self.get_cap_section()
        
        # define solid cap
        SapFrame(node1=self.base_point.name, node2=self.cap_point.name,section=cap_section_name,name=self.name+"_base2cap").define()
        SapFrame(node1=self.cap_point.name, node2=self.cap_top_point.name,section=cap_section_name,name=self.name+"_cap2bottom").define()
    
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
        SapFrame(node1=self.pier_bottom_point[side].name, node2=self.pier_hollow_bottom[side].name,section=solid_section.name,name=self.name+'_'+side+"_bottom2hollowBottom").define()
        
        for i,h in enumerate(self.hollow_points[side]):
            if i == 0:
                SapFrame(node1=self.pier_hollow_bottom[side].name, node2=h.name, section=box_section.name, name=self.name+'_'+side+f"_hollow_{i+1}").define()
            else:
                SapFrame(node1=self.hollow_points[side][i-1].name, node2=h.name, section=box_section.name, name=self.name+'_'+side+f"_hollow_{i+1}").define()
        if len(self.hollow_points[side]) == 0:
            SapFrame(node1=self.pier_hollow_bottom[side].name, node2=self.pier_hollow_top[side].name, section=box_section.name, name=self.name+'_'+side+"_hollowBottom2Top").define()
        else:
            SapFrame(node1=self.hollow_points[side][-1].name, node2=self.pier_hollow_top[side].name, section=box_section.name, name=self.name+'_'+side+"_hollowBottom2Top").define()
        SapFrame(node1=self.pier_hollow_top[side].name, node2=self.pier_top[side].name, section=solid_section.name, name=self.name+'_'+side+"_hollowTop2Top").define()


class Sap_Bearing:
    def __init__(self):
        logger.error('Sap_Bearing is a abstract class!Should not be instantiated!')
        raise ShouldNotInstantiateError('Abstract class Sap_Bearing accidentally instantiated!')
    
    def add_link(self,point1:SapPoint=None,point2:SapPoint=None):
        if not self.linkprop_instance.is_defined:
            self.linkprop_instance.define_link()
        if not point1:
            point1 = self.start_point
        if not point2:
            point2 = self.end_point
        ret = Saproject().Assign.Link.AddByPoint(point1.name, point2.name, IsSingleJoint=False, PropName = self.linkprop_name, UserName=self.name)
        if ret[1] == 0:
            logger.opt(colors=True).success(f"Link <yellow>{self.name}</yellow> Added!")
        else:
            logger.opt(colors=True).error(f"Link <yellow>{self.name}</yellow> Failed to Add!")
    
    def get_link_between_points(self,point1:SapPoint=None,point2:SapPoint=None)-> list[str]:
        if not point1:
            point1 = self.start_point
        if not point2:
            point2 = self.end_point
        ret1 = Saproject().Assign.PointObj.Get.Connectivity(point1.name)
        ret2 = Saproject().Assign.PointObj.Get.Connectivity(point2.name)
        if ret1[-1] == 0 and ret2[-1] == 0:
            # both points exist
            if ret1[0]>0 and ret2[0]>0:
                # both points are connected
                # get {name:linktype} dict, only need to check if type is 7(Link)
                dict1 = {ret1[2][i]:ret1[1][i]for i in range(ret1[0]) if ret1[1][i]==7}
                dict2 = {ret2[2][i]:ret2[1][i]for i in range(ret2[0]) if ret2[1][i]==7}
                commonlink = [link for link in dict1.keys() if link in dict2.keys()]
                # should only have one common link, but i'll return whole list just in case
                return commonlink
        else:
            logger.error(f"Point {point1.name} or {point2.name} does not exist.")
        return None

    def AxialF_under_dead_weight(self,link_name:str):
        # make sure dead load analysis is run
        if not Saproject().is_locked:
            # run dead load analysis
            Saproject().Scripts.Analyze.RemoveCases("All")
            Saproject().Scripts.Analyze.AddCases(CaseName = ['DEAD'])
            filepath = Saproject()._Model.GetModelFilename(True)
            if len(filepath) >0:
                Saproject().File.Save(filepath)
            else:
                logger.warning("Model is not saved! Saving as default")
                Saproject().File.Save()
            Saproject().Analyze.RunAnalysis()
            
        # read axial force
        Saproject().Scripts.SelectCombo_Case("DEAD")
        ret = Saproject().Results.Link.Force(link_name,ItemTypeElm=1)
        if ret[-1] == 0:
            axialF = max([abs(val) for val in ret[7]])
            return axialF
        else:
            logger.error(f"Failed to get axial force for link {link_name}")
            return None
            

@dataclass
class Sap_LinkProp_Linear(Sap_Bearing):
    prop_name:str
    DOF: List[Literal['U1', 'U2', 'U3', 'R1', 'R2', 'R3']] = field(default_factory=list)
    Fixed: List[Literal['U1', 'U2', 'U3', 'R1', 'R2', 'R3']] = field(default_factory=list)
    Ke: Dict[Literal['U1', 'U2', 'U3', 'R1', 'R2', 'R3'], float] = field(default_factory=dict)
    Ce: Dict[Literal['U1', 'U2', 'U3', 'R1', 'R2', 'R3'], float] = field(default_factory=dict)
    dj2: float = 0.0
    dj3: float = 0.0
    KeCoupled:bool = False
    CeCoupled:bool = False
    notes: str = ""
    GUID: str = ""
    _instances: ClassVar = weakref.WeakSet()

    def __hash__(self):
        return hash((self.prop_name, tuple(self.DOF), tuple(self.Fixed), frozenset(self.Ke.items()), frozenset(self.Ce.items()), self.dj2, self.dj3, self.notes, self.GUID))
    
    def __post_init__(self):
        self.__class__._instances.add(self)
    
    @property
    def is_defined(self):
        ret = Saproject().Define.section.PropLink.Get.Linear(self.prop_name)
        return ret[-1]==0
    
    def get_LinkProp_from_Sap(self):
        if self.is_defined:
            ret = Saproject().Define.section.PropLink.Get.Linear(self.prop_name)
            dofdict = ['U1', 'U2', 'U3', 'R1', 'R2', 'R3']
            DOF:list[Literal['U1', 'U2', 'U3', 'R1', 'R2', 'R3']] = [dofdict[i] for i,dof in enumerate(ret[0]) if dof] 
            Fixed:list[Literal['U1', 'U2', 'U3', 'R1', 'R2', 'R3']] = [dofdict[i] for i,dof in enumerate(ret[1]) if dof] 
            Ke:dict[Literal['U1', 'U2', 'U3', 'R1', 'R2', 'R3'], float] = {dof:k for dof,k in zip(dofdict,ret[2])}
            Ce:dict[Literal['U1', 'U2', 'U3', 'R1', 'R2', 'R3'], float] = {dof:c for dof,c in zip(dofdict,ret[3])}
            dj2:float = ret[4]
            dj3:float = ret[5]
            KeCoupled:bool = ret[6]
            CeCoupled:bool = ret[7]
            Notes:str = ret[8]
            GUID:str = ret[9]
            return DOF,Fixed,Ke,Ce,dj2,dj3,KeCoupled,CeCoupled,Notes,GUID
        else:
            logger.error(f"Link Property {self.prop_name} is not defined.")
            return None
    
    def define_link(self):
        if not self.is_defined:
            ret = Saproject().Define.section.PropLink.Set.Linear(self.prop_name, DOF=self.DOF, Fixed=self.Fixed, Ke=self.Ke, Ce = self.Ce, dj2=self.dj2, dj3=self.dj3,KeCoupled=self.KeCoupled,CeCoupled=self.CeCoupled, Notes=self.notes)
            if ret[-1]==0:
                logger.opt(colors=True).info(f"LinearLink Property <yellow>{self.prop_name}</yellow> defined.")

    @classmethod
    def get_instances(cls):
        return list(cls._instances)


class Sap_Bearing_Linear(Sap_LinkProp_Linear):
    def __init__(self,name:str, start_point:SapPoint, end_point:SapPoint, linkprop_name:str):
        self.name = name
        self.start_point = start_point
        self.end_point = end_point
        self.linkprop_name = linkprop_name
        # check if link property already exists
        self.linkprop_instance = [link for link in Sap_LinkProp_Linear.get_instances() if link.prop_name == self.linkprop_name][0]
        if not isinstance(self.linkprop_instance, Sap_LinkProp_Linear):
            self.linkprop_instance = [link for link in Sap_LinkProp_Linear.get_instances() if link.name == self.linkprop_name][0]
            self.linkprop_instance.define_link()
        self.add_link()
        
@dataclass
class Sap_LinkProp_MultiLinearElastic(Sap_Bearing):
    prop_name: str
    DOF: List[Literal['U1', 'U2', 'U3', 'R1', 'R2', 'R3']] = field(default_factory=list)
    Fixed: List[Literal['U1', 'U2', 'U3', 'R1', 'R2', 'R3']] = field(default_factory=list)
    Nonlinear: Dict[Literal['U1', 'U2', 'U3', 'R1', 'R2', 'R3'],dict] = field(default_factory=dict)
    Ke: Dict[Literal['U1', 'U2', 'U3', 'R1', 'R2', 'R3'], float] = field(default_factory=dict)
    Ce: Dict[Literal['U1', 'U2', 'U3', 'R1', 'R2', 'R3'], float] = field(default_factory=dict)
    dj2: float = 0.0
    dj3: float = 0.0
    notes: str = ""
    GUID: str = ""
    _instances: ClassVar = weakref.WeakSet()

    def __hash__(self) -> int:
        return hash((self.prop_name, tuple(self.DOF), tuple(self.Fixed), tuple(self.Nonlinear), frozenset(self.Ke.items()), frozenset(self.Ce.items()), self.dj2, self.dj3, self.notes, self.GUID))
    
    def __post_init__(self):
        self.__class__._instances.add(self)
    
    @property
    def is_defined(self):
        ret = Saproject().Define.section.PropLink.Get.MultiLinearElastic(self.prop_name)
        return ret[-1]==0
    
    def get_LinkProp_from_Sap(self):
        if self.is_defined:
            ret = Saproject().Define.section.PropLink.Get.MultiLinearElastic(self.prop_name)
            dofdict = ['U1', 'U2', 'U3', 'R1', 'R2', 'R3']
            DOF:list[Literal['U1', 'U2', 'U3', 'R1', 'R2', 'R3']] = [dofdict[i] for i,dof in enumerate(ret[0]) if dof] 
            Fixed:list[Literal['U1', 'U2', 'U3', 'R1', 'R2', 'R3']] = [dofdict[i] for i,dof in enumerate(ret[1]) if dof] 
            Nonlinear:list[Literal['U1', 'U2', 'U3', 'R1', 'R2', 'R3']] = [dofdict[i] for i,dof in enumerate(ret[2]) if dof] 
            Ke:dict[Literal['U1', 'U2', 'U3', 'R1', 'R2', 'R3'], float] = {dof:k for dof,k in zip(dofdict,ret[3])}
            Ce:dict[Literal['U1', 'U2', 'U3', 'R1', 'R2', 'R3'], float] = {dof:c for dof,c in zip(dofdict,ret[4])}
            dj2:float = ret[5]
            dj3:float = ret[6]
            Notes:str = ret[7]
            GUID:str = ret[8]
            return DOF,Fixed,Nonlinear,Ke,Ce,dj2,dj3,Notes,GUID
        else:
            logger.error(f"Link Property {self.prop_name} is not defined.")
            return None
    
    def __define_link(self):
        ret = Saproject().Define.section.PropLink.Set.MultiLinearElastic(self.prop_name, DOF=self.DOF, Fixed=self.Fixed, Nonlinear = list(self.Nonlinear.keys()),Ke=self.Ke,Ce=self.Ce,dj2=self.dj2,dj3=self.dj3,Notes=self.notes)
        return ret
    
    def __define_nonlinear_points(self):
        if not self.is_defined:
            logger.error(f"Link Property {self.prop_name} is not defined. Trying to fix...")
            self.define_link()
        for dof,pointsdict in self.Nonlinear.items():
            forcelist = pointsdict['forcelist']
            displist = pointsdict['displist']
            ret = Saproject().Define.section.PropLink.Set.MultiLinearPoints(self.prop_name, dof, forcelist, displist, Type='Isotropic')
            points = "["+", ".join(f"({d:.2f},{f:.2f})" for d,f in zip(displist,forcelist))+"]"
            if ret[-1]==0:
                logger.opt(colors=True).success(f"Link Property <yellow>{self.prop_name}</yellow> updated with points:{points}.")
            else:
                logger.opt(colors=True).error(f"Link Property <yellow>{self.prop_name}</yellow> failed to update with points:{points}.")
    
    def define_link(self):
        if not self.is_defined:
            ret = self.__define_link()
            if ret[-1] == 0:
                logger.opt(colors=True).success(f"Multi Elastic Linear Link Property <yellow>{self.prop_name}</yellow> defined.")
        else:
            DOF, Fixed, Nonlinear, Ke, Ce, dj2, dj3, Notes, GUID = self.get_LinkProp_from_Sap()
            discrepancies = []
            if DOF != self.DOF:
                discrepancies.append(f"DOF: expected {self.DOF}, got {DOF}")
            if Fixed != self.Fixed:
                discrepancies.append(f"Fixed: expected {self.Fixed}, got {Fixed}")
            if Nonlinear != list(self.Nonlinear.keys()):
                discrepancies.append(f"Nonlinear: expected {list(self.Nonlinear.keys())}, got {Nonlinear}")
            if Ke != self.Ke:
                discrepancies.append(f"Ke: expected {self.Ke}, got {Ke}")
            if Ce != self.Ce and any(val != 0.0 for val in Ce.values()):
                discrepancies.append(f"Ce: expected {self.Ce}, got {Ce}")
            if dj2 != self.dj2:
                discrepancies.append(f"dj2: expected {self.dj2}, got {dj2}")
            if dj3 != self.dj3:
                discrepancies.append(f"dj3: expected {self.dj3}, got {dj3}")
            if Notes != self.notes:
                discrepancies.append(f"Notes: expected {self.notes}, got {Notes}")
            if GUID != self.GUID:
                discrepancies.append(f"GUID: expected {self.GUID}, got {GUID}")

            if not discrepancies:
                logger.opt(colors=True).info(f"Link Property <yellow>{self.prop_name}</yellow> already defined.")
            else:
                logger.opt(colors=True).warning(
                    f"Link Property <yellow>{self.prop_name}</yellow> already defined but with different parameters: {', '.join(discrepancies)}. Updating..."
                )
                # Update the properties with the new values
                ret = self.__define_link()
                if ret[-1] == 0:
                    logger.opt(colors=True).info(f"Link Property <yellow>{self.prop_name}</yellow> updated with new parameters.")
        self.__define_nonlinear_points()
    
    def _update_link_yield_prop_1dof(self,DOF:Literal['U1', 'U2', 'U3', 'R1', 'R2', 'R3'],forceList:list,dispList:list):
        if DOF not in self.Nonlinear.keys():
            newdict = {DOF:{'forcelist':forceList,'displist':dispList}}
            self.Nonlinear.update(newdict)
         
    @classmethod
    def get_instances(cls):
        return list(cls._instances)

class Sap_Bearing_MultiLinearElastic(Sap_LinkProp_MultiLinearElastic):
    def __init__(self,name:str,start_point:SapPoint,end_point:SapPoint,linkprop_name:str):
        self.name = name
        self.start_point = start_point
        self.end_point = end_point
        self.linkprop_name = linkprop_name
        # check if link property already exists
        self.linkprop_instance = [link for link in Sap_LinkProp_MultiLinearElastic.get_instances() if link.prop_name == self.linkprop_name][0]
        if not isinstance(self.linkprop_instance, Sap_LinkProp_MultiLinearElastic):
            self.linkprop_instance = [link for link in Sap_LinkProp_MultiLinearElastic.get_instances() if link.prop_name == self.linkprop_name][0]
    
    def calculate_yield_properties(self,mu:float = 0.02,yield_disp:float=0.002,ultimate_disp:float=1)->tuple[list[float],list[float]]:
        """
        Ideal bilinear elastic, yield force is static frictional force, reached at 2mm, infinite length of platform segment (default 1m)
        Args:
            mu (float, optional): _description_. Defaults to 0.03.
            yield_disp (float, optional): _description_. Defaults to 0.002 m.
            ultimate_disp (float, optional): _description_. Defaults to 1 m.

        """
        if Saproject().Units != 'KN_m_C':
            Saproject().setUnits('KN_m_C')
        yield_force = self.AxialF_under_dead_weight(self.name) * mu
        forcelist = [-yield_force,-yield_force,0,yield_force,yield_force]
        displist = [-ultimate_disp,-yield_disp,0,yield_disp,ultimate_disp]
        return forcelist,displist
    
    def update_yield_prop_for_existing_linear_link(self):
        existing_link = self.get_link_between_points(self.start_point,self.end_point)[0]
        existing_linkprop = Saproject()._Model.LinkObj.GetProperty(existing_link)[0]
        [link_type,ret] = Saproject().Define.section.PropLink.Get.TypeOAPI(existing_linkprop)
        if ret==0 and link_type == 'Linear':
            existing_link_instance = [link for link in Sap_LinkProp_Linear.get_instances() if link.prop_name == existing_linkprop][0]
            if isinstance(existing_link_instance, Sap_LinkProp_Linear):
                # assume already defined
                Ke = existing_link_instance.Ke
                doflist = [dof for dof,ke in Ke.items() if ke == 0 and dof not in ['R1','R2','R3']]
                forceList,dispList = self.calculate_yield_properties(mu=0.03,yield_disp=0.002,ultimate_disp=1)
                for dof in doflist:
                    self.linkprop_instance._update_link_yield_prop_1dof(dof,forceList,dispList)
                logger.debug(f"Yield properties updated for {existing_link}")
            else:
                raise ValueError(f"Sap_LinkProp_Linear instance for {existing_link} is not existing!")
        else:
            logger.error(f"Link {existing_link} is not Not Supported yet!")
            raise NotImplementedError
        
    def add_link(self):
        """
        little different from Sap_Bearing.add_link,this function checks if link already exists, if yes, remove the previous one first.
        """
        exist_link = self.get_link_between_points(self.start_point,self.end_point)
        if exist_link:
            for link in exist_link:
                Saproject().Assign.Link.Delete(link)
        super().add_link()
        
class Sap_Girder:
    def __init__(self):
        logger.error('Sap_Girder is a abstract class!Should not be instantiated!')
        raise ShouldNotInstantiateError('Abstract class Sap_Girder accidentally instantiated!')

    def _define_ideal_links(self):
        # 刚度取大值，不直接固定,暂时不考虑阻尼
        # U1为竖向，U2为纵桥向，U3为横桥向
        FixedDOF = []
        DOF = ['U1', 'U2', 'U3', 'R1', 'R2', 'R3']
        # dampingCe = {}
        # 固定支座:
        uncoupleKe = {"U1":1e10,"U2":1e10,"U3":1e10,"R1":0,"R2":0,"R3":0}
        # fixed_link = "Fixed"
        # Saproject().Define.section.PropLink.Set.Linear(fixed_link, DOF=DOF, Fixed=FixedDOF, Ke=uncoupleKe)
        fixed_link = Sap_LinkProp_Linear("Fixed",DOF=DOF,Fixed=FixedDOF,Ke=uncoupleKe)
        fixed_link.define_link()
        # 横桥向（y）滑动支座
        uncoupleKe = {"U1":1e10,"U2":1e10,"U3":0,"R1":0,"R2":0,"R3":0}
        # y_sliding_link = "y_sliding"
        # Saproject().Define.section.PropLink.Set.Linear(y_sliding_link, DOF=DOF, Fixed=FixedDOF, Ke=uncoupleKe)
        y_sliding_link = Sap_LinkProp_Linear("y_sliding",DOF=DOF,Fixed=FixedDOF,Ke=uncoupleKe)
        y_sliding_link.define_link()
        # 纵桥向（x）滑动支座
        uncoupleKe = {"U1":1e10,"U2":0,"U3":1e10,"R1":0,"R2":0,"R3":0}
        # x_sliding_link = "x_sliding"
        # Saproject().Define.section.PropLink.Set.Linear(x_sliding_link, DOF=DOF, Fixed=FixedDOF, Ke=uncoupleKe)
        x_sliding_link = Sap_LinkProp_Linear("x_sliding",DOF=DOF,Fixed=FixedDOF,Ke=uncoupleKe)
        x_sliding_link.define_link()
        # 双向滑动支座
        uncoupleKe = {"U1":1e10,"U2":0,"U3":0,"R1":0,"R2":0,"R3":0}
        # both_sliding_link = "Both_sliding"
        # Saproject().Define.section.PropLink.Set.Linear(both_sliding_link, DOF=DOF, Fixed=FixedDOF, Ke=uncoupleKe)
        both_sliding_link = Sap_LinkProp_Linear("Both_sliding",DOF=DOF,Fixed=FixedDOF,Ke=uncoupleKe)
        both_sliding_link.define_link()
        return fixed_link, y_sliding_link, x_sliding_link, both_sliding_link

    def _update_ideal_link2MultiElactic_link(self,linear_link:Sap_Bearing_Linear):
        new_link_name = linear_link.name
        new_linkprop_name = new_link_name+"_MultiElastic"
        new_MultiElastic_linkprop = Sap_LinkProp_MultiLinearElastic(new_linkprop_name,
                                                                    DOF=linear_link.linkprop_instance.DOF,Fixed=linear_link.linkprop_instance.Fixed,Nonlinear={},Ke=linear_link.linkprop_instance.Ke,Ce=linear_link.linkprop_instance.Ce,dj2=linear_link.linkprop_instance.dj2,dj3=linear_link.linkprop_instance.dj3,notes=f"Converted from {linear_link.linkprop_instance.prop_name}")
        new_MultiElastic_link = Sap_Bearing_MultiLinearElastic(new_link_name,
                                                               linear_link.start_point,linear_link.end_point,linkprop_name=new_linkprop_name)
        new_MultiElastic_link.update_yield_prop_for_existing_linear_link()
        return new_MultiElastic_link
        
    def _add_body_constraints_for_points(self,constraint_name:str, points : list):
        for point in points:
            if not point.exists():
                logger.opt(colors=True).warning(f"<yellow>{point.name}</yellow> Accidentally does not exist!")
                point.add()
            ret = Saproject().Assign.PointObj.Set.Constraint(point.name,constraint_name,ItemType = 0)
            if ret[1] == 0:
                logger.opt(colors=True).success(f"<yellow>{point.name}</yellow> added to Body constraint : <yellow>{constraint_name}</yellow>")
            else:
                logger.opt(colors=True).error(f"<yellow>{point.name}</yellow> failed to add to Body constraint : <yellow>{constraint_name}</yellow>")


@dataclass
class Sap_Box_Girder(Sap_Girder):
    """_summary_

    Returns:
        _type_: _description_
    """
    name: str
    pierlist: list
    fixedpier: list
    num_of_ele_foreach_girder: int = 8
    Thickness_of_bearing: float = 0.3
    Height_of_girder: float = 2.678
    Plan:Literal['方案一','方案二','方案三'] = '方案一'
    DefaultSpan:float = 0.0 # if only one pier for this girder, this value will be used to calculate concentrated mass
    spanCount:int = 1 # only useful for one pier girder, this value will be used to calculate concentrated mass along the bridge
           
    def __post_init__(self):
        # sort pierlist by station
        self.pierlist = sorted(self.pierlist, key=lambda x: x.station)
        # makesure the 1st and last pier is intermediate pier
        if self.pierlist[0].is_intermediate_pier and self.pierlist[-1].is_intermediate_pier:
            if any([pier.is_intermediate_pier for pier in self.pierlist[1:-1]]):
                logger.opt(colors=True).error(f"Intermediate pier must be the 1st and last pier. Please check pier: <yellow>{[pier.name for pier in self.pierlist[1:-1] if pier.is_intermediate_pier]}</yellow>")
                return
        self.start_intermediate_pier = self.pierlist[0]
        self.end_intermediate_pier = self.pierlist[-1]
        self.generate_girder_points()
        self.girder_section = self.get_girder_section()
        if len(self.pierlist) > 1:
            self.generate_girder_elements()
        else:
            self.add_mass_for_concentrated_girder()
            self.add_restraints_for_concentrated_girder()
        self.add_body_constraint()
        # self.add_bearing_links(strategy='ideal')
        Saproject().RefreshView()
    
    def add_restraints_for_concentrated_girder(self):
        pier = self.pierlist[0]
        girdername = f"{pier.name}_{pier.name}"
        self.girder_points[girdername]['left'].fix(['Ry','Rz'])
        self.girder_points[girdername]['right'].fix(['Ry','Rz'])
    
    def add_mass_for_concentrated_girder(self):
        pier = self.pierlist[0]
        girdername = f"{pier.name}_{pier.name}"
        self.girder_points[girdername]['left'].defineMass((self.q1+self.q2)*self.DefaultSpan/9.81, dof = ['Uy','Uz'])
        self.girder_points[girdername]['left'].defineMass((self.q1+self.q2)*self.DefaultSpan*self.spanCount/9.81, dof = ['Ux'])
        self.girder_points[girdername]['right'].defineMass((self.q1+self.q2)*self.DefaultSpan/9.81, dof = ['Uy','Uz'])
        self.girder_points[girdername]['right'].defineMass((self.q1+self.q2)*self.DefaultSpan*self.spanCount/9.81, dof = ['Ux'])
    
    def update_links_parameters(self):
        """update bilinear ideal links for girder
        mu(float): frictional coefficient
        """
        
        for pier in self.pierlist:
            bearings = self.bearings[pier.name]
            for side in ['left','right']:
                linksdict = {}
                for key,link in bearings[side].items():
                    new_link = self._update_ideal_link2MultiElactic_link(link)
                    linksdict.update({key:new_link})
                self.bearings[pier.name][side] = linksdict
    
    def update_links_in_Sap(self):
        """update bilinear ideal links for girder in sap
        """
        if Saproject().is_locked:
            Saproject().unlockModel()
            
        for pier in self.pierlist:
            bearings = self.bearings[pier.name]
            for side in ['left','right']:
                for link in bearings[side].values():
                    link.linkprop_instance.define_link()
                    link.add_link()
    
    def add_ideal_bearing_links(self):
        fixed_link, y_sliding_link, x_sliding_link, both_sliding_link = self._define_ideal_links()
        if not hasattr(self, "bearings"):
            self.bearings = {}
        # 所有墩默认内侧用固定，外侧用滑动
        for pier in self.pierlist:
            if pier.name not in self.bearings.keys():
                self.bearings[pier.name] = {}
            for side in ['left','right']:
                if side not in self.bearings[pier.name].keys():
                    self.bearings[pier.name][side] = {}
                
                x_fixed = pier in self.fixedpier
                if x_fixed:
                    inner_link = fixed_link
                    outer_link = y_sliding_link
                else:
                    inner_link = x_sliding_link
                    outer_link = both_sliding_link
                    
                inner_bearing_top = self.girder_bearing_top_points[pier.name][side]['inner']
                if isinstance(pier.bearing_bottom_point_inner[side],list):
                    inner_bearing_bottom = [p for p in pier.bearing_bottom_point_inner[side] if p.x == inner_bearing_top.x][0]
                else:
                    inner_bearing_bottom = pier.bearing_bottom_point_inner[side]

                link_inner = Sap_Bearing_Linear(f"{self.name}_{pier.name}_{side}_inner_Bearing", inner_bearing_bottom, inner_bearing_top, inner_link.prop_name)
                
                outer_bearing_top = self.girder_bearing_top_points[pier.name][side]['outer']
                if isinstance(pier.bearing_bottom_point_outer[side],list):
                    outer_bearing_bottom = [p for p in pier.bearing_bottom_point_outer[side] if p.x == inner_bearing_top.x][0]
                else:
                    outer_bearing_bottom = pier.bearing_bottom_point_outer[side]
                link_outer = Sap_Bearing_Linear(f"{self.name}_{pier.name}_{side}_outer_Bearing", outer_bearing_bottom, outer_bearing_top, outer_link.prop_name)
                
                self.bearings[pier.name][side] = {'inner':link_inner, 'outer':link_outer}
        
    def add_body_constraint(self):
        body_dof = ["UX", "UY", "UZ", "RX", "RY", "RZ"]
        def flatten(l):  # noqa: E741
            return list(chain.from_iterable(map(lambda x: flatten(x) if isinstance(x, list) else [x], l)))
        for side in ['left','right']:
            for pier in self.pierlist:
                Saproject().Define.jointConstraints.SetBody(f"{pier.name}_{side}_Girder", body_dof)
                girder_point = self.girder_points[pier.name][side]
                bearing_top_points = list(self.girder_bearing_top_points[pier.name][side].values())
                self._add_body_constraints_for_points(pier.name+"_"+side+"_girder", flatten([girder_point,bearing_top_points]))
                
    def generate_girder_elements(self):
        for pier_start,pier_end in zip(self.pierlist[0:-1],self.pierlist[1:]):
            self.__generate_girder_elements(pier_start,pier_end, side = 'both')
    
    def __get_varying_rule(self,pier_start,
                           pier_end, uniform_length_for_intermediate_pier:float=0.3,
                           uniform_length_for_middle_pier:float=0.04,
                           uniform_length_for_middle_span:float=0.0,side:Literal['left','right']='left'):
        
        case_intermediate2middle = [[uniform_length_for_intermediate_pier,self.girder_section_middle_span,self.girder_section_middle_span],
                                   [1-uniform_length_for_intermediate_pier-uniform_length_for_middle_pier,self.girder_section_middle_span,self.girder_section_pier],
                                   [uniform_length_for_middle_pier,self.girder_section_pier,self.girder_section_pier]]
        case_middle2intermediate = [[uniform_length_for_middle_pier,self.girder_section_pier,self.girder_section_pier],
                                   [1-uniform_length_for_intermediate_pier-uniform_length_for_middle_pier,self.girder_section_pier,self.girder_section_middle_span],
                                   [uniform_length_for_intermediate_pier,self.girder_section_middle_span,self.girder_section_middle_span]]
        case_mieele2middle =       [[0.5-uniform_length_for_middle_span/2,self.girder_section_pier,self.girder_section_middle_span],
                                    [uniform_length_for_middle_span,self.girder_section_middle_span,self.girder_section_middle_span],
                                    [0.5-uniform_length_for_middle_span/2,self.girder_section_middle_span,self.girder_section_pier]]
        
        varying_rule:list[float,Section_General,Section_General] = []   # [length_ratio,section1,section2]
        if pier_start.is_intermediate_pier and pier_end.is_intermediate_pier:
            varying_rule = None
        elif pier_start.is_intermediate_pier and not pier_end.is_intermediate_pier:
            if side == 'left':
                varying_rule = case_intermediate2middle
            elif side == 'right':
                varying_rule = case_middle2intermediate
        elif not pier_start.is_intermediate_pier and pier_end.is_intermediate_pier:
            if side == 'left':
                varying_rule = case_middle2intermediate
            elif side == 'right':
                varying_rule = case_intermediate2middle
        else:
            # from middle pier to middle pier
            varying_rule = case_mieele2middle
            
        return varying_rule

    def __generate_girder_elements(self,pier_start,pier_end,side = Literal['left','right','both']):
        
        if side == 'both':
            self.__generate_girder_elements(pier_start,pier_end,'left')
            self.__generate_girder_elements(pier_start,pier_end,'right')
            return
        
        gidername = f"{pier_start.name}_{pier_end.name}"
        points_to_connect = self.girder_points[gidername][side]
        if self.is_varing_section:
            span_length = pier_end.station - pier_start.station
            varying_rule = self.__get_varying_rule(pier_start,pier_end,
                                                        uniform_length_for_intermediate_pier=0.723,
                                                        uniform_length_for_middle_pier=0.0422,
                                                        uniform_length_for_middle_span=0.447,side=side)
            varying_rule_list:\
                list[Literal['Variable','Absolute'],float,str,str,Literal['Linear','Parabolic','Cubic'],Literal['Linear','Parabolic','Cubic']] \
                = [['Variable',rule[0],rule[1].name,rule[2].name,'Linear','Linear'] for rule in varying_rule]
            var_section = Section_NonPrismatic(name = gidername+f"_{side}",VaryingRules = varying_rule_list)
            var_section.define()
            
        i=1
        for point1,point2 in zip(points_to_connect[0:-1],points_to_connect[1:]):
            if self.is_varing_section:
                section = var_section
            else:
                section = self.girder_section
            
            girder = SapFrame(node1 = point1, node2 = point2, section = section, name = f"{gidername}_{side}_girder_{i}")
            girder.define()
            
            if self.is_varing_section:
                # Relative start location of varying section
                x_start = points_to_connect[0].x
                relative_startLoc = min(abs((point1.x-x_start)),abs((point2.x-x_start))) / span_length
                girder.set_varying_sec_params(VarTotalLength = span_length,RelStartLoc=relative_startLoc)
                # Cardinal Point
                girder.define_Cardinal_Point('Top Center')
                
            # 一期恒载q1
            girder.add_line_mass(self.q1/9.81,Replace=True)
            # 二期恒载q2
            girder.add_line_mass(self.q2/9.81,Replace=False)
            i+=1
    
    def get_girder_section(self):
        if self.Plan == '方案一':
            # 方案一:等截面钢箱梁(mm)
            self.is_varing_section = False
            Area = 855043.2 
            Asy,Asz = 476380.0,79827.2 
            Ixx,Iyy,Izz = 3.13E+12,2.32E+12,2.32E+13
            # 20.105m x 4m
            Depth,Width = 4000, 20105
            # 一期恒载和二期恒载kN/m
            self.q1 = 117.5
            self.q2 = 43.9
            self.girder_section = Section_General(
                name = self.name+"_girder",
                material = "Q420q",
                Area = Area,
                Depth = Depth,Width = Width,
                As2=Asz,As3=Asy,
                I22=Izz,I33=Iyy,I23=0,J=Ixx,
                unit_of_sec='mm',
                notes = self.name+"_main_girder_section")
        elif self.Plan == '方案二':
            # 方案二:等截面组合梁
            self.is_varing_section = False
            Area = 1364813.0 
            Asy,Asz = 1038166.0,127892.0 
            Ixx,Iyy,Izz = 6.82E+12,3.52E+12,3.98E+13
            # 20.105m x 4.5m
            Depth,Width = 4500, 20105
            # 一期恒载和二期恒载kN/m
            self.q1 = 246.9
            self.q2 = 56.0
            self.girder_section = Section_General(
                name = self.name+"_girder",
                material = "C60",
                Area = Area,
                Depth = Depth,Width = Width,
                As2=Asz,As3=Asy,
                I22=Izz,I33=Iyy,I23=0,J=Ixx,
                unit_of_sec='mm',
                notes = self.name+"_main_girder_section")
        elif self.Plan == '方案三':
            # 方案三:变截面连续梁
            self.is_varing_section = True
            self.variation_curve:Literal['Linear','Parabolic','Cubic'] = 'Parabolic'
            self.girder_section = None
            # 一期恒载和二期恒载kN/m
            self.q1 = 707.0
            self.q2 = 60.19
            # 分跨中和中墩截面
            # 中墩截面
            Area = 3.210E+07
            Asy,Asz = 1.563E+07,1.322E+07
            Ixx,Iyy,Izz = 3.009E+14,1.622E+14,7.218E+14
            # 20.105m x 6.0m
            Depth,Width = 6000, 20105
            self.girder_section_pier = Section_General(
                name = self.name+"_girder_pier",
                material = "C60",
                Area = Area,
                Depth = Depth,Width = Width,
                As2=Asz,As3=Asy,
                I22=Izz,I33=Iyy,I23=0,J=Ixx,
                unit_of_sec='mm',
                notes = self.name+"_main_girder_section")
            # 跨中截面
            Area = 1.737E+07
            Asy,Asz = 9.598E+06,4.663E+06
            Ixx,Iyy,Izz = 9.234E+13,4.068E+13,4.645E+14
            # 20.105m x 4.0m
            Depth,Width = 4000, 20105
            self.girder_section_middle_span = Section_General(
                name = self.name+"_girder_middle_span",
                material = "C60",
                Area = Area,
                Depth = Depth,Width = Width,
                As2=Asz,As3=Asy,
                I22=Izz,I33=Iyy,I23=0,J=Ixx,
                unit_of_sec='mm',
                notes = self.name+"_main_girder_section")
        else:
            logger.error("Plan is not valid.")
            return None
        if self.Plan in ['方案一','方案二']:
            self.girder_section.define()
            # do not consider mass and weight of girder automatically
            self.girder_section.ignore_mass_effect()
            return self.girder_section
        if self.Plan == '方案三':
            self.girder_section_middle_span.define()
            self.girder_section_middle_span.ignore_mass_effect()
            
            self.girder_section_pier.define()
            self.girder_section_pier.ignore_mass_effect()
            
            return [self.girder_section_pier,self.girder_section_middle_span]

    def generate_girder_points(self):
        if not hasattr(self, 'girder_points'):
            self.girder_points = {}
            self.girder_bearing_top_points = {}
            for pier in self.pierlist:
                self.girder_points[pier.name] = {}
                self.girder_bearing_top_points[pier.name] = {}

        if len(self.pierlist) == 1:
            logger.opt(colors=True).warning(f"Only one pier in the list, Assuming Concentrated Mass of default {self.DefaultSpan}m span !")
            pier = self.pierlist[0]
            self.__generate_concentrated_girder_points(pier,side='both')
            return
        for pier_start,pier_end in zip(self.pierlist[0:-1],self.pierlist[1:]):
            self.__generate_girder_points(pier_start,pier_end, side = 'both')
    
    def __generate_concentrated_girder_points(self,pier,side = Literal['left','right','both']):
        gidername = f"{pier.name}_{pier.name}"
        if gidername not in self.girder_points.keys():
            self.girder_points[gidername] = {}
            
        if side == 'left':
            y =  pier.Distance_between_piers/2   
        elif side == 'right':
            y = - pier.Distance_between_piers/2
        elif side == 'both':
            self.__generate_concentrated_girder_points(pier,'left')
            self.__generate_concentrated_girder_points(pier,'right')
            return
            
        def calc_y_bearing(y,pier):
            if y>0:
                y_outer = y + pier.Distance_between_bearings/2
                y_inner = y - pier.Distance_between_bearings/2
            else:
                y_outer = y - pier.Distance_between_bearings/2
                y_inner = y + pier.Distance_between_bearings/2
            return y_outer,y_inner
        
        x = pier.station
        z = pier.Height_of_pier_bottom + pier.Height_of_pier + self.Thickness_of_bearing + self.Height_of_girder
        self.girder_points[pier.name][side] = SapPoint(x, y, z, f"{self.name}_{pier.name}_{side}_girder_point")
        self.girder_points[pier.name][side].add()
        y_outer,y_inner = calc_y_bearing(y,pier)
        self.girder_bearing_top_points[pier.name][side] = {
            'inner':SapPoint(x, y_inner, z - self.Height_of_girder, f"{self.name}_{pier.name}_{side}_BearingTop_inner"),
            'outer':SapPoint(x, y_outer, z - self.Height_of_girder, f"{self.name}_{pier.name}_{side}_BearingTop_outer")}
        for point in self.girder_bearing_top_points[pier.name][side].values():
            point.add()
 
        self.girder_points[gidername][side] = self.girder_points[pier.name][side]
      
    def __generate_girder_points(self,pier_start,pier_end,side = Literal['left','right','both']):
        num = self.num_of_ele_foreach_girder
        gidername = f"{pier_start.name}_{pier_end.name}"
        if gidername not in self.girder_points.keys():
            self.girder_points[gidername] = {}
            
        if side == 'left':
            y_start =  pier_start.Distance_between_piers/2   
            y_end =  pier_end.Distance_between_piers/2  
        elif side == 'right':
            pier_start,pier_end = pier_end,pier_start
            y_start = - pier_start.Distance_between_piers/2
            y_end = - pier_end.Distance_between_piers/2
        elif side == 'both':
            self.__generate_girder_points(pier_start,pier_end,'left')
            self.__generate_girder_points(pier_start,pier_end,'right')
            return
        
        def calc_y_bearing(y,pier):
            if y>0:
                y_outer = y + pier.Distance_between_bearings/2
                y_inner = y - pier.Distance_between_bearings/2
            else:
                y_outer = y - pier.Distance_between_bearings/2
                y_inner = y + pier.Distance_between_bearings/2
            return y_outer,y_inner
        
            
        points = []
        if pier_start.is_intermediate_pier:
            x_start = pier_start.station + pier_start.offset * (1 if side =='left' else -1)
        else:
            x_start = pier_start.station
            
        if pier_end.is_intermediate_pier:
            x_end = pier_end.station - pier_end.offset * (1 if side =='left' else -1)
        else:
            x_end = pier_end.station
            
        for i in range(1,num):
            x = x_start + (x_end - x_start) * i / num
            y = y_start + (y_end - y_start) * i / num
            h_start = pier_start.Height_of_pier_bottom + pier_start.Height_of_pier + self.Thickness_of_bearing + self.Height_of_girder
            h_end = pier_end.Height_of_pier_bottom + pier_end.Height_of_pier + self.Thickness_of_bearing + self.Height_of_girder
            z = h_start + (h_end - h_start) * i / num
            
            if i==1:
                self.girder_points[pier_start.name][side] = SapPoint(x_start, y, h_start, f"{self.name}_{pier_start.name}_{side}_girder_point")
                points.append(self.girder_points[pier_start.name][side])
                
                y_outer,y_inner = calc_y_bearing(y_start,pier_start)
                self.girder_bearing_top_points[pier_start.name][side] = {
                    'inner':SapPoint(x_start, y_inner, h_start - self.Height_of_girder, f"{self.name}_{pier_start.name}_{side}_BearingTop_inner"),
                    'outer':SapPoint(x_start, y_outer, h_start - self.Height_of_girder, f"{self.name}_{pier_start.name}_{side}_BearingTop_outer")}
                for point in self.girder_bearing_top_points[pier_start.name][side].values():
                    point.add()
            
            points.append(SapPoint(x, y, z, f"{gidername}_girder_{side}_{i}"))
            
            if i==num-1:
                self.girder_points[pier_end.name][side] = SapPoint(x_end, y, h_end, f"{self.name}_{pier_end.name}_{side}_girder_point")
                points.append(self.girder_points[pier_end.name][side])
                
                y_outer,y_inner = calc_y_bearing(y_end,pier_end)
                self.girder_bearing_top_points[pier_end.name][side] = {
                    'inner':SapPoint(x_end, y_inner, h_end - self.Height_of_girder, f"{self.name}_{pier_end.name}_{side}_BearingTop_inner"),
                    'outer':SapPoint(x_end, y_outer, h_end - self.Height_of_girder, f"{self.name}_{pier_end.name}_{side}_BearingTop_outer")}
                for point in self.girder_bearing_top_points[pier_end.name][side].values():
                    point.add()
            

        for point in points:
            point.add()    
        self.girder_points[gidername][side] = points
    