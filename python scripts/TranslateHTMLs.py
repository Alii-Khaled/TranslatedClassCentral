import time
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from bs4.element import Comment
from Image2Source import save_html, get_all_htmls
import translators as ts
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from ReturnUniqueHTMLs import get_htmls

ALL_TEXT_TAGS = ['p', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'ul', 'li', 'i', 'a', 'ol']


def visible_tags(element):
    if isinstance(element, Comment):
        return False

    if element.parent.name in ['meta', '[document]', 'style', 'script', 'head']:
        return False
    return True


def is_not_empty(text):
    if text.getText().strip():
        return True
    return False


# It takes almost 3-6 minutes to translate a single .HTML file, which takes many hours but also works well,
# So I switched to use Google Api for the end2end HTML translation to save much time.
def translate_html_from_scratch(page):
    soup = BeautifulSoup(page, 'lxml')
    # translated = translate_text_to_hindi(soup.get_text(strip=True), from_lang="en", to_lang="hi")
    texts = soup.findAll(string=True)
    texts = filter(is_not_empty, texts)
    from_lang = "en"
    to_lang = "hi"

    for text in texts:
        translated_text = translate_text_to_hindi(text.getText(), from_lang, to_lang)
        text.replaceWith(str(translated_text))
    return soup


def setup_browser_driver():
    chrome_driver_path = r"C:\Users\aliik\Desktop\TranslatedClassCentral\python scripts\Chromedriver\chromedriver.exe"
    chrome_binary_path = r"C:\Users\aliik\AppData\Local\Google\Chrome\Application\chrome.exe"
    from_lang = "en"
    to_lang = "hi"

    custom_options = webdriver.ChromeOptions()
    prefs = {"translate_whitelists": {from_lang: to_lang}, "translate": {"enabled": "true"}}
    custom_options.add_experimental_option("prefs", prefs)
    custom_options.add_argument("--lang=hi")
    custom_options.binary_location = chrome_binary_path
    # custom_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # custom_options.add_argument("--headless")
    # custom_options.add_argument("--window-size=1920,1080")
    driver_service = Service(executable_path=chrome_driver_path)

    driver = webdriver.Chrome(service=driver_service, options=custom_options)

    # Chrome Browser Establishing settings in another thread.
    time.sleep(15)
    return driver


def translate_html_end2end(driver, page):
    driver.get(page)
    translated_page = driver.page_source
    return translated_page


def translate_text_to_hindi(text, from_lang, to_lang):
    # translated = ts.translate_html(html_text=text, translator="bing", from_languague=from_lang, to_language=to_lang)
    translated = ts.translate_text(query_text=text, translator="google", from_languague=from_lang, to_language=to_lang)
    return translated


if __name__ == '__main__':
    index_directory = r"C:/Users/aliik/Desktop/TranslatedClassCentralCopy/www.classcentral.com"

    # chrome_driver = setup_browser_driver()
    finished_pages = 0

    htmls = get_all_htmls(index_directory)
    htmls.sort(key=len)

    for html_url in htmls:
        req = Request(html_url)
        site = urlopen(req)
        translated_html_page = translate_html_from_scratch(site)

        # translated_html_page = translate_html_end2end(chrome_driver, html_url)
        save_html(translated_html_page, html_url)
        finished_pages += 1
        print("Finished page num.", finished_pages)

    # chrome_driver.close()
    print("Finished All pages !")
