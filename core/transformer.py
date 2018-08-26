from .geometry import Point, Polygon, norm

class Twister(object):
    def __init__(self, htwist=0, vtwist=0):
        self.htwist = htwist
        self.vtwist = vtwist

    def twist_image(self, image):
        from math import pi
        return [self.twist_polygon(polygon, image.width, image.height, image.resolution) for polygon in image.polygons()]

    def twist_polygon(self, polygon, width, height, resolution=None):
        return Polygon([self.twist_point(point, width, height, resolution) for point in polygon], color=polygon.color)

    def twist_point(self, point, width, height, resolution=None):
        from math import pi,sin,cos
        xin,yin = point
        hangle = self.htwist*xin/width
        vangle = self.vtwist*yin/height

        if self.htwist == 0:
            xout = xin
            ymid = 0
        else:
            xout = width/self.htwist * sin(hangle)
            ymid = width/self.htwist * (1-cos(hangle))
        dtheta = Point(cos(hangle), sin(hangle), 0)
        zmid = yin

        if self.vtwist == 0:
            point = Point(xout, ymid, zmid)
        else:
            yout = (ymid+height/self.vtwist) * cos(vangle) - height/self.vtwist
            zout = (ymid+height/self.vtwist) * sin(vangle)
            point = Point(xout,yout,zout)
        dphi = Point(sin(hangle)*sin(vangle),-cos(hangle)*sin(vangle),cos(vangle))

        point.set_twist(self.htwist, self.vtwist)
        point.set_width(width, height)
        point.set_angle(hangle, vangle)
        point.set_resolution(resolution)

        return point


