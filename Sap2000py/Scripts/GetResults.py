import numpy as np
class GetResults:
    def __init__(self,Sapobj):
        """
        Get Results from Sap easily, you just need to relax
        """
        self.__Object = Sapobj._Object
        self.__Model = Sapobj._Model
        self._Sapobj = Sapobj

    def JointReact_by_Group(self,Name,Dealflag = True):
        """
        Get JointReaction by group and return a np.array:[F1,F2,F3,M1,M2,M3]
        input:
            Name(str):the Group's name you want to extract
            Dealflag(bool):
                if Dealflag = True, get the max absolute value of each item
                if Dealflag = False, return everything we got
        output:
        Namelist(list):Item Name List with order
        Result(ndarray):results in np.array
        """
        # get result by group name
        GroupElm = 2
        ret = self._Sapobj.Results.JointReact(Name,GroupElm)
        colstart,colend = 6,12
        if Dealflag:
            uniquelist,JointMaxReaction = deal_with_item(ret,colstart,colend)
            return uniquelist,JointMaxReaction
        else:
            return ret[1],ret[colstart:colend]
         
    def ElementForce_by_Group(self,Name,Dealflag = True):
        """
        Get ElementForce by group and return a np.array:[P,V2,V3,T,M2,M3]
        input:
            Name(str):the Group's name you want to extract
            Dealflag(bool):
                if Dealflag = True, get the max absolute value of each item
                if Dealflag = False, return everything we got
        output:
        Namelist(list):Item Name List with order
        Result(ndarray):results in np.array:[P,V2,V3,T,M2,M3]
        """
        # get result by group name
        GroupElm = 2
        ret = self._Sapobj.Results.FrameForce(Name,GroupElm)
        colstart,colend = 8,14
        if Dealflag:
            uniquelist,JointMaxReaction = deal_with_item(ret,colstart,colend)
            return uniquelist,JointMaxReaction
        else:
            return ret[1],ret[colstart:colend]
    
    def ElementJointForce_by_Group(self,Name,Dealflag = True):
        """
        Get ElementJointForce by group and return a np.array:[F1,F2,F3,M1,M2,M3]
        input:
            Name(str):the Group's name you want to extract
            Dealflag(bool):
                if Dealflag = True, get the max absolute value of each item
                if Dealflag = False, return everything we got
        output:
        Namelist(list):Item Name List with order
        Result(ndarray):results in np.array:[F1,F2,F3,M1,M2,M3]
        """
        # get result by group name
        GroupElm = 2
        ret = self._Sapobj.Results.FrameJointForce(Name,GroupElm)
        colstart,colend = 7,13
        if Dealflag:
            uniquelist,JointMaxReaction = deal_with_item(ret,colstart,colend)
            return uniquelist,JointMaxReaction
        else:
            return ret[1],ret[colstart:colend]

    def LinkForce_by_Group(self,Name,Dealflag = True):
        """
        Get LinkForce by group and return a np.array:[P,V2,V3,T,M2,M3]
        input:
            Name(str):the Group's name you want to extract
            Dealflag(bool):
                if Dealflag = True, get the max absolute value of each item
                if Dealflag = False, return everything we got
        output:
        Namelist(list):Item Name List with order
        Result(ndarray):results in np.array:[P,V2,V3,T,M2,M3]
        """
        # get result by group name
        GroupElm = 2
        ret = self._Sapobj.Results.LinkForce(Name,GroupElm)
        colstart,colend = 7,13
        if Dealflag:
            uniquelist,JointMaxReaction = deal_with_item(ret,colstart,colend)
            return uniquelist,JointMaxReaction
        else:
            return ret[1],ret[colstart:colend]

    def LinkJointForce_by_Group(self,Name,Dealflag = True):
        """
        Get LinkJointForce by group and return a np.array:[F1,F2,F3,M1,M2,M3]
        input:
            Name(str):the Group's name you want to extract
            Dealflag(bool):
                if Dealflag = True, get the max absolute value of each item
                if Dealflag = False, return everything we got
        output:
        Namelist(list):Item Name List with order
        Result(ndarray):results in np.array:[F1,F2,F3,M1,M2,M3]
        """
        # get result by group name
        GroupElm = 2
        ret = self._Sapobj.Results.LinkJointForce(Name,GroupElm)
        colstart,colend = 7,13
        if Dealflag:
            uniquelist,JointMaxReaction = deal_with_item(ret,colstart,colend)
            return uniquelist,JointMaxReaction
        else:
            return ret[1],ret[colstart:colend]

    def LinkDeformation_by_Group(self,Name,Dealflag = True):
        """
        Get LinkDeformation by group and return a np.array:[U1,U2,U3,R1,R2,R3]
        input:
            Name(str):the Group's name you want to extract
            Dealflag(bool):
                if Dealflag = True, get the max absolute value of each item
                if Dealflag = False, return everything we got
        output:
        Namelist(list):Item Name List with order
        Result(ndarray):results in np.array:[U1,U2,U3,R1,R2,R3]
        """
        # get result by group name
        GroupElm = 2
        ret = self._Sapobj.Results.LinkDeformation(Name,GroupElm)
        colstart,colend = 6,12
        if Dealflag:
            uniquelist,JointMaxReaction = deal_with_item(ret,colstart,colend)
            return uniquelist,JointMaxReaction
        else:
            return ret[1],ret[colstart:colend]


def deal_with_item(results,colstart,colend):
    reaction = np.transpose(np.array(results[colstart:colend]))
    # get all item in the out put
    itemtext = results[1]
    # Get Item Name List with order
    uniquelist = sorted(list(set(itemtext)))
    # find duplicates
    indexdict = find_duplicates(itemtext)
    MaxReaction = np.zeros((len(uniquelist),reaction.shape[1]))
    for item in uniquelist:
        num = uniquelist.index(item)
        itemreaction = reaction[indexdict[item],:]
        MaxReaction[num,:] = np.max(np.fabs(itemreaction),0)
    return uniquelist,MaxReaction



def find_duplicates(lst):
    """
    ---find duplicate items and put them in a dict---
    input(list)-1 by N list
    output(dict)
    """
    index_all={}
    for i in range(len(lst)):
        target=lst[i]
        index_=[] # initialize a position list
        for index,nums in enumerate(lst):
            if nums==target:
                index_.append(index)
        index_all[target]=index_
    return index_all