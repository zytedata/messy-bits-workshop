import datetime

from clear_html import clean_node, cleaned_node_to_html
from dateparser.search import search_dates
from lxml.html import fromstring
from parsel import Selector
from price_parser import Price
from zyte_parsers import extract_breadcrumbs, extract_price, extract_rating_stars

html = open("messy_page.html").read()
sel = Selector(html)

# TODO 1 (parsing): the title lives in one element -- a plain parsel
# selector is enough. Extract the text of the <h1>.
title = None

# TODO 2 (parsing): the price is split across three elements (currency,
# dollars, cents). Grab the ".price" selector, then let zyte_parsers merge
# and normalize the fragments -- see extract_price.
price = None

# TODO 3 (parsing): breadcrumbs are a chain of <a> tags inside ".crumbs".
# Use extract_breadcrumbs (it needs base_url="https://example.com").
crumbs = None

# TODO 4 (parsing): ".rating" is five star icons and no text. Use
# extract_rating_stars.
rating = None

# TODO 5 (cleaning): the ".desc" block has inline styles and tracking
# attributes. Parse it with lxml's fromstring, then clean_node +
# cleaned_node_to_html.
clean_desc = None

# TODO 6 (normalizing): ".posted-x92" holds a relative date as plain text
# ("Listed N days ago"). Use search_dates with RELATIVE_BASE set to
# datetime.datetime(2026, 8, 27), the day the page was fetched.
posted_at = None

# BONUS (the long tail): ".shipping" holds free-text shipping info that no
# deterministic parser here handles. Sketch the JSON schema you'd send to an
# LLM to normalize it, then write the prompt that goes with it.
shipping_text = sel.css(".shipping::text").get()
shipping_schema = None  # your schema goes here
shipping_prompt = None  # your prompt goes here

print("title:", title)
print("price:", price)
print("breadcrumbs:", crumbs)
print("rating:", rating)
print("clean description:", clean_desc)
print("posted_at:", posted_at)
print("shipping text:", shipping_text)
print("your schema:", shipping_schema)

# self-check -- uncomment once you've filled in the TODOs above
# assert title == "4-Person Dome Tent"
# assert price.amount == Price.fromstring("$189.99").amount
# assert crumbs[-1].name == "Tents"
# assert rating == 4.0
# assert "loadAd" not in clean_desc and "style=" not in clean_desc
# assert posted_at == datetime.datetime(2026, 8, 22)
# print("\nall checks passed")