# Project into 2D image and plot
class Projector(object):
    def __init__(self, h=None, v=None):
        self._xlim = [None,None]
        self._ylim = [None,None]
        self.set_view_angle(h, v)

    def set_view_angle(self, h=None, v=None):
        from math import sqrt
        if h is None:
            h = (sqrt(3)/2,sqrt(3)/2,0)
        if v is None:
            v = (-1/2,1/2,1)
        nh = norm(h)
        nv = norm(v)
        self.h = Point(*[i/nh for i in h])
        self.v = Point(*[i/nv for i in v])
        self.z = self.v.cross(self.h)

    def set_limits(self, x=None, y=None):
        if x is not None:
            self._xlim = x
        if y is not None:
            self._ylim = y

    def project(self, polygons3d):
        from math import pi, sin, cos, atan2, asin,tan,sqrt
        output = []
        for polygon in polygons3d:
            this = self.split_polygon(polygon)
            if type(this) is list:
                output += [self.project_polygon(p) for p in this]
            else:
                output.append(self.project_polygon(this))
        return output

    def split_polygon(self, polygon):
        from math import floor,pi
        point = polygon[0]
        h1, h2 = polygon.min(lambda x:x.angle(0)), polygon.max(lambda x:x.angle(0))
        v1, v2 = polygon.min(lambda x:x.angle(1)), polygon.max(lambda x:x.angle(1))
        if point.twist(0) > 0:
            hradius = point.width(0) / point.twist(0)
            htop,htop2 = self.get_twist_limits(v1)
            hbot,hbot2 = self.get_twist_limits(v2)
            if h1 < htop < h2 or h1 < htop2 < h2 or h1 < hbot < h2 or h1 < hbot2 < h2:
                poly0 = []
                poly1 = []
                poly2 = []
                poly3 = []
                for point in polygon:
                    hh1,hh2 = self.get_twist_limits(point.angle(1))
                    h = point.angle(0)
                    if h < hh1-pi:
                        poly0.append(point)
                    elif h < hh1:
                        poly1.append(point)
                    elif h < hh2:
                        poly2.append(point)
                    else:
                        poly3.append(point)
                # TODO(
                t = Twister(*point.twist())
                if point.twist(1) > 0:
                    vradius = point.width(1) / point.twist(1)
                    y1, y2 = vradius * v1, vradius * v2
                else:
                    y1, y2 = 0,0
                yticks = int(floor(point.resolution()*(y2-y1)))
                if point.twist(1) > 0:
                    edge0 = []
                    edge1 = []
                    edge2 = []
                    edge3 = []
                    added2 = False
                    done2 = False
                    done3 = False
                    for i in range(yticks+1):
                        hh1,hh2 = self.get_twist_limits(y1/vradius)
                        if h1 < hh1-pi < h2:
                            edge0.append(Point(hradius*(hh1-pi),y1))
                        if h1 < hh1 < h2:
                            edge1.append(Point(hradius*hh1,y1))
                        if h1 < hh2 < h2:
                            if done2:
                                edge3.append(Point(hradius*hh2,y1))
                            else:
                                edge2.append(Point(hradius*hh2,y1))
                                added2 = True
                        elif added2:
                            done2 = True
                        elif done2:
                            done3 = True
                        y1 += 1/point.resolution()
                    hh1,hh2 = self.get_twist_limits(y2/vradius)


                    edge0 = [t.twist_point(p, *point.width()) for p in edge0]
                    edge1 = [t.twist_point(p, *point.width()) for p in edge1]
                    edge2 = [t.twist_point(p, *point.width()) for p in edge2]
                    edge3 = [t.twist_point(p, *point.width()) for p in edge3]

                output = []
                if len(poly0) > 2:
                    poly0 = Polygon(poly0, color=polygon.color)
                    try:
                        if point.twist(1) > 0:
                            if len(edge0) > 2:
                                poly0.add_edge(edge0)
                        output.append(poly0)
                    except ValueError:
                        print(len(edge0))
                        print("0 missing")
                if len(poly1) > 2:
                    poly1 = Polygon(poly1, color=polygon.color)
                    try:
                        if point.twist(1) > 0:
                            if len(edge0) > 2:
                                poly1.add_edge(edge0)
                            if len(edge1) > 2:
                                poly1.add_edge(edge1)
                        output.append(poly1)
                    except ValueError:
                        print("1 missing")
                if len(poly2) > 2:
                    poly2 = Polygon(poly2, color=polygon.color)
                    try:
                        if point.twist(1) > 0:
                            if len(edge1) > 2:
                                poly2.add_edge(edge1)
                            if len(edge2) > 2:
                                poly2.add_edge(edge2)
                            if len(edge3) > 2:
                                poly2.add_edge(edge3)
                        output.append(poly2)
                    except ValueError:
                        print("2 missing")
                if len(poly3) > 2:
                    poly3 = Polygon(poly3, color=polygon.color)
                    try:
                        if point.twist(1) > 0:
                            if len(edge2) > 2:
                                poly3.add_edge(edge2)
                            if len(edge3) > 2:
                                poly3.add_edge(edge3)
                        output.append(poly3)
                    except ValueError:
                        print("3 missing")
                return output
        return polygon

    def get_twist_limits(self, v):
        from math import sin, cos, atan2, pi
        xtop = atan2(self.z[1]*cos(v)+self.z[2]*sin(v),self.z[0])
        xtop %= 2*pi
        return xtop,xtop+pi

    def project_polygon(self, polygon, color=None):
        from math import sqrt
        if color is None:
            color = polygon.color
        # TODO: The 2* here is a hack to make the image larger
        return Polygon([Point(2*point.dot(self.h), 2*point.dot(self.v)) for point in polygon],color=color, front=polygon.front())

    def project_and_plot(self, polygons3d,filename="output/output.png",height=None,width=None):
        polygons2d = self.project(polygons3d)

        import svgwrite

        size = (self._xlim[1]-self._xlim[0],self._ylim[1]-self._ylim[0])
        dwg = svgwrite.Drawing("output/temp.svg", size=size)
        front = []
        for polygon in polygons2d:
            if polygon.front():
                front.append(polygon)
            else:
                dwg.add(dwg.polygon([(i-(self._xlim[0],self._ylim[0])).as_tuple(ytransform=lambda y:size[1]-y) for i in polygon], fill=svgwrite.rgb(*polygon.rgb_color())))
        for polygon in front:
            dwg.add(dwg.polygon([(i-(self._xlim[0],self._ylim[0])).as_tuple(ytransform=lambda y:size[1]-y) for i in polygon], fill=svgwrite.rgb(*polygon.rgb_color())))
        dwg.save()
        import cairosvg
        scale = 1
        if width is not None:
            scale = max(1+int(width//size[0]),scale)
        if height is not None:
            scale = max(1+int(height//size[1]),scale)
        cairosvg.svg2png(url='output/temp.svg', write_to=filename,parent_width=size[0],parent_height=size[1],scale=scale)
