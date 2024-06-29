"""Does some weather stuff
Requirements: requests
made by Jan :)"""

import os
import requests

class GetError(Exception):
    """The program has failed a get request""" # If you get here its probably internet connection



def main() -> None:
    """Main, do not run from other libs"""

    with open(os.path.join("transition_tasks", "openwm.token"), encoding="utf-8") as token:
        key = token.readline() # gets the owm token

    guess, lat, long = get_ip_loc() # unpacks the tuple returned
    yes_no = input(f"Are you in {guess}? Y/N\n")

    if yes_no.upper() == "Y":
        lat_lon = (lat, long) # passes in the parameters given by the IP api
    elif yes_no.upper() == "N":
        place_to_check = input("What city/town are you in?\t")
        place_to_check.replace(" ", "+")
        lat_lon = get_lat_long(place_to_check, key)
    else:
        print("NOT Y or N")
        raise NotImplementedError # I could add a while loop but this is already too long

    weather = get_weather(lat_lon, key)
    wind_speed = weather["wind"]["speed"] # gets stuff from the JSON
    temp = weather["main"]["temp"]
    cond = weather["weather"][0]["description"]

    print(f"wind speed is {wind_speed} m/s, temperature is {temp} C and the weather is {cond}")
    print("ChatGPT thinks:")
    print(chat_gpt_opinion(temp, wind_speed, cond, "openAI.token"))

def get_weather(lat_long: tuple[float, float], api_key: str) -> dict:
    """Gets the weather JSON at the specified lat lon"""
    owm_url = "https://api.openweathermap.org/data/2.5/weather?"
    to_send = owm_url + f"lat={lat_long[0]}&lon={lat_long[1]}" # Adds in the information to send
    to_send += f"&appid={api_key}"
    to_send += "&units=metric" # Otherwise it sends degrees kelvin
    response = requests.get(to_send, timeout=5)

    if response.status_code != 200:
        raise GetError
    else:
        data = response.json()
        return data

def get_ip_loc() -> tuple[str, float, float]:
    """Gets your public IP to guess where you are, returns the name, lat and long in a tuple"""
    response = requests.get("https://checkip.amazonaws.com/", timeout=5)
    if response.status_code != 200:
        raise GetError
    else:
        ip = response.content.decode().replace("\n", "")
        # Asks where this IP is
        location_response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        if location_response.status_code != 200:
            raise GetError
        else:
            location_response = location_response.json()
            city = location_response["city"]
            lat = location_response["lat"]
            long = location_response["lon"]

            return (city, lat, long)

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
        for pos, place in enumerate(data): # Top 5 places with that name
            print(f"\t{pos} : {place["name"]}, {place["country"]}")

        answer = int(input()) # input query already printed
        lat_long = (data[answer]["lat"], data[answer]["lon"])

        return lat_long

def chat_gpt_opinion(temp: float, wind_speed: float, clouds: str, token_file_name: str) -> str:
    """Asks CHATGPT about what to wear in given conditions"""
    with open(os.path.join("transition_tasks", token_file_name), encoding="utf-8") as token_file:
        token = token_file.readline() # gets the openAI token

        start_prompt = "You are a helpful weather assistant that gives in depth answers \
about what you would wear in provided conditions without \
repeating already given information" # This is just a pain to do but works alright

        data = f"""{{
                    "model": "gpt-3.5-turbo",
                    "messages": [
                    {{
                        "role": "system",
                        "content": "{str(start_prompt)}"
                    }},
                    {{
                        "role": "user",
                        "content": "{temp}7C, {wind_speed}m/s wind, {clouds}"
                    }}
                    ]
                }}""" # Double {} to escape f-string
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        url = "https://api.openai.com/v1/chat/completions"

        response = requests.post(url, headers=headers, data=data, timeout=10)

        if response.status_code != 200:
            raise GetError
        else:
            unformated_response = str(response.json()["choices"][0]["message"]["content"])
            formatted = unformated_response.strip("\n'\"()") # gives it as a werid tuple but string
            return formatted

if __name__ == "__main__":
    main()
