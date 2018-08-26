from .geometry import Point, Polygon

class Image(object):
    def __init__(self, image_data, background="w"):
        self.data = image_data.strip().split("\n")
        self.width = len(self.data[0])
        self.height = len(self.data)
        self.set_resolution(1)
        self.background = background

    def make_polygon(self, x, xwidth, y, ywidth, color=None, front=None):
        if color == None:
            color = self.background
        from math import floor
        x2 = x+xwidth
        y2 = y+ywidth
        xticks = int(floor(self.resolution*xwidth))
        yticks = int(floor(self.resolution*ywidth))

        corners = [Point(x,y)]
        for k in range(xticks):
            corners.append(corners[-1]+(1/self.resolution,0))
        corners.append(Point(x2,y))
        for k in range(yticks):
            corners.append(corners[-1]+(0,1/self.resolution))
        corners.append(Point(x2,y2))
        for k in range(xticks):
            corners.append(corners[-1]-(1/self.resolution,0))
        corners.append(Point(x,y2))
        for k in range(yticks):
            corners.append(corners[-1]-(0,1/self.resolution))
        corners.append(Point(x,y))

        return Polygon(corners, color=color, front=front)

    def make_bg_polygon(self, x, xwidth, y, ywidth, color=None, htwist=0, vtwist=0, start=False, end=False, front=None):
        if color == None:
            color = self.background
        #if vtwist == 0:
        #    if x < self.width and x + xwidth > 0:
        #        return self.make_polygon(max(0,x), min(xwidth,self.width), y, ywidth, color=color, front=front)
        #    else:
        #        return None
        from math import floor, cos, pi, atan2,sin
        x2 = x+xwidth
        y2 = y+ywidth
        if start or htwist == 0:
            def xpre(y):
                return max(0,min(self.width, x))
        else:
            def xpre(y):
                return max(0,min(self.width, x - pi/4 + 2*self.width/htwist * atan2(1,sin(y/self.height*vtwist)-cos(y/self.height*vtwist))))
                #return max(0,min(self.width, x + y/2))
                #return max(0,min(self.width, x + self.width/htwist * pi * (1-cos(y/self.height*vtwist)/2)))
                #return max(0,min(self.width, x - self.height/vtwist * pi/4 * (cos(y/self.height*vtwist)-1)))
        x3 = xpre(y2)

        if end or htwist == 0:
            def xpost(y):
                return max(0,min(self.width, x2))
        else:
            def xpost(y):
                return max(0,min(self.width, x2 - pi/4 + 2*self.width/htwist * atan2(1,sin(y/self.height*vtwist)-cos(y/self.height*vtwist))))
                #return max(0,min(self.width, x2 + y/2))
                #return max(0,min(self.width, x2 + self.width/htwist * pi * (1-cos(y/self.height*vtwist)/2)))
                #return max(0,min(self.width, x2 - self.height/vtwist * pi/4 * (cos(y/self.height*vtwist)-1)))
        x4 = xpost(y2)

        xtopticks = int(floor(self.resolution*xwidth))
        yticks = int(floor(self.resolution*ywidth))
        xbottomticks = int(floor(self.resolution * (x4-x3)))

        corners = [Point(x,y)]
        for k in range(xtopticks):
            corners.append(corners[-1]+(1/self.resolution,0))
        corners.append(Point(x2,y))
        for k in range(yticks):
            x_, y_ = corners[-1]
            y_ += 1/self.resolution
            x_ = xpost(y_)
            corners.append(Point(x_,y_))
        corners.append(Point(x4,y2))
        for k in range(xbottomticks):
            corners.append(corners[-1]-(1/self.resolution,0))
        corners.append(Point(x3,y2))
        for k in range(yticks):
            x_, y_ = corners[-1]
            y_ -= 1/self.resolution
            x_ = xpre(y_)
            corners.append(Point(x_,y_))
        corners.append(Point(x,y))

        return Polygon(corners, color=color, front=front)

    def polygons(self, htwist=0, vtwist=0):
        #TODO: work out what to do when htwist == 0 and vtwist != 0
        from math import pi
        output = []
        if htwist > 7*pi/4:
            split_bg = [self.width*3*pi/(4*htwist),self.width*7*pi/(4*htwist)]
        elif htwist > 3*pi/4:
            split_bg = [self.width*3*pi/(4*htwist)]
        else:
            split_bg = []
        if htwist > 0:
            split_bg = [-self.width*pi/(4*htwist),0,self.width*3*pi/(4*htwist),self.width*7*pi/(4*htwist),self.width*11*pi/(4*htwist),self.width*15*pi/(4*htwist)]
            #split_bg = [self.width*3*pi/(4*htwist),self.width*7*pi/(4*htwist)]
        else:
            split_bg = [0,self.width]

        #output.append(self.make_bg_polygon(0,0,0,self.height,vtwist=vtwist,start=True, front=True))
        front = True
        col = "r"
        for i,j in zip(split_bg[:-1],split_bg[1:]):
            pg = self.make_bg_polygon(i,j-i,0,self.height,vtwist=vtwist,htwist=htwist, front=front, color=col)
            if pg is not None:
                output.append(pg)
                if front:
                    front = False
                else:
                    front = True
                if col == "r": col = "g"
                elif col == "g": col = "b"
                elif col == "b": col = "c"
                elif col == "c": col = "m"
                elif col == "m": col = "y"
                elif col == "y": col = "k"
        last = ([0]+split_bg)[-1]
        #output.append(self.make_bg_polygon(last,self.width-last,0,self.height,vtwist=vtwist,end=True, front=True, color="r"))


        # Non-background coloured
        for i,line in enumerate(self.data[::-1]):
            for j,pixel in enumerate(line):
                if pixel != self.background:
                    output.append(self.make_polygon(j,1,i,1,color=pixel))
        return output

    def set_resolution(self, resolution):
        self.resolution = resolution

    def plot(self, filename=None):
        import matplotlib.pylab as plt
        for polygon in self.polygons():
            plt.fill([i[0] for i in polygon],[i[1] for i in polygon], polygon.color)
        plt.axis("equal")
        if filename is None:
            plt.show()
        else:
            plt.savefig(filename)
        plt.clf()


