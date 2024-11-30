import argparse
from typing import Tuple

from HitlerFinder import multiprocess_search
from loguru import logger
from PagesFinder import PageNode, get_path_to_page, get_random_page


def args_pars() -> Tuple[int, int, PageNode]:
    parser = argparse.ArgumentParser(description="Hitler game parameters")
    parser.add_argument(
        "--depth",
        type=int,
        help="an integer for the max acceptable search depth ",
        default=6,
    )
    parser.add_argument(
        "--processed_numbers",
        type=int,
        help="an integer: number of processes",
        default=10,
    )
    parser.add_argument(
        "--url",
        type=str,
        help="The link from which the search will be started",
        default=get_random_page().url,
    )
    args = parser.parse_args()
    return args.depth, args.processed_numbers, PageNode(args.url)


def search_game(depth: int, processed_nums: int, start_page: PageNode) -> str:
    logger.info(f"Searching for Hitler from {start_page.url}")
    if start_page.url == "Adolf_Hitler":
        return "Already on Hitlers page"
    result = multiprocess_search(depth, processed_nums, start_page)
    if result:
        path = get_path_to_page(result)
        message = "".join([elem + " --> " if i != len(path) - 1 else elem for i, elem in enumerate(path)])
        return message
    else:
        logger.info(f"Nothing was find with depth: {depth} and process_number: {processed_nums}")
        return ""


if __name__ == "__main__":
    print(search_game(*args_pars()))
