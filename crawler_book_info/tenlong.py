#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import logging
import requests
import sys
import urllib3

from crawler_book_info.common import to_html as common_to_html


# disable ssl warn message.
urllib3.disable_warnings()
logging.captureWarnings(True)


def get_data(book_url):
    try:
        res = requests.get(book_url)
        soup = BeautifulSoup(res.text)
        return soup, book_url

    except Exception as e:
        print(e)


def parser_book_title(data):
    title = data.title
    title = str(title).replace("<title>天瓏網路書店-", "")
    title = title.replace("</title>", "")
    return title


def parser_book_info(data):
    parser_item_info = data.find_all("div", class_="item-info")
    info = str(parser_item_info[0])
    info = info.replace('<i class="fa fa-eye fa-before"></i>', "")
    info = info.replace('<a class="item-preview btn btn-plain" href="#">', "")
    info = info.replace("預覽內頁</a>", "")
    return info


def parser_book_desc(data):
    parser_item_desc = data.find_all("div", class_="item-desc")
    book_desc = str(parser_item_desc[0])
    return book_desc


def parser_book_author(data):
    parser_item_desc = data.find_all("div", class_="item-desc")
    try:
        author = parser_item_desc[1]
    except IndexError:
        print("'item-desc[1]' is not found.")
        author = "Not found."
    finally:
        return author


def parser_book_outline(data):
    parser_item_desc = data.find_all("div", class_="item-desc")
    try:
        outline = parser_item_desc[2]
    except IndexError:
        print("'item-desc[2]' is not found.")
        outline = "Not found."
    finally:
        return outline


def to_html(data, fp):
    common_to_html(data, "tenlong.tmpl", fp)


def crawl_tenlong(book_url):
    try:
        # Get data.
        data = get_data(book_url)

        # Parser.
        book_title = parser_book_title(data[0])
        book_url = data[1]
        book_info = parser_book_info(data[0])
        book_desc = parser_book_desc(data[0])
        book_author = parser_book_author(data[0])
        book_outline = parser_book_outline(data[0])

        # Mapping the parser data to template.
        result = {
            "site_name": "天瓏書局",
            "title": book_title,
            "url": book_url,
            "info": [book_info],
            "desc": book_desc,
            "author": book_author,
            "outline": book_outline,
        }

        return result
    except Exception as e:
        print(e)


if __name__ == "__main__":
    arg = sys.argv[1]

    if arg.isdigit():
        # send get request and get reposoe.
        book_url = str("https://www.tenlong.com.tw/products/" + arg)
    else:
        book_url = str(arg)

    data = crawl_tenlong(book_url)
    to_html(data)
