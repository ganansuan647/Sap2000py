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
        all_joints = Sapobj.coord_joints if N0 else np.empty(shape=(0,Cartesian_coord.shape[1]))
        # Add new coords
        N,dim = Cartesian_coord.shape
        uniqueN = N
        for i in range(N):
            if (Cartesian_coord[i]==all_joints).all(-1).any():
                uniqueN -= 1  # point already exists
                print('coordinates ',Cartesian_coord[i],' duplicates! please check!')
            else:
                if dim==2:
                    Sapobj.Assign.PointObj.AddCartesian(Cartesian_coord[i,0],Cartesian_coord[i,1])
                if dim==3:
                    Sapobj.Assign.PointObj.AddCartesian(Cartesian_coord[i,0],Cartesian_coord[i,1],Cartesian_coord[i,2])
                all_joints = np.vstack((all_joints, Cartesian_coord[i]))
        Sapobj.coord_joints = all_joints
        print(uniqueN,' Joints Added to the Model!')
        if N != uniqueN:print(N-uniqueN,' joints duplicates! please check!')
        

