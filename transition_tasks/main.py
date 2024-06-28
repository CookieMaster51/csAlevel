"""Main"""

import pprint
import os
import requests

class GetError(Exception):
    """The program has failed a get request"""



def main() -> None:
    """Main"""
    print(get_ip())

    with open(os.path.join("transition_tasks", "openwm.token"), encoding="utf-8") as token:
        key = token.readline()

    place_to_check = input("What city/town are you in?\t")
    place_to_check.replace(" ", "+")
    lat_lon = get_lat_long(place_to_check, key)
    pprint.pprint(get_weather(lat_lon, key))

def get_weather(lat_long: tuple[float, float], api_key: str) -> dict:
    """Gets the weather JSON at the specified lat lon"""
    owm_url = "https://api.openweathermap.org/data/2.5/weather?"
    to_send = owm_url + f"lat={lat_long[0]}&lon={lat_long[1]}"
    to_send += f"&appid={api_key}"
    to_send += "&units=metric"
    response = requests.get(to_send, timeout=5)

    if response.status_code != 200:
        raise GetError
    else:
        data = response.json()
        return data

def get_ip() -> str:
    """Gets your public IP to guess where you are"""
    response = requests.get("https://checkip.amazonaws.com/", timeout=5)
    if response.status_code != 200:
        raise GetError
    else:
        ip = response.content.decode().replace("\n", "")
        location_response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        if location_response.status_code != 200:
            raise GetError
        else:
            location_response = location_response.json()
            city = location_response["city"]
            return city

def get_lat_long(name:str, api_key:str) -> tuple[float, float]:
    """Gets the latitude and longitude of a city"""
    omw_url = "http://api.openweathermap.org/geo/1.0/direct?q="
    to_send = omw_url + name + "&limit=5"
    to_send += f"&appid={api_key}"
    response = requests.get(to_send, timeout=5)


    if response.status_code != 200:
        raise GetError

    else:
        data = response.json()

        print("Was that:")
        for pos, place in enumerate(data):
            print(f"\t{pos} : {place["name"]}, {place["country"]}")

        answer = int(input()) # input query already asked for
        lat_long = (data[answer]["lat"], data[answer]["lon"])

        return lat_long




main()
