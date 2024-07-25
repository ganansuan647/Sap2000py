import ezdxf
from shapely.geometry import Polygon
import numpy as np
import math

class DXF2Polygons:
    """
    read dxf file and extract polygons, output unit is meter
    """
    def __init__(self, file_path, unit_of_dxf='m', show_log=False):
        if show_log:
            from loguru import logger
            self.log = True
            self.logger = logger.bind(name='DXF2Polygons')
        else:
            self.log = False
        self.file_path = file_path
        self.unit_of_dxf = unit_of_dxf
        # 提取封闭图形(提取后单位为m)
        self.polygons = self.get_polygons_from_dxf(file_path, unit_of_dxf)
        # 分类外侧边界和内侧边界
        outer_boundaries, inner_boundaries = self.classify_polygons(self.polygons)
        self.outer_boundaries = outer_boundaries
        self.inner_boundaries = inner_boundaries
        # 合并外边界和内边界的几何性质
        if len(outer_boundaries) == 1:
            if self.log:
                self.logger.success(f'合并后的几何属性（几何单位：m）:{self.combine_geometric_properties}')
        else:
            if self.log:
                self.logger.warning('发现多个外侧边界，无法合并几何属性')

    def plot(self):
        import matplotlib.pyplot as plt
        import geopandas as gpd
        p = gpd.GeoSeries(self.combined_polygon)
        p.plot()
        plt.show()    

    def get_geometry_from_entity(self,entity):
        """从实体中获取几何信息"""
        if entity.dxftype() == 'LWPOLYLINE' or entity.dxftype() == 'POLYLINE':
            points = []
            if entity.dxftype() == 'LWPOLYLINE':
                # explode() 方法将多段线分解为基本图元
                for sub_entity in entity.explode():
                    if sub_entity.dxftype() == 'LINE':
                        start_point = (sub_entity.dxf.start.x, sub_entity.dxf.start.y)
                        end_point = (sub_entity.dxf.end.x, sub_entity.dxf.end.y)
                        # 去重添加(距离小于0.1mm的点认为是同一个点)
                        if len(points) == 0 or np.linalg.norm(np.array(points[-1]) - np.array(start_point)) > 0.01:
                            points.append(start_point)
                        if np.linalg.norm(np.array(start_point) - np.array(end_point)) > 0.01:
                            points.append(end_point)
                    elif sub_entity.dxftype() == 'ARC':
                        center = (sub_entity.dxf.center.x, sub_entity.dxf.center.y)
                        radius = sub_entity.dxf.radius
                        start_angle = math.radians(sub_entity.dxf.start_angle)
                        end_angle = math.radians(sub_entity.dxf.end_angle)
                        arc_points = self.arc_to_points(center, radius, start_angle, end_angle)
                        for arc_point in arc_points:
                            if len(points) == 0 or np.linalg.norm(np.array(points[-1]) - np.array(arc_point)) > 0.01:
                                points.append(arc_point)
            else:  # POLYLINE
                for vertex in entity.vertices:
                    x, y = vertex.dxf.location.x, vertex.dxf.location.y
                    points.append((x, y))
            return points
        elif entity.dxftype() == 'LINE':
            start_point = (entity.dxf.start.x, entity.dxf.start.y)
            end_point = (entity.dxf.end.x, entity.dxf.end.y)
            return []
        else:
            self.logger.warning(f"Unsupported entity type: {entity.dxftype()}. Ignored!")
            return []
            # raise ValueError(f"Unsupported entity type: {entity.dxftype()}")
        
    def arc_to_points(self,center, radius, start_angle, end_angle, num_points=40):
        """将ARC转换为一系列点"""
        cx, cy = center
        if start_angle > end_angle:
            end_angle += 2 * math.pi

        angle_range = end_angle - start_angle
        points = [
            (
                cx + radius * math.cos(start_angle + angle_range * (i / num_points)),
                cy + radius * math.sin(start_angle + angle_range * (i / num_points))
            )
            for i in range(num_points + 1)
        ]
        return points
        
    def calculate_bulge(self,start_point, end_point, radius):
        """计算弧的凸度"""
        x1, y1 = start_point
        x2, y2 = end_point
        chord_length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        sagitta = radius - math.sqrt(radius ** 2 - (chord_length / 2) ** 2)
        return sagitta * 2 / chord_length

    def bulge_to_arc(self,start_point, bulge, prev_point=None, points=None, index=None):
        """将 bulge 转换为圆弧点集"""
        arc_points = []
        if prev_point is None:
            arc_points.append(start_point)
        else:
            # Calculate arc center and radius
            x1, y1 = prev_point
            x2, y2 = start_point
            angle = 4 * np.arctan(bulge)
            chord_length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            radius = chord_length / (2 * np.sin(angle / 2))

            # Calculate start and end angles
            start_angle = np.arctan2(y1 - y2, x1 - x2)
            end_angle = start_angle + angle

            # Calculate number of points on the arc
            num_points = int(np.ceil(np.abs(angle) / (np.pi / 180)))

            # Generate arc points
            for i in range(num_points + 1):
                theta = start_angle + (i / num_points) * (end_angle - start_angle)
                x = x2 + radius * np.cos(theta)
                y = y2 + radius * np.sin(theta)
                arc_points.append((x, y))

        return arc_points

    def get_polygons_from_dxf(self,file_path, unit_of_dxf='m'):
        """从 DXF 文件中提取封闭的多边形图形"""
        doc = ezdxf.readfile(file_path)
        msp = doc.modelspace()

        polygons = []
        entities = list(msp)  # 复制所有实体到一个列表中,以免炸开后msp发生变化
        for entity in entities:
            points = self.get_geometry_from_entity(entity)
            if len(points) == 0:
                continue
            # Convert unit to m
            if unit_of_dxf == 'cm':
                points = [(x / 100, y / 100) for x, y in points]
            elif unit_of_dxf == 'mm':
                points = [(x / 1000, y / 1000) for x, y in points]
            elif unit_of_dxf == 'm':
                pass
            else:
                raise ValueError(f"Unsupported unit of dxf: {unit_of_dxf}")
            
            
            if points:
                # 去除重复点
                unique_points = [points[i] for i in range(len(points)) if i == 0 or points[i] != points[i-1]]
                polygon = Polygon(unique_points)
                if polygon.is_valid:
                    polygons.append(polygon)
                    if self.log:
                        self.logger.trace(f"Found a polygon with {len(unique_points)} points")
                else:
                    if self.log:
                        self.logger.warning(f"Found an invalid polygon with {len(unique_points)} points\nInvalid points: {unique_points}")
        return polygons

    def classify_polygons(self,polygons):
        """分类外侧边界和内侧边界"""
        outer_boundaries = []
        inner_boundaries = []

        for polygon in polygons:
            is_inner = False
            for other_polygon in polygons:
                if polygon != other_polygon and polygon.within(other_polygon):
                    inner_boundaries.append(polygon)
                    is_inner = True
                    break
            if not is_inner:
                outer_boundaries.append(polygon)
        
        if self.log:
            self.logger.info(f"Found {len(outer_boundaries)} outer boundaries and {len(inner_boundaries)} inner boundaries")

        return outer_boundaries, inner_boundaries

    def calculate_geometric_properties(self,polygon):
        """计算几何属性：面积，特征尺寸，惯性矩和惯性积"""
        area = polygon.area
        bounds = polygon.bounds  # (minx, miny, maxx, maxy)
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]

        cx, cy = polygon.centroid.x, polygon.centroid.y

        Ixx = 0
        Iyy = 0
        Ixy = 0

        coords = list(polygon.exterior.coords)
        for i in range(len(coords) - 1):
            x0, y0 = coords[i]
            x1, y1 = coords[i + 1]
            a = x0 * y1 - x1 * y0
            Ixx += (y0**2 + y0 * y1 + y1**2) * a
            Iyy += (x0**2 + x0 * x1 + x1**2) * a
            Ixy += (x0 * y1 + 2 * x0 * y0 + 2 * x1 * y1 + x1 * y0) * a

        Ixx = abs(Ixx) / 12
        Iyy = abs(Iyy) / 12
        Ixy = abs(Ixy) / 24

        J = Ixx + Iyy  # 转动惯量

        # 计算剪切面积
        Asx = area / (1 + (Ixx / (area * (height / 2)**2)))
        Asy = area / (1 + (Iyy / (area * (width / 2)**2)))

        properties = {
            'area': area,
            'width': width,
            'height': height,
            'centroid': (cx, cy),
            'Ixx': Ixx, # I33
            'Iyy': Iyy, # I22
            'Ixy': Ixy,  # 惯性积I23
            'J': J,  # 转动惯量
            'Asx': Asx,  # 剪切面积 As3
            'Asy': Asy  # 剪切面积 As2
        }
        
        return properties

    @property
    def combine_geometric_properties(self):
        """合并外边界和内边界的几何性质"""
        return self.calculate_geometric_properties(self.combined_polygon)
    
    @property
    def combined_polygon(self):
        return Polygon(self.outer_polygon.exterior.coords, [inner.exterior.coords for inner in self.inner_polygons])
    
    @property
    def outer_polygon(self):
        return self.outer_boundaries[0]
    
    @property
    def outer_geometric_properties(self):
        """外边界的几何性质"""
        return self.calculate_geometric_properties(self.outer_polygon)

    @property
    def inner_polygons(self):
        return self.inner_boundaries

if __name__ == '__main__':
    # 示例文件路径
    # dxf_file_path = r'Test\TongZhouSha_H_above_50.dxf'
    # unit_of_dxf = 'cm'
    # show_log = True
    # H50section = DXF2Polygons(dxf_file_path, unit_of_dxf, show_log)
    # H50section.plot()
    dxf_file_path = r'Test\TongZhouSha_Main_Girder_1.dxf'
    unit_of_dxf = 'cm'
    show_log = True
    mainsec = DXF2Polygons(dxf_file_path, unit_of_dxf, show_log)
    mainsec.plot()
