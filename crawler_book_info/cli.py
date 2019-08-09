#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawler-book-info
==========
License: MIT, see LICENSE for more details.
"""
import argparse
from urllib.parse import urlparse
from crawler_book_info import tenlong, books
from crawler_book_info.generic import find_crawler


def main():
    parser = argparse.ArgumentParser(
        prog="crawler_book_info",
        description="crawler book info")
    parser.add_argument(
        '-o', '--output', type=argparse.FileType('w'),
        help="Output HTML filename",
        default="output.html")
    parser.add_argument(
        'url', nargs='?')
    args = parser.parse_args()

    url = args.url
    crawl, to_html = find_crawler(url)
    data = crawl(url)
    to_html(data, args.output)
    print("'{}' was crawled to '{}'".format(url, args.output.name))


if __name__ == "__main__":
    main()
