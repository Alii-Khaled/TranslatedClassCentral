from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import os


def get_all_htmls(pth):
    html_files = []
    for dir_path, _, filenames in os.walk(pth):
        for filename in filenames:
            if filename.endswith('.html'):
                html_files.append("file:///" + os.path.join(dir_path, filename))

    return html_files


def save_html(soup, url):
    url = url[8:]
    print(url)
    with open(url, "w", encoding='utf-8') as html:
        html.write(str(soup))


def modify_image_sources(url):
    req = Request(url)
    page = urlopen(req)
    soup = BeautifulSoup(page, "lxml")
    any_modification = False

    for img_tag in soup.findAll('img'):
        if img_tag.has_attr('data-src'):
            img_tag['src'] = img_tag.get('data-src')
            del img_tag['data-src']
            any_modification = True

    if any_modification:
        save_html(soup, url)


if __name__ == "__main__":
    path = "C:/Users/aliik/Desktop/pages/www.classcentral.com"
    html_files = get_all_htmls(path)

    for page in html_files:
        modify_image_sources(page)
