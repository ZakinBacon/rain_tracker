import requests
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
MY_TWILIO_PHONE_NUMBER = os.getenv("MY_TWILIO_PHONE_NUMBER")
MY_PHONE_NUMBER = os.getenv("MY_PHONE_NUMBER")
API_KEY = os.getenv("API_KEY")

san_diego_lat = 33.158092
san_diego_lon = -117.350594
# test_lat = 31.27
# test_lon = 83.30
parameters = {
    "lat": san_diego_lat,
    "lon": san_diego_lon,
    "appid": API_KEY,
    "cnt": "5",
    "units": "imperial"
}

response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=parameters)
response.raise_for_status()

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

future_weather_data = response.json()["list"][:5]
rain = False

for hour in range(0, len(future_weather_data)):
    weather_id = future_weather_data[hour]["weather"][0]["id"]
    if weather_id <= 781:
        rain = True

if rain == True:
    print("You need an umbrella")
    message = client.messages \
        .create(
        body="There is a High chance that it will rain today. Dont forget to bring an umbrella! ☔",
        from_=MY_TWILIO_PHONE_NUMBER,
        to=MY_PHONE_NUMBER
    )
    print(message.sid)
    print(message.status)
else:
    print("You are in the clear")
