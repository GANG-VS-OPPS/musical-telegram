import requests
from bs4 import BeautifulSoup as bs4
import re

PLATFORMS = ['spotify', 'apple', 'youtube', 'amazon']


def get_links(url):
    r = requests.post('https://songwhip.com', json={
        "url": url})
    soup = bs4(r.content, features="lxml")
    a = str(soup.body.p)[3:-4]
    a = eval(a.replace("null", "None").replace(
        "true", "True").replace("false", "False"))
    new_url = a["url"]
    r = requests.get(new_url)
    soup = bs4(r.content, features="lxml")
    b = str(soup.body.div.div.div.div)
    pattern = r'https://[\w\d#_/.?=:&;\-\']+(?=")'
    links = list(re.finditer(pattern, b))
    norm_list = [i.group(0) for i in links]
    platforms = {}

    for track_links in norm_list:
        for platform in PLATFORMS:
            if platform in track_links:
                platforms[platform] = track_links

    return platforms
