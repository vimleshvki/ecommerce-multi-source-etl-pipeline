import requests
import pandas as pd


def read_customers_from_api(api_url):
    response = requests.get(api_url)

    if response.status_code == 200:
        customer_data = response.json()
        return pd.DataFrame(customer_data)
    else:
        raise Exception(f"API request failed with status code: {response.status_code}")