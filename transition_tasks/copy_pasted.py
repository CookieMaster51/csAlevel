import requests

ISS_URL = "http://api.open-notify.org/iss-now.json"

GEOAPIFY_KEY = "c3c44ea46a8b4d0e9f9aacd3d3a5e512" # PUT YOUR API KEY HERE

response = requests.get(ISS_URL, timeout=10)

if response.status_code == 200:

    data = response.json()

    iss_data = data["iss_position"]

    latitude = iss_data["latitude"]

    longitude = iss_data["longitude"]

    print(f"The ISS is at latitude {latitude}, longitude {longitude}")

    geoapify_URL = "https://api.geoapify.com/v1/geocode/reverse?lat="

    geoapify_URL += latitude + "&lon=" + longitude

    geoapify_URL += "&apiKey=" + GEOAPIFY_KEY

    print(geoapify_URL)
    response = requests.get(geoapify_URL, timeout=10)

    if response.status_code == 200:

        data = response.json()["features"][0]

        properties = data["properties"]

        print(properties)

        name = properties["formatted"]

        distance = float(properties["distance"])

        print(f"Location: {name} {distance:.2f}km away")

    else:
        print("Error getting data from URL", response.status.code)

else:
    print("Error getting data from URL", response.status.code)
