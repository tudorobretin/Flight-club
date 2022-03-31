import os
import requests
from pprint import pprint


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.KEY = os.environ['tequila_key']
        self.endpoint = "https://tequila-api.kiwi.com/locations/query"
        self.search_endpoint = "https://tequila-api.kiwi.com/v2/search"

        self.header = {
            "apikey": self.KEY
        }
        self.IATA_codes = []
        self.price = None
        self.link = None

    def get_IATA_codes(self, city_names):
        for city in city_names:
            params = {
                "term": city
            }
            response = requests.get(url=self.endpoint, params=params, headers=self.header)
            self.IATA_codes.append(response.json()["locations"][0]["code"])
            # print(response.text)
        return self.IATA_codes

    def search_cheapest_flight(self, start, end, city):
        # print(city)
        # print(start.strftime("%d/%m/%Y"))
        # print(end.strftime("%d/%m/%Y"))
        params = {
            "fly_from": "OTP",
            "fly_to": city,
            "limit": 1,
            "date_from": start.strftime("%d/%m/%Y"),
            "date_to": end.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 3,
            "nights_in_dst_to": 3,
            "return_from": end.strftime("%d/%m/%Y"),
            "return_to": end.strftime("%d/%m/%Y"),
            "max_stopovers": 0
        }
        response = requests.get(url=self.search_endpoint, params=params, headers=self.header)
        raw_data = response.json()
        # pprint(raw_data["data"])
        try:
            self.price = raw_data["data"][0]["price"]
        except IndexError:
            print("no direct flights, searching with one layover")
            # self.price = 0
            # self.link = "No flights found"
            # pprint(raw_data["data"])
            try:
                params = {
                    "fly_from": "OTP",
                    "fly_to": city,
                    "limit": 1,
                    "date_from": start.strftime("%d/%m/%Y"),
                    "date_to": end.strftime("%d/%m/%Y"),
                    "nights_in_dst_from": 3,
                    "nights_in_dst_to": 3,
                    "return_from": end.strftime("%d/%m/%Y"),
                    "return_to": end.strftime("%d/%m/%Y"),
                    "max_stopovers": 1
                }
                response = requests.get(url=self.search_endpoint, params=params, headers=self.header)
                raw_data = response.json()
                self.price = raw_data["data"][0]["price"]
            except IndexError:
                try:
                    print("no flights with only one layover, searching with 2 layovers")  #TODO: doesnt work
                    params = {
                        "fly_from": "OTP",
                        "fly_to": city,
                        "limit": 1,
                        "date_from": start.strftime("%d/%m/%Y"),
                        "date_to": end.strftime("%d/%m/%Y"),
                        "nights_in_dst_from": 3,
                        "nights_in_dst_to": 3,
                        "return_from": end.strftime("%d/%m/%Y"),
                        "return_to": end.strftime("%d/%m/%Y"),
                        "max_stopovers": 1
                    }
                    response = requests.get(url=self.search_endpoint, params=params, headers=self.header)
                    raw_data = response.json()
                    self.price = raw_data["data"][0]["price"]
                except IndexError:
                    print(f"No flights to {city}")
                    self.price = 0
                    self.link = "No flights found"

        else:
            self.link = raw_data["data"][0]['deep_link']






