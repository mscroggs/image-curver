class Point(object):
    def __init__(self, *coords):
        self.coords = tuple(float(i) for i in coords)
        # TODO: take all this hacking out of point
        self._twist = None
        self._width = None
        self._angle = None
        self._resolution = None

    def set_resolution(self, resolution):
        self._resolution = resolution

    def resolution(self):
        return self._resolution

    def set_twist(self, *twist):
        self._twist = twist

    def twist(self, n=None):
        if n is None:
            return self._twist
        return self._twist[n]

    def set_angle(self, *angle):
        self._angle = angle

    def angle(self, n=None):
        if n is None:
            return self._angle
        return self._angle[n]

    def set_width(self, *width):
        self._width = width

    def width(self, n=None):
        if n is None:
            return self._width
        return self._width[n]

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

    def __len__(self):
        return len(self.corners)

    def add_edge(self, edge):
        n = self.argmin(lambda x:norm(edge[0]-x))
        m = self.argmin(lambda x:norm(edge[-1]-x))
        if m in [n+1,n+2]:
            self.corners = self.corners[:m] + edge + self.corners[m:]
        elif n in [m+1,m+2]:
            self.corners = self.corners[:n] + edge[::-1] + self.corners[n:]
        elif n in [0,1]:
            self.corners = self.corners + edge[::-1]
        elif m in [0,1]:
            self.corners = self.corners + edge
        else:
            if n+1<len(self) and norm(edge[-1]-self[n+1]) < 3:
                self.corners = self.corners[:n+1] + edge + self.corners[n+1:]
            elif norm(edge[-1]-self[n-1]) < 3:
                self.corners = self.corners[:n] + edge[::-1] + self.corners[n:]
            elif m+1<len(self) and norm(edge[0]-self[m+1]) < 3:
                self.corners = self.corners[:m-1] + edge[::-1] + self.corners[m-1:]
            elif norm(edge[0]-self[m-1]) < 3:
                self.corners = self.corners[:m] + edge + self.corners[m:]
            elif n+2<len(self) and norm(edge[-1]-self[n+2]) < 3:
                self.corners = self.corners[:n+2] + edge + self.corners[n+2:]
            elif norm(edge[-1]-self[n-2]) < 3:
                self.corners = self.corners[:n] + edge[::-1] + self.corners[n:]
            elif m+2<len(self) and norm(edge[0]-self[m+2]) < 3:
                self.corners = self.corners[:m-2] + edge[::-1] + self.corners[m-2:]
            elif norm(edge[0]-self[m-2]) < 3:
                self.corners = self.corners[:m] + edge + self.corners[m:]
            else:
                print("WARNING:",m,n)
                pass #raise ValueError

    def point_pairs(self):
        return zip(self.corners[:-1],self.corners[1:])

    def __getitem__(self, n):
        return self.corners[n]

    def front(self):
        if self._front is not None:
            return self._front
        n = self.normal()
        if n.dot(Point(1,-1,0)) < 0:
            return False
        return True

    def normal(self):
        a = self[0]
        b = self[2]
        c = self[-3]
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
            return 0,0,100,"%"
        if self.color == "c":
            return 0,100,100,"%"
        if self.color == "m":
            return 100,0,100,"%"
        if self.color == "y":
            return 100,100,0,"%"

    def min(self, f=norm):
        return min(f(point) for point in self.corners)

    def max(self, f=norm):
        return max(f(point) for point in self.corners)

    def argmin(self, f=norm):
        i,m = None,None
        for p,point in enumerate(self.corners):
            if m is None or f(point) < m:
                i,m = p, f(point)
        return i

    def argmax(self, f=norm):
        i,m = None,None
        for p,point in enumerate(self.corners):
            if m is None or f(point) > m:
                i,m = p, f(point)
        return i

    def center(self):
        return Point(*[sum(p[i] for p in self.corners[:-1])/len(self.corners[:-1]) for i in range(3)])

    def __unicode__(self):
        return "Polygon{" + "->".join(str(i) for i in self.corners) + ", "+self.color+"}"

    def __str__(self):
        return self.__unicode__()

    def __iter__(self):
        return self.corners.__iter__()

