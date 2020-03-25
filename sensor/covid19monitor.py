from typing import List

from platform.characteristic import Characteristic, Characteristics
from platform.sensor import Sensor

import requests


class COVID19Monitor(Sensor):

    def __init__(self, id: int, name: str, country: str):
        super().__init__(id, name)
        self.country = country

    def get_characteristics(self) -> List[Characteristic]:
        return [Characteristics.virusCases]

    def get_value(self, characteristic: Characteristic) -> object:
        url = "https://corona.lmao.ninja/countries/" + self.country
        response = requests.get(url=url)
        json = response.json()
        active = json['active']
        recovered = json['recovered']
        deaths = json['deaths']
        return [active, recovered, deaths]

    def is_storable(self):
        return False
