import numpy as np


class Object3D:
    #color = None
    def intersect(self, Ray, Hit, tmin):
        pass



class Sphere(Object3D):
    radius = None
    center = None
    near = 0
    far = 1000

    def __init__(self, radius, center, color):
        self.radius = radius
        self.center = center
        self.color = color

    def intersect(self, Ray, Hit, tmin):
        grayValue = None
        origin = Ray.origin
        direction = Ray.direction
        C = np.dot((origin - self.center), (origin - self.center)) - self.radius * self.radius
        B = 2 * (np.dot(direction, (origin - self.center)))
        A = np.dot(direction, direction)

        solutions = np.roots([A, B, C])
        if not np.iscomplex(solutions[0]):
            solutions = np.abs(solutions)  # menda
            t = np.min(solutions)  # menda
            distance = t * np.matrix(direction) + np.matrix(origin)
            grayValue = (self.far - t) / (self.far - self.near)  # menda
            grayValue = np.rint(grayValue * 255)
            return t, grayValue  # menda
        else:
            return None


class Group(Object3D):
    objectArray = []
    cam_plan = None
    near = 0
    far = 100000000

    def __init__(self, objectArray):
        self.objectArray = objectArray
        self.objects = []

    def setObjects(self):
        x = 0
        #print('Objects     :' + str(self.objects))
        while x < len(self.objectArray):
            if self.objectArray[x]['sphere']:
                self.objects.append(
                    Sphere(self.objectArray[x]['sphere']['radius'], self.objectArray[x]['sphere']['center'],
                           self.objectArray[x]['sphere']['color']))
            x += 1

        print('Object Array:'+str(self.objectArray))
        print('Objects     :' + str(self.objects))
    def setObjectsNearFar(self):
        x = 0
        while x < len(self.objects):
            self.objects[x].near = self.near
            self.objects[x].far = self.far
            x+=1

    def intersect(self, ray, hit, tmin):
        x = 0
        minDistance = 10000
        grayShade = None
        index = None
        while x < len(self.objects):
            currentDistance = self.objects[x].intersect(ray, hit, tmin)
            x += 1
            if currentDistance:
                if currentDistance[0] < minDistance:
                    minDistance = currentDistance[0]
                    grayShade = currentDistance[1]
                    index = x - 1
            else:
                continue
        if minDistance != 10000:
            hit.color = self.objects[index].color
            return tuple(hit.color), grayShade
