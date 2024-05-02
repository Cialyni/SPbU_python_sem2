import asyncio
from typing import List

import requests
from bs4 import BeautifulSoup

QUOTES_ON_PAGE = 25
PAGES = 3487


def init() -> None:
    req = requests.get("https://башорг.рф")
    s = BeautifulSoup(req.text, "html.parser")
    PAGES = int(s.input["value"])


def get_best_quote(quote_nums: int = 10) -> List[str]:
    url = "https://башорг.рф/byrating/"
    quote_lst: List[str] = []
    pages_num = quote_nums // QUOTES_ON_PAGE + 1
    for page_num in range(1, pages_num + 1):
        page_url = url + str(page_num)
        req = requests.get(page_url)
        soup = BeautifulSoup(req.text, "html.parser")
        for tag in soup.find_all("div", class_="quote__body"):
            if len(quote_lst) >= quote_nums:
                break
            quote = ""
            for string in tag:
                if string.string is not None and string.string != "\n":
                    quote += string.string.lstrip().rstrip() + "\n"
            quote_lst.append(quote)
    return quote_lst


def get_last_quote(quote_nums: int = 10) -> List[str]:
    url = "https://башорг.рф/index/"
    quote_lst: List[str] = []
    pages_num = quote_nums // QUOTES_ON_PAGE + 1
    for page_num in range(PAGES, PAGES - pages_num, -1):
        page_url = url + str(page_num)
        req = requests.get(page_url)
        soup = BeautifulSoup(req.text, "html.parser")
        for tag in soup.find_all("div", class_="quote__body"):
            if len(quote_lst) >= quote_nums:
                break
            quote = ""
            for string in tag:
                if string.string is not None and string.string != "\n":
                    quote += string.string.lstrip().rstrip() + "\n"
            quote_lst.append(quote)

    return quote_lst


def get_random_quote(quote_nums: int = 10) -> List[str]:
    url = "https://башорг.рф/random?"
    quote_lst: List[str] = []
    pages_num = quote_nums // QUOTES_ON_PAGE + 1
    for page_num in range(1, pages_num + 1):
        page_url = url + str(page_num)
        req = requests.get(page_url)
        soup = BeautifulSoup(req.text, "html.parser")
        for tag in soup.find_all("div", class_="quote__body"):
            if len(quote_lst) >= quote_nums:
                break
            quote = ""
            for string in tag:
                if string.string is not None and string.string != "\n":
                    quote += string.string.lstrip().rstrip() + "\n"
            quote_lst.append(quote)

    return quote_lst
