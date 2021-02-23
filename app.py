import requests
import json
import ctypes
import time
from os import path
from random import randint

# unsplash api client_id and other configs
client_id = 'YOUR UNSPLASH CLIENT ID HERE' #=> (api.unsplash.com)
url = 'https://api.unsplash.com/search/photos?query=wallpaper&orientation=landscape&client_id=' + client_id
documents_path = path.expanduser('~\\Documents')
wallpaper_local_path = documents_path + '\\wallpaper-rnd.jpg'

# desktop background changes after every 1 hour (3600s)
time_interval = 3600

# keep app alive
while True:
    try:
        # get all wallpapers list
        data = requests.get(url)
        json_data = json.loads(data.text)

        # get number of wallpaper pages
        pages = int(json_data['total_pages'])

        # select a random page
        selected_page = randint(1, pages)
        url += '&page=' + str(selected_page)
        data = requests.get(url)
        json_data = json.loads(data.text)

        # select a random wallpaper from selected page
        items = len(json_data['results'])
        selected_item = randint(1, items)
        wallpaper_url = json_data['results'][selected_item]['urls']['full']
        # download and save selected wallpaper to documents
        download = requests.get(wallpaper_url)
        open(wallpaper_local_path, 'wb').write(download.content)

        # now change desktop background
        ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper_local_path , 0)

        # wait for next wallpaper
        time.sleep(time_interval)

    except:
        print('ERROR!')
        # try again after 5 seconds
        time.sleep(5)