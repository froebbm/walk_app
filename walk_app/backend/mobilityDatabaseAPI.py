import requests
import datetime as dt
import pandas as pd
from walk_app.ref.api_keys import REFRESH_KEY
from walk_app.backend import gtfs

token_data_url = "https://api.mobilitydatabase.org/v1/tokens"
feed_data_url = "https://api.mobilitydatabase.org/v1/gtfs_feeds"

standard_params = {
    'offset': '0',
    'status': 'active',
    'is_official': 'true',
}

one_hour = dt.timedelta(hours=1)

def get_access_token(ref_key = REFRESH_KEY):
    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
        'refresh_token': f"{ref_key}",
    }
    
    response = requests.post(
        token_data_url, 
        headers=headers, 
        json=json_data
        )
    access_token = response.json()['access_token']
    
    return access_token

def pull_current_feeds(access_token, params=standard_params):
    headers = {
        # 'Content-Type': 'application/json',
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(
        feed_data_url, 
        params=params, 
        headers=headers
    )

    df = pd.DataFrame.from_dict(response.json())
    return df

def pull_feed(access_token, id):
    headers = {
        # 'Content-Type': 'application/json',
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    
    response = requests.get(
        f'{feed_data_url}/{id}', 
        # params=params, 
        headers=headers
    )

    feed_url = response.json()["latest_dataset"]['hosted_url']
    
    feed = gtfs.from_zip(feed_url)
    
    return feed
    
class openMobilityInterface:
    def __init__(self, feeds_param=standard_params):
        self._access_token = get_access_token()
        self._access_token_fetched_time = dt.datetime.now()
        self.__feeds = pull_current_feeds(access_token=self._access_token,
                                         params=feeds_param)
        self.__active_feed = None
    
    @property           
    def access_token(self):
        if dt.datetime.now() - self._access_token_fetched_time > one_hour:
            print("Access Token Expired, fetching new token!")
            self._access_token = get_access_token()
            return self._access_token
        
        else:
            return self._access_token
    
    @property
    def feeds(self):
        return self.__feeds
    
    @feeds.setter
    def feeds(self, new_param):
        self.__feeds = pull_current_feeds(
            access_token=self.access_token,
            params=new_param
        )
    
    @property
    def active_feed(self):
        if self.__active_feed == None:
            print("No active feed selected, please select feed.")
        else:
            return self.__active_feed
    
    @active_feed.setter
    def active_feed(self, id):
        self.__active_feed = pull_feed(
            access_token=self.access_token,
            id=id
        )

if __name__ == "__main__":
    from pprint import pprint
    omdb = openMobilityInterface()
    pprint(omdb.feeds)
    omdb.active_feed = "mdb-1846"
    pprint(omdb.active_feed)
