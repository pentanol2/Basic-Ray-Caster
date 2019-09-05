import numpy as np
from Ray import Ray
class Camera:
    def generateRay(self,x,y):
        pass

class OrthographicCamera(Camera):
    center = None
    direction = None
    up = None
    size = None
    horizontal = None
    cameraPlane = None
    def __init__(self,OrthCamConfig):
        self.center = OrthCamConfig['center']
        self.direction = OrthCamConfig['direction']
        self.up = OrthCamConfig['up']
        self.size = OrthCamConfig['size']
        self.horizontal = np.cross(self.direction,self.up)
        self.setCameraPlane()


    def generateRay(self,x,y):
        pt = np.matrix(self.center) + self.size * (x-0.5)*np.matrix(self.horizontal)+ self.size * (0.5-y)*np.matrix(self.up)
        pt = np.squeeze(np.asarray(pt))
        return Ray(pt,self.direction)
        #return Ray(pt,self.direction)

    def setCameraPlane(self):
        A = self.direction[0]
        B = self.direction[1]
        C = self.direction[2]
        D = -(A*self.center[0]+B*self.center[1]+C*self.center[2])
        self.cameraPlane = [A,B,C,D]

    # a distance function
    def distanceToCamera(self, spoint):
        return abs(spoint[0]*self.cameraPlane[0]+spoint[1]*self.cameraPlane[1]+spoint[2]*self.cameraPlane[2]+self.cameraPlane[3])/np.sqrt(np.square(self.cameraPlane[0])+np.square(self.cameraPlane[1])+np.square(self.cameraPlane[2]))


    def setCenter(self,C):
        center = C

    def setRadius(self,R):
        radius = R
    def getSize(self):
        return  self.size

'''
class PerspectiveCamera(Camera):
    center = None
    direction = None
    up = None
    size = None
    def __init__(self):

'''