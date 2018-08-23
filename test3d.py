from core import Image,Twister,Projector

image = Image("bwbwbrb\n"
              "wbwbwbw\n"
              "bwbwbwb\n"
              "wbwbwbw\n"
              "bwbwbwb\n"
              "wbwbwbw\n"
              "bwbwbwb")

# Bend surface

from math import pi

for i in range(11):
    t = Twister(htwist=i*2*pi/10)
    polygons3d = t.twist_image(image)
    p = Projector()
    p.project_and_plot(polygons3d, filename="output/"+str(i)+".png")

for i in range(11):
    t = Twister(htwist=2*pi, vtwist=i*2*pi/10)
    polygons3d = t.twist_image(image)
    p = Projector()
    p.project_and_plot(polygons3d, filename="output/"+str(11+i)+".png")


