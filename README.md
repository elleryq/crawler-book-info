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

### View Result

1. Open html in GNU/Linux.

    ```
    $ xdg-open output.html
    ```

1. Finally, we can clip the information to Evernote with [Evernote Web Clipper](https://evernote.com/intl/zh-tw/webclipper/).

## License

* Copyright (c) chusiang from 2017-2019 under the MIT license.
* Copyright (c) elleryq from 2019 under the MIT license.
