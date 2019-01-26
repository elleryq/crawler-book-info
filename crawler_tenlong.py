#!/usr/bin/python
#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from jinja2 import Template
import logging
import lxml
import requests
import sys
import urllib3

# disable ssl warn message.
urllib3.disable_warnings()
logging.captureWarnings(True)

# set utf-8 codecs for Jinja2.
#reload(sys)
#sys.setdefaultencoding('utf-8')

def main():
  try:

    '''
    get data
    '''
    arg = sys.argv[1]

    if arg.isdigit():
      # send get request and get reposoe.
      book_url = str('https://www.tenlong.com.tw/products/' + arg)
      res = requests.get(book_url)
      soup = BeautifulSoup(res.text, 'lxml')

    else:
      # get web page from local for development.
      soup = BeautifulSoup(open(arg), 'lxml')

    '''
    parser book data
    '''
    parser_book_title = soup.title
    book_title = str(parser_book_title).replace('<title>天瓏網路書店-', '').replace('</title>', '')

    #book info.
    parser_book_info = soup.find_all('div', class_='item-info')
    book_info = parser_book_info[0]

    #book desc.
    parser_book_intro = soup.find_all('div', class_='item-desc')
    book_intro = parser_book_intro[0]

    #remove the extra text.
    remove_order_element1 = str(book_intro).replace('立即出貨\n', '')

    #remove delivery status.
    delivery_status = soup.find_all('span', class_='delivery-status')
    if len(delivery_status) != 0:
      remove_order_element2     = remove_order_element1.replace(str(delivery_status[0].encode('utf-8') + b'\n'), '')
    else:
      remove_order_element2     = remove_order_element1

    remove_order_element3     = remove_order_element2.replace('<p>\n              </p>', '')

    remove_order_element4     = remove_order_element3.replace('<p>\n\t下單後立即進貨\n</p>', '')

    remove_shipment_element  = remove_order_element4.replace('<p>\n\t立即出貨\n</p>', '').replace('<p> </p><p>', '<p>')

    replace_head_color       = remove_shipment_element.replace('<span style="color: #ff00ff;">', '<span style="color: #000000;">')

    remove_copyright_element = replace_head_color.replace('<p>Copyright ® 2016 Tenlong Computer Book Co, Ltd. All rights reserved.</p>', '')

    remove_footer = remove_copyright_element.replace('<p>\n<a href="/faq">客服與FAQ</a> |\n\t\t<a href="/about">連絡我們</a> |\n\t\t<a href="/privacy">隱私權政策</a> |\n\t\t<a href="/terms">服務條款</a>\n</p>', '')

    book_desc = remove_footer.replace('<p>天瓏提供<strong>超商代收！</strong></p>', '')

    template = Template('''\
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width" />
    <title> {{ title }} </title>
  </head>
  <body>
    Buy: <br/>
    <ul>
      <li> <a href="{{ url }}" target="_blank">天瓏書局</a> </li>
    </ul>
    <hr>
    {{ info }}
    {{ desc }}
  </body>
</html>
''')

    result = template.render(title=book_title, url=book_url, info=book_info, desc=book_desc)

    f = open('index.html', 'w')
    f.write(result)
    f.close()

  except Exception as e:
    print(e)

if __name__ == "__main__":
  main()

