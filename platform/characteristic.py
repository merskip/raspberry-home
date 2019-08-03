

class Characteristic:

    def __init__(self, id: int, name: str, type: type, unit: str = None):
        self._id = id
        self.name = name
        self.type = type
        self.unit = unit

    @property
    def id(self):
        return self._id


class Characteristics(object):
    temperature = Characteristic(1, "temperature", float, "°C")
    humidity = Characteristic(2, "humidity", float, "%")
    light = Characteristic(3, "light", float, "lx")
    pressure = Characteristic(4, "pressure", float, "hPa")
    boolean = Characteristic(5, "boolean", bool)
