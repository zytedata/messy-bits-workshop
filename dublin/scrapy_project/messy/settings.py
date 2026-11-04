import os

BOT_NAME = "messy"
SPIDER_MODULES = ["messy.spiders"]
ROBOTSTXT_OBEY = False  # local file

# scrapy-poet: inject Page Objects into callbacks
ADDONS = {
    "scrapy_poet.Addon": 300,
    # scrapy-jev: registers QualityGatePipeline
    "scrapy_jev.Addon": 350,
}

# Jev spot-checks these fields; an implausible/empty one stops the crawl.
JEV_FIELDS = ["name", "price"]
JEV_SAMPLE_SIZE = 1  # one-item demo; default is 20
JEV_API_KEY = os.environ.get("TYPESAFE_API_TOKEN")  # export it first (see README)
JEV_BASE_URL = "https://api.typesafe.ai/v1/systemone"
JEV_MODEL = "jev-latest"
