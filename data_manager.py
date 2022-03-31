import os
import requests


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.KEY = os.environ['sheety_key']
        self.retrieve_endpoint = "https://api.sheety.co/239abbffd62b4a4b0f6011af61ec9b42/copyOfFlightDeals/prices"
        self.header ={
            "Authorization": self.KEY
        }
        self.row = 2

    def retrieve_city_names(self):
        response = requests.get(url=self.retrieve_endpoint, headers=self.header)
        sheety_data = response.json()["prices"]
        #print(self.sheety_data)
        city_names = [item["city"] for item in sheety_data]
        return city_names

    def retrieve_city_codes(self):
        response = requests.get(url=self.retrieve_endpoint, headers=self.header)
        sheety_data = response.json()["prices"]
        city_codes = [item["iatacode"] for item in sheety_data]
        return city_codes

    def populate_city_codes(self, city_codes):
        id = 2
        for code in city_codes:
            #print(code)
            put_endpoint = f"https://api.sheety.co/239abbffd62b4a4b0f6011af61ec9b42/copyOfFlightDeals/prices/{id}"
            data = {
                "price": {
                    "iatacode": code  #does not populate values in google sheets if key is not all lower case :/
                }
            }
            response = requests.put(url=put_endpoint, json = data, headers=self.header)
            #print(response.text)
            id += 1

    def write_flight(self, date_from, date_to, price, link):

        put_endpoint = f"https://api.sheety.co/239abbffd62b4a4b0f6011af61ec9b42/copyOfFlightDeals/prices/{self.row}"
        data = {
            "price":{
                "from": date_from,
                "to": date_to,
                "price": price,
                "link": link
            }
        }
        response = requests.put(url=put_endpoint, headers=self.header, json=data)
        print(response.text)



