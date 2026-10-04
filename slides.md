---
marp: true
theme: default
paginate: true
header: '![h:80](setup-qr.svg)'
style: |
  header { left: auto; right: 30px; }
---

# AI for the messy bits
### parsing, cleaning, normalizing

Extract Summit 2026

---

## The messy bits

- No structured data
- A price split across three `<span>`s
- A rating that is five icons and no text
- "Listed 5 days ago"
- "Ships from our Reno warehouse within 2-3 business days..."

`exercise/messy_page.html` is all of this, toy-sized so it fits on a screen. The real thing is 300 KB of it.

---

## What an assistant writes for it today

Asked for a parsel-based extractor for a trimmed version of this page, no other instructions (`hook/vanilla.py`):

```python
price = float(f"{dollars}.{cents}")

description = re.sub(r'\s*style="[^"]*"', "", desc_html)

days_ago = int(re.search(r"(\d+)", posted_text).group(1))
posted_at = FETCHED_AT - timedelta(days=days_ago)

origin = re.search(r"from our (\w+) warehouse", shipping_text).group(1)
min_days, max_days = (int(n) for n in
    re.search(r"(\d+)-(\d+) business days", shipping_text).groups())
```

Runs. Passes on this page. Four regexes you now own.

---

<!-- _class: lead -->

> Some people, when confronted with a problem, think
> "I know, I'll use regular expressions."
> Now they have two problems.

— Jamie Zawinski, 1997

---

## Thesis

**Use the right tool for the job — in the code, whether you write it or an LLM does.**

Increasingly, an LLM writes the scraper *once*. Parsing then runs as ordinary generated code — not a live LLM call on every page. The risk is that the LLM (or you) reaches for a regex where a library already exists.

Every library today is from the Scrapy / Zyte ecosystem.

*(detecting a broken parser and having an LLM fix it is the self-healing workshop, later today)*

---

# Parsing

→ `demo/01_parsing.py`, cell by cell

---

## When the whole template is the problem

Not one field's markup — the whole site's layout, inconsistently.

Maintaining per-template selectors stops paying off. Full-page AI extraction (e.g. [Zyte API’s](https://docs.zyte.com/zyte-api/usage/extract.html)) can beat hand-written selectors on **quality per engineering hour** at that point.

*A different tier of decision. Not a per-field AI call.*

---

# Cleaning

→ `demo/02_cleaning.py`, cell by cell

---

# Normalizing

→ `demo/03_normalizing.py`, cell by cell

---

## The long tail, scoped and cached

One narrow, schema-constrained LLM call for *that field* — not a fallback to calling an LLM on the whole page, and not a regex either.

Scoped to the field also means a small, cheap model is enough: a shipping string plus a four-field schema is an easy task, a whole page is not. And the input repeats. A site with thousands of products has tens of distinct shipping strings; `@lru_cache` on `extract_shipping(text)` and the LLM runs tens of times per crawl, not thousands. Same trick as caching OCR per image hash when prices are images.

---

# Hands-on — ~10 minutes

`exercise/starter.py` — 6 `TODO`s, same functions just shown.

```
uv run starter.py
```

**Done looks like:**
```
title: 4-Person Dome Tent
price: Price(amount=Decimal('189.99'), currency='$')
rating: 4.0
...
all checks passed
```

Bonus: the schema *and* the prompt for the shipping field.

---

# The checklist

1. Structured data present? → [`extruct`](https://github.com/scrapinghub/extruct)
2. Single clean element? → [`parsel`](https://github.com/scrapy/parsel)
3. Field split across markup, or icons instead of text? → [`zyte_parsers`](https://github.com/zytedata/zyte-parsers)
4. Text you already have needs a type? → [`price_parser`](https://github.com/scrapinghub/price-parser) / [`dateparser`](https://github.com/scrapinghub/dateparser)
5. Genuinely free text? → LLM call, schema-constrained, scoped
6. Whole template inconsistent? → full-page AI extraction (e.g. [Zyte API’s](https://docs.zyte.com/zyte-api/usage/extract.html))

---

## Same prompt, checklist loaded

`hook/with_checklist.py` — the hook prompt again, with the six lines above prepended:

```python
price = extract_price(sel.css(".price")[0])
extract_breadcrumbs(sel.css("nav.crumbs")[0], base_url=URL)
cleaned_node_to_html(clean_node(sel.css(".desc")[0].root))
posted_at = search_dates(
    sel.css(".posted-x92::text").get(),
    settings={"RELATIVE_BASE": FETCHED_AT},
)[0][1]
shipping = extract_shipping(sel.css(".shipping::text").get())
# extract_shipping: one tool_choice-forced call with a four-field input_schema
```

Zero regexes. Six lines of instructions did that.

Four fields, still no `business_days`: the checklist picks the libraries, the schema is still yours to check.

---

## Parting notes

[zytedata/skills](https://github.com/zytedata/skills) is those six lines, maintained, for your coding assistant — no need to write your own instructions telling it to reach for `zyte_parsers` over regex.

[scrapy-agent-plugin](https://github.com/scrapy/scrapy-agent-plugin) is the Scrapy-only counterpart: a Scrapy skill for the same assistants.

[web-poet](https://github.com/scrapinghub/web-poet), Zyte's page-object library: parsing code that is testable by default, a fixture being the saved response plus the JSON it should produce.

[Zyte MCP](https://docs.zyte.com/zyte-web-data/mcp.html) lets your assistant use Zyte directly: fetch pages, extract data, search the web, and work with your Scrapy Cloud projects.

