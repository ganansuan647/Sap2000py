from Sap2000py.Saproject import Saproject
from loguru import logger
from pathlib import Path
# from Sap2000py.Scripts.Build_Continuous_Bridge import Sap_Double_Box_Pier, Sap_Box_Girder, SapPoint, SapBase_6Spring, Section_General, DXF2Polygons
from dataclasses import dataclass
from loguru import logger
from shapely import Polygon
from sectionproperties.pre import Geometry
from sectionproperties.analysis import Section
from typing import Literal
from itertools import chain
import numpy as np
import math

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
    I23: float = 0
    J: float = 1e10 # torsion constant,默认给大值
    geom: Geometry = None
    sec: Section = None
    unit_of_sec:Literal['mm','cm','m'] = 'm'
    notes: str = ""
    
    @property
    def t3(self):
        return self.Depth
    
    @property
    def t2(self):
        return self.Width

    def define(self):
        if self.unit_of_sec == 'mm':
            Sap.setUnits("KN_mm_C")
        elif self.unit_of_sec == 'cm':
            Sap.setUnits("KN_cm_C")
        elif self.unit_of_sec == 'm':
            Sap.setUnits("KN_m_C")
        ret = Sap.Define.section.PropFrame_SetGeneral(self.name, self.material, self.t3, self.t2, self.Area, self.As2, self.As3, self.I22, self.I33, self.J, notes=self.notes)
        if ret == 0:
            logger.opt(colors=True).success(f"Section <yellow>{self.name}</yellow> added!")
        Sap.setUnits("KN_m_C")
        return ret
    
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
class SapPoint(Saproject):
    x: float
    y: float
    z: float
    name: str = ""
    mass: float = 0.0
    
    def add(self):
        ret = Saproject().Assign.PointObj.AddCartesian(self.x, self.y, self.z, UserName=self.name)
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

    def exists(self):
        return Sap.Assign.PointObj.Get.CoordCartesian(self.name)[-1] == 0

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
    Height_of_cap: float = None
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
        Sap.RefreshView()
        
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
        ret = Sap._Model.PropFrame.SetRectangle(self.name+"_Cap", "C30", width, depth)
        if ret == 0:
            logger.success(f"Cap section {self.name}_Cap added!")
        self.cap_section = self.name+"_Cap"
        return self.cap_section
    
    def __add_body_constraints_for_points(self,constraint_name:str, points : list):
        for point in points:
            if not point.exists():
                logger.opt(colors=True).warning(f"<yellow>{point.name}</yellow> Accidentally does not exist!")
                point.add()
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

@dataclass
class Sap_Bearing_Linear:
    name: str
    start_point: SapPoint
    end_point: SapPoint
    link_name: str
    
    def __post_init__(self):
        self.add()
        
    def add(self):
        ret = Sap.Assign.Link.AddByPoint(self.start_point.name, self.end_point.name, IsSingleJoint=False, PropName = self.link_name, UserName=self.name)
        if ret[1] == 0:
            logger.opt(colors=True).success(f"Link <yellow>{self.name}</yellow> Added!")
        else:
            logger.opt(colors=True).error(f"Link <yellow>{self.name}</yellow> Failed to Add!")
    
