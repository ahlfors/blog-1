#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'goreliu'
SITENAME = '陌辞寒'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'zh'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

#SOCIAL = (('GitHub', 'https://github.com/goreliu'),
#        ('微博', 'http://weibo.com/ly50247'),
#        )

DEFAULT_PAGINATION = 100

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

EXTRA_PATH_METADATA = {
        'extras/favicon.ico' : {'path': 'favicon.ico'},
        }
DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M'
ARTICLE_EXCLUDES = ['apps']
STATIC_PATHS = ['images', 'apps']
THEME = 'theme'
DISPLAY_PAGES_ON_MENU = True
PYGMENTS_STYLE = 'default'
CUSTOM_CSS = 'theme/css/github.css'
