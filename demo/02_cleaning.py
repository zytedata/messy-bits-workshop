# %% clear-html: strip tracking attrs, inline styles, ad scripts -- keep
# structure. The before/after size is the point: this is what the LLM
# writing the scraper gets to read. On a real page it decides whether the
# model sees the product or 300 KB of scripts around it.
from lxml.html import fromstring

from clear_html import clean_node, cleaned_node_to_html

html_c = open("page_c_junk.html").read()
cleaned = cleaned_node_to_html(clean_node(fromstring(html_c)))
print(f"before: {len(html_c)} chars, after: {len(cleaned)} chars")
print(cleaned)

# %% html-text: the text you hand to dateparser, price_parser or the one
# narrow LLM call. Compare with a raw ::text dump: script contents leak,
# whitespace is noise, block boundaries are lost.
import html_text
from parsel import Selector

print(repr(" ".join(Selector(html_c).css("*::text").getall())))
print(repr(html_text.extract_text(html_c)))

# %% w3lib: HTML entity decoding, one of the smaller messes that still
# needs handling before anything downstream can trust the string
import w3lib.html

print(w3lib.html.replace_entities("Caf&eacute; Press Coffee Maker"))
