#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib_resources as _resources
import pangu
from jinja2 import FileSystemLoader, Environment


def to_html(data, template_filename, fp):
    # Template with Jinja2
    with _resources.path("crawler_book_info", "templates") as _path:
        template_path = str(_path)
        loader = FileSystemLoader(searchpath=template_path)
        env = Environment(loader=loader)
        template = env.get_template(template_filename)

        # Mapping the parser data to template.
        result = template.render(**data)

        # Write to HTML file.
        fp.write(pangu.spacing_text(result))
