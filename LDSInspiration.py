#!/usr/bin/python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
from variety.Util import Util
from bs4 import BeautifulSoup
from variety.plugins.IQuoteSource import IQuoteSource
from variety import _, _u

import logging
import random

logger = logging.getLogger("variety")

class LDSQuotesSource(IQuoteSource):


    def __init__(self):
        super(IQuoteSource, self).__init__()
        self.quotes = []

    @classmethod
    def get_info(cls):
        return {
            "name": "LDSInspiration",
            "description": _("Fetches quotes from lds.org quotes RSS feed.\n"
                             "Does not support searching by tags, authors, or topics...yet."),
            "author": "Andrew Payne",
            "version": "0.2"
        }

    def supports_search(self):
        return False

    def activate(self):
        if self.active:
            return
        self.active = True

        self.quotes = []
	    self.get_inspired_quotes()

    def deactivate(self):
        self.quotes = []
        self.active = False

    def get_inspired_quotes(self):
        self.quotes = []
        url = "http://feeds.lds.org/lds-inspirational-messages-eng"

        bs = Util.html_soup(url)
        items = bs.select("item")
        for item in items:
            formatted_item = BeautifulSoup(item.prettify(formatter=None))

            quote = formatted_item.find("blockquote")
            sQuote = quote.get_text().encode('utf-8')

            author = formatted_item.find("p")

            link = author.find("a").get('href')

            sAuthor = author.get_text().encode('utf-8')
            sAuthor = sAuthor[3:]
            if (sAuthor.find(',') != -1):
                sAuthor = sAuthor[:sAuthor.index(',')]
            if (sAuthor.find('Topics') != -1):
                sAuthor = sAuthor[:sAuthor.index('Topics')]

            tempitem = {"quote": sQuote, "author": sAuthor, "sourceName": "LDS.org", "link": link}
            self.quotes.append(tempitem)

        if not self.quotes:
                logger.warning("Could not find quotes for URL " + url)

    def get_for_author(self, author):
        return []

    def get_for_keyword(self, keyword):
        return []

    def get_random(self):
        return self.quotes


        """
        url = "http://feeds.lds.org/lds-inspirational-messages-eng"

        bs = Util.xml_soup(url)
        items = bs.find_all("item")
#        if not item:
#            logger.warning(lambda: "Could not find quotes for URL " + url)
#            return None
        quotes = [];

        for item in items:
            link = item.find("link").contents[0].strip()
            s = item.find("description").contents[0]
            author = s[s.rindex("\n")+4:].replace(',' , '').replace('"','').strip()
            author = author[:author.index('<a')-1].strip()
            author = author.encode('utf-8')
            if ((author == " ") or (author == "")):
                author = "none" 

            quote = s[:s.rindex("\n")].replace('"', '').replace('<br>', '\n').replace('<br/>', '\n').replace("</blockquote>",'').strip()
            quote = quote[quote.rindex('>')+1:].strip()
            quote = "\"" + quote + "\""
            quote = quote.encode('utf-8')
            
            tempitem = {"quote": quote, "author": author, "sourceName": "LDS.org", "link": link}
            self.quotes.append(tempitem)

        if not self.quotes:
            logger.warning("Could not find quotes for URL " + url)
            return []

        return [random.choice(self.quotes)]"""
