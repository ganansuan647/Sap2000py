from dataclasses import dataclass
from pathlib import Path
from loguru import logger
from Sap2000py import Saproject
from typing import Literal, Tuple
from dataclasses import dataclass, field
from typing import List
import numpy as np


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
    g: float = 9.81

    def unit_convert(self,origin_unit:Literal['m/s^2','cm/s^2','g'],target:Literal['m/s^2','cm/s^2','g'] = 'g'):
        """_summary_

        Args:
            origin_unit (Literal['m/s^-2','cm/s^-2','g']): _description_
            target (Literal['m/s^-2','cm/s^-2','g']): _description_. Defaults to 'g'.
        """
        if origin_unit==target:
            return
        if origin_unit=='m/s^2':
            if target=='cm/s^2':
                self.values = [x*100 for x in self.values]
            elif target=='g':
                self.values = [x/self.g for x in self.values]
        elif origin_unit=='cm/s^2':
            if target=='m/s^2':
                self.values = [x/100 for x in self.values]
            elif target=='g':
                self.values = [x/self.g/100 for x in self.values]
        elif origin_unit=='g':
            if target=='m/s^2':
                self.values = [x*self.g for x in self.values]
            elif target=='cm/s^2':
                self.values = [x*self.g*100 for x in self.values]
        else:
            raise NotImplementedError("Unit conversion from {origin_unit} to {target} not supported yet!")
    
    def get_from_txt(self,file_path:Path = Path('..\..\Examples\waves\Examples\waves\GH1NMB01.txt'),dt:float=0.02) -> Tuple[List[float], List[float]]:
        """Parses a txt file containing time history data
        the txt file should be in the format of:
        (maybe some header lines)
        time value (or only value, then time will be calculated by dt)

        Args:
            file_path (Path, optional): file path as a Path instance. Defaults to Path('..\..\Examples\waves\Examples\waves\GH1NMB01.txt').
            dt (float, optional): dt will only be used when only value included in the txt file. Defaults to 0.02.

        Raises:
            NotImplementedError: Time history series format not supported!

        Returns:
            _type_: _description_
        """
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
    
    def response_spectrum(self, max_T: float = 10.0, dt: float = 0.02, damping: float = 0.05) -> Tuple[List[float], List[float], List[float], List[float]]:
        """
        Calculates the response spectrum (Sa, Sv, Sd) for the given time history data.

        Args:
            max_T (float, optional): Maximum period to calculate the response spectrum. Defaults to 10.0.
            dt (float, optional): Interval between periods from 0 to max_T. Defaults to 0.02.

        Returns:
            Tuple[List[float], List[float], List[float], List[float]]: periods, Sa, Sv, Sd
        """

        acc = np.array(self.values)  # Acceleration time history
        times = np.array(self.times)  # Time values

        if len(times) != len(acc):
            logger.error("Length of times and values do not match!")
            return

        dt_hist = times[1] - times[0]  # Time step of the time history

        T_values = np.arange(0.0, max_T + dt, dt)  # Periods from 0.05 to max_T in steps of dt
        Sa = []
        Sv = []
        Sd = []

        for T in T_values:
            if T == 0.0:
                vel = np.cumsum(acc) * dt_hist
                dis = np.cumsum(vel) * dt_hist
                MAcc = np.max(np.abs(acc))
                MVel = np.max(np.abs(vel))
                MDis = np.max(np.abs(dis))
                Sd.append(MDis)
                Sv.append(MVel)
                Sa.append(MAcc)
                continue
            omega = 2 * np.pi / T
            DamFrcy = omega * np.sqrt(1 - damping ** 2)
            e_t = np.exp(-damping * omega * dt_hist)
            s = np.sin(DamFrcy * dt_hist)
            c = np.cos(DamFrcy * dt_hist)

            sqrt_term = np.sqrt(1 - damping ** 2)
            A = np.zeros((2, 2))
            B = np.zeros((2, 2))

            A[0, 0] = e_t * (s * damping / sqrt_term + c)
            A[0, 1] = e_t * s / DamFrcy
            A[1, 0] = -omega * e_t * s / sqrt_term
            A[1, 1] = e_t * (-s * damping / sqrt_term + c)

            d_f = (2 * damping ** 2 - 1) / (omega ** 2 * dt_hist)
            d_3t = damping / (omega ** 3 * dt_hist)

            B[0, 0] = e_t * ((d_f + damping / omega) * s / DamFrcy + (2 * d_3t + 1 / omega ** 2) * c) - 2 * d_3t
            B[0, 1] = -e_t * (d_f * s / DamFrcy + 2 * d_3t * c) - 1 / omega ** 2 + 2 * d_3t
            B[1, 0] = e_t * (
                (d_f + damping / omega) * (c - damping / sqrt_term * s) -
                (2 * d_3t + 1 / omega ** 2) * (DamFrcy * s + damping * omega * c)
            ) + 1 / (omega ** 2 * dt_hist)
            B[1, 1] = e_t * (
                1 / (omega ** 2 * dt_hist) * c + s * damping / (omega * DamFrcy * dt_hist)
            ) - 1 / (omega ** 2 * dt_hist)

            count = len(acc)
            Displace = np.zeros(count)
            Velocity = np.zeros(count)
            AbsAcce = np.zeros(count)

            for ii in range(count - 1):
                Displace[ii + 1] = (
                    A[0, 0] * Displace[ii] + A[0, 1] * Velocity[ii] +
                    B[0, 0] * acc[ii] + B[0, 1] * acc[ii + 1]
                )
                Velocity[ii + 1] = (
                    A[1, 0] * Displace[ii] + A[1, 1] * Velocity[ii] +
                    B[1, 0] * acc[ii] + B[1, 1] * acc[ii + 1]
                )
                AbsAcce[ii + 1] = -2 * damping * omega * Velocity[ii + 1] - omega ** 2 * Displace[ii + 1]

            MDis = np.max(np.abs(Displace))
            MVel = np.max(np.abs(Velocity))
            MAcc = np.max(np.abs(AbsAcce))

            Sd.append(MDis)
            Sv.append(MVel)
            Sa.append(MAcc)

        self.periods = T_values.tolist()
        self.sa = Sa
        self.sv = Sv
        self.sd = Sd
        return self.periods, self.sa, self.sv, self.sd
    
    @classmethod
    def get_from_DAT(cls, file_path:Path = Path('..\..\Examples\waves\cz2-2-34.DAT')):
        """Parses a DAT file containing time history data.
        The DAT file should follow this format:
        1. The first line contains two values: the number of data points and the time interval (dt).
        2. The subsequent lines contain the data points for the time history.
        3. Each time history consists of 11 lines: one header line followed by 10 lines of data.
        4. The file can contain multiple time histories, each following the same format.
        Example of a DAT file content:
            4096     0.0200
            -0.0037   -0.0039    -0.0053    -0.0029     0.0030     0.0005    -0.0148
            -0.0215    0.0059     0.0267    -0.0153    -0.0514    -0.0330     0.0489
            0.0704    -0.0229    -0.0964     0.0263     0.1186    -0.0238    -0.1617
            ...
            0.0337
            file_path (Path, optional): The path to the DAT file. Defaults to Path('..\..\Examples\waves\cz2-2-34.DAT').
            
        Returns:
            tuple: A tuple containing two lists:
                - times: A list of time values.
                - values: A list of corresponding data values.
                
        Args:
            file_path (Path, optional): path to .DAT file. Defaults to Path('..\..\Examples\waves\cz2-2-34.DAT').
        """
        if not file_path.is_file():
            logger.error(f"{file_path} is not a file!")
            return
        timelist = []
        valuelist = []
        with open(file_path, 'r') as file:
            lines = file.readlines()
            i = 0
            num_points, dt = int(lines[0].split()[0]), float(lines[0].split()[1])
            
            def get_i_line(lines,i):
                return list(map(float,lines[i].split()))
            
            values = []
            while i < len(lines):
                line_values = get_i_line(lines,i)
                if len(line_values) == 2:
                    if len(get_i_line(lines,i+1)) != 2:
                        # end the last record
                        if len(values) > 0:
                            times = [dt*k for k in range(num_points)]
                            timelist.append(times)
                            valuelist.append(values)
                        
                        # the i line is considered as the header line
                        num_points, dt = int(lines[i].split()[0]), float(lines[i].split()[1])
                        values = []
                    else:
                        values.extend(line_values)
                else:
                    values.extend(line_values)
                        
                i += 1
                
            times = [dt*k for k in range(num_points)]
            timelist.append(times)
            valuelist.append(values)
            
        funcs = []
        for i in range(len(timelist)):
            TH_name = f"{file_path.stem}_{i+1}"
            newfun = cls(name=TH_name)
            newfun.times = timelist[i]
            newfun.values = valuelist[i]
            funcs.append(newfun)
        return funcs
    
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
            newfun.get_from_txt(file)
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
        ret = Saproject().Define.loadcases.ModalHistNonLinear.SetCase(self.name)
        if ret==0:
            logger.opt(colors=True).success(f"Modal Time History Case <yellow>{self.name}</yellow> defined!")
        else:
            logger.opt(colors=True).error(f"Modal Time History Case <yellow>{self.name}</yellow> Failed to define!")
            
        ret = Saproject().Define.loadcases.ModalHistNonLinear.SetDampConstant(self.name,self.damping)
        if ret==0:
            logger.opt(colors=True).success(f"Modal Time History Case <yellow>{self.name}</yellow> damping set as <yellow>{self.damping}</yellow>!")
        else:
            logger.opt(colors=True).error(f"Modal Time History Case <yellow>{self.name}</yellow> damping failed to set as <yellow>{self.damping}</yellow>!")
        
        ret = Saproject().Define.loadcases.ModalHistNonLinear.SetTimeStep(self.name,nstep=self.nstep, dt=self.dt)
        if ret==0:
            logger.opt(colors=True).success(f"Modal Time History Case <yellow>{self.name}</yellow> Time Step set as <yellow>{self.dt}</yellow>s!")
        else:
            logger.opt(colors=True).error(f"Modal Time History Case <yellow>{self.name}</yellow> Time Step failed to set as <yellow>{self.dt}</yellow>s!")
        
        LoadName = self.Loads['LoadName']
        LoadType = self.Loads['LoadType']
        LoadFunc = self.Loads['LoadFunc']
        LoadSF = self.Loads['LoadSF']
        NumberLoads = len(LoadName)
        ret = Saproject().Define.loadcases.ModalHistNonLinear.SetLoads(self.name,NumberLoads=NumberLoads,LoadName=LoadName,LoadType = LoadType,Func=LoadFunc,SF=LoadSF)
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
        ret = Saproject().Define.loadcases.DirHistNonLinear.SetCase(self.name)
        if ret==0:
            logger.opt(colors=True).success(f"Dir Time History Case <yellow>{self.name}</yellow> defined!")
        else:
            logger.opt(colors=True).error(f"Dir Time History Case <yellow>{self.name}</yellow> Failed to define!")
            
        ret = Saproject().Define.loadcases.DirHistNonLinear.SetTimeIntegration(self.name,self.IntegrationMethod)
        if ret==0:
            logger.opt(colors=True).success(f"Dir Time History Case <yellow>{self.name}</yellow> Integration Method set as <yellow>{self.IntegrationMethod}</yellow>!")
        else:
            logger.opt(colors=True).error(f"Dir Time History Case <yellow>{self.name}</yellow> Integration Method failed to set as <yellow>{self.IntegrationMethod}</yellow>!")
            
        ret = Saproject().Define.loadcases.DirHistNonLinear.SetLoads(self.name,NumberLoads=len(self.Loads['LoadName']),LoadName=self.Loads['LoadName'],LoadType=self.Loads['LoadType'],Func=self.Loads['LoadFunc'],SF=self.Loads['LoadSF'])
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
        ret = Saproject().Define.loadcases.DirHistNonLinear.SetDampProportional(self.name,DampType=DampType,Dampa=Dampa, Dampb=Dampb, Dampf1=Dampf1, Dampf2=Dampf2,Dampd1= Dampd1,Dampd2= Dampd2)
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
    
    