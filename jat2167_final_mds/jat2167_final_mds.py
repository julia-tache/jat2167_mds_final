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

def music_newsletter():
    '''Returns a dataframe with information on album reviews from Pitchfork, including album title, artist, 
    genre, review link, score, and review preview. 
    
    The dataframe is converted to a CSV which is attached to an email. The email also includes recommendations of
    similar artists for the artists which received the top three best scores on Pitchfork at the moment when 
    this client function is run. This information is taken from the LastFm API, so make sure you have an
    API key to input when asked. You can get an API key at https://secure.last.fm/login?next=/api/account/create 
    
    You will be prompted to enter your email credentials in order to send the summary information to 
    yourself or others. 
    
    '''
    # retrieve the data 
    res = requests.get('https://pitchfork.com/reviews/albums/')
    reviews = BeautifulSoup(res.text, 'html.parser')

    review_data = reviews.find_all('div', {'class' : 'review'})

    # clean the data 
    title = [review_data[i].find('h2', {'class' : 'review__title-album'}) for i in range(len(review_data))]
    title = [str(i).strip('<h2 class="review__title-album"') for i in title]
    title = [str(i).strip('>') for i in title]
    title = [str(i).strip('</h2') for i in title]

    artists = [review_data[i].find('li') for i in range(len(review_data))]
    artists = [str(i).strip('<li>') for i in artists]
    artists = [str(i).strip('</') for i in artists]

    genre = [review_data[i].find('a', {'class' : 'genre-list__link'}) for i in range(len(review_data))]
    genre = [re.findall('genre=\w{2,}', str(i)) for i in genre]
    flatten = lambda t: [i for genre in t for i in genre]
    genre = flatten(genre)
    genre = [i.strip('genre') for i in genre]
    genre = [i.strip('=') for i in genre]

    URL = 'pitchfork.com'
    review_link = [URL + review_data[i].find('a').attrs['href'] for i in range(len(review_data))]
    
    reviews = str(reviews)
    score = re.findall('"display_rating":"\d.\d"', reviews)
    score = [float(i.strip('"display_rating":')) for i in score]

    preview = re.findall('seoDescription":"[\D|\d]{100,101}', reviews)
    preview = [i.strip('seoDessccription":') + '...' for i in preview]
    
    df = pd.DataFrame()
    df['Album Title'] = title
    df['Artist'] = artists 
    df['Genre'] = genre
    df['Score'] = score
    df['Review Preview'] = preview
    df['Review Link'] = review_link

    df.to_csv('music_picks.csv', index=False)

    top_3 = df.sort_values(by=['Score'], ascending=False)[0:3]
    top_3 = [i.replace(" ", "+") for i in top_3['Artist']]

    top = top_3[0]
    top_2 = top_3[1]
    top_3 = top_3[2]
    
    url_1 = "http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist="
    url_2 = "&"
    url_3 = "api_key="
    url_4 = "&format=json"
    API_key = input("Please enter your API key")
    
    full_url_1 = url_1 + top + url_2 + url_3 + API_key + url_4 
    full_url_2 = url_1 + top_2 + url_2 + url_3 + API_key + url_4 
    full_url_3 = url_1 + top_3 + url_2 + url_3 + API_key + url_4 
    
    r_top = requests.get(full_url_1)
    top_json = r_top.json()
    top_ten_artists = [i['name'] for i in top_json['similarartists']['artist']][0:5]
    top_ten_artists = ', '.join(top_ten_artists)
    
    r_top_2 = requests.get(full_url_2)
    top_2_json = r_top_2.json()
    top_2_ten_artists = [i['name'] for i in top_2_json['similarartists']['artist']][0:5]
    top_2_ten_artists = ', '.join(top_2_ten_artists)
    
    r_top_3 = requests.get(full_url_3)
    top_3_json = r_top_3.json()
    top_3_ten_artists = [i['name'] for i in top_3_json['similarartists']['artist']][0:5]
    top_3_ten_artists = ', '.join(top_3_ten_artists)
    
    top = top.replace("+", " ")
    top_2 = top_2.replace("+", " ")
    top_3 = top_3.replace("+", " ")

    subject = "Music Updates"
    body = f'''Hello there, music lover! Here are the 12 latest reviews on Pitchfork. 
    The top three artists of the day are {top}, {top_2}, and {top_3}. Digging their tunes? Check out these similar artists courtesy of LastFm: 

    If you like {top}, you might like {top_ten_artists}

    If you like {top_2}, you might like {top_2_ten_artists}

    If you like {top_3}, you might like {top_3_ten_artists}

    Enjoy, and keep it groovy!'''
    sender_email = input("Type in sender email")
    receiver_email = input("Type in receiving email")
    password = input("Type your password and press enter:")

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = "music_picks.csv"  # In same directory as script

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
    
def lastfm_artist_client():
    '''Returns a dataframe with information on artists from the LastFm API such as artist info, top 3 tracks,
        top albums, and similar artists. The dataframe is exported as a CSV. 
        
        The function will ask you for artist names and your LastFm API key. 
    '''
    artist = input("Please enter artist Names (SEPARATED BY COMMAS)")
    artist_list = artist.split(", ")
    artist = [i.replace(" ", "+").lower() for i in artist_list]
    
    API_key = input("Please enter your API key")
    
    url_artist_info1 = "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist="
    url_artist_info2 = "&"
    url_artist_info3 = "api_key="
    url_artist_info4 = "&format=json"
    
    url_top_tracks1 = "http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist="
    url_top_tracks2 = "&"
    url_top_tracks3 = "api_key="
    url_top_tracks4 = "&format=json"

    url_top_albums1 = "http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist="
    url_top_albums2 = "&"
    url_top_albums3 = "api_key="
    url_top_albums4 = "&format=json"

    url_get_similar1 = "http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist="
    url_get_similar2 = "&"
    url_get_similar3 = "api_key="
    url_get_similar4 = "&format=json"
    
    info_URLS = [url_artist_info1 + i + url_artist_info2 + url_artist_info3 + API_key + url_artist_info4 for i in artist]
    
    for url in info_URLS:
        try:
            response = requests.get(url) # If the response was successful, no Exception will be raised
            response.raise_for_status()
            response.json()['artist']['bio']['summary']
        except KeyError:
            print('Uh Oh! Did you make sure you typed in the artist names/your API key correctly?')
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred, is your API key correct?: {http_err}')
        else:
            print(f'{url} success!')
    
    r_artist_info = [requests.get(i) for i in info_URLS]
    artist_info_json = [i.json() for i in r_artist_info]
    artist_info = [i['artist']['bio']['summary'] for i in artist_info_json]
    artist_info = [i.strip() for i in artist_info]

    top_tracks_URLS = [url_top_tracks1 + i + url_top_tracks2 + url_top_tracks3 + API_key + url_top_tracks4 for i in artist]
    r_top_tracks = [requests.get(i) for i in top_tracks_URLS]
    top_tracks_json = [i.json() for i in r_top_tracks]
    top_tracks = [i['toptracks']['track'] for i in top_tracks_json]
    top_3 = [i[0:3] for i in top_tracks]
    top_3 = [j['name'] for i in top_3 for j in i]
    top_3 = [top_3[i:i+3] for i in range(0, len(top_3),3)]

    top_albums_URLS = [url_top_albums1 + i + url_top_albums2 + url_top_albums3 + API_key + url_top_albums4 for i in artist]
    r_top_albums = [requests.get(i) for i in top_albums_URLS]
    top_albums_json = [i.json() for i in r_top_albums]
    top_album = [i['topalbums']['album'][0] for i in top_albums_json]
    top_album = [i['name'] for i in top_album]

    similar_URLS = [url_get_similar1 + i + url_get_similar2 + url_get_similar3 + API_key + url_get_similar4 for i in artist]
    r_similar = [requests.get(i) for i in similar_URLS]
    similar_json = [i.json() for i in r_similar]
    similar_artists = [i['similarartists']['artist'] for i in similar_json]
    top_5 = [i[0:5] for i in similar_artists]
    top_5 = [j['name'] for i in top_5 for j in i]
    top_5 = [top_5[i:i+5] for i in range(0, len(top_5),5)]

    # put the data together in a dataframe 

    df_lastfm = pd.DataFrame()
    df_lastfm['Artist Name'] = artist_list
    df_lastfm['Artist Info'] = artist_info
    df_lastfm['Top 3 Tracks'] = top_3
    df_lastfm['Top Album'] = top_album
    df_lastfm['Similar Artists'] = top_5

    df_lastfm.to_csv('df_lastfm.csv', index=False)

    return df_lastfm