import random
from dataclasses import dataclass
from typing import Optional

import requests
from bs4 import BeautifulSoup

WIKI_PREF = "https://en.wikipedia.org/wiki/"


@dataclass
class PageNode:
    url: str
    parent: Optional["PageNode"] = None

    def __hash__(self) -> int:
        return hash(self.url)


def get_all_pages(current_page: PageNode) -> set[PageNode]:
    sub_pages: set[PageNode] = set()
    reqs = requests.get(WIKI_PREF + current_page.url)
    if reqs.status_code != 200:
        return set()
    soup = BeautifulSoup(reqs.text, "html.parser")
    for link in soup.find_all("a"):
        wiki_suff = link.get("href")
        if wiki_suff and wiki_suff[0:6] == "/wiki/":
            sub_pages.add(PageNode(wiki_suff[6:], current_page))
    return sub_pages


def get_path_to_page(node: PageNode) -> list[str]:
    return [node.url] if node.parent is None else get_path_to_page(node.parent) + [node.url]


def get_random_page() -> PageNode:
    reqs = requests.get(WIKI_PREF + "Special:Random")
    soup = BeautifulSoup(reqs.content, "html.parser")
    suff = " - Wikipedia"
    title = soup.title
    if title is not None:
        random_url = title.text[: -len(suff)]
        return PageNode(random_url)
    return PageNode("Main_Page")
