from os import walk
from os import path
from os import listdir
from os.path import isfile, join

dir_path = path.dirname(path.realpath(__file__))
print(dir_path)
json_files = [f for f in listdir(dir_path) if isfile(join(dir_path, f)) and f.endswith('.json')]
print(json_files)
x = 1
print('=== === === Scenes === === ===')
for file in json_files:
    print(str(x)+') '+ file.split('.')[0].format())
    x+=1

x = 0
while True :
    x = input('\nPlease choose scene number \nPress 0 to exit : ')
    try:
        x = int(x)
    except:
        print('Please input and integer')
    if int(x) in range(len(json_files)):
        break
    else:
        print('Wrong input!\nPlease try again: ')



'''
f = []
for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(filenames)
    break
'''
'''
from Scene import Scene
s1 = Scene('Scene1.json',(360,360))
s1.create_scene()
s1.display_scene()
s1.save_scene('Scene1.json')
print(Scene.s_camera)
print(s1.s_camera)
'''