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
        self._xlim = [None,None]
        self._ylim = [None,None]

    def set_limits(self, x=None, y=None):
        if x is not None:
            self._xlim = x
        if y is not None:
            self._ylim = y

    def project(self, polygons3d):
        return [self.project_polygon(polygon) for polygon in polygons3d]

    def project_polygon(self, polygon):
        ## TODO: split into two polygons if it goes round the back
        from math import sqrt
        center = polygon.center()
        return Polygon([Point((x+y)*sqrt(3)/2,z+(y-x)/2) for x,y,z in polygon], color=polygon.color, distance=center[1]-center[0])

    def project_and_plot(self, polygons3d,filename="output/output.png",height=None,width=None):
        polygons2d = self.project(polygons3d)
        polygons2d.sort(key=lambda x:-x.distance)

        import svgwrite

        size = (self._xlim[1]-self._xlim[0],self._ylim[1]-self._ylim[0])
        dwg = svgwrite.Drawing("output/temp.svg", size=size)
        for polygon in polygons2d:
            dwg.add(dwg.polygon([(i-(self._xlim[0],self._ylim[0])).as_tuple(ytransform=lambda y:size[1]-y) for i in polygon], fill=svgwrite.rgb(*polygon.rgb_color())))
        dwg.save()
        import cairosvg
        scale = 1
        if width is not None:
            scale = max(1+int(width//size[0]),scale)
        if height is not None:
            scale = max(1+int(height//size[1]),scale)
        cairosvg.svg2png(url='output/temp.svg', write_to=filename,parent_width=size[0],parent_height=size[1],scale=scale)
