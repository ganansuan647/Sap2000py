import ezdxf
from shapely.geometry import Polygon,MultiPolygon,MultiPoint,Point
from shapely.ops import unary_union,triangulate
from shapely.validation import make_valid,explain_validity # 需要Shapely >= 1.8a3版本
from sectionproperties.pre import Geometry, CompoundGeometry
from sectionproperties.analysis import Section
import numpy as np
import math
import matplotlib.pyplot as plt
import geopandas as gpd
# from typing import Literial
from functools import total_ordering

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
        try:
            self.logger.success(f'Properities of Combined Sectiom(Unit:m):{self.combine_geometric_properties}')
        except Exception as e:
            if self.log:
                self.logger.error(f'Failed to calculate properties of Combined Section:{e}')
            else:
                print(f'Failed to calculate properties of Combined Section:{e}')

    def plot(self):
        if self.log:
            self.logger.info("Plotting the combined polygon...")
            
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
                arcs = []
                for point in entity:
                    if point.is_arc_segment:
                        arcs.append(point)
                print(arcs)
                # explode() 方法将多段线分解为基本图元
                for sub_entity in entity.explode():
                    if sub_entity.dxftype() == 'LINE':
                        start_point = (sub_entity.dxf.start.x, sub_entity.dxf.start.y)
                        end_point = (sub_entity.dxf.end.x, sub_entity.dxf.end.y)
                        if len(points)==1 and type(points[0])==list:
                            # 前一个元素是不知道方向的圆弧或直线
                            d_start_start = np.linalg.norm(np.array(start_point) - np.array(points[0][0]))
                            d_start_end = np.linalg.norm(np.array(start_point) - np.array(points[0][-1]))
                            d_end_start = np.linalg.norm(np.array(end_point) - np.array(points[0][0]))
                            d_end_end = np.linalg.norm(np.array(end_point) - np.array(points[0][-1]))
                            min_d = min(d_start_start,d_start_end,d_end_start,d_end_end)
                            if min_d == d_start_start:
                                #第一个元素反了，第二个直线是正的
                                points = points[0][::-1]
                                addflag = 'unreversed'
                            elif min_d == d_end_end:
                                #第一个元素正的，第二个直线是反的
                                points = points[0][:]
                                addflag = 'reversed'
                            elif min_d == d_start_end:
                                #两个都是正的
                                points = points[0][:]
                                addflag = 'unreversed'
                            elif min_d == d_end_start:
                                # 两个都是反的
                                points = points[0][::-1]
                                addflag = 'reversed'
                            else:
                                raise ValueError("Unknown situation")
                            if addflag == 'unreversed':
                                points2add = [start_point,end_point]
                            elif addflag == 'reversed':
                                points2add = [end_point,start_point]
                                
                            for point in points2add:
                                d = min(np.linalg.norm(np.array(point) - np.array(points), axis=1))
                                if d > 1e-4:
                                    points.append(point)
                            continue
                        # 添加直线
                        if len(points) == 0:
                            # 第一个元素，不知方向，直接加list
                            points.append([start_point,end_point])
                        else:
                            # 计算新点与之前所有点的距离
                            d_start = min(np.linalg.norm(points - np.array(start_point), axis=1))
                            d_end = min(np.linalg.norm(points - np.array(end_point), axis=1))
                            if d_start >1e-4:
                                points.append(start_point)
                            if d_end >1e-4:
                                points.append(end_point)
                    elif sub_entity.dxftype() == 'ARC':
                        center = (sub_entity.dxf.center.x, sub_entity.dxf.center.y)
                        radius = sub_entity.dxf.radius
                        start_angle = math.radians(sub_entity.dxf.start_angle)
                        end_angle = math.radians(sub_entity.dxf.end_angle)
                        arc_points = self.arc_to_points(center, radius, start_angle, end_angle)
                        if len(points)==1 and type(points[0])==list:
                            # 前一个元素是不知道方向的圆弧或直线
                            d_start_start = np.linalg.norm(np.array(arc_points[0]) - np.array(points[0][0]))
                            d_start_end = np.linalg.norm(np.array(arc_points[0]) - np.array(points[0][-1]))
                            d_end_start = np.linalg.norm(np.array(arc_points[-1]) - np.array(points[0][0]))
                            d_end_end = np.linalg.norm(np.array(arc_points[-1]) - np.array(points[0][-1]))
                            min_d = min(d_start_start,d_start_end,d_end_start,d_end_end)
                            if min_d == d_start_start:
                                #第一个元素反了，第二个弧是正的
                                points = points[0][::-1]
                                points.extend(arc_points)
                            elif min_d == d_end_end:
                                #第一个元素正的，第二个弧是反的
                                points = points[0][:]
                                points.extend(arc_points[::-1])
                            elif min_d == d_start_end:
                                #两个都是正的
                                points = points[0][:]
                                points.extend(arc_points)
                            elif min_d == d_end_start:
                                # 两个都是反的
                                points = points[0][::-1]
                                points.extend(arc_points[::-1])
                            else:
                                raise ValueError("Unknown situation")
                            continue
                        # 添加圆弧
                        d_start = np.linalg.norm(np.array(arc_points[0]) - np.array(points[-1]))
                        d_end = np.linalg.norm(np.array(arc_points[-1]) - np.array(points[-1]))
                        if d_end < d_start:
                            # 方向正了
                            arc_points = arc_points[::-1]
                        points.extend(arc_points)
                       
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
        
    def arc_to_points(self,center, radius, start_angle, end_angle, num_points=20):
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
        if points[0] == points[-1]:
            points.pop()
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
                if np.linalg.norm(np.array(points[0]) - np.array(points[-1])) < 1e-4:
                    unique_points = points[:-1]
                polygon = Polygon(unique_points)
                p = gpd.GeoSeries(polygon)
                p.plot()
                plt.show()
                if polygon.is_valid:
                    polygons.append(polygon)
                    if self.log:
                        self.logger.trace(f"Found a valid polygon with {len(unique_points)} points")
                else:
                    if self.log:
                        self.logger.opt(colors=True).warning(f"Found an invalid polygon! Detail: <yellow>{explain_validity(polygon)}</yellow>. Trying to fix it...")
                    try:
                        previous_point = None
                        # for point in unique_points:
                        #     fig, ax = plt.gcf(), plt.gca()  # 获取当前图形和轴
                        #     ax.plot(point[0], point[1], 'ro-')
                        #     if previous_point is not None:
                        #         ax.plot([previous_point[0], point[0]], [previous_point[1], point[1]], 'k--', lw=0.5)
                        #     plt.show()
                        valid_polygon = make_valid(polygon)
                        polygons.append(valid_polygon)
                        if self.log:
                            self.logger.success(f"Successfully fixed the invalid polygon with {len(unique_points)} points")
                        p = gpd.GeoSeries(valid_polygon)
                        p.plot()
                        plt.show()
                    except Exception as e:
                        if self.log:
                            self.logger.error(f"Failed to fix the invalid polygon! Detail: {e}. Ignored!")
                    
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

    # def calculate_geometric_properties(self,polygon:Literial[Polygon,MultiPolygon]):
    def calculate_geometric_properties(self,polygon):
        """计算几何属性：面积，特征尺寸，惯性矩和惯性积"""
        
        bounds = polygon.bounds  # (minx, miny, maxx, maxy)
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        
        if isinstance(polygon,MultiPolygon):

            geom = CompoundGeometry(polygon)
            geom.plot_geometry()
            geom.create_mesh(mesh_sizes=[polygon.area/10]) # 最大单元面积不大于多边形面积的1/100
        else:
            geom = Geometry(polygon)
            geom.create_mesh(mesh_sizes=[polygon.area/10]) # 最大单元面积不大于多边形面积的1/100
        sec = Section(geometry=geom)
        sec.plot_mesh(materials=False)

        Ixx = 0
        Iyy = 0
        Ixy = 0
        A = 0
        cx,cy = 0,0
        area = polygon.area
        cx_all, cy_all = polygon.centroid.x, polygon.centroid.y
        for triangle in triangles:
            dA,dcx,dcy,dIxx,dIyy,dIxy = calculate_triangle_properties(triangle,cx_all,cy_all)
            A += dA
            cx += dA/area*dcx
            cy += dA/area*dcy
            Ixx += dIxx
            Iyy += dIyy
            Ixy += dIxy
            
        # check if A,cx,cy match the polygon calculations
        if abs(A-area) > 1e-6 or abs(cx-cx_all) > 1e-6 or abs(cy-cy_all) > 1e-6:
            if self.log:
                self.logger.warning(f"Centroid and Area mismatch! Calculated: {A,cx,cy}, Polygon: {area,cx_all,cy_all}")
                self.logger.info(f"Using Shapely calculated values: {area,cx_all,cy_all}")
            else:
                print(f"Centroid and Area mismatch! Calculated: {A,cx,cy}, Polygon: {area,cx_all,cy_all}")
                print(f"Using Shapely calculated values: {area,cx_all,cy_all}")
            A = area
            cx = cx_all
            cy = cy_all     

        J = Ixx + Iyy  # 转动惯量

        # 计算剪切面积
        # Asx = A / (1 + (Ixx_c / (A * (height / 2)**2)))
        # Asy = A / (1 + (Iyy_c / (A * (width / 2)**2)))
        Asx = 0
        Asy = 0
        if self.log:
            self.logger.warning("Shear area calculation is not implemented yet!")
        # else:
        #     print("Shear area calculation is not implemented yet!")

        properties = {
            'area': A,
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

    # def calculate_geometric_properties(self,polygon, tolerance=0.01, max_iter=10):
    #     """计算几何属性：面积，特征尺寸，惯性矩和惯性积"""
        
    #     def compute_properties(points, dx, dy):
    #         A = dx * dy * len(points)  # 计算面积
    #         cx = np.mean(points[:, 0])
    #         cy = np.mean(points[:, 1])
    #         Ixx = np.sum(dy * dx * (points[:, 1] - cy)**2)
    #         Iyy = np.sum(dy * dx * (points[:, 0] - cx)**2)
    #         Ixy = np.sum(dy * dx * (points[:, 0] - cx) * (points[:, 1] - cy))
    #         J = Ixx + Iyy  # 转动惯量
    #         Asx = A / height  # 剪切面积近似
    #         Asy = A / width  # 剪切面积近似

    #         return {
    #             'area': A,
    #             'centroid': (cx, cy),
    #             'Ixx': Ixx,  # I33
    #             'Iyy': Iyy,  # I22
    #             'Ixy': Ixy,  # 惯性积I23
    #             'J': J,  # 转动惯量
    #             'Asx': Asx,  # 剪切面积 As3
    #             'Asy': Asy  # 剪切面积 As2
    #         }
        
    #     # 获取多边形的边界
    #     bounds = polygon.bounds  # (minx, miny, maxx, maxy)
    #     width = bounds[2] - bounds[0]
    #     height = bounds[3] - bounds[1]
        
    #     # 初始点阵分辨率
    #     num_points_x = 100  # 初始点数量
    #     num_points_y = 100

    #     last_properties = None
    #     for _ in range(max_iter):
    #         # 生成在多边形内部的点阵
    #         x = np.linspace(bounds[0], bounds[2], num_points_x)
    #         y = np.linspace(bounds[1], bounds[3], num_points_y)
    #         xv, yv = np.meshgrid(x, y)
    #         points = np.column_stack((xv.ravel(), yv.ravel()))

    #         # 判断这些点是否在多边形内部
    #         points_geom = [Point(p) for p in points]
    #         contains = np.array([polygon.contains(p) for p in points_geom])
    #         inside_points = points[contains]

    #         dx = width / num_points_x
    #         dy = height / num_points_y

    #         current_properties = compute_properties(inside_points, dx, dy)
            
    #         # 比较新旧属性的变化
    #         if last_properties:
    #             changes = {k: abs(current_properties[k] - last_properties[k]) / last_properties[k] for k in current_properties}
    #             max_change = max(changes.values())
    #             if max_change < tolerance:
    #                 break

    #         last_properties = current_properties
    #         num_points_x *= 2  # 加密点阵
    #         num_points_y *= 2
        
    #     # 返回最终计算的属性
    #     final_properties = {
    #         'area': last_properties['area'],
    #         'width': width,
    #         'height': height,
    #         'centroid': last_properties['centroid'],
    #         'Ixx': last_properties['Ixx'],
    #         'Iyy': last_properties['Iyy'],
    #         'Ixy': last_properties['Ixy'],
    #         'J': last_properties['J'],
    #         'Asx': last_properties['Asx'],
    #         'Asy': last_properties['Asy']
    #     }

    #     return final_properties


    @property
    def combine_geometric_properties(self):
        """合并外边界和内边界的几何性质"""
        return self.calculate_geometric_properties(self.combined_polygon)
    
    @property
    def combined_polygon(self):
        combined_polygon = self.outer_polygon.difference(unary_union(self.inner_polygons))
        if not isinstance(combined_polygon, Polygon) or isinstance(combined_polygon, MultiPolygon):
            polygon = [geom for geom in combined_polygon.geoms if isinstance(geom, Polygon) or isinstance(geom, MultiPolygon)]
        else:
            polygon = [combined_polygon]
        if len(polygon) == 1:
            return polygon[0]
        else:
            p0 = polygon[0]
            for p in polygon[1:]:
                p0 = p0.union(p)
            return p0
    
    @property
    def outer_polygon(self):
        if len(self.outer_boundaries) == 1:
            return self.outer_boundaries[0]
        else:
            if self.log:
                self.logger.warning("More than one outer boundary found, Combining all of them!")
            else:
                print("More than one outer boundary found, Combining all of them!")
            merged_polygon = unary_union(self.outer_boundaries)
            if not merged_polygon.is_valid:
                if self.log:
                    self.logger.warning(f"Merged outer Boundary not valid! Detail: {explain_validity(merged_polygon)}. Trying to fix it...")
                else:
                    print(f"Merged outer Boundary not valid! Detail: {explain_validity(merged_polygon)}. Trying to fix it...")
                merged_polygon = make_valid(merged_polygon)
                if self.log:
                    if merged_polygon.is_valid:
                        self.logger.success(f"Successfully fixed the invalid merged polygon")
                    else:
                        print(f"Failed to fix the invalid merged polygon! Detail: {explain_validity(merged_polygon)}. Ignored!")
            return merged_polygon
    
    @property
    def outer_geometric_properties(self):
        """外边界的几何性质"""
        return self.calculate_geometric_properties(self.outer_polygon)

    @property
    def inner_polygons(self):
        return self.inner_boundaries

if __name__ == '__main__':
    # 示例文件路径
    dxf_file_path = r'Test\TongZhouSha_H_above_50.dxf'
    unit_of_dxf = 'cm'
    show_log = True
    H50section = DXF2Polygons(dxf_file_path, unit_of_dxf, show_log)
    H50section.plot()
    # dxf_file_path = r'Test\TongZhouSha_Main_Girder_1.dxf'
    # unit_of_dxf = 'm'
    # show_log = True
    # mainsec = DXF2Polygons(dxf_file_path, unit_of_dxf, show_log)
    # mainsec.plot()
