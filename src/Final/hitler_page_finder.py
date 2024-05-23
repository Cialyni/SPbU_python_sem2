import copy
from concurrent.futures import ProcessPoolExecutor, as_completed
from math import ceil
from queue import Queue
from typing import List

import requests
from bs4 import BeautifulSoup

needed_to_find = "https://en.wikipedia.org/wiki/Adolf_Hitler"


def bfs_with_multyprocces(start_urls: List[str], max_depth: int, workers):
    with ProcessPoolExecutor(max_workers=workers) as executor:
        step = ceil(len(start_urls) / workers)
        fs = [
            executor.submit(
                bfs_hitler_search, start_urls[i * step : min((i + 1) * step, len(start_urls))], max_depth, i
            )
            for i in range(workers)
        ]
        minimal = [""] * 99999
        for f in as_completed(fs):
            result = f.result()
            if not result:
                continue
            if len(result) < len(minimal):
                minimal = result
        return minimal


def bfs_hitler_search(start_urls: List[str], max_depth: int, pack_num: int):
    print("Checking process number:", pack_num)
    que = Queue()
    for url in start_urls:
        que.put([url])
    while not que.empty():
        page = que.get()
        if page[-1] == needed_to_find:
            return page
        if len(page) > max_depth:
            break
        urls = url_scan(page[-1])
        for url_i in urls:
            que.put(page + [url_i])
    return None


def url_scan(current_url: str) -> List[str]:
    res = []
    reqs = requests.get(current_url)
    soup = BeautifulSoup(reqs.text, "html.parser")
    for link in soup.find_all("a"):
        wiki_suff = link.get("href")
        if wiki_suff and wiki_suff[0:6] == "/wiki/":
            res.append("https://en.wikipedia.org" + wiki_suff)
    return list(set(res))
