import datetime

from clear_html import clean_node, cleaned_node_to_html
from dateparser.search import search_dates
from lxml.html import fromstring
from parsel import Selector
from price_parser import Price
from zyte_parsers import extract_breadcrumbs, extract_price, extract_rating_stars

html = open("messy_page.html").read()
sel = Selector(html)

# parsing: title is one field, one element -> parsel is enough
title = sel.css(".product h1::text").get()

# parsing: price is split across three elements -> zyte-parsers flattens the
# selector and parses the result in one call
price = extract_price(sel.css(".price")[0])

# parsing: breadcrumbs are a chain of <a> tags -> zyte-parsers again
crumbs = extract_breadcrumbs(sel.css(".crumbs")[0], base_url="https://example.com")

# parsing: rating is five icons with no text -> zyte-parsers counts them
rating = extract_rating_stars(sel.css(".rating")[0])

# cleaning: strip the ad script, inline styles, tracking attributes
clean_desc = cleaned_node_to_html(clean_node(fromstring(sel.css(".desc").get())))

# normalizing: text already extracted -> dateparser, with the crawl time as base
raw_posted = sel.css(".posted-x92::text").get()
[(_, posted_at)] = search_dates(
    raw_posted, settings={"RELATIVE_BASE": datetime.datetime(2026, 8, 27)}
)

# the long tail: free-text shipping info, no deterministic parser for this
shipping_text = sel.css(".shipping::text").get()
shipping_schema = {
    "origin": "string",
    "min_days": "integer",
    "max_days": "integer",
    "business_days": "boolean",
    "expedited_available": "boolean",
}
shipping_prompt = (
    "Extract shipping details from this product page text. Return only JSON "
    f"matching {shipping_schema}. Use null for anything the text does not "
    f"state.\n\n{shipping_text}"
)

print("title:", title)
print("price:", price)
print("breadcrumbs:", crumbs)
print("rating:", rating)
print("clean description:", clean_desc.strip())
print("posted_at:", posted_at)
print("shipping text:", shipping_text)
print("your schema:", shipping_schema)

assert title == "4-Person Dome Tent"
assert price.amount == Price.fromstring("$189.99").amount
assert crumbs[-1].name == "Tents"
assert rating == 4.0
assert "loadAd" not in clean_desc and "style=" not in clean_desc
assert posted_at == datetime.datetime(2026, 8, 22)
print("\nall checks passed")
