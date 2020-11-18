class Color:
    rgba = property(lambda self: (self.red, self.green, self.blue, round(self.alpha * 255)))

    def __init__(self, red: int, green: int, blue: int, alpha: float = 1.0):
        self.red = red % 256
        self.green = green % 256
        self.blue = blue % 256
        self.alpha = alpha

    def copy(self, red: int = None, green: int = None, blue: int = None, alpha: float = None):
        return Color(
            red if red is not None else self.red,
            green if green is not None else self.green,
            blue if blue is not None else self.blue,
            alpha if alpha is not None else self.alpha,
        )

    @staticmethod
    def from_hex(hex_str: str):
        hex_str = hex_str.lstrip('#')
        rgb = tuple(int(hex_str[i:i + 2], 16) for i in (0, 2, 4, 6))
        return Color(rgb[0], rgb[1], rgb[2], rgb[3] / 255)

    def to_hex(self) -> str:
        return "#%02x%02x%02x%02x" % (self.red, self.green, self.blue, round(self.alpha * 255) % 256)

    @staticmethod
    def clear(): return Color(255, 255, 255, 0.0)

    @staticmethod
    def black(): return Color(0, 0, 0)

    @staticmethod
    def white(): return Color(255, 255, 255)

    @staticmethod
    def red(): return Color(255, 0, 0)

    @staticmethod
    def green(): return Color(0, 255, 0)

    @staticmethod
    def blue(): return Color(0, 0, 255)

    @staticmethod
    def yellow(): return Color(255, 255, 0)

    @staticmethod
    def magnate(): return Color(255, 0, 255)

    @staticmethod
    def cyan(): return Color(0, 255, 255)
