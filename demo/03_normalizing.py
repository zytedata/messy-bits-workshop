# %% price-parser: currency symbols, thousands separators, European
# decimal commas, "Free" -- all resolve to a comparable (amount, currency)
from price_parser import Price

for text in ["US$1,299.00", "£999", "1.299,00 €", "Free"]:
    print(text, "->", Price.fromstring(text))

# %% dateparser: relative dates, and it doesn't need the surrounding
# sentence stripped out first -- search_dates finds the date inside free
# text, in more than one language. RELATIVE_BASE is the crawl time; without
# it "5 days ago" silently means "5 days before whenever this code runs".
import datetime

from dateparser.search import search_dates

base = datetime.datetime(2026, 8, 27)
print(
    search_dates(
        "Listed 5 days ago by a top-rated seller", settings={"RELATIVE_BASE": base}
    )
)
print(
    search_dates(
        "Publié il y a 2 jours", languages=["fr"], settings={"RELATIVE_BASE": base}
    )
)

# %% the long tail: free-text shipping info. Nothing deterministic parses
# this reliably -- this is where generated code embeds one narrow,
# schema-constrained LLM call for this one field. The first schema loses
# the "business" in "2-3 business days"; the second keeps it.
shipping_text = (
    "Ships from our Reno warehouse within 2-3 business days; expedited "
    "delivery available at checkout for an extra fee."
)
schema_v1 = {
    "origin": "string",
    "min_days": "integer",
    "max_days": "integer",
    "expedited_available": "boolean",
}
schema_v2 = {**schema_v1, "business_days": "boolean"}
print("on:", shipping_text)
print("v1 loses 'business':", schema_v1)
print("v2:", schema_v2)
