

class Point(object):
    def __init__(self, *coords):
        self.coords = tuple(float(i) for i in coords)

    def __getitem__(self, n):
        return self.coords[n]

    def __add__(self, other):
        return Point(*[j+other[i] for i,j in enumerate(self.coords)])

    def __sub__(self, other):
        return Point(*[j-other[i] for i,j in enumerate(self.coords)])

    def __len__(self):
        return len(self.coords)

    def __unicode__(self):
        return "("+", ".join(str(i) for i in self.coords) + ")"

    def __str__(self):
        return self.__unicode__()

    def __iter__(self):
        return self.coords.__iter__()

class Polygon(object):
    def __init__(self, corners, color="w", distance=0):
        self.dimension = len(corners[0])
        self.corners = corners
        self.color = color
        self.distance = distance

    def center(self):
        return Point(*[sum(p[i] for p in self.corners[:-1])/len(self.corners[:-1]) for i in range(3)])

    def __unicode__(self):
        return "Polygon{" + "->".join(str(i) for i in self.corners) + ", "+self.color+"}"

    def __str__(self):
        return self.__unicode__()

    def __iter__(self):
        return self.corners.__iter__()

