"""
crawler-book-info
==========
License: MIT, see LICENSE for more details.
"""
import argparse
from urllib.parse import urlparse
from crawler_book_info import tenlong, books


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

    netloc_mapping = (
        ('tenlong.com.tw', tenlong.crawl_tenlong, tenlong.to_html),
        ('books.com.tw', books.crawl_books_com_tw, books.to_html),
    )

    url = args.url
    o = urlparse(url)
    for netloc, crawl, to_html in netloc_mapping:
        if netloc in o.netloc:
            data = crawl(url)
            to_html(data, args.output)
            print("'{}' was crawled to '{}'".format(url, args.output.name))
            break


if __name__ == "__main__":
    main()
