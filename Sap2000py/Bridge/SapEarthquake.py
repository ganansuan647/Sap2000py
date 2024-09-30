from dataclasses import dataclass
from pathlib import Path
from loguru import logger
from Sap2000py import Saproject
from typing import Literal
from dataclasses import dataclass, field
from typing import List


@dataclass
class SapSpectrumFunc:
    name: str
    times: List[float] = field(default_factory=list)
    values: List[float] = field(default_factory=list)
    damping: float = 0.05
    
    def get_from_file(self,file_path:Path = Path('..\..\Examples\ResponseSpectrum_E2_Damping_0.02.txt')):
        times = []
        values = []
        with open(file_path, 'r') as file:
            header_flag = 0
            # Skip the header line with while loop
            while not header_flag:
                try:
                    i=0
                    for line in file:
                        data = line.strip().split()
                        time, value = [float(x) for x in data]
                        if i==0:
                            logger.trace(f"first data pair of spectrum file is:({time},{value})")
                        times.append(time)
                        values.append(value)
                        i+=1
                    header_flag = 1
                except:
                    # skip the header line
                    next(file)
            
        self.times = times
        self.values = values
        return file_path
    
    def define(self):
        if len(self.times) == 0 or len(self.values) == 0 or len(self.times) != len(self.values):
            logger.error(f"Please check the times and values of the spectrum function! Using Default Spectrum Example in {self.get_from_file()}")
        
        ret = Saproject().Define.function.ResponseSpectrum.Set_User(self.name,self.times,self.values,self.damping)
        if ret[-1]==0:
            logger.opt(colors=True).success(f"Response Spectrum Function <yellow>{self.name}</yellow> with damping <yellow>{self.damping}</yellow> defined!")
        else:
            logger.opt(colors=True).error(f"Response Spectrum Function <yellow>{self.name}</yellow> with damping <yellow>{self.damping}</yellow> Failed to define!")

@dataclass
class SapSpectrumCase:
    name: str
    damping: float = 0.05
    CombMethod: Literal['SRSS', 'ABS', 'CQC3'] = 'SRSS'
    Loads: dict[Literal['LoadName', 'LoadFunc', 'LoadSF']] = field(default_factory=dict)
    
    def define(self):
        ret = Saproject().Define.loadcases.ResponseSpectrum.SetCase(self.name)
        if ret==0:
            logger.opt(colors=True).success(f"Response Spectrum Case <yellow>{self.name}</yellow> defined!")
        else:
            logger.opt(colors=True).error(f"Response Spectrum Case <yellow>{self.name}</yellow> Failed to define!")
            
        ret = Saproject().Define.loadcases.ResponseSpectrum.SetDampConstant(self.name,self.damping)
        if ret==0:
            logger.opt(colors=True).success(f"Response Spectrum Case <yellow>{self.name}</yellow> damping set as <yellow>{self.damping}</yellow>!")
        else:
            logger.opt(colors=True).error(f"Response Spectrum Case <yellow>{self.name}</yellow> damping failed to set as <yellow>{self.damping}</yellow>!")
        
        ret = Saproject().Define.loadcases.ResponseSpectrum.SetDirComb(self.name,CombMethod=self.CombMethod)
        if ret==0:
            logger.opt(colors=True).success(f"Response Spectrum Case <yellow>{self.name}</yellow> Combination Method set as <yellow>{self.CombMethod}</yellow>!")
        else:
            logger.opt(colors=True).error(f"Response Spectrum Case <yellow>{self.name}</yellow> Combination Method failed to set as <yellow>{self.CombMethod}</yellow>!")
        
        LoadName = self.Loads['LoadName']
        LoadFunc = self.Loads['LoadFunc']
        LoadSF = self.Loads['LoadSF']
        NumberLoads = len(LoadName)
        ret = Saproject().Define.loadcases.ResponseSpectrum.SetLoads(self.name,NumberLoads=NumberLoads,LoadName=LoadName,Func=LoadFunc,SF=LoadSF)
        if ret[-1]==0:
            logger.opt(colors=True).success(f"Response Spectrum Case <yellow>{self.name}</yellow> Loads set!")
        else:
            logger.opt(colors=True).error(f"Response Spectrum Case <yellow>{self.name}</yellow> Loads failed to set!")

