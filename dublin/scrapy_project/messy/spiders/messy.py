from pathlib import Path

import scrapy

from messy.pages import MessyProductPage

PAGE = Path(__file__).resolve().parents[3] / "exercise" / "messy_page.html"


class MessySpider(scrapy.Spider):
    name = "messy"

    async def start(self):
        yield scrapy.Request(PAGE.as_uri())

    async def parse(self, response, page: MessyProductPage):
        yield await page.to_item()
