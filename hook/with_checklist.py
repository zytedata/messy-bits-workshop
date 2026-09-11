from datetime import datetime

from anthropic import Anthropic
from clear_html import clean_node, cleaned_node_to_html
from dateparser.search import search_dates
from parsel import Selector
from zyte_parsers import extract_breadcrumbs, extract_price

FETCHED_AT = datetime(2026, 8, 27)
URL = "https://example.com/outdoor/tents/dome-4"


def extract_shipping(text: str) -> dict:
    # Free text with no dedicated parser: one narrow, schema-constrained LLM call.
    schema = {
        "type": "object",
        "properties": {
            "origin": {"type": "string"},
            "min_days": {"type": "integer"},
            "max_days": {"type": "integer"},
            "expedited_available": {"type": "boolean"},
        },
        "required": ["origin", "min_days", "max_days", "expedited_available"],
    }
    msg = Anthropic().messages.create(
        model="claude-haiku-4-5",
        max_tokens=200,
        tools=[{"name": "shipping", "input_schema": schema}],
        tool_choice={"type": "tool", "name": "shipping"},
        messages=[{"role": "user", "content": text}],
    )
    return msg.content[0].input


def extract_product(html: str) -> dict:
    sel = Selector(html)
    price = extract_price(sel.css(".price")[0])
    breadcrumbs = [
        {"name": b.name, "url": b.url}
        for b in extract_breadcrumbs(sel.css("nav.crumbs")[0], base_url=URL)
    ]
    description = cleaned_node_to_html(clean_node(sel.css(".desc")[0].root))
    posted_at = search_dates(
        sel.css(".posted-x92::text").get(),
        settings={"RELATIVE_BASE": FETCHED_AT},
    )[0][1]
    shipping = extract_shipping(sel.css(".shipping::text").get())

    return {
        "title": sel.css("h1::text").get(),
        "price": float(price.amount),
        "currency": price.currency,
        "breadcrumbs": breadcrumbs,
        "description": description,
        "posted_at": posted_at,
        "shipping": shipping,
    }
