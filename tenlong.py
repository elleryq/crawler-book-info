#!/usr/bin/env python
#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from jinja2 import Template
import logging
import lxml
import requests
import sys
import git
import urllib3
import pangu

# disable ssl warn message.
urllib3.disable_warnings()
logging.captureWarnings(True)

def get_data():
  try:
    arg = sys.argv[1]

    if arg.isdigit():
      # send get request and get reposoe.
      book_url = str('https://www.tenlong.com.tw/products/' + arg)
      res = requests.get(book_url)
      soup = BeautifulSoup(res.text, 'lxml')
      return soup, book_url

    else:
      # get web page from local for development.
      soup = BeautifulSoup(open(arg), 'lxml')
      return soup

  except Exception as e:
    print(e)

def parser_book_title(data):
  book_title = data.title
  book_title = str(book_title).replace('<title>天瓏網路書店-', '').replace('</title>', '')
  return book_title

def parser_book_info(data):
  parser_book_info = data.find_all('div', class_='item-info')
  book_info = str(parser_book_info[0])
  book_info = book_info.replace('<a class="item-preview btn btn-plain" href="#"><i class="fa fa-eye fa-before"></i>預覽內頁</a>', '')
  return book_info

def parser_book_desc(data):
  parser_item_desc = data.find_all('div', class_='item-desc')
  book_desc = str(parser_item_desc[0])
  return book_desc

def parser_book_author(data):
  parser_item_desc = data.find_all('div', class_='item-desc')
  try:
    book_author = parser_item_desc[1]
  except Exception as e:
    print("'Author' is not found.")
    book_author = "Not found."
  finally:
    return book_author

def parser_book_outline(data):
  parser_item_desc = data.find_all('div', class_='item-desc')
  try:
    book_outline = parser_item_desc[2]
  except Exception as e:
    print("'Outline' is not found.")
    book_outline = "Not found."
  finally:
    return book_outline

def git_sha():
  git_repo = git.Repo(search_parent_directories=True)
  git_sha = git_repo.head.object.hexsha
  short_git_sha = git_sha[:8]
  return short_git_sha

def main():
  try:

    # Template with Jinja2
    template = Template('''\
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width" />
    <title> {{ title }} </title>
  </head>
  <body>
    <p>
      Buy:
      <ul>
        <li> <a href="{{ url }}" target="_blank">天瓏書局</a> </li>
      </ul>
    </p>
    <hr>
    {{ info }}

    <h2>商品描述</h2>
    {{ desc }}

    <h2>作者簡介</h2>
    {{ author }}

    <h2>目錄大綱</h2>
    {{ outline }}

  <footer style="text-align: center;">
    Power by <a href="https://github.com/chusiang/crawler-book-info" target="_blank">chusiang/crawler-book-info</a> ({{ version }}).
  </footer>
  </body>
</html>
''')

    # Get data.
    data = get_data()

    # Parser.
    book_title = parser_book_title(data[0])
    book_url = data[1]
    book_info = parser_book_info(data[0])
    book_desc = parser_book_desc(data[0])
    book_author = parser_book_author(data[0])
    book_outline = parser_book_outline(data[0])
    project_version = git_sha()

    # Mapping the parser data to template.
    result = template.render(
        title=book_title,
        url=book_url,
        info=book_info,
        desc=book_desc,
        author=book_author,
        outline=book_outline,
        version=project_version
    )

    # Write to HTML file.
    f = open('index.html', 'w')
    f.write(pangu.spacing_text(result))
    f.close()

  except Exception as e:
    print(e)

if __name__ == "__main__":
  main()
