import pandas as pd

import requests

from walk_app.ref.keys import REFRESH_KEY

open_data_url = "https://api.mobilitydatabase.org/v1/tokens"

headers = {
    'Content-Type': 'application/json',
}

json_data = {
    'refresh_token': f'[{REFRESH_KEY}]',
}

requests.get()

def get_access_token(ref_key = REFRESH_KEY):
    pass