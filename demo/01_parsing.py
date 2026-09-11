# %% extruct: check for structured data before writing a single selector
import json

import extruct

html_a = open("page_a_structured.html").read()
print(json.dumps(extruct.extract(html_a, syntaxes=["json-ld"]), indent=2))

# %% parsel: no structured data, price lives in one element -> trivial
from parsel import Selector

html_b1 = open("page_b_simple.html").read()
sel_b1 = Selector(html_b1)
print(sel_b1.css(".price::text").get())

# %% same selector, a different (very common) template: price split into
# currency/dollars/cents spans. ::text only grabs direct text nodes, so it
# silently gets whitespace.
html_b2 = open("page_b_split.html").read()
sel_b2 = Selector(html_b2)
print(repr(sel_b2.css(".price::text").get()))

# %% parsel can still do it: normalize-space() flattens the subtree. The
# string still needs turning into a number -- that's the Normalizing segment.
print(sel_b2.css(".price").xpath("normalize-space()").get())

# %% zyte-parsers: the same flatten-then-parse, as one call that returns a
# typed value, and it works on both templates
from zyte_parsers import extract_price

print(extract_price(sel_b1.css(".price")[0]))
print(extract_price(sel_b2.css(".price")[0]))

# %% where the shared shape pays off: fields that no XPath trick flattens.
# Breadcrumbs are a chain of <a> tags with relative hrefs ...
from zyte_parsers import extract_breadcrumbs

for c in extract_breadcrumbs(sel_b2.css(".crumbs")[0], base_url="https://example.com"):
    print(c.name, "->", c.url)

# %% ... and a rating is five icons with no text at all
from zyte_parsers import extract_rating_stars

print(extract_rating_stars(sel_b2.css(".rating")[0]))

# %% NOTE: when the template itself is inconsistent site-wide,
# not just one field's markup, maintaining selectors per template stops
# paying off. Running Zyte API's automatic extraction on every page can
# beat hand-written selectors on quality-per-engineering-cost at that point
# -- a different tier of the decision, not a per-field AI call.
