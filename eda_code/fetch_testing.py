import pandas as pd
import requests

from walk_app.ref.api_keys import REFRESH_KEY

token_data_url = "https://api.mobilitydatabase.org/v1/tokens"
feed_data_url = "https://api.mobilitydatabase.org/v1/gtfs_feeds"

def get_access_token(ref_key = REFRESH_KEY):
    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
        'refresh_token': f"{REFRESH_KEY}",
    }
    response = requests.post(
    token_data_url, 
    headers=headers, 
    json=json_data
    )

    access_token = response.json()['access_token']
    
    return access_token

access_token = get_access_token()

test_params = {
    'offset': '0',
    'status': 'active',
    'is_official': 'true',
}

def pull_current_feeds(access_token, params=test_params):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(
        feed_data_url, 
        params=params, headers=headers
    )

    df = pd.DataFrame.from_dict(response.json())
    return df

feeds = pull_current_feeds(access_token=access_token)