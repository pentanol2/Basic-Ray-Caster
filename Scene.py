from PIL import Image
import json as jsn
from Object3D import Group
from Object3D import Sphere
from Camera import OrthographicCamera
from Hit import Hit
class Scene:
    # a scene object generates a specefic scene for a specific json file
    scene = None
    resolution = None
    # extract the data from json
    s_background = []
    #s_group = []
    s_camera = []
    s_cam_center = []
    s_cam_direction = []
    s_cam_up = []
    s_cam_size = []
    s_cam_object = None
    img = None
    depth = None

    def __init__(self,sceneLocation,resolution):
        with open(sceneLocation) as file:
            self.scene = jsn.load(file)
        self.resolution = resolution
        self.set_scene_elements()


    def set_scene_elements(self):
        # extract the data from json
        self.s_background = self.scene['background'] # we exatract the background color array
        self.s_group = self.scene['group']   # we extrat the group array
        self.s_camera = self.scene['orthocamera'] # we extract the camera array
        self.s_cam_center = self.s_camera['center'] # we extract the center array
        self.s_cam_direction = self.s_camera['direction'] # we extract the direction array
        self.s_cam_up = self.s_camera['up'] # we extract the up vector array
        self.s_cam_size = self.s_camera['size'] # we extract the cam size array
        self.img = Image.new('RGB',self.resolution ,tuple(self.s_background['color']))
        self.depth = Image.new('L', self.resolution)

    def set_resolution(self,width, height):
        self.resolution = (width,height)

    def create_scene(self):
        # create a group from the scene objects
        self.s_group = Group(self.s_group)
        self.s_group.setObjects()
        self.set_up_camera(self.s_camera)
        self.nearest_fathest_object_to_camera(self.s_cam_object,self.s_group)
        self.s_group.setObjectsNearFar()
        # we pass the camera plan coeffs to the group class field cam_plan for use in calculating near and far
        self.s_group.cam_plan = self.s_cam_object.cameraPlane
        self.mapp = self.img.load()
        self.mapToDepth = self.depth.load()
        counter = 0
        y = self.resolution[1] - 1
        while 0 <= y:
            x = 0
            while x < self.resolution[0]:
                counter -= 1
                x_pos = x / self.resolution[0]
                y_pos = y / self.resolution[1]
                ray = self.s_cam_object.generateRay(x_pos, y_pos)
                hit = Hit()
                intersection = self.s_group.intersect(ray, hit, (0, 0))
                if intersection:
                    self.mapp[x, y] = intersection[0]
                    self.mapToDepth[x, y] = int(intersection[1])
                x += 1
            y -= 1


    def set_up_camera(self,cam_config = s_camera):
        # create a camera object from the camera array
        self.s_cam_object = OrthographicCamera(cam_config)

    def nearest_fathest_object_to_camera(self,camera, group):
        # find the nearest and the farthest object to camera
        far = 0
        near = 1000000
        nearest_object = None
        farthest_object = None
        nearest_point = 0;
        farthest_point = 10000
        objects = group.objects
        for x in range(len(objects)):
            if isinstance(objects[x], Sphere):
                center = objects[x].center
                if isinstance(camera, OrthographicCamera):
                    dist = camera.distanceToCamera(center);
                    if (dist > far):
                        far = dist
                        farthest_object = objects[x]
                    if (dist < near):
                        near = dist
                        nearest_object = objects[x]
        nearest_point = near - nearest_object.radius
        farthest_point = far + farthest_object.radius
        group.near = nearest_point
        group.far = farthest_point

    def display_scene(self):
        # display scene function, diplays the image and the depth image after ray tracing
        self.img.show()
        self.depth.show()

    def save_scene(self,filename, format = 'PNG',size = (360,360)):
        # save the image and the depth image after creating both
        self.img.save(filename+'.png',format)
        self.depth.save(filename+'_depth.png',format)
