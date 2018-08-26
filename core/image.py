from .geometry import Point, Polygon

class Image(object):
    def __init__(self, image_data, background="w"):
        self.data = image_data.strip().split("\n")
        self.width = len(self.data[0])
        self.height = len(self.data)
        self.set_resolution(1)
        self.background = background
        self.arrows = {"left":None,"right":None,"top":None,"bottom":None}

    def add_arrows(self, left=None, right=None, top=None, bottom=None):
        if left is not None:
            self.arrows["left"] = left
        if right is not None:
            self.arrows["right"] = right
        if top is not None:
            self.arrows["top"] = top
        if bottom is not None:
            self.arrows["bottom"] = bottom

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

    def polygons(self):
        output = [self.make_polygon(0,self.width,0,self.height-0.01, color=self.background)]
        # Non-background coloured
        for i,line in enumerate(self.data[::-1]):
            for j,pixel in enumerate(line):
                if i==0 or j==0 or i==self.height-1 or j==self.width-1:
                    output.append(self.make_polygon(j,1,i,1,color="w"))
                elif pixel != self.background:
                    output.append(self.make_polygon(j,1,i,1,color=pixel))
        # arrows
        asize = 1+min(self.height,self.width) // 8
        if self.arrows["left"] == "up":
            for i in range(asize):
                output.append(self.make_polygon(self.width-(asize-i)/2,asize-i,(self.height-asize)//2+i,1, color="r"))
        if self.arrows["left"] == "down":
            for i in range(asize):
                output.append(self.make_polygon(self.width-i/2,i,(self.height-asize)//2+i,1, color="r"))
        if self.arrows["right"] == "up":
            for i in range(asize):
                output.append(self.make_polygon(-(asize-i)/2,asize-i,(self.height-asize)//2+i,1, color="r"))
        if self.arrows["right"] == "down":
            for i in range(asize):
                output.append(self.make_polygon(-i/2,i,(self.height-asize)//2+i,1, color="r"))
        if self.arrows["top"] == "right":
            for i in range(asize):
                output.append(self.make_polygon((self.width-asize)//6+i,1,-(asize-i)/2,asize-i, color="b"))
        if self.arrows["top"] == "left":
            for i in range(asize):
                output.append(self.make_polygon((self.width-asize)//6+i,1,-i/2,i, color="b"))
        if self.arrows["bottom"] == "right":
            for i in range(asize):
                output.append(self.make_polygon((self.width-asize)//6+i,1,self.height-(asize-i)/2,asize-i, color="b"))
        if self.arrows["bottom"] == "left":
            for i in range(asize):
                output.append(self.make_polygon((self.width-asize)//6+i,1,self.height-i/2,i, color="b"))
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


