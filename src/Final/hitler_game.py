import argparse
import random

from src.Final.hitler_page_finder import *



def args_pars():
    parser = argparse.ArgumentParser(description="Hitler game parameters")
    parser.add_argument(
        "depth",
        metavar="Max acceptable depth",
        type=int,
        help="an integer for the max acceptable search depth ",
        nargs='?',
        default=2,
    )
    parser.add_argument(
        "processed_numbers",
        type=int,
        metavar="The number of processes involved ",
        help="an integer: number of processes",
        nargs='?',
        default=10,
    )
    parser.add_argument(
        "url",
        type=str,
        metavar="Start url",
        help="The link from which the search will be started",
        nargs='?',
        default=get_random_page(),
    )
    args = parser.parse_args()
    return args.depth, args.processed_numbers, args.url


def get_random_page():
    main_url = 'https://en.wikipedia.org/wiki/Main_Page'
    pages = url_scan(main_url)
    page = url_scan(main_url)[random.randint(0, len(pages))]
    return page


def main():
    depth, processed_nums, url = args_pars()
    pool_url = url_scan(url)
    result = bfs_with_multyprocces(pool_url, depth, processed_nums)
    if result[0] == '':
        print('Cant find Hitler with given params')
    else:
        print(result)


if __name__ == '__main__':
    main()


    #print(needed_to_find in pool_url)



