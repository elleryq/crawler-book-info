#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import importlib_resources as _resources
from jinja2 import Template, FileSystemLoader, Environment
import logging
import requests
import sys
import urllib3
import pangu

# disable ssl warn message.
urllib3.disable_warnings()
logging.captureWarnings(True)


def get_data(book_url):
    try:
        # send get request and get reposoe.
        res = requests.get(book_url)
        soup = BeautifulSoup(res.text)
        return soup, book_url
    except Exception as e:
        print(e)


def parser_book_title(data):
    title = data.title
    title = str(title).replace("<title>博客來-", "")
    title = title.replace("</title>", "")
    return title


def parser_book_full_title(data):
    parser_full_title = data.find_all("div", class_="mod type02_p002 clearfix")
    full_title = str(parser_full_title[0])
    full_title = full_title.replace('<div class="mod type02_p002', "")
    full_title = full_title.replace(' clearfix">', "")
    full_title = full_title.replace("</div>", "")
    return full_title


def parser_book_cover(data):
    parser_cover = data.find_all("img", itemprop="image")
    cover = str(parser_cover[0])
    cover = cover.split("https")
    cover = "https" + cover[1]
    cover = cover.split(".jpg")
    cover = cover[0] + ".jpg"
    return cover


def parser_book_info1(data):
    parser_info = data.find_all("div", class_="type02_p003 clearfix")
    info = str(parser_info[0])
    info = info.replace('<div class="type02_p003 clearfix">', "")
    info = info.replace('<span class="arrow"></span>', "")

    info = info.replace('<h4>已追蹤作者：<strong class="edit">', "")
    info = info.replace('[ <a href="" id="editTrace">修改</a>', "")
    info = info.replace(" ]</strong></h4>", "")
    info = info.replace('<ul id="list_traced"></ul>', "")
    info = info.replace('<ul class="list_trace" id="list_trace"></ul>', "")

    info = info.replace('<a class="type02_btn09"', "")
    info = info.replace(' href="javascript:saveTrace();">確定</a>', "")
    info = info.replace('<a class="type02_btn09"', "")
    info = info.replace(' href="javascript:cancelTrace();">取消</a>', "")

    info = info.replace('     <a class="type02_btn02" href="" ', "")
    info = info.replace('id="trace_btn1"><span><span class="trace_txt">', "")
    info = info.replace(" </span></span></a>", "")

    info = info.replace('<a href="//www.books.com.tw/activity/2015/06/', "")
    info = info.replace('trace/index.html#author" target="_blank" ', "")
    info = info.replace('title="新功能介紹"><cite class="help">', "")
    info = info.replace("新功能介紹</cite></a>", "")

    info = info.replace('     <a class="type02_btn02" href="" ', "")
    info = info.replace('id="trace_btn2"><span><span class="trace_txt">', "")
    info = info.replace(" </span></span></a>", "")

    info = info.replace('<a href="//www.books.com.tw/activity/2015/06/', "")
    info = info.replace('trace/index.html#publisher" target="_blank" ', "")
    info = info.replace('title="新功能介紹"><cite class="help">', "")
    info = info.replace("新功能介紹</cite></a>", "")

    info = info.replace("</ul></div>", "")
    return info


def parser_book_price(data):
    parser_price = data.find_all("ul", class_="price")
    price = str(parser_price[0])
    price = price.replace('<ul class="price">', "")
    price = price.replace("</ul>", "")
    return price


def parser_book_info2(data):
    parser_info = data.find_all("div", class_="mod_b type02_m058 clearfix")
    info = str(parser_info[0])
    info = info.replace('<div class="mod_b type02_m058 clearfix">', "")
    info = info.replace('<a name="P00a400020016"> </a>', "")
    info = info.replace("<h3>詳細資料</h3>", "")
    info = info.replace('<div class="bd">', "")
    info = info.replace("<ul>", "")
    info = info.replace("                          </li></ul>", "</li>")
    info = info.replace('<ul class="sort">', "")
    info = info.replace("</div></div>", "")
    return info


def parser_book_desc(data):
    parser_bd = data.find_all("div", class_="bd")
    desc = str(parser_bd[0])
    return desc


def parser_book_author(data):
    parser_bd = data.find_all("div", class_="bd")
    try:
        author = str(parser_bd[1])
        author = author.replace("作者簡介<br/>", "")
        author = author.replace("<strong>\n<br/>", "<strong>")
        # author = book_author.replace(r'\r\n','')
    except IndexError:
        print("'Author' is not found.")
        author = "Not found."
    finally:
        return author


def parser_book_outline(data):
    parser_bd = data.find_all("div", class_="bd")
    try:
        outline = str(parser_bd[2])
    except IndexError:
        print("'Outline' is not found.")
        outline = "Not found."
    finally:
        return outline


def to_html(data):
    try:
        # Template with Jinja2
        with _resources.path("crawler_book_info", "templates") as _path:
            template_path = str(_path)
            loader = FileSystemLoader(searchpath=template_path)
            env = Environment(loader=loader)
            template = env.get_template("books.tmpl")

            # Mapping the parser data to template.
            result = template.render(**data)

            # Write to HTML file.
            with open("index.html", "w") as f:
                f.write(pangu.spacing_text(result))
    except Exception as e:
        print(e)


def crawl_books_com_tw(book_url):
    try:
        # Get data.
        data = get_data(book_url)

        # Parser.
        book_title = parser_book_title(data[0])
        book_url = data[1]
        book_full_title = parser_book_full_title(data[0])
        book_cover = parser_book_cover(data[0])
        book_info1 = parser_book_info1(data[0])
        book_price = parser_book_price(data[0])
        book_info2 = parser_book_info2(data[0])
        book_desc = parser_book_desc(data[0])
        book_author = parser_book_author(data[0])
        book_outline = parser_book_outline(data[0])

        # Mapping the parser data to template.
        result = {
            "title": book_title,
            "url": book_url,
            "full_title": book_full_title,
            "cover": book_cover,
            "info1": book_info1,
            "price": book_price,
            "info2": book_info2,
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
        book_url = str("https://www.books.com.tw/products/" + arg)
    else:
        book_url = str(arg)

    data = crawl_books_com_tw(book_url)
    to_html(data)
