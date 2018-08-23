from .geometry import Point, Polygon

class Twister(object):
    def __init__(self, htwist=0, vtwist=0):
        self.htwist = htwist
        self.vtwist = vtwist

    def twist_image(self, image):
        return [self.twist_polygon(polygon, image.width, image.height) for polygon in image.polygons()]

    def twist_polygon(self, polygon, width, height):
        return Polygon([self.twist_point(point, width, height) for point in polygon], color=polygon.color)

    def twist_point(self, point, width, height):
        from math import pi,sin,cos
        xin,yin = point
        if self.htwist == 0:
            xout = point[0]
            ymid = 0
            zmid = point[1]
        else:
            xout = width/self.htwist * sin(self.htwist*xin/width)
            ymid = width/self.htwist * (1-cos(self.htwist*xin/width))
            zmid = yin
        if self.vtwist == 0:
            return Point(xout, ymid, zmid)

        yout = (ymid+height/self.vtwist) * cos(self.vtwist*zmid/height) - height/self.vtwist
        zout = (ymid+height/self.vtwist) * sin(self.vtwist*zmid/height)
        return Point(xout,yout,zout)



# Project into 2D image and plot
class Projector(object):
    def __init__(self):
        pass

    def project(self, polygons3d):
        return [self.project_polygon(polygon) for polygon in polygons3d]

    def project_polygon(self, polygon):
        from math import sqrt
        center = polygon.center()
        return Polygon([Point((x+y)*sqrt(3)/2,z+(y-x)/2) for x,y,z in polygon], color=polygon.color, distance=center[1]-center[0])

    def project_and_plot(self, polygons3d,filename=None):
        polygons2d = self.project(polygons3d)
        polygons2d.sort(key=lambda x:-x.distance)
        import matplotlib.pylab as plt
        for polygon in polygons2d:
            plt.fill([i[0] for i in polygon],[i[1] for i in polygon], polygon.color)
        plt.axis("equal")
        if filename is None:
            plt.show()
        else:
            plt.savefig(filename)
        plt.clf()