@dataclass
class Sap_Box_Girder:
    name: str
    pierlist: list
    fixedpier: list
    num_of_ele_foreach_girder: int = 6
    Thickness_of_bearing: float = 0.3
    Height_of_girder: float = 2.678
    Plan:Literal['方案一','方案二','方案三'] = '方案一'
    
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
        self.generate_girder_elements()
        self.add_body_constraint()
        self.add_bearing_links()
        Sap.RefreshView()
    
    def __define_links(self):
        # 刚度取大值，不直接固定,暂时不考虑阻尼
        # U1为竖向，U2为纵桥向，U3为横桥向
        FixedDOF = []
        # dampingCe = {}
        # 固定支座:
        DOF = ['U1', 'U2', 'U3']
        uncoupleKe = {"U1":1e10,"U2":1e10,"U3":1e10}
        fixed_link = "Fixed"
        Sap.Define.section.PropLink.SetLinear(fixed_link, DOF=DOF, Fixed=FixedDOF, Ke=uncoupleKe)
        # 横桥向（y）滑动支座
        DOF = ['U1', 'U2']
        uncoupleKe = {"U1":1e10,"U2":1e10}
        y_sliding_link = "y_sliding"
        Sap.Define.section.PropLink.SetLinear(y_sliding_link, DOF=DOF, Fixed=FixedDOF, Ke=uncoupleKe)
        # 纵桥向（x）滑动支座
        DOF = ['U1', 'U3']
        uncoupleKe = {"U1":1e10,"U3":1e10}
        x_sliding_link = "x_sliding"
        Sap.Define.section.PropLink.SetLinear(x_sliding_link, DOF=DOF, Fixed=FixedDOF, Ke=uncoupleKe)
        # 双向滑动支座
        DOF = ['U1']
        uncoupleKe = {"U1":1e10}
        both_sliding_link = "Both_sliding"
        Sap.Define.section.PropLink.SetLinear(both_sliding_link, DOF=DOF, Fixed=FixedDOF, Ke=uncoupleKe)
        return fixed_link, y_sliding_link, x_sliding_link, both_sliding_link
    
    def add_bearing_links(self):
        fixed_link, y_sliding_link, x_sliding_link, both_sliding_link = self.__define_links()
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
                if type(pier.bearing_bottom_point_inner[side]) == list:
                    inner_bearing_bottom = [p for p in pier.bearing_bottom_point_inner[side] if p.x == inner_bearing_top.x][0]
                else:
                    inner_bearing_bottom = pier.bearing_bottom_point_inner[side]

                link_inner = Sap_Bearing_Linear(f"{pier.name}_{side}_inner_Bearing", inner_bearing_bottom, inner_bearing_top, inner_link)
                
                outer_bearing_top = self.girder_bearing_top_points[pier.name][side]['outer']
                if type(pier.bearing_bottom_point_outer[side]) == list:
                    outer_bearing_bottom = [p for p in pier.bearing_bottom_point_outer[side] if p.x == inner_bearing_top.x][0]
                else:
                    outer_bearing_bottom = pier.bearing_bottom_point_outer[side]
                link_outer = Sap_Bearing_Linear(f"{pier.name}_{side}_outer_Bearing", outer_bearing_bottom, outer_bearing_top, outer_link)
                
                self.bearings[pier.name][side] = {'inner':link_inner, 'outer':link_outer}
        
    def __add_body_constraints_for_points(self,constraint_name:str, points : list):
        for point in points:
            if not point.exists():
                logger.opt(colors=True).warning(f"<yellow>{point.name}</yellow> Accidentally does not exist!")
                point.add()
            ret = Sap.Assign.PointObj.Set.Constraint(point.name,constraint_name,ItemType = 0)
            if ret[1] == 0:
                logger.opt(colors=True).success(f"<yellow>{point.name}</yellow> added to Body constraint : <yellow>{constraint_name}</yellow>")
            else:
                logger.opt(colors=True).error(f"<yellow>{point.name}</yellow> failed to add to Body constraint : <yellow>{constraint_name}</yellow>")
        
    def add_body_constraint(self):
        body_dof = ["UX", "UY", "UZ", "RX", "RY", "RZ"]
        flatten = lambda l: list(chain.from_iterable(map(lambda x: flatten(x) if isinstance(x, list) else [x], l)))
        for side in ['left','right']:
            for pier in self.pierlist:
                Sap.Define.jointConstraints.SetBody(f"{pier.name}_{side}_Girder", body_dof)
                girder_point = self.girder_points[pier.name][side]
                bearing_top_points = list(self.girder_bearing_top_points[pier.name][side].values())
                self.__add_body_constraints_for_points(pier.name+"_"+side+"_girder", flatten([girder_point,bearing_top_points]))
                
    def generate_girder_elements(self):
        for pier_start,pier_end in zip(self.pierlist[0:-1],self.pierlist[1:]):
            self.__generate_girder_elements(pier_start,pier_end, side = 'both')
            
    def __generate_girder_elements(self,pier_start,pier_end,side = Literal['left','right','both']):
        num = self.num_of_ele_foreach_girder
        
        if side == 'both':
            self.__generate_girder_elements(pier_start,pier_end,'left')
            self.__generate_girder_elements(pier_start,pier_end,'right')
            return
        
        gidername = f"{pier_start.name}_{pier_end.name}"
        points_to_connect = self.girder_points[gidername][side]
        i = 1
        for point1,point2 in zip(points_to_connect[0:-1],points_to_connect[1:]):
            ret = Sap.Assign.FrameObj.AddByPoint(point1.name, point2.name, propName = self.girder_section.name, userName = f"{gidername}_{side}_girder_{i}")
            if ret[1] == 0:
                logger.opt(colors=True).success(f"Girder element <yellow>{gidername}_{side}_girder_{i}</yellow> added!")
            else:
                logger.opt(colors=True).error(f"Girder element <yellow>{gidername}_{side}_girder_{i}</yellow> failed to add!")
            
            # add line mass manually instead(一期+二期恒载)
            ret = Sap.Assign.FrameObj.Set.Mass(f"{gidername}_{side}_girder_{i}",(self.q1+self.q2)/9.81,Replace=True)
            if ret == 0:
                logger.opt(colors=True).success(f"Girder element <yellow>{gidername}_{side}_girder_{i}</yellow> mass set!")
            else:
                logger.opt(colors=True).error(f"Girder element <yellow>{gidername}_{side}_girder_{i}</yellow> mass failed to set!")
            i += 1
    
    def get_girder_section(self):
        unit_of_sec = 'mm'
        if self.Plan == '方案一':
            # 方案一:等截面钢箱梁(mm)
            Area = 855043.2 
            Asx,Asy = 476380.0,79827.2 
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
                As2=Asy,As3=Asx,
                I22=Iyy,I33=Ixx,I23=0,J=Izz,
                unit_of_sec='mm',
                notes = self.name+"_main_girder_section")
        elif self.Plan == '方案二':
            # 方案二:等截面组合梁
            Area = 1364813.0 
            Asx,Asy = 1038166.0,127892.0 
            Ixx,Iyy,Izz = 6.82E+12,3.52E+12,3.98E+13
            # 20.105m x 4.5m
            Depth,Width = 4500, 20105
            # 一期恒载和二期恒载kN/m
            q1 = 246.9
            q2 = 56.0
            raise NotImplementedError
        elif self.Plan == '方案三':
            # 方案三:变截面连续梁
            # 分跨中和中墩截面
            raise NotImplementedError
        else:
            logger.error("Plan is not valid.")
            return None
        self.girder_section.define()
            
        # do not consider mass and weight of girder automatically
        ret = Sap._Model.PropFrame.SetModifiers(self.girder_section.name,[1,1,1,1,1,1,0,0])
        if ret[1] == 0:
            logger.opt(colors=True).success(f"Girder element <yellow>{self.girder_section.name}</yellow> modifiers set!")
        else:
            logger.opt(colors=True).error(f"Girder element <yellow>{self.girder_section.name}</yellow> modifiers failed to set!")
        return self.girder_section

    def generate_girder_points(self):
        if not hasattr(self, 'girder_points'):
            self.girder_points = {}
            self.girder_bearing_top_points = {}
            for pier in self.pierlist:
                self.girder_points[pier.name] = {}
                self.girder_bearing_top_points[pier.name] = {}

        for pier_start,pier_end in zip(self.pierlist[0:-1],self.pierlist[1:]):
            self.__generate_girder_points(pier_start,pier_end, side = 'both')
                
    def __generate_girder_points(self,pier_start,pier_end,side = Literal['left','right','both']):
        num = self.num_of_ele_foreach_girder
        gidername = f"{pier_start.name}_{pier_end.name}"
        if not gidername in self.girder_points.keys():
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
    
