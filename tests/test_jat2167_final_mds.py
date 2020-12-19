from jat2167_final_mds import __version__
from jat2167_final_mds import jat2167_final_mds

def test_version():
    assert __version__ == 0.1.0

import requests 
import os
import json

def tests():
    for url in ['https://pitchfork.com/reviews/albums/']:
        try:
            response = requests.get(url) # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            print('Success!')

    API_Key = input('API Key')

    URL = ['http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist=cher&api_key=' + API_Key + '&format=json']

    for url in URL:
        try:
            response = requests.get(url) # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            print('Success!')