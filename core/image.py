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

    def polygons(self):
        output = [self.make_polygon(0,self.width,0,self.height-0.01, color=self.background)]
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


