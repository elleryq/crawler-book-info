"""
crawler-book-info
==========
License: MIT, see LICENSE for more details.
"""
import sys
from urllib.parse import urlparse
from crawler_book_info import tenlong, books


def main():
    if len(sys.argv) < 2:
        print("Need url.")
        sys.exit(-1)

    netloc_mapping = (
        ('tenlong.com.tw', tenlong.crawl_tenlong, tenlong.to_html),
        ('books.com.tw', books.crawl_books_com_tw, books.to_html),
    )
    url = sys.argv[1]
    o = urlparse(url)
    for netloc, crawl, to_html in netloc_mapping:
      if netloc in o.netloc:
        data = crawl(url)
        to_html(data)
        break


if __name__ == "__main__":
    main()
