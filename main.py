import time

import requests
from datetime import datetime
import smtplib

MY_EMAIL = "your_email"
PASSWORD = "your_password" # You should get this from the settings of ur gmail account.

MY_LAT = 40.035073
MY_LONG = 28.413278
while True:
    time.sleep(60)
    response = requests.get(url = "http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()
    longitude = float(data["iss_position"]["longitude"])
    latitude = float(data["iss_position"]["latitude"])

    #Your position is within +5 or -5 degrees of ISS position.
    iss_longtiude_range = range(int(MY_LONG)-5,int(MY_LONG)+5)
    iss_latitude_range = range(int(MY_LAT)-5,int(MY_LAT)+5)


    iss_positions = (longitude,latitude)

    parameters = {
        "lat" : MY_LAT,
        "long" : MY_LONG,
        "formatted" : 0
    }
    response = requests.get(url = "https://api.sunrise-sunset.org/json", params = parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    if (longitude in iss_longtiude_range and latitude in iss_latitude_range) and (time_now.hour > sunset and time_now.hour < sunrise):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user = MY_EMAIL, password= PASSWORD)
            connection.sendmail(from_addr= MY_EMAIL
                                ,to_addrs= to_where@gmail.com
                                ,msg = "Subject:Look UP\n\nThe ISS is above you in the sky")




