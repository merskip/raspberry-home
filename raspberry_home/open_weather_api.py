import requests


class OpenWeatherApi:

    def __init__(self, city: str, app_id: str):
        self.city = city
        self.app_id = app_id

    def fetch(self) -> map:
        url = "http://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s" % (self.city, self.app_id)
        response = requests.get(url=url)
        return response.json()
