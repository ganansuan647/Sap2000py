
class Sapfunctions:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model
        self.ResponseSpectrum = fun_ResponseSpectrum(Sapobj)
        self.TimeHistory = fun_TimeHistory(Sapobj)

class fun_ResponseSpectrum:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model
    
    def Set_Chinese2010(self,name,JGJ32010AlphaMax,JGJ32010SI,JGJ32010Tg,JGJ32010PTDF,DampRatio):
        """
        ---This function defines a Chinese 2010 response spectrum function.---
        inputs:
        name(str)-The name of an existing or new function
        JGJ32010AlphaMax(float)-The maximum influence factor
        JGJ32010SI(int)-This is 1, 2, 3, 4, 5 or 6, indicating the seismic intensity.1 = 6 (0.05g),2 = 7 (0.10g)
            3 = 7 (0.15g),4 = 8 (0.20g),5 = 8 (0.30g),6 = 9 (0.40g)
        JGJ32010Tg(float)-The characteristic ground period, Tg > 0.1. [s]
        JGJ32010PTDF(float)-The period time discount factor
        DampRatio(float)-The damping ratio for the function, 0 <= DampRatio < 1.
        """
        self.__Model.Func.FuncRS.SetChinese2010(name,JGJ32010AlphaMax,JGJ32010SI,JGJ32010Tg,JGJ32010PTDF,DampRatio)

    def Set_JTGB022013(self,name,direction,peakAccel,Tg,Ci,Cs,dampRatio):
        """
        ---This function defines a JTG B02-2013 response spectrum function---
        inputs:
        name(str)-The name of an existing or new function
        direction(int)-This is 1, 2 or 3, indicating the response spectrum direction.1 = Horizontal,2 = Vertical-Rock
            3 = Vertical-Soil
        peakAccel(float)-The peak acceleration, A.
        Tg(float)-The characteristic ground period, Tg > 0.1. [s]
        Ci(float)-The importance coefficient.
        Cs(float)-The site soil coefficient.
        dampRatio(float)-The damping ratio for the function, 0 <= DampRatio < 1.
        """
        self.__Model.Func.FuncRS.SetJTGB022013(name,direction,peakAccel,Tg,Ci,Cs,dampRatio)

    def Set_CJJ1662011(self,name,direction,peakAccel,Tg,dampRatio):
        """
        ---This function defines a CJJ 166-2011 response spectrum function---
        inputs:
        name(str)-The name of an existing or new function.
        direction(int)-This is 1 or 2, indicating the response spectrum direction.1 = Horizontal,2 = Vertical
        peakAccel(float)-The peak acceleration, A.
        Tg(float)-The characteristic ground period, Tg > 0.1. [s]
        dampRatio(float)-The damping ratio for the function, 0 <= DampRatio < 1.
        """
        self.__Model.Func.FuncRS.SetCJJ1662011(name,direction,peakAccel,Tg,dampRatio)

    def Set_User(self,name,period,value,dampRatio):
        """
        ---This function defines a user response spectrum function.---
        inputs:
        name(str)-The name of an existing or new function.
        period(list)-This is a list that includes the period for each data point. [s]
        value(list)-This is a list that includes the function value for each data point.
        dampRatio(float)-The damping ratio for the function, 0 <= DampRatio < 1.
        """
        numberItems=len(period)
        self.__Model.Func.FuncRS.SetUser(name,numberItems,period,value,dampRatio)

class fun_TimeHistory:
    def __init__(self,Sapobj):
        """
        Passing in the parent class object directly is to avoid 
        getting only the last opened SAP2000 window when initializing the 
        parent class instance to get the model pointer in the subclass.
        """
        self.__Object = Sapobj._Object 
        self.__Model = Sapobj._Model

    def Set_User(self,name,myTime,value):
        """
        ---This function defines a user time history function.---
        inputs:
        name(str)-The name of an existing or new function
        myTime(list)-This is a list that includes the time for each data point. [s]
        value(list)-This is a list that includes the function value for each data point.
        """
        numberItems=len(myTime)
        self.__Model.Func.FuncTH.SetUser(name,numberItems,myTime,value)