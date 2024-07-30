
class SapAnalyze:
    def __init__(self,Sapobj):
        """
        Choose cases to run and Analyze model
        """
        self.__Object = Sapobj._Object
        self.__Model = Sapobj._Model
        self.CaseFlags = {1:'Not run',2:'Could not start',3:'Not finished',4:'Finished'}

    def AddCases(self,CaseName="All"):
        """
        Add CaseName(list) to Analyze
        """
        self.__ChangeCases(CaseName,Run = True)

    def RemoveCases(self,CaseName="All"):
        """
        Remove CaseName(list) from Analyze
        """
        self.__ChangeCases(CaseName,Run = False)

    def __ChangeCases(self,Casename,Run:bool):
        """
        Change Cases in Casename(list) to Run(bool)
        """
        CaseRunFlags = self.__Model.Analyze.GetRunCaseFlag()

        # All CaseName
        if Casename == "All":
            Casename = CaseRunFlags[1]

        # Change type to list
        if type(Casename)==str:
            Casename = [Casename]

        nonameflag = False
        for Name in Casename:
            if Name not in CaseRunFlags[1]:
                print('CaseName "{}"dosen\'t exist!'.format(Name))
                nonameflag = True
            else:
                self.__Model.Analyze.SetRunCaseFlag(Name, Run)

        if nonameflag:
            print('You have entered the wrong CaseName, please check in the Caselist below:')
            print(CaseRunFlags[1])

    def RunAll(self,iter=3):
        """
        Run All cases set to run
        """
        CaseRunFlags = self.__Model.Analyze.GetRunCaseFlag()
        allflag = False
        i = 1
        while not allflag:
            self.__Model.Analyze.RunAnalysis()
            CaseStatus = self.GetCaseStatus()
            for Name in CaseRunFlags[1]:
                allflag = True
                index = CaseRunFlags[1].index(Name)
                CasetoRun = CaseRunFlags[2][index]
                Runflag = CaseStatus[Name]
                if  CasetoRun == True and Runflag != "Finished":
                    # if any case not finished, run again
                    allflag = False
                    print('Case: "{}" {} in iteration {}!!'.format(Name,Runflag,i))
                    
            i = i+1
            if i > iter:
                print('Analysis not finished in {} times, please check the cases above!:'.format(iter))
                break

    def DeleteResults(self,Casename="All"):
        """
        Delete Results of CaseName(list)
        """
        CaseStatus = self.__Model.Analyze.GetCaseStatus()

        # All CaseName
        if Casename == "All":
            Casename = CaseStatus[1]

        # Change type to list
        if type(Casename)==str:
            Casename = [Casename]

        nonameflag = False
        for Name in Casename:
            if Name not in CaseStatus[1]:
                print('CaseName "{}"dosen\'t exist!'.format(Name))
                nonameflag = True
            else:
                self.__Model.Analyze.DeleteResults(Name)

        if nonameflag:
            print('You have entered the wrong CaseName, please check in the Caselist below:')
            print(CaseStatus[1])

    def GetCaseStatus(self,Casename="All"):
        """
        Get Case Status, All cases by default
        """
        CaseStatus = self.__Model.Analyze.GetCaseStatus()

        # All CaseName
        if Casename == "All":
            Casename = CaseStatus[1]

        # Change type to list
        if type(Casename)==str:
            Casename = [Casename]

        caseflag = {}
        nonameflag = False
        for Name in Casename:
            if Name not in CaseStatus[1]:
                print('CaseName "{}"dosen\'t exist!'.format(Name))
                nonameflag = True
            else:
                index = CaseStatus[1].index(Name)
                stat = CaseStatus[2][index]
                caseflag[Name] = self.CaseFlags[stat]

        if nonameflag:
            print('You have entered the wrong CaseName, please check in the Caselist below:')
            print(CaseStatus[1])

        return caseflag