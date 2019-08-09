"""
crawler-book-info
==========
License: MIT, see LICENSE for more details.
"""
import argparse
from urllib.parse import urlparse
from crawler_book_info import tenlong, books


netloc_mapping = (
    ('tenlong.com.tw', tenlong.crawl_tenlong, tenlong.to_html),
    ('books.com.tw', books.crawl_books_com_tw, books.to_html),
)


def find_crawler(url):
    o = urlparse(url)
    for netloc, crawl, to_html in netloc_mapping:
        if netloc in o.netloc:
            return crawl, to_html
    return (None, None)
