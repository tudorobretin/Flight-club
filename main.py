#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import os
from data_manager import DataManager
from flight_search import FlightSearch
import datetime as dt
from notification_manager import NotificationManager
from pprint import pprint

sheety = DataManager()
flights = FlightSearch()
notif = NotificationManager()

# city_names = sheety.retrieve_city_names()
# print(city_names)
city_names = ["Prague"]

city_codes = flights.get_IATA_codes(city_names)
# print(city_codes)

# sheety.populate_city_codes(city_codes)

for code in city_codes:

    until = dt.datetime(year=2022, month=6, day=12).date()
    today = dt.datetime.today().date()

    while today.weekday() != 4:
        today = today + dt.timedelta(days=1)
    start = today
    if start == dt.datetime.today().date():
        start += dt.timedelta(days=7)

    min_price = 10000
    while start < until:

        end = start + dt.timedelta(days=3)

        flights.search_cheapest_flight(start=start, end=end, city=code)

        price = flights.price
        link = flights.link
        print(price)
        print(link)

        if price < min_price:
            min_price = price
            winning_from = start.strftime("%d/%m/%Y")
            winning_to = end.strftime("%d/%m/%Y")
            winning_link = link

        start = start + dt.timedelta(days=7)

    if winning_link == "No flights found":
        winning_from = "No flights found"
        winning_to = "No flights found"

    if min_price < 40:
        notif.send_sms(code=code, min_price=min_price, date_from=winning_from, date_to=winning_to, link=link)

    code_dict = {}
    code_dict["1.Destination"] = code
    code_dict['2.Price'] = min_price
    code_dict['3.From'] = winning_from
    code_dict['4.To'] = winning_to
    code_dict['5.Link'] = winning_link
    winning_dict = {}
    winning_dict[f'{code}'] = code_dict
    pprint(winning_dict)

    #sheety.write_flight(date_from=winning_from, date_to=winning_to, price=min_price, link=winning_link)

    sheety.row += 1

    #missing part that sends email to sheety users





