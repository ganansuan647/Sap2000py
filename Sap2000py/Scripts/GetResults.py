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
        AbsReaction(ndarray):results in np.array:[F1,F2,F3,M1,M2,M3]
        MaxReaction(ndarray):results in np.array:[F1,F2,F3,M1,M2,M3]
        MinReaction(ndarray):results in np.array:[F1,F2,F3,M1,M2,M3]
        """
        # get result by group name
        GroupElm = 2
        ret = self._Sapobj.Results.Joint.React(Name,GroupElm)
        colstart,colend = 6,12
        if Dealflag:
            uniquelist,AbsReaction,MaxReaction,MinReaction = deal_with_item(ret,colstart,colend)
            return uniquelist,AbsReaction,MaxReaction,MinReaction
        else:
            return ret[1],ret[colstart:colend]

    def JointDispl_by_Group(self,Name,Dealflag = True):
        """
        Get JointDisplacement by group and return results in np.array: [U1, U2, U3, R1, R2, R3].
        
        input:
            Name (str): The group's name you want to extract displacements for.
            Dealflag (bool):
                if Dealflag = True, returns the max absolute value for each displacement and rotation component.
                if Dealflag = False, returns all displacement and rotation data retrieved.

        output:
            Namelist (list): Item name list in order.
            AbsReaction (ndarray): Absolute displacements and rotations in np.array: [U1, U2, U3, R1, R2, R3].
            MaxReaction (ndarray): Maximum displacements and rotations in np.array: [U1, U2, U3, R1, R2, R3].
            MinReaction (ndarray): Minimum displacements and rotations in np.array: [U1, U2, U3, R1, R2, R3].
        """
        # get result by group name
        GroupElm = 2
        ret = self._Sapobj.Results.Joint.Displ(Name,GroupElm)
        colstart,colend = 6,12
        if Dealflag:
            uniquelist,AbsReaction,MaxReaction,MinReaction = deal_with_item(ret,colstart,colend)
            return uniquelist,AbsReaction,MaxReaction,MinReaction
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
        AbsReaction(ndarray):results in np.array:[P,V2,V3,T,M2,M3]
        MaxReaction(ndarray):results in np.array:[P,V2,V3,T,M2,M3]
        MinReaction(ndarray):results in np.array:[P,V2,V3,T,M2,M3]
        """
        # get result by group name
        GroupElm = 2
        ret = self._Sapobj.Results.Frame.Force(Name,GroupElm)
        colstart,colend = 8,14
        if Dealflag:
            uniquelist,AbsReaction,MaxReaction,MinReaction = deal_with_item(ret,colstart,colend)
            return uniquelist,AbsReaction,MaxReaction,MinReaction
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
        AbsReaction(ndarray):results in np.array:[F1,F2,F3,M1,M2,M3]
        MaxReaction(ndarray):results in np.array:[F1,F2,F3,M1,M2,M3]
        MinReaction(ndarray):results in np.array:[F1,F2,F3,M1,M2,M3]
        """
        # get result by group name
        GroupElm = 2
        ret = self._Sapobj.Results.Frame.JointForce(Name,GroupElm)
        colstart,colend = 7,13
        if Dealflag:
            uniquelist,AbsReaction,MaxReaction,MinReaction = deal_with_item(ret,colstart,colend)
            return uniquelist,AbsReaction,MaxReaction,MinReaction
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
        AbsReaction(ndarray):results in np.array:[P,V2,V3,T,M2,M3]
        MaxReaction(ndarray):results in np.array:[P,V2,V3,T,M2,M3]
        MinReaction(ndarray):results in np.array:[P,V2,V3,T,M2,M3]
        """
        # get result by group name
        GroupElm = 2
        ret = self._Sapobj.Results.Link.Force(Name,GroupElm)
        colstart,colend = 7,13
        if Dealflag:
            uniquelist,AbsReaction,MaxReaction,MinReaction = deal_with_item(ret,colstart,colend)
            return uniquelist,AbsReaction,MaxReaction,MinReaction
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
        AbsReaction(ndarray):results in np.array:[F1,F2,F3,M1,M2,M3]
        MaxReaction(ndarray):results in np.array:[F1,F2,F3,M1,M2,M3]
        MinReaction(ndarray):results in np.array:[F1,F2,F3,M1,M2,M3]
        """
        # get result by group name
        GroupElm = 2
        ret = self._Sapobj.Results.LinkJointForce(Name,GroupElm)
        colstart,colend = 7,13
        if Dealflag:
            uniquelist,AbsReaction,MaxReaction,MinReaction = deal_with_item(ret,colstart,colend)
            return uniquelist,AbsReaction,MaxReaction,MinReaction
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
        AbsReaction(ndarray):results in np.array:[U1,U2,U3,R1,R2,R3]
        MaxReaction(ndarray):results in np.array:[U1,U2,U3,R1,R2,R3]
        MinReaction(ndarray):results in np.array:[U1,U2,U3,R1,R2,R3]
        """
        # get result by group name
        GroupElm = 2
        ret = self._Sapobj.Results.Link.Deformation(Name,GroupElm)
        colstart,colend = 6,12
        if Dealflag:
            uniquelist,AbsReaction,MaxReaction,MinReaction = deal_with_item(ret,colstart,colend)
            return uniquelist,AbsReaction,MaxReaction,MinReaction
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
    MinReaction = np.zeros((len(uniquelist),reaction.shape[1]))
    AbsReaction = np.zeros((len(uniquelist),reaction.shape[1]))
    try:
        sorted_indices = sorted(range(len(uniquelist)), key=lambda i: int(uniquelist[i].split('_')[1][1:]))
    except:
        sorted_indices = range(len(uniquelist))
    for i in sorted_indices:
        itemreaction = reaction[indexdict[uniquelist[i]],:]
        MaxReaction[i,:] = np.max(itemreaction,0)
        MinReaction[i,:] = np.min(itemreaction,0)
        AbsReaction[i,:] = np.max(np.fabs(itemreaction),0)
    return uniquelist,AbsReaction,MaxReaction,MinReaction



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