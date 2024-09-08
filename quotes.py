import requests

API_KEY = "CVp+AeIR/bk5xYFh7ZdiAg==pULXxey5OMzllvgf"


def fetch_data(api_url):
    response = requests.get(api_url, headers={"X-Api-Key": API_KEY})
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}


def get_quote(category):
    api_url = f"https://api.api-ninjas.com/v1/quotes?category={category}"
    res = fetch_data(api_url)
    if "error" in res:
        return res
    return res[0]


# def get_limit