#full path to the model
ModelPath = Path('.\Test\TongZhouShaLow.sdb')
# ModelPath = Path('.\Test\TongZhouShaLow.sdb')

# Create a Sap2000py obj (default: attatch to instance and create if not exist)
Sap = Saproject()

# Change Sap api settings if you want
# Sap.createSap(AttachToInstance = True,SpecifyPath = False,ProgramPath = "your sap2000 path")

# Open Sap2000program
Sap.openSap()

# Open Sap2000 sdb file (create if not exist, default: CurrentPath\\NewSapProj.sdb)
# Sap.File.Open(ModelPath)

Sap.File.New_Blank()
# And print the project information
Sap.getProjectInfo()

# Set Units to KN_m_C
Sap.setUnits("KN_m_C")

# Add China Common Material Set·
Sap.Scripts.AddCommonMaterialSet(standard = "JTG")

pier1 = Sap_Double_Box_Pier(
    name="#1",
    station=0,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=29.3,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = True,
    offset = 1.0
)

pier2 = Sap_Double_Box_Pier(
    name="#2",
    station=90,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=29.3,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = False,
)

pier3 = Sap_Double_Box_Pier(
    name="#3",
    station=180,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=29.3,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = False,
)

pier4 = Sap_Double_Box_Pier(
    name="#4",
    station=270,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=29.3,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = False,
)

pier5 = Sap_Double_Box_Pier(
    name="#5",
    station=360,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=29.3,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = False,
)

pier6 = Sap_Double_Box_Pier(
    name="#6",
    station=450,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=29.3,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = True,
    offset=1.0
)

pier7 = Sap_Double_Box_Pier(
    name="#7",
    station=540,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=29.3,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = False,
)

pier8 = Sap_Double_Box_Pier(
    name="#8",
    station=630,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=29.3,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = False,
)

pier9 = Sap_Double_Box_Pier(
    name="#9",
    station=720,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=29.3,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = False,
)

pier10 = Sap_Double_Box_Pier(
    name="#10",
    station=810,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=29.3,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = False,
)

pier11 = Sap_Double_Box_Pier(
    name="#11",
    station=900,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=29.3,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = True,
    offset=1.0
)

pier12 = Sap_Double_Box_Pier(
    name="#12",
    station=990,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=29.3,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = False,
)

pier13 = Sap_Double_Box_Pier(
    name="#13",
    station=1080,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=29.3,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = False,
)

pier14 = Sap_Double_Box_Pier(
    name="#14",
    station=1170,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=29.3,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = False,
)

pier15 = Sap_Double_Box_Pier(
    name="#15",
    station=1260,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=29.3,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = False,
)

pier16 = Sap_Double_Box_Pier(
    name="#16",
    station=1350,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=29.3,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = True,
    offset=1.0
)

girderleft = Sap_Box_Girder(
    name = "SpanLeft",
    pierlist=[pier1,pier2,pier3,pier4,pier5,pier6],
    fixedpier = [pier3,pier4],
    Plan = '方案一')
        
girdermain = Sap_Box_Girder(
    name = "SpanMain",
    pierlist=[pier6,pier7,pier8,pier9,pier10,pier11],
    fixedpier = [pier8,pier9],
    Plan = '方案一')

girderright = Sap_Box_Girder(
    name = "SpanRight",
    pierlist=[pier11,pier12,pier13,pier14,pier15,pier16],
    fixedpier = [pier13,pier14],
    Plan = '方案一')
    
    
Sap.RefreshView()

base_names = [pier.base.point.name for pier in girdermain.pierlist]
Sap.Scripts.Group.AddtoGroup('Base',base_names,type='Point')

pier_bottom_names = [pier.name+"_left_bottom2hollowBottom" for pier in girdermain.pierlist]
Sap.Scripts.Group.AddtoGroup('PierBottom',pier_bottom_names,type='Frame')

pier_hollow_bottom_names = [pier.name+"_left_hollow_1" for pier in girdermain.pierlist]
Sap.Scripts.Group.AddtoGroup('PierHollowBottom',pier_hollow_bottom_names,type='Frame')

bearing_names = [girdermain.bearings[pier.name]['left']['inner'].name for pier in girdermain.pierlist]
Sap.Scripts.Group.AddtoGroup('Bearing',bearing_names,type='Link')

# set modal analysis
Sap.Define.loadcases.ModalEigen.SetLoads('MODAL',NumberLoads=3,LoadType=['Accel','Accel','Accel'],LoadName=['UX','UY','UZ'])
Sap.Define.loadcases.ModalEigen.SetNumberModes('MODAL',MaxModes=500)
# Remove all cases for analysis
Sap.Scripts.Analyze.RemoveCases("All")
# Select cases for analysis
Sap.Scripts.Analyze.AddCases(CaseName = ['DEAD', 'MODAL'])
# must save the model before running analysis!
Sap.File.Save(ModelPath)
Sap.Analyze.RunAnalysis()
# Get Modal results
PartiMassRatios = Sap.Results.Modal.ParticipatingMassRatios()
periods = PartiMassRatios[4]
# print Modal results(20 modes)
from rich.console import Console
from rich.table import Table
# setup table
table = Table(title="Modal Information Comparison", show_header=True, header_style="bold magenta")
table.add_column("Mode", justify="left", style="cyan", no_wrap=True)
table.add_column("Period", justify="right", style="green")
table.add_column("SumUx", justify="right", style="green")
table.add_column("SumUy", justify="right", style="green")
table.add_column("SumUz", justify="right", style="green")
count = 0
for i in range(PartiMassRatios[0]):
    # add data to the table (only when any of mass ratio in Ux, Uy, Uz is greater than 0.01)
    if any(np.array([PartiMassRatios[5][i],PartiMassRatios[6][i],PartiMassRatios[7][i]])>0.01):
        table.add_row(
            f"{i+1:02d}",
            f"{PartiMassRatios[4][i]:.2f}",
            f"{PartiMassRatios[8][i]:.2f}",
            f"{PartiMassRatios[9][i]:.2f}",
            f"{PartiMassRatios[10][i]:.2f}",
        )
        count+=1
    if count >= 50:
        break
    
# Rayleigh damping period 1: get the periods with mass ratio greater than 0.1
period_x_1 = [periods[i] for i in range(len(periods)) if PartiMassRatios[5][i]>0.1][0]
period_y_1 = [periods[i] for i in range(len(periods)) if PartiMassRatios[6][i]>0.1][0]
period_z_1 = [periods[i] for i in range(len(periods)) if PartiMassRatios[7][i]>0.1][0]
# Rayleigh damping period 2: get the periods with sum mass ratio greater than 0.9
period_x_2 = [periods[i] for i in range(len(periods)) if PartiMassRatios[8][i]>0.9][0]
period_y_2 = [periods[i] for i in range(len(periods)) if PartiMassRatios[9][i]>0.9][0]
period_z_2 = [periods[i] for i in range(len(periods)) if PartiMassRatios[10][i]>0.9][0]

# print table
console = Console()
console.print(table)
# unlck the model to make more settings
ret = Sap._Model.SetModelIsLocked(False)

def get_spectrum_from_file(file_path:Path):
    times = []
    values = []
    with open(file_path, 'r') as file:
        # Skip the header line
        next(file)
        for line in file:
            time, value = line.strip().split()
            times.append(float(time))
            values.append(float(value))
    return times,values

def get_time_history_from_file(file_path:Path,dt:float):
    time = 0.0
    times = []
    values = []
    with open(file_path, 'r') as file:
        # Skip the header line
        for line in file:
            value = line.strip().split()[0]
            times.append(float(time))
            values.append(float(value))
            time+=dt
    return times,values

spectrum_path = Path('./Test/converted_spectrum.txt')
times,values = get_spectrum_from_file(spectrum_path)

# E2 Spectrum Function
Sap.Define.function.ResponseSpectrum.Set_User('E2Spectrum',times,values,0.05)   
# E2X Spectrum
Sap.Define.loadcases.ResponseSpectrum.SetCase("E2X")
Sap.Define.loadcases.ResponseSpectrum.SetDampConstant('E2X',0.05)
Sap.Define.loadcases.ResponseSpectrum.SetDirComb('E2X','SRSS')
Sap.Define.loadcases.ResponseSpectrum.SetLoads('E2X',NumberLoads=2,LoadName=['U1','U3'],Func=['E2Spectrum','E2Spectrum'],SF=[1,1*0.65])

# E2Y Spectrum
Sap.Define.loadcases.ResponseSpectrum.SetCase("E2Y")
Sap.Define.loadcases.ResponseSpectrum.SetDampConstant('E2Y',0.05)
Sap.Define.loadcases.ResponseSpectrum.SetDirComb('E2Y','SRSS')
Sap.Define.loadcases.ResponseSpectrum.SetLoads('E2Y',NumberLoads=2,LoadName=['U2','U3'],Func=['E2Spectrum','E2Spectrum'],SF=[1,1*0.65])

TH_names = []
time_history_folder_path = Path('./Test/waves')
TH_files = time_history_folder_path.glob('*.txt')
for file_path in TH_files:
    times,values = get_time_history_from_file(file_path,dt=0.02)
    time_history_name = 'E2'+file_path.stem.split('.')[0]
    TH_names.append(time_history_name)
    Sap.Define.function.TimeHistory.Set_User(time_history_name,times,values)
    # E2X Time History
    Sap.Define.loadcases.DirHistNonlinear.SetCase('E2X'+time_history_name)
    Sap.Define.loadcases.DirHistNonlinear.SetTimeIntegration('E2X'+time_history_name,'Newmark')
    Sap.Define.loadcases.DirHistNonlinear.SetLoads('E2X'+time_history_name,NumberLoads=2,LoadType=['Load','Accel'],LoadName=['DEAD','U1'],Func=["RAMPTH",time_history_name],SF=[1,1])
    Sap.Define.loadcases.DirHistNonlinear.SetDampProportional('E2X'+time_history_name,DampType='Period', Dampa=0, Dampb=0, Dampf1=period_x_1, Dampf2=period_x_2,Dampd1= 0.05,Dampd2= 0.05)  # Rayleigh damping at period f1/s and f2/s is set to 0.05
    # E2Y Time History
    Sap.Define.loadcases.DirHistNonlinear.SetCase('E2Y'+time_history_name)
    Sap.Define.loadcases.DirHistNonlinear.SetTimeIntegration('E2Y'+time_history_name,'Newmark')
    Sap.Define.loadcases.DirHistNonlinear.SetLoads('E2Y'+time_history_name,NumberLoads=2,LoadType=['Load','Accel'],LoadName=['DEAD','U2'],Func=["RAMPTH",time_history_name],SF=[1,1])
    Sap.Define.loadcases.DirHistNonlinear.SetDampProportional('E2Y'+time_history_name,DampType='Period', Dampa=0, Dampb=0, Dampf1=period_y_1, Dampf2=period_y_2,Dampd1= 0.05,Dampd2= 0.05)  # Rayleigh damping at period f1/s and f2/s is set to 0.05
    # E2Z Time History
    Sap.Define.loadcases.DirHistNonlinear.SetCase('E2Z'+time_history_name)
    Sap.Define.loadcases.DirHistNonlinear.SetTimeIntegration('E2Z'+time_history_name,'Newmark')
    Sap.Define.loadcases.DirHistNonlinear.SetLoads('E2Z'+time_history_name,NumberLoads=2,LoadType=['Load','Accel'],LoadName=['DEAD','U3'],Func=["RAMPTH",time_history_name],SF=[1,0.65])
    Sap.Define.loadcases.DirHistNonlinear.SetDampProportional('E2Z'+time_history_name,DampType='Period', Dampa=0, Dampb=0, Dampf1=period_z_1, Dampf2=period_z_2,Dampd1= 0.05,Dampd2= 0.05)  # Rayleigh damping at period f1/s and f2/s is set to 0.05
    
