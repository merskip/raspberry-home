from typing import List

from raspberry_home.platform.characteristic import Characteristic, Characteristics
from raspberry_home.platform.sensor import Sensor

import requests


class COVID19Monitor(Sensor):

    def __init__(self, id: int, name: str, country: str):
        super().__init__(id, name)
        self.country = country

    def get_characteristics(self) -> List[Characteristic]:
        return [Characteristics.virusCases]

    def get_value(self, characteristic: Characteristic) -> object:
        url = "https://corona.lmao.ninja/v3/covid-19/countries/" + self.country
        response = requests.get(url=url)
        json = response.json()
        cases = json['cases']
        today_cases = json['todayCases']
        return [cases, today_cases]

    def is_storable(self):
        return False
