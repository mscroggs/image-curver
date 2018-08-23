from .geometry import Point, Polygon

class Image(object):
    def __init__(self, image_data, background="w"):
        self.data = image_data.strip().split("\n")
        self.width = len(self.data[0])
        self.height = len(self.data)
        self.set_resolution(1)
        self.background = background

    def polygons(self):
        output = []
        corners = [Point(0,0)]
        for k in range(self.resolution*self.width):
            corners.append(corners[-1]+(1/self.resolution,0))
        for k in range(self.resolution*self.height):
            corners.append(corners[-1]+(0,1/self.resolution))
        for k in range(self.resolution*self.width):
            corners.append(corners[-1]-(1/self.resolution,0))
        for k in range(self.resolution*self.height):
            corners.append(corners[-1]-(0,1/self.resolution))
        output.append(Polygon(corners,color=self.background))
        for i,line in enumerate(self.data[::-1]):
            for j,pixel in enumerate(line):
                if pixel != self.background:
                    corners = [Point(j,i)]
                    for k in range(self.resolution):
                        corners.append(corners[-1]+(1/self.resolution,0))
                    for k in range(self.resolution):
                        corners.append(corners[-1]+(0,1/self.resolution))
                    for k in range(self.resolution):
                        corners.append(corners[-1]-(1/self.resolution,0))
                    for k in range(self.resolution):
                        corners.append(corners[-1]-(0,1/self.resolution))
                    output.append(Polygon(corners,color=pixel))
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


