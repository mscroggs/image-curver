from .geometry import Point, Polygon

class Image(object):
    def __init__(self, image_data):
        self.data = image_data.strip().split("\n")
        self.width = len(self.data[0])
        self.height = len(self.data)
        self.set_resolution(10)

    def polygons(self):
        output = []
        for i,line in enumerate(self.data):
            for j,pixel in enumerate(line):
                corners = [Point(i,j)]
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
