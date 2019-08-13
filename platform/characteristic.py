class Characteristic:

    def __init__(self, name: str, type: type, unit: str = None):
        self.name = name
        self.type = type
        self.unit = unit
        self.min_value = None
        self.max_value = None
        self.accuracy = None

    def set(self, min_value: float = None, max_value: float = None, accuracy: float = None):
        self.min_value = min_value
        self.max_value = max_value
        self.accuracy = accuracy
        return self


class Characteristics(object):
    temperature = Characteristic("temperature", float, "°C")
    humidity = Characteristic("humidity", float, "%")
    light = Characteristic("light", float, "lx")
    pressure = Characteristic("pressure", float, "hPa")
    boolean = Characteristic("boolean", bool)
