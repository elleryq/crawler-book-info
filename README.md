# Crawler Book Info

[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

A sample crawler for quick parser some books information.

## Installation

```
pip install git+https://github.com/elleryq/crawler-book-info#egg=crawler-book-info
```

## Usage

Run crawler-book-info with the url of the book.
```
# 天瓏書局
$ crawler-book-info https://www.tenlong.com.tw/products/9789865020774
$ crawler-book-info -o tenlong.html https://www.tenlong.com.tw/products/9789865020774

# 博客來
$ crawler-book-info https://www.books.com.tw/products/0010811947
$ crawler-book-info -o books.html https://www.books.com.tw/products/0010811947
```

Or use seperated commands
```
# 天瓏書局
$ crawler-book-info.tenlong https://www.tenlong.com.tw/products/9789865020774
$ crawler-book-info.tenlong 9789865020774
$ crawler-book-info.tenlong -o tenlong.html 9789865020774

# 博客來
$ crawler-book-info.books https://www.books.com.tw/products/0010811947
$ crawler-book-info.books 0010811947
$ crawler-book-info.books -o books.html 0010811947
```

### View Result

1. Open html in GNU/Linux.

    ```
    $ xdg-open output.html
    ```

1. Finally, we can clip the information to Evernote with [Evernote Web Clipper](https://evernote.com/intl/zh-tw/webclipper/).

### Run local Nginx for Evernote Web Clipper

The **Evernote Web Clipper** is not support local files, so we can clip it with Nginx.

1. Run Nginx container.

    ```
    $ docker run --name nginx -v "$(pwd)":/usr/share/nginx/html/ -p 80:80 -d nginx
    ```

1. Open html via Firefox on GNU/Linux.

    ```
    (.venv) [ jonny@xenial ~/vcs/crawler-book-outline ]
    $ firefox http://localhost/output.html
    ```

1. (option) Run Nginx container via make.

    ```
    $ make start_nginx_docker
    ```

1. (option) Open web via make.

    ```
    $ make review_serve
    ```

1. Finally, we can clip the information to Evernote with [Evernote Web Clipper](https://evernote.com/intl/zh-tw/webclipper/).

## License

* Copyright (c) chusiang from 2017-2019 under the MIT license.
* Copyright (c) elleryq from 2019 under the MIT license.
