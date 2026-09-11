# Hands-on: parse, clean, normalize one page

You have about 10 minutes. Open `starter.py`, fill in the 6 `TODO`s,
uncomment the asserts at the bottom, run it, and get `all checks passed`. If
you finish early: write the schema and the prompt for the bonus field.

```
uv run starter.py
```

## What "done" looks like

```
title: 4-Person Dome Tent
price: Price(amount=Decimal('189.99'), currency='$')
breadcrumbs: (Breadcrumb(name='Home', ...), ..., Breadcrumb(name='Tents', ...))
rating: 4.0
clean description: <article>...<p>Waterproof 3-season tent, ...</p>...</article>
posted_at: 2026-08-22 00:00:00

all checks passed
```

## If you're stuck

- TODO 1: `sel.css("...::text").get()`.
- TODO 2/3/4: `zyte_parsers` functions take a `parsel` `Selector`, not a
  string: pass `sel.css(".price")[0]`, not `sel.css(".price").get()`.
- TODO 5: `clean_node` takes an `lxml` element (`fromstring(...)`), not a
  `parsel` selector or a string.
- TODO 6: `search_dates` returns a list of `(matched_text, datetime)` pairs,
  not a datetime.
- `solution.py` has the answer if you want to compare, but try first.

## The point of the bonus field

`.shipping` is free text ("Ships from our Reno warehouse within 2-3 business
days; expedited delivery available at checkout for an extra fee."). None of
the libraries used above parse this reliably; it's genuinely the long tail.
This is the one field in the exercise worth an LLM call, schema-constrained,
scoped to this field, not the whole page. Check your schema against the text:
does it keep "business" days apart from calendar days? And since the same
shipping text repeats across a whole catalogue, cache the call on the input
string; thousands of products usually means tens of distinct strings.
