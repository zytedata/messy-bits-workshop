import re
from datetime import datetime, timedelta
from urllib.parse import urljoin
from parsel import Selector

BASE_URL = "https://example.com/outdoor/tents/dome-4"
FETCHED_AT = datetime(2026, 8, 27)


def parse_product(html: str) -> dict:
    sel = Selector(html)

    title = sel.css("h1::text").get("").strip()

    dollars = sel.css(".price .dollars::text").get()
    cents = sel.css(".price .cents::text").get()
    price = float(f"{dollars}.{cents}")
    currency = sel.css(".price .currency::text").get("").strip()

    breadcrumbs = [
        {"name": a.css("::text").get("").strip(),
         "url": urljoin(BASE_URL, a.attrib["href"])}
        for a in sel.css("nav.crumbs a")
    ]

    desc_html = sel.css(".desc").get().strip()
    description = re.sub(r'\s*style="[^"]*"', "", desc_html)

    posted_text = sel.xpath('//p[contains(., "Listed")]/text()').get("")
    days_ago = int(re.search(r"(\d+)", posted_text).group(1))
    posted_at = FETCHED_AT - timedelta(days=days_ago)

    shipping_text = sel.xpath('//p[contains(., "Ships from")]/text()').get("")
    origin = re.search(r"from our (\w+) warehouse", shipping_text).group(1)
    min_days, max_days = (
        int(n) for n in re.search(r"(\d+)-(\d+) business days", shipping_text).groups()
    )
    expedited_available = "expedited delivery available" in shipping_text

    return {
        "title": title,
        "price": price,
        "currency": currency,
        "breadcrumbs": breadcrumbs,
        "description": description,
        "posted_at": posted_at,
        "shipping": {
            "origin": origin,
            "min_days": min_days,
            "max_days": max_days,
            "expedited_available": expedited_available,
        },
    }
