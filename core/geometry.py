class Point(object):
    def __init__(self, *coords):
        self.coords = tuple(float(i) for i in coords)

    def dot(self, other):
        return sum(i*j for i,j in zip(self,other))

    def cross(self, other):
        x,y,z = self
        a,b,c = other
        return Point(y*c-z*b,z*a-x*c,x*b-y*a)

    def as_tuple(self, xtransform=None, ytransform=None):
        if xtransform is None and ytransform is None:
            return self.coords
        if ytransform is None:
            return (xtransform(self.coords[0]), self.coords[1])
        if xtransform is None:
            return (self.coords[0], ytransform(self.coords[1]))
        return (xtransform(self.coords[0]), ytransform(self.coords[1]))

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

def norm(x):
    output = 0
    for i in x:
        output += i**2
    return output

class Polygon(object):
    def __init__(self, corners, color="w", front=None):
        self.dimension = len(corners[0])
        self.corners = corners
        self.color = color
        self._front = front

    def front(self):
        if self._front is not None:
            return self._front
        n = self.normal()
        if n.dot(Point(1,-1,0)) < 0:
            return False
        return True

    def normal(self):
        a = self.corners[0]
        b = self.corners[2]
        c = self.corners[-3]
        return (b-a).cross(c-a)

    def rgb_color(self):
        if self.color == "w":
            return 100,100,100,"%"
        if self.color == "k":
            return 0,0,0,"%"
        if self.color == "r":
            return 100,0,0,"%"
        if self.color == "g":
            return 0,100,0,"%"
        if self.color == "b":
            return 0,100,0,"%"
        if self.color == "c":
            return 0,100,100,"%"
        if self.color == "m":
            return 100,0,100,"%"
        if self.color == "y":
            return 100,100,0,"%"

    def min(self, f=norm):
        return min(f(point.coords) for point in self.corners)

    def max(self, f=norm):
        return max(f(point.coords) for point in self.corners)

    def center(self):
        return Point(*[sum(p[i] for p in self.corners[:-1])/len(self.corners[:-1]) for i in range(3)])

    def __unicode__(self):
        return "Polygon{" + "->".join(str(i) for i in self.corners) + ", "+self.color+"}"

    def __str__(self):
        return self.__unicode__()

    def __iter__(self):
        return self.corners.__iter__()