class SapSpectrum:
    Func = SapSpectrumFunc
    Case = SapSpectrumCase

@dataclass
class SapTimeHistoryFunc:
    name: str
    times: List[float] = field(default_factory=list)
    values: List[float] = field(default_factory=list)

    def get_from_file(self,file_path:Path = Path('..\..\Examples\waves\Examples\waves\GH1NMB01.txt'),dt:float=0.02):
        if not file_path.is_file():
            logger.error(f"{file_path} is not a file!")
            return
        time = 0.0
        times = []
        values = []
        with open(file_path, 'r') as file:
            header_flag = 0
            # Skip the header line with while loop
            while not header_flag:
                try:
                    i=0
                    for line in file:
                        data = line.strip().split()
                        if len(data)==1:
                            # assume only value is given
                            value = float(data[0])
                        elif len(data)==2:
                            # assume time and value is given
                            time, value = [float(x) for x in data]
                        else:
                            raise NotImplementedError("Time history series format not supported!")
                        if i==0:
                            logger.trace(f"first data pair of time history file is::({float(time)},{float(value)})")
                        times.append(float(time))
                        values.append(float(value))
                        time+=dt
                        i+=1
                    header_flag = 1
                except:
                    # skip the header line
                    next(file)
        self.times = times
        self.values = values
        return times,values
    
    def define(self):
        if len(self.times) == 0 or len(self.values) == 0 or len(self.times) != len(self.values):
            logger.error(f"Please check the times and values of the time history function! Using Default Time History Example in {self.get_from_file()}")
        
        ret = Saproject().Define.function.TimeHistory.Set_User(self.name,self.times,self.values)
        if ret[-1]==0:
            logger.opt(colors=True).success(f"Time History Function <yellow>{self.name}</yellow> defined!")
        else:
            logger.opt(colors=True).error(f"Time History Function <yellow>{self.name}</yellow> Failed to define!")

    @classmethod
    def get_from_folder(cls,file_folder:Path = Path('..\..\Examples\waves\Examples\waves'),suffix:str='txt'):
        TH_files = file_folder.glob(f'*.{suffix}')
        funcs = []
        for file in TH_files:
            TH_name = "THFun"+file.stem.split('.')[0]
            newfun = cls(name=TH_name)
            newfun.get_from_file(file)
            funcs.append(newfun)
        return funcs

@dataclass
class SapModalTimeHistoryCase:
    name: str
    damping: float = 0.05
    nstep: int = 8192
    dt: float = 0.02
    Loads: dict[Literal['LoadName','LoadType', 'LoadFunc', 'LoadSF']] = field(default_factory=dict)
    
    def define(self):
        ret = Saproject().Define.loadcases.ModalHistNonlinear.SetCase(self.name)
        if ret==0:
            logger.opt(colors=True).success(f"Modal Time History Case <yellow>{self.name}</yellow> defined!")
        else:
            logger.opt(colors=True).error(f"Modal Time History Case <yellow>{self.name}</yellow> Failed to define!")
            
        ret = Saproject().Define.loadcases.ModalHistNonlinear.SetDampConstant(self.name,self.damping)
        if ret==0:
            logger.opt(colors=True).success(f"Modal Time History Case <yellow>{self.name}</yellow> damping set as <yellow>{self.damping}</yellow>!")
        else:
            logger.opt(colors=True).error(f"Modal Time History Case <yellow>{self.name}</yellow> damping failed to set as <yellow>{self.damping}</yellow>!")
        
        ret = Saproject().Define.loadcases.ModalHistNonlinear.SetTimeStep(self.name,nstep=self.nstep, dt=self.dt)
        if ret==0:
            logger.opt(colors=True).success(f"Modal Time History Case <yellow>{self.name}</yellow> Time Step set as <yellow>{self.dt}</yellow>s!")
        else:
            logger.opt(colors=True).error(f"Modal Time History Case <yellow>{self.name}</yellow> Time Step failed to set as <yellow>{self.dt}</yellow>s!")
        
        LoadName = self.Loads['LoadName']
        LoadType = self.Loads['LoadType']
        LoadFunc = self.Loads['LoadFunc']
        LoadSF = self.Loads['LoadSF']
        NumberLoads = len(LoadName)
        ret = Saproject().Define.loadcases.ModalHistNonlinear.SetLoads(self.name,NumberLoads=NumberLoads,LoadName=LoadName,LoadType = LoadType,Func=LoadFunc,SF=LoadSF)
        if ret[-1]==0:
            logger.opt(colors=True).success(f"Modal Time History Case <yellow>{self.name}</yellow> Loads set!")
        else:
            logger.opt(colors=True).error(f"Modal Time History Case <yellow>{self.name}</yellow> Loads failed to set!")

    
