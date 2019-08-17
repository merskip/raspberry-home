class Characteristic:

    def __init__(self, name: str, type: type, unit: str = None):
        self.name = name
        self.type = type
        self.unit = unit
        self.min_value = None
        self.max_value = None
        self.accuracy = None

    def set(self, min_value: float = None, max_value: float = None, accuracy: float = None):
        self.min_value = Characteristic._to_float(min_value)
        self.max_value = Characteristic._to_float(max_value)
        self.accuracy = Characteristic._to_float(accuracy)
        return self

    @staticmethod
    def _to_float(value):
        if isinstance(value, float) or value is None:
            return value
        elif isinstance(value, int):
            return float(value)
        else:
            raise ValueError("Expected float or int, got %s " % type(value))


class Characteristics(object):
    temperature = Characteristic("temperature", float, "°C")
    humidity = Characteristic("humidity", float, "%")
    light = Characteristic("light", float, "lx")
    pressure = Characteristic("pressure", float, "hPa")
    boolean = Characteristic("boolean", bool)
