from loguru import logger
from collections import namedtuple

class ShouldNotInstantiateError(Exception):
    pass

class SapBase(object):
    """Base class for all Sap2000 scripts"""
    
    def __init__(self):
        def __init__(self):
            logger.error('EZOpsMaterial is a abstract class!Should not be instantiated!')
            raise ShouldNotInstantiateError('Abstract class EZOpsMaterial accidentally instantiated!')
        
    @property
    @staticmethod
    def NODE2(self)-> namedtuple:
        """
        2D Node namedtuple Parameters:
            tag: int, node tag
            x: float, x coordinate
            y: float, y coordinate
        """
        Node = namedtuple('Node', ['tag', 'x', 'y'], defaults=[0, 0.0, 0.0])
        return Node
    
    @property
    @staticmethod
    def NODE3(self)-> namedtuple:
        """
        3D Node namedtuple Parameters:
            tag: int, node tag
            x: float, x coordinate
            y: float, y coordinate
            z: float, z coordinate
        """
        Node = namedtuple('Node', ['tag', 'x', 'y', 'z'], defaults=[0, 0.0, 0.0, 0.0])
        return Node