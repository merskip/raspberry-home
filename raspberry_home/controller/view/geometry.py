

class Point:
    xy = property(lambda self: (self.x, self.y))

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @staticmethod
    def zero():
        return Point(0, 0)

    def adding(self, x=0, y=0):
        return Point(self.x + x, self.y + y)


class Size:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    @staticmethod
    def zero():
        return Size(0, 0)

    def adding(self, width=0, height=0):
        return Size(self.width + width, self.height + height)


class Rect:
    min_x = property(lambda self: self.origin.x)
    max_x = property(lambda self: self.origin.x + self.size.width)
    min_y = property(lambda self: self.origin.y)
    max_y = property(lambda self: self.origin.y + self.size.height)

    def __init__(self, origin: Point, size: Size):
        self.origin = origin
        self.size = size

    @staticmethod
    def zero():
        return Rect(Point.zero(), Size.zero())

    def adding(self, x=0, y=0, width=0, height=0):
        return Rect(self.origin.adding(x, y), self.size.adding(width, height))
