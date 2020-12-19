# jat2167_final_mds 

![](https://github.com/julia-tache/jat2167_final_mds/workflows/build/badge.svg) [![codecov](https://codecov.io/gh/julia-tache/jat2167_final_mds/branch/main/graph/badge.svg)](https://codecov.io/gh/julia-tache/jat2167_final_mds) ![Release](https://github.com/julia-tache/jat2167_final_mds/workflows/Release/badge.svg) [![Documentation Status](https://readthedocs.org/projects/jat2167_final_mds/badge/?version=latest)](https://jat2167_final_mds.readthedocs.io/en/latest/?badge=latest)

This cookiecutter creates a boilerplate for Final Project for QMSS - Modern Data Structures, an API client which receives information from a popular music website and sends the user email updates.

## Installation

```bash
$ pip install -i https://test.pypi.org/simple/ jat2167_final_mds
```

## Features

LastFm API Client for Artist Info/Creating my Own Personal Music Newsletter 

This package returns the most current music reviews off the popular music-rating website, Pitchfork, in a convenient CSV format, while also providing the user with recommendations for similar artists for the top-rated artist of the day using the LastFm API. This information is put together in an easy-to-read, email format and the user has the option of sending this info to themselves or others! 

The package also works with the LastFm API to deliver information on artists based on the users' input. 

## Dependencies

import requests 
import os
import json
import re
from bs4 import BeautifulSoup
import pandas as pd

import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText    

## Usage

music_newsletter:

    Returns a dataframe with information on album reviews from Pitchfork, including album title, artist, 
    genre, review link, score, and review preview. 
    
    The dataframe is converted to a CSV which is attached to an email. The email also includes recommendations of
    similar artists for the artists which received the top three best scores on Pitchfork at the moment when 
    this client function is run. This information is taken from the LastFm API, so make sure you have an
    API key to input when asked. You can get an API key at https://secure.last.fm/login?next=/api/account/create 
    
    You will be prompted to enter your email credentials in order to send the summary information to 
    yourself or others. 
    
lastfm_artist_client:
    Returns a dataframe with information on artists from the LastFm API such as artist info, top 3 tracks,
    top albums, and similar artists. The dataframe is exported as a CSV. 
        
    The function will ask you for artist names and your LastFm API key. 

## Documentation

The official documentation is hosted on Read the Docs: https://jat2167-final-project-back-up-.readthedocs.io/en/latest/

## Contributors

We welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/julia-tache/jat2167_final_mds/graphs/contributors).

### Credits

This package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).
