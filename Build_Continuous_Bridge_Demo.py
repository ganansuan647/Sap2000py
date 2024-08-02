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
from rich.console import Console
from rich.table import Table

#full path to the model
ModelPath = Path('.\Test\Span5SteelBoxPierBridge.sdb')

# Create a Sap2000py obj (default: attatch to instance and create if not exist)
Sap = Saproject()

# Change Sap api settings if you want
# SapSap(AttachToInstance = True,SpecifyPath = False,ProgramPath = "your sap2000 path")

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

# Build 5 Span Steel Bouble Box Pier Continuous Bridge
# filepath of the spring data
SixSpringFile = Path('.\Examples\ContinuousBridge6spring.txt')

from Sap2000py.Bridge.SapBridge import SapBridge as Bridge
# Build Piers and connect with base springs
pier1 = Bridge.Pier.DoubleBox(
    name="#1",
    station=0,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=60.9,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = True,
    offset = 1.0
)
pier1base = Bridge.Base.Six_Spring(pier1.base_point,pier1.name,spring_data_name='1',spring_file_path=SixSpringFile)
pier1.connect_with_base(pier1base)

pier2 = Bridge.Pier.DoubleBox(
    name="#2",
    station=90,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=60.9,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = False,
)
pier2base = Bridge.Base.Six_Spring(pier2.base_point,pier2.name,spring_data_name='2',spring_file_path=SixSpringFile)
pier2.connect_with_base(pier2base)

pier3 = Bridge.Pier.DoubleBox(
    name="#3",
    station=180,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=60.9,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = False,
)
pier3base = Bridge.Base.Six_Spring(pier3.base_point,pier3.name,spring_data_name='3',spring_file_path=SixSpringFile)
pier3.connect_with_base(pier3base)

pier4 = Bridge.Pier.DoubleBox(
    name="#4",
    station=270,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=60.9,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = False,
)
pier4base = Bridge.Base.Six_Spring(pier4.base_point,pier4.name,spring_data_name='4',spring_file_path=SixSpringFile)
pier4.connect_with_base(pier4base)

pier5 = Bridge.Pier.DoubleBox(
    name="#5",
    station=360,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=60.9,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = False,
)
pier5base = Bridge.Base.Six_Spring(pier5.base_point,pier5.name,spring_data_name='5',spring_file_path=SixSpringFile)
pier5.connect_with_base(pier5base)

pier6 = Bridge.Pier.DoubleBox(
    name="#6",
    station=450,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=60.9,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = True,
    offset=1.0
)
pier6base = Bridge.Base.Six_Spring(pier6.base_point,pier6.name,spring_data_name='6',spring_file_path=SixSpringFile)
pier6.connect_with_base(pier6base)

pier7 = Bridge.Pier.DoubleBox(
    name="#7",
    station=540,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=60.9,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = False,
)
pier7base = Bridge.Base.Six_Spring(pier7.base_point,pier7.name,spring_data_name='7',spring_file_path=SixSpringFile)
pier7.connect_with_base(pier7base)

pier8 = Bridge.Pier.DoubleBox(
    name="#8",
    station=630,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=60.9,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = False,
)
pier8base = Bridge.Base.Six_Spring(pier8.base_point,pier8.name,spring_data_name='8',spring_file_path=SixSpringFile)
pier8.connect_with_base(pier8base)

pier9 = Bridge.Pier.DoubleBox(
    name="#9",
    station=720,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=60.9,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = False,
)
pier9base = Bridge.Base.Six_Spring(pier9.base_point,pier9.name,spring_data_name='9',spring_file_path=SixSpringFile)
pier9.connect_with_base(pier9base)

pier10 = Bridge.Pier.DoubleBox(
    name="#10",
    station=810,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=60.9,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = False,
)
pier10base = Bridge.Base.Six_Spring(pier10.base_point,pier10.name,spring_data_name='10',spring_file_path=SixSpringFile)
pier10.connect_with_base(pier10base)

pier11 = Bridge.Pier.DoubleBox(
    name="#11",
    station=900,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=60.9,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = True,
    offset=1.0
)
pier11base = Bridge.Base.Six_Spring(pier11.base_point,pier11.name,spring_data_name='11',spring_file_path=SixSpringFile)
pier11.connect_with_base(pier11base)

pier12 = Bridge.Pier.DoubleBox(
    name="#12",
    station=990,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=60.9,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = False,
)
pier12base = Bridge.Base.Six_Spring(pier12.base_point,pier12.name,spring_data_name='12',spring_file_path=SixSpringFile)
pier12.connect_with_base(pier12base)

pier13 = Bridge.Pier.DoubleBox(
    name="#13",
    station=1080,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=60.9,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = False,
)
pier13base = Bridge.Base.Six_Spring(pier13.base_point,pier13.name,spring_data_name='13',spring_file_path=SixSpringFile)
pier13.connect_with_base(pier13base)

pier14 = Bridge.Pier.DoubleBox(
    name="#14",
    station=1170,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=60.9,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = False,
)
pier14base = Bridge.Base.Six_Spring(pier14.base_point,pier14.name,spring_data_name='14',spring_file_path=SixSpringFile)
pier14.connect_with_base(pier14base)

pier15 = Bridge.Pier.DoubleBox(
    name="#15",
    station=1260,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=60.9,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = False,
)
pier15base = Bridge.Base.Six_Spring(pier15.base_point,pier15.name,spring_data_name='15',spring_file_path=SixSpringFile)
pier15.connect_with_base(pier15base)

pier16 = Bridge.Pier.DoubleBox(
    name="#16",
    station=1350,
    Distance_between_piers=20.75,
    Height_of_pier_bottom=0.0,
    Height_of_pier=60.9,
    bottom_solid_length=2.0,
    top_solid_length=3.0,
    Distance_between_bearings=7.0,
    num_of_hollow_elements=3,
    is_intermediate_pier = True,
    offset=1.0
)
pier16base = Bridge.Base.Six_Spring(pier16.base_point,pier16.name,spring_data_name='16',spring_file_path=SixSpringFile)
pier16.connect_with_base(pier16base)

girderleft = Bridge.Girder.Box(
    name = "SpanLeft",
    pierlist=[pier1,pier2,pier3,pier4,pier5,pier6],
    fixedpier = [pier3,pier4],
    Plan = '方案一')
girderleft.add_bearing_links(strategy = 'ideal')        

girdermain = Bridge.Girder.Box(
    name = "SpanMain",
    pierlist=[pier6,pier7,pier8,pier9,pier10,pier11],
    fixedpier = [pier8,pier9],
    Plan = '方案一')
girdermain.add_bearing_links(strategy = 'ideal')

girderright = Bridge.Girder.Box(
    name = "SpanRight",
    pierlist=[pier11,pier12,pier13,pier14,pier15,pier16],
    fixedpier = [pier13,pier14],
    Plan = '方案一')
girderright.add_bearing_links(strategy = 'ideal')

# create groups for results
base_names = [pier.base.point.name for pier in girdermain.pierlist]
Sap.Scripts.Group.AddtoGroup('Base',base_names,type='Point')

pier_bottom_names = [pier.name+"_left_bottom2hollowBottom" for pier in girdermain.pierlist]
Sap.Scripts.Group.AddtoGroup('PierBottom',pier_bottom_names,type='Frame')

pier_hollow_bottom_names = [pier.name+"_left_hollow_1" for pier in girdermain.pierlist]
Sap.Scripts.Group.AddtoGroup('PierHollowBottom',pier_hollow_bottom_names,type='Frame')

bearing_names = [girdermain.bearings[pier.name]['left']['inner'].name for pier in girdermain.pierlist]
Sap.Scripts.Group.AddtoGroup('Bearing',bearing_names,type='Link')

# set Modal analysis
Sap.Define.loadcases.ModalEigen.SetInitialCase('MODAL', None)
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

spectrum_path = Path('.\Examples\ResponseSpectrum_E2_Damping_0.02.txt')
times,values = get_spectrum_from_file(spectrum_path)

# E2 Spectrum Function
Sap.Define.function.ResponseSpectrum.Set_User('E2Spectrum',times,values,0.02)   
# E2X Spectrum
Sap.Define.loadcases.ResponseSpectrum.SetCase("E2X")
Sap.Define.loadcases.ResponseSpectrum.SetDampConstant('E2X',0.02)
Sap.Define.loadcases.ResponseSpectrum.SetDirComb('E2X','SRSS')
Sap.Define.loadcases.ResponseSpectrum.SetLoads('E2X',NumberLoads=2,LoadName=['U1','U3'],Func=['E2Spectrum','E2Spectrum'],SF=[1,1*0.65])

# E2Y Spectrum
Sap.Define.loadcases.ResponseSpectrum.SetCase("E2Y")
Sap.Define.loadcases.ResponseSpectrum.SetDampConstant('E2Y',0.02)
Sap.Define.loadcases.ResponseSpectrum.SetDirComb('E2Y','SRSS')
Sap.Define.loadcases.ResponseSpectrum.SetLoads('E2Y',NumberLoads=2,LoadName=['U2','U3'],Func=['E2Spectrum','E2Spectrum'],SF=[1,1*0.65])
TH_names = []
time_history_folder_path = Path('.\Examples\waves')
TH_files = time_history_folder_path.glob('*.txt')
for file_path in TH_files:
    times,values = get_time_history_from_file(file_path,dt=0.02)
    time_history_name = 'E2'+file_path.stem.split('.')[0]
    TH_names.append(time_history_name)
    Sap.Define.function.TimeHistory.Set_User(time_history_name,times,values)
    # E2X Time History
    Sap.Define.loadcases.DirHistNonlinear.SetCase('E2X'+time_history_name)
    Sap.Define.loadcases.DirHistNonlinear.SetTimeIntegration('E2X'+time_history_name,'Newmark')
    Sap.Define.loadcases.DirHistNonlinear.SetLoads('E2X'+time_history_name,NumberLoads=3,LoadType=['Load','Accel','Accel'],LoadName=['DEAD','U1','U3'],Func=["RAMPTH",time_history_name,time_history_name],SF=[1,1,0.65])
    Sap.Define.loadcases.DirHistNonlinear.SetDampProportional('E2X'+time_history_name,DampType='Period', Dampa=0, Dampb=0, Dampf1=period_x_1, Dampf2=min(period_x_2,period_z_2),Dampd1= 0.02,Dampd2= 0.02)  # Rayleigh damping at period f1/s and f2/s is set to 0.05
    # E2Y Time History
    Sap.Define.loadcases.DirHistNonlinear.SetCase('E2Y'+time_history_name)
    Sap.Define.loadcases.DirHistNonlinear.SetTimeIntegration('E2Y'+time_history_name,'Newmark')
    Sap.Define.loadcases.DirHistNonlinear.SetLoads('E2Y'+time_history_name,NumberLoads=3,LoadType=['Load','Accel','Accel'],LoadName=['DEAD','U2','U3'],Func=["RAMPTH",time_history_name,time_history_name],SF=[1,1,0.65])
    Sap.Define.loadcases.DirHistNonlinear.SetDampProportional('E2Y'+time_history_name,DampType='Period', Dampa=0, Dampb=0, Dampf1=period_y_1, Dampf2=min(period_y_2,period_z_2),Dampd1= 0.02,Dampd2= 0.02)  # Rayleigh damping at period f1/s and f2/s is set to 0.05
    
logger.opt(colors=True).success(f"Rayleigh damping Control Period of X direction is {period_x_1:.2f}s and {period_x_2:.2f}s (actually {min(period_x_2,period_z_2):.2f}s)")
logger.opt(colors=True).success(f"Rayleigh damping Control Period of Y direction is {period_y_1:.2f}s and {period_y_2:.2f}s (actually {min(period_y_2,period_z_2):.2f}s)")
logger.opt(colors=True).success(f"Rayleigh damping Control Period of Z direction is {period_z_1:.2f}s and {period_z_2:.2f}s")

Sap.Define.LoadCombo.Add('E2纵向+竖向', comboType = 'AbsAdd')
ret = [Sap.Define.LoadCombo.SetCaseList('E2纵向+竖向',CNameType="LoadCase",CName = 'E2X'+name, SF = 1/len(TH_names)) for name in TH_names]
if all([r[1] == 0 for r in ret]):
    logger.opt(colors=True).success(f"Load Combination E2纵向+竖向 has been successfully defined.")
else:
    logger.opt(colors=True).error(f"An error occurred while defining the Load Combination E2纵向.")

Sap.Define.LoadCombo.Add('E2横向+竖向', comboType = 'AbsAdd')
ret = [Sap.Define.LoadCombo.SetCaseList('E2横向+竖向',CNameType="LoadCase",CName = 'E2Y'+name, SF = 1/len(TH_names)) for name in TH_names]
if all([r[1] == 0 for r in ret]):
    logger.opt(colors=True).success(f"Load Combination E2横向+竖向 has been successfully defined.")
else:
    logger.opt(colors=True).error(f"An error occurred while defining the Load Combination E2横向.")

print("程序暂停,等待用户确认已重设MODAL工况...")
user_input = input("请操作并按下回车键: ")

Sap.File.Save(ModelPath)
# Sap.Scripts.Analyze.AddCases(CaseName = ['DEAD', 'MODAL','E2X','E2Y'])
# Sap.Analyze.RunAnalysis()
Sap.Scripts.Analyze.RunAll()

table = Table(title="纵桥向+竖向支座反应比较", show_header=True, header_style="bold magenta")
table.add_column("墩号", justify="left", style="cyan", no_wrap=True)
table.add_column("支座位移(反应谱)", justify="right", style="green")
table.add_column("支座反力(反应谱)", justify="right", style="yellow")
table.add_column("支座位移(E2时程)", justify="right", style="green")
table.add_column("支座反力(E2时程)", justify="right", style="yellow")
if True:
    Sap.Scripts.SelectCombo_Case("E2X")
    # get Link deformation result by group name
    Name,LinkAbsDeformationS,__,__ = Sap.Scripts.GetResults.LinkDeformation_by_Group("Bearing")
    # get Link shearforce result by group name
    Name,LinkAbsForceS,LinkMaxForceS,LinkMinForceS = Sap.Scripts.GetResults.LinkForce_by_Group("Bearing")
    
    Sap.Scripts.SelectCombo_Case("E2纵向+竖向")
    
    # get Link deformation result by group name
    Name,LinkAbsDeformationTH,__,__ = Sap.Scripts.GetResults.LinkDeformation_by_Group("Bearing")
    # get Link shearforce result by group name
    Name,LinkAbsForceTH,LinkMaxForceTH,LinkMinForceTH = Sap.Scripts.GetResults.LinkForce_by_Group("Bearing")
    sorted_indices = sorted(range(len(Name)), key=lambda i: int(Name[i].split('_')[0][1:]))
    for i in sorted_indices:
        table.add_row(
                f"{Name[i].split('_')[0].split('#')[-1]}",
                f"{max(LinkAbsDeformationS[i][1:2]):.2f}",
                f"{max(LinkAbsForceS[i][1:2]):.2f}",
                f"{max(LinkAbsDeformationTH[i][1:2]):.2f}",
                f"{max(LinkAbsForceTH[i][1:2]):.2f}",
            )
# print table
console = Console()
console.print(table)

table = Table(title="横桥向+竖向支座反应比较", show_header=True, header_style="bold magenta")
table.add_column("墩号", justify="left", style="cyan", no_wrap=True)
table.add_column("支座位移(反应谱)", justify="right", style="green")
table.add_column("支座反力(反应谱)", justify="right", style="yellow")
table.add_column("支座位移(E2时程)", justify="right", style="green")
table.add_column("支座反力(E2时程)", justify="right", style="yellow")
if True:
    Sap.Scripts.SelectCombo_Case("E2Y")
    # get Link deformation result by group name
    Name,LinkAbsDeformationS,__,__ = Sap.Scripts.GetResults.LinkDeformation_by_Group("Bearing")
    # get Link shearforce result by group name
    Name,LinkAbsForceS,LinkMaxForceS,LinkMinForceS = Sap.Scripts.GetResults.LinkForce_by_Group("Bearing")
    
    Sap.Scripts.SelectCombo_Case("E2横向+竖向")
    
    # get Link deformation result by group name
    Name,LinkAbsDeformationTH,__,__ = Sap.Scripts.GetResults.LinkDeformation_by_Group("Bearing")
    # get Link shearforce result by group name
    Name,LinkAbsForceTH,LinkMaxForceTH,LinkMinForceTH = Sap.Scripts.GetResults.LinkForce_by_Group("Bearing")
    sorted_indices = sorted(range(len(Name)), key=lambda i: int(Name[i].split('_')[0][1:]))
    for i in sorted_indices:
        table.add_row(
                f"{Name[i].split('_')[0].split('#')[-1]}",
                f"{max(LinkAbsDeformationS[i][1:2]):.2f}",
                f"{max(LinkAbsForceS[i][1:2]):.2f}",
                f"{max(LinkAbsDeformationTH[i][1:2]):.2f}",
                f"{max(LinkAbsForceTH[i][1:2]):.2f}",
            )
# print table
console = Console()
console.print(table)


table = Table(title="纵桥向+竖向墩底单元受力比较", show_header=True, header_style="bold magenta")
table.add_column("墩号", justify="left", style="cyan", no_wrap=True)
table.add_column("空心段墩底剪力(反应谱)", justify="right", style="green")
table.add_column("墩底剪力(反应谱)", justify="right", style="yellow")
table.add_column("空心段墩底剪力(E2时程)", justify="right", style="green")
table.add_column("墩底剪力(E2时程)", justify="right", style="yellow")
if True:
    Sap.Scripts.SelectCombo_Case(["E2X"])
    # get Frame Shear force result by group name
    Name,EleAbsForceS1,__,__ = Sap.Scripts.GetResults.ElementJointForce_by_Group("PierHollowBottom")
    Name,EleAbsForceS2,__,__ = Sap.Scripts.GetResults.ElementJointForce_by_Group("PierBottom")
    
    Sap.Scripts.SelectCombo_Case("E2纵向+竖向")
    
    # get Frame Shear force result by group name
    Name,EleAbsForceTH1,__,__ = Sap.Scripts.GetResults.ElementJointForce_by_Group("PierHollowBottom")
    Name,EleAbsForceTH2,__,__ = Sap.Scripts.GetResults.ElementJointForce_by_Group("PierBottom")
    sorted_indices = sorted(range(len(Name)), key=lambda i: int(Name[i].split('_')[0][1:]))
    for i in sorted_indices:
        table.add_row(
                f"{Name[i].split('_')[0].split('#')[-1]}",
                f"{max(EleAbsForceS1[i][1:2]):.2f}",
                f"{max(EleAbsForceS2[i][1:2]):.2f}",
                f"{max(EleAbsForceTH1[i][1:2]):.2f}",
                f"{max(EleAbsForceTH2[i][1:2]):.2f}",
            )
# print table
console = Console()
console.print(table)

table = Table(title="横桥向+竖向墩底单元受力比较", show_header=True, header_style="bold magenta")
table.add_column("墩号", justify="left", style="cyan", no_wrap=True)
table.add_column("空心段墩底剪力(反应谱)", justify="right", style="green")
table.add_column("墩底剪力(反应谱)", justify="right", style="yellow")
table.add_column("空心段墩底剪力(E2时程)", justify="right", style="green")
table.add_column("墩底剪力(E2时程)", justify="right", style="yellow")
if True:
    Sap.Scripts.SelectCombo_Case(["E2Y"])
    # get Frame Shear force result by group name
    Name,EleAbsForceS1,__,__ = Sap.Scripts.GetResults.ElementJointForce_by_Group("PierHollowBottom")
    Name,EleAbsForceS2,__,__ = Sap.Scripts.GetResults.ElementJointForce_by_Group("PierBottom")
    
    Sap.Scripts.SelectCombo_Case("E2横向+竖向")
    
    # get Frame Shear force result by group name
    Name,EleAbsForceTH1,__,__ = Sap.Scripts.GetResults.ElementJointForce_by_Group("PierHollowBottom")
    Name,EleAbsForceTH2,__,__ = Sap.Scripts.GetResults.ElementJointForce_by_Group("PierBottom")
    sorted_indices = sorted(range(len(Name)), key=lambda i: int(Name[i].split('_')[0][1:]))
    for i in sorted_indices:
        table.add_row(
                f"{Name[i].split('_')[0].split('#')[-1]}",
                f"{max(EleAbsForceS1[i][1:2]):.2f}",
                f"{max(EleAbsForceS2[i][1:2]):.2f}",
                f"{max(EleAbsForceTH1[i][1:2]):.2f}",
                f"{max(EleAbsForceTH2[i][1:2]):.2f}",
            )
# print table
console = Console()
console.print(table)


table = Table(title="纵桥向+竖向承台底节点受力比较", show_header=True, header_style="bold magenta")
table.add_column("墩号", justify="left", style="cyan", no_wrap=True)
table.add_column("承台底轴力(反应谱)", justify="right", style="green")
table.add_column("承台底剪力(反应谱)", justify="right", style="green")
table.add_column("承台底弯矩(反应谱)", justify="right", style="green")
table.add_column("承台底轴力(E2时程)", justify="right", style="yellow")
table.add_column("承台底剪力(E2时程)", justify="right", style="yellow")
table.add_column("承台底弯矩(E2时程)", justify="right", style="yellow")
if True:
    Sap.Scripts.SelectCombo_Case("E2X")
    # get jointresult by group name
    Name,JointAbsReacS,__,__ = Sap.Scripts.GetResults.JointReact_by_Group("Base")
    
    Sap.Scripts.SelectCombo_Case("E2纵向+竖向")
    
    # get jointresult by group name
    Name,JointAbsReacTH,__,__ = Sap.Scripts.GetResults.JointReact_by_Group("Base")
    sorted_indices = sorted(range(len(Name)), key=lambda i: int(Name[i].split('_')[0][1:]))
    for i in sorted_indices:
        table.add_row(
                f"{Name[i].split('_')[0].split('#')[-1]}",
                f"{JointAbsReacS[i][2]:.2f}",
                f"{max(JointAbsReacS[i][0:1]):.2f}",
                f"{max(JointAbsReacS[i][3:4]):.2f}",
                f"{JointAbsReacTH[i][2]:.2f}",
                f"{max(JointAbsReacTH[i][0:1]):.2f}",
                f"{max(JointAbsReacTH[i][3:4]):.2f}",
            )

# print table
console = Console()
console.print(table)



table = Table(title="横桥向+竖向承台底节点受力比较", show_header=True, header_style="bold magenta")
table.add_column("墩号", justify="left", style="cyan", no_wrap=True)
table.add_column("承台底轴力(反应谱)", justify="right", style="green")
table.add_column("承台底剪力(反应谱)", justify="right", style="green")
table.add_column("承台底弯矩(反应谱)", justify="right", style="green")
table.add_column("承台底轴力(E2时程)", justify="right", style="yellow")
table.add_column("承台底剪力(E2时程)", justify="right", style="yellow")
table.add_column("承台底弯矩(E2时程)", justify="right", style="yellow")
if True:
    Sap.Scripts.SelectCombo_Case("E2Y")
    # get jointresult by group name
    Name,JointAbsReacS,__,__ = Sap.Scripts.GetResults.JointReact_by_Group("Base")
    
    Sap.Scripts.SelectCombo_Case("E2横向+竖向")
    
    # get jointresult by group name
    Name,JointAbsReacTH,__,__ = Sap.Scripts.GetResults.JointReact_by_Group("Base")
    sorted_indices = sorted(range(len(Name)), key=lambda i: int(Name[i].split('_')[0][1:]))
    for i in sorted_indices:
        table.add_row(
                f"{Name[i].split('_')[0].split('#')[-1]}",
                f"{JointAbsReacS[i][2]:.2f}",
                f"{max(JointAbsReacS[i][0:1]):.2f}",
                f"{max(JointAbsReacS[i][3:4]):.2f}",
                f"{JointAbsReacTH[i][2]:.2f}",
                f"{max(JointAbsReacTH[i][0:1]):.2f}",
                f"{max(JointAbsReacTH[i][3:4]):.2f}",
            )

# print table
console = Console()
console.print(table)
    
    
    # get Link deformation result by group name
    
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