@dataclass
class SapDirTimeHistoryCase:
    name : str
    IntegrationMethod: Literal['Newmark','Wilson','Collocation','Hilber-Hughes-Taylor','Chung and Hulbert'] = 'Newmark'
    Loads: dict[Literal['LoadName','LoadType', 'LoadFunc', 'LoadSF']] = field(default_factory=dict)
    
    def define(self):
        ret = Saproject().Define.loadcases.DirHistNonlinear.SetCase(self.name)
        if ret==0:
            logger.opt(colors=True).success(f"Dir Time History Case <yellow>{self.name}</yellow> defined!")
        else:
            logger.opt(colors=True).error(f"Dir Time History Case <yellow>{self.name}</yellow> Failed to define!")
            
        ret = Saproject().Define.loadcases.DirHistNonlinear.SetTimeIntegration(self.name,self.IntegrationMethod)
        if ret==0:
            logger.opt(colors=True).success(f"Dir Time History Case <yellow>{self.name}</yellow> Integration Method set as <yellow>{self.IntegrationMethod}</yellow>!")
        else:
            logger.opt(colors=True).error(f"Dir Time History Case <yellow>{self.name}</yellow> Integration Method failed to set as <yellow>{self.IntegrationMethod}</yellow>!")
            
        ret = Saproject().Define.loadcases.DirHistNonlinear.SetLoads(self.name,NumberLoads=len(self.Loads['LoadName']),LoadName=self.Loads['LoadName'],LoadType=self.Loads['LoadType'],Func=self.Loads['LoadFunc'],SF=self.Loads['LoadSF'])
        if ret[-1]==0:
            logger.opt(colors=True).success(f"Dir Time History Case <yellow>{self.name}</yellow> Loads set!")
        else:
            logger.opt(colors=True).error(f"Dir Time History Case <yellow>{self.name}</yellow> Loads failed to set!")
            
    def set_damping_rayleigh(self,DampType:Literal['MassStiffness','Period','Frequency'],Dampa:float = 0,Dampb:float = 0, Dampf1:float=0.0, Dampf2:float=0.0,Dampd1:float=0.05,Dampd2:float=0.05):
        """_summary_

        Args:
            DampType (Literal['MassStiffness','Period','Frequency']): _description_
            Dampa (float, optional): only usefual when DampType=MassStiffness. Defaults to 0.
            Dampb (float, optional): only usefual when DampType=MassStiffness. Defaults to 0.
            Dampf1 (float, optional): period/frequency for 1st mode. Defaults to 0.0.
            Dampf2 (float, optional): period/frequency for 2nd mode. Defaults to 0.0.
            Dampd1 (float, optional): damping for 1st mode. Defaults to 0.05.
            Dampd2 (float, optional): damping for 2nd mode. Defaults to 0.05.
        """
        ret = Saproject().Define.loadcases.DirHistNonlinear.SetDampProportional(self.name,DampType=DampType,Dampa=Dampa, Dampb=Dampb, Dampf1=Dampf1, Dampf2=Dampf2,Dampd1= Dampd1,Dampd2= Dampd2)
        if ret==0:
            logger.opt(colors=True).success(f"Dir Time History Case <yellow>{self.name}</yellow> Damping set!")
        else:
            logger.opt(colors=True).error(f"Dir Time History Case <yellow>{self.name}</yellow> Damping failed to set!")
    
    
    
class SapTimeHistory:
    Func = SapTimeHistoryFunc
    ModalCase = SapModalTimeHistoryCase
    DirCase = SapDirTimeHistoryCase

class SapEarthquake:
    Spectrum = SapSpectrum
    TimeHistory = SapTimeHistory
    
    
