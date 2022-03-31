import os
from twilio.rest import Client


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.account_sid = os.environ['twillio_account_sid']
        self.auth_token = os.environ['twillo_auth_token']

    def send_sms(self, code, min_price, date_from, date_to, link):
        print("enetered twillo")
        client = Client(self.account_sid, self.auth_token)
        # this body is kinda hardcoded, it can be done more automated by list comprehension
        body = f"\nCheap flight alert!\n" \
               f"Fly from OTP to: {code}\n" \
               f"Price: {min_price}Eur.\n" \
               f"From: {date_from} to {date_to}\n" \
               f"{link}"

        message = client.messages \
                    .create(
                    body=f"{body}",
                    from_='+13867533168',
                    to='+400727727397'
                )
    pass