import os
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup


def get_htmls(index_directory):
    directory = index_directory.removesuffix('index.html')

    req = Request(index_directory)
    site = urlopen(req)
    soup = BeautifulSoup(site, 'lxml')
    soupA = soup.findAll('a')
    links = set()
    for s in soupA:
        link = s.get('href')
        if link and link.endswith(".html") and (not ('https://' in link)):
            links.add(os.path.join(directory, link))
    return links
