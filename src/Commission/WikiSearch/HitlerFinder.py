from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Optional

from loguru import logger

from PagesFinder import PageNode, get_all_pages

needed_to_find = "Adolf_Hitler"


def multiprocess_bfs( depth: int, processed_nums: int, start_page: PageNode,) -> Optional[PageNode]:

    with ProcessPoolExecutor(max_workers=processed_nums) as executor:
        cur_wave: set[PageNode] = set()
        next_wave: set[PageNode] = set()
        visited: set[PageNode] = set()
        cur_wave.add(start_page)
        for depth in range(depth):
            logger.info(f"Checking level: {depth}")
            futures = [executor.submit(get_all_pages, node, visited) for node in cur_wave]
            for future in as_completed(futures):
                deeper_pages = future.result()
                for page in deeper_pages:
                    if page.url not in visited:
                        visited.add(page)
                        next_wave.add(page)
                    else:
                        continue
                    if page.url == needed_to_find:
                        logger.info("FIND!")
                        for process in futures:
                            process.cancel()
                        return page
                    next_wave.add(page)
            cur_wave = next_wave
