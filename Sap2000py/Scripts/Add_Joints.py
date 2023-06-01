import numpy as np
class Add_Joints_Cartesian:
    def __init__(self,Sapobj,Cartesian_coord):
        """
        Add Joints by Cartesian coordinate system
        input Cartesian_coord(ndarray)-Nx3 array or Nx2 array in 2D model
        """
        self.__Object = Sapobj._Object
        self.__Model = Sapobj._Model
        N0 = Sapobj.coord_joints.shape[0] if 'coord_joints' in Sapobj.__dict__ else 0
        if N0:all_joints = Sapobj.coord_joints
        # Add new coords
        N,dim = Cartesian_coord.shape
        uniqueN = N
        for i in range(N):
            if (Cartesian_coord[i]==all_joints).all(-1).any():
                uniqueN -= 1  # point already exists
                print('coordinates ',Cartesian_coord[i],' duplicates! please check!')
            else:
                if dim==2:
                    Sapobj.Assign.PointObj.AddCartesian(Cartesian_coord[i,1],Cartesian_coord[i,2])
                if dim==3:
                    Sapobj.Assign.PointObj.AddCartesian(Cartesian_coord[i,1],Cartesian_coord[i,2],Cartesian_coord[i,3])
                all_joints = np.vstack((all_joints, Cartesian_coord[i]))
        Sapobj.coord_joints = all_joints
        print(uniqueN,' Joints Added to the Model!')
        if N != uniqueN:print(N-uniqueN,' joints duplicates! please check!')
        

