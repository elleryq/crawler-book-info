#!/usr/bin/env python
"""
crawler-book-info
==========
.. code:: shell
  $ crawler-book-info https://www.books.com.tw/products/0010810939 --output index.html
"""
from setuptools import find_packages, setup


install_requires = ["beautifulsoup4", "requests", "jinja2", "pangu"]
tests_requires = ["pytest", "flake8"]

setup(
    name="crawler-book-info",
    version="0.1.0",
    author="Yan-ren Tsai",
    author_email="elleryq@gmail.com",
    url="https://github.com/elleryq/crawler-book-info",
    description="A tool for crawling book informationi from bookstore site.",
    long_description=__doc__,
    packages=find_packages(exclude=["tests"]),
    zip_safe=False,
    license="MIT",
    install_requires=install_requires,
    extras_require={
        "tests": install_requires + tests_requires,
    },
    tests_require=tests_requires,
    include_package_data=True,
    entry_points={"console_scripts": ["crawler-book-info = crawler_book_info:main"]},
    classifiers=[
        "Intended Audience :: Other Audience",
        "Operating System :: OS Independent",
        "Topic :: Text Processing",
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
