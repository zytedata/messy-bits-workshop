"""Page Object reusing the extraction functions from exercise/solution.ipynb."""
from clear_html import clean_node, cleaned_node_to_html
from lxml.html import fromstring
from web_poet import field
from zyte_common_items import (
    AggregateRating,
    Breadcrumb,
    ProductPage,
)
from zyte_parsers import extract_breadcrumbs, extract_price, extract_rating_stars


class MessyProductPage(ProductPage):
    # parsing: title is one element -> parsel is enough
    @field
    def name(self):
        return self.css(".product h1::text").get()

    # parsing: price split across three elements -> zyte-parsers flattens it
    @field
    def price(self):
        p = extract_price(self.css(".price")[0])
        return str(p.amount) if p and p.amount is not None else None

    @field
    def currency(self):
        p = extract_price(self.css(".price")[0])
        return "USD" if p and p.currency == "$" else None  # ponytail: only "$" mapped

    @field
    def regularPrice(self):
        p = extract_price(self.css("del.was")[0])
        return str(p.amount) if p and p.amount is not None else None

    # parsing: chain of <a> tags -> zyte-parsers
    @field
    def breadcrumbs(self):
        crumbs = extract_breadcrumbs(self.css(".crumbs")[0], base_url=str(self.url))
        return [Breadcrumb(name=c.name, url=c.url) for c in crumbs or []]

    # parsing: five icons, no text -> zyte-parsers counts them
    @field
    def aggregateRating(self):
        stars = extract_rating_stars(self.css(".rating")[0])
        count = self.css(".rating .count::text").re_first(r"\d+")
        return AggregateRating(
            ratingValue=stars, bestRating=5, reviewCount=int(count) if count else None
        )

    # cleaning: strip ad script, inline styles, tracking attributes
    @field
    def descriptionHtml(self):
        return cleaned_node_to_html(clean_node(fromstring(self.css(".desc").get())))
