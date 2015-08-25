import re
from bs4 import BeautifulSoup

RE_URL_PLAIN = r'(https?://[^\s>]+)'

from pprint import pprint


def _extract_urls_text(content):
    urls = set()

    found = re.findall(RE_URL_PLAIN, content)

    for u in found:
        urls.add(u)

    return urls


def _extract_urls_html(body):
    urls = set()
    soup = BeautifulSoup(body, "lxml")

    for link in soup.find_all('a'):
        if link.get('href'):
            urls.add(str(link.get('href')))

    return urls


def extract_urls(content, html=False):
    urls = set()

    if content:
        if html:
            urls = _extract_urls_html(content)
        else:
            urls = _extract_urls_text(content)
    else:
        raise RuntimeError('no content to extract urls from')

    return urls