logger.opt(colors=True).success(f"Rayleigh damping Control Period of X direction is {period_x_1:.2f}s and {period_x_2:.2f}s")
logger.opt(colors=True).success(f"Rayleigh damping Control Period of Y direction is {period_y_1:.2f}s and {period_y_2:.2f}s")
logger.opt(colors=True).success(f"Rayleigh damping Control Period of Z direction is {period_z_1:.2f}s and {period_z_2:.2f}s")

Sap.Define.LoadCombo.Add('E2纵向', comboType = 'AbsAdd')
ret = [Sap.Define.LoadCombo.SetCaseList('E2纵向',CNameType="LoadCase",CName = 'E2X'+name, SF = 1/len(TH_names)) for name in TH_names]
if all([r[1] == 0 for r in ret]):
    logger.opt(colors=True).success(f"Load Combination E2纵向 has been successfully defined.")
else:
    logger.opt(colors=True).error(f"An error occurred while defining the Load Combination E2纵向.")

Sap.Define.LoadCombo.Add('E2横向', comboType = 'AbsAdd')
ret = [Sap.Define.LoadCombo.SetCaseList('E2横向',CNameType="LoadCase",CName = 'E2Y'+name, SF = 1/len(TH_names)) for name in TH_names]
if all([r[1] == 0 for r in ret]):
    logger.opt(colors=True).success(f"Load Combination E2横向 has been successfully defined.")
else:
    logger.opt(colors=True).error(f"An error occurred while defining the Load Combination E2横向.")

Sap.Define.LoadCombo.Add('E2竖向', comboType = 'AbsAdd')
ret = [Sap.Define.LoadCombo.SetCaseList('E2竖向',CNameType="LoadCase",CName = 'E2Z'+name, SF = 1/len(TH_names)) for name in TH_names]
if all([r[1] == 0 for r in ret]):
    logger.opt(colors=True).success(f"Load Combination E2竖向 has been successfully defined.")
else:
    logger.opt(colors=True).error(f"An error occurred while defining the Load Combination E2竖向.")
    
Sap.Define.LoadCombo.Add('E2纵向+竖向', comboType = 'SRSS')
Sap.Define.LoadCombo.SetCaseList('E2纵向+竖向',CNameType="LoadCase",CName = "E2纵向", SF = 1)
Sap.Define.LoadCombo.SetCaseList('E2纵向+竖向',CNameType="LoadCase",CName = "E2竖向", SF = 1)

Sap.Define.LoadCombo.Add('E2横向+竖向', comboType = 'SRSS')
Sap.Define.LoadCombo.SetCaseList('E2横向+竖向',CNameType="LoadCase",CName = "E2横向", SF = 1)
Sap.Define.LoadCombo.SetCaseList('E2横向+竖向',CNameType="LoadCase",CName = "E2竖向", SF = 1)


Sap.File.Save(ModelPath)

Sap.Analyze.RunAnalysis()

a=1
# Sap.closeSap()

# dzb=[]    
# # 批量生成时程函数
# for file_name in file_names:
#     # 从文件名中提取时程函数的名称
#     time_history_path_name, _ = os.path.splitext(file_name)#分离出带路径的文件名和扩展名
#     time_history_name = os.path.basename(time_history_path_name)#返回路径最后的最后一级文件名
#     dzb.append(time_history_name)
#     # 删除已定义的函数
#     SapObject.SapModel.Func.Delete(time_history_name)
#     # 定义时程函数的文件路径
#     time_history_file_path = os.path.join(e_folder_path, file_name)
#     # 使用SetFromFile方法从文件中设置时程函数
#     ret = SapModel.Func.FuncTH.SetFromFile(time_history_name, time_history_file_path, 0, 0, 1, 2, True)

#     if ret == 0:
#         # print(f"Time history function '{time_history_name}' has been successfully defined from the file {file_name}.")
#         pass
#     else:
#         print(f"An error occurred while defining the time history function from file {file_name}.")

