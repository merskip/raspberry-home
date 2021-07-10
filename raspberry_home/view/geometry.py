from typing import cast


class Point:
    xy = property(lambda self: (self.x, self.y))

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @staticmethod
    def zero():
        return Point(0, 0)

    def __add__(self, other):
        return self.adding(x=other.x, y=other.y)

    def adding(self, x=0, y=0):
        return Point(self.x + x, self.y + y)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Point):
            return self.xy == other.xy
        return False

    def __str__(self) -> str:
        return "Point(%s, %s)" % (self.x, self.y)

    def __repr__(self) -> str:
        return "Point(%s, %s)" % (self.x, self.y)


class Size:
    xy = property(lambda self: (self.width, self.height))

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    @staticmethod
    def zero():
        return Size(0, 0)

    def adding(self, width=0, height=0):
        return Size(self.width + width, self.height + height)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Size):
            return self.xy == other.xy
        return False

    def __str__(self) -> str:
        return "Size(%s, %s)" % (self.width, self.height)

    def __repr__(self) -> str:
        return "Size(%s, %s)" % (self.width, self.height)


class EdgeInsets:

    def __init__(self, left: int = 0, top: int = 0, right: int = 0, bottom: int = 0):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    @staticmethod
    def symmetric(horizontal: int = 0, vertical: int = 0):
        return EdgeInsets(horizontal, vertical, horizontal, vertical)

    @staticmethod
    def all(value: int = 0):
        return EdgeInsets(value, value, value, value)

    @staticmethod
    def zero():
        return EdgeInsets(0, 0, 0, 0)


class Rect:
    min_x = property(lambda self: self.origin.x)
    max_x = property(lambda self: self.origin.x + self.size.width)
    min_y = property(lambda self: self.origin.y)
    max_y = property(lambda self: self.origin.y + self.size.height)

    xy = property(lambda self: ((self.min_x, self.min_y), (self.max_x, self.max_y)))

    def __init__(self, origin: Point, size: Size):
        self.origin = origin
        self.size = size

    @staticmethod
    def zero():
        return Rect(Point.zero(), Size.zero())

    def adding(self, x=0, y=0, width=0, height=0):
        return Rect(self.origin.adding(x, y), self.size.adding(width, height))
