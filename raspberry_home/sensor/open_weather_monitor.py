from typing import List

import requests

from raspberry_home.platform.characteristic import Characteristic, Characteristics
from raspberry_home.platform.sensor import Sensor


class OpenWeatherMonitor(Sensor):

    def get_characteristics(self) -> List[Characteristic]:
        return [Characteristics.wind_speed.set(accuracy=0.1), Characteristics.wind_direction]

    def get_value(self, characteristic: Characteristic) -> object:
        url = "http://api.openweathermap.org/data/2.5/weather?q=Lublin&appid=41e4c8c15e16553fddc1103361723979"
        response = requests.get(url=url)
        json = response.json()

        if characteristic == Characteristics.wind_speed:
            return json["wind"]["speed"]
        elif characteristic == Characteristics.wind_direction:
            return json["wind"]["deg"]
        else:
            return None

