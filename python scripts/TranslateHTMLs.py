import string
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from bs4.element import Comment
from Image2Source import get_all_htmls, save_html
import translators as ts
from googletrans import Translator

def visible_tags(element):
    if isinstance(element, Comment):
        return False

    if element.parent.name in ['title', 'meta', '[document]', 'style', 'script', 'head']:
        return False
    return True


def get_text_from_html(body, url):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    translator = Translator()

    for text in texts:
        if visible_tags(text) and text.text.strip():
            tranlated_text = translator.translate(text.getText(), dest="hi", src="en")
            text.text = tranlated_text.text
            # print(text)

    # save_html(soup, url)


def translate_text_to_hindi(text):
    translated_page = ts.translate_text(query_text=text, translator="google", to_language="hi")
    return translated_page


if __name__ == '__main__':
    dir_path = "C:/Users/aliik/Desktop/pages/www.classcentral.com"
    html_url = "file:///C:/Users/aliik/Desktop/TranslatedClassCentral%20-%20Copy/www.classcentral.com/collection/ivy-league-moocs.html"
    req = Request(html_url)
    page = urlopen(req)
    result = get_text_from_html(page, html_url)
    print(result)
    """
    htmls = get_all_htmls(dir_path)
    for html_url in htmls:

        req = Request(html_url)
        page = urlopen(req)
        soup = BeautifulSoup(page, "lxml")
        soup = translate_html_page(soup)
        save_html(soup, html_url)
"""