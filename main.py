from Scene import Scene

def main():
    sc1 = Scene('scene1.json',(360,360))
    sc2 = Scene('scene2.json',(360,360))
    sc1.create_scene()
    sc2.create_scene()
    sc1.display_scene()
    sc2.display_scene()
    sc1.save_scene('scene1.png')
    sc2.save_scene('scene2.png')

main()