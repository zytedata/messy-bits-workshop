I have this HTML fragment from a product page fetched on 2026-08-27 from https://example.com/outdoor/tents/dome-4:

```html
<div class="product" data-track="pdp-9931" style="--accent: #1a73e8">
  <div class="ad-slot"><script>loadAd('sidebar-1');</script></div>

  <nav class="crumbs">
    <a href="/">Home</a> &gt;
    <a href="/outdoor">Outdoor</a> &gt;
    <a href="/outdoor/tents">Tents</a>
  </nav>

  <h1 class="pdp-title-x92">4-Person Dome Tent</h1>

  <span class="price">
    <span class="currency">$</span><span class="dollars">189</span>.<span class="cents">99</span>
  </span>

  <p class="posted-x92" style="color:#888">Listed 5 days ago</p>

  <div class="desc">
    <p style="font-weight:400">Waterproof <span style="color:green">3-season</span> tent, sets up in under 10 minutes.</p>
  </div>

  <p class="shipping">Ships from our Reno warehouse within 2-3 business days; expedited delivery available at checkout for an extra fee.</p>
</div>
```

Write Python code that takes this HTML as a string `html` and produces a dict with: `title` (str), `price` (a number) and `currency`, `breadcrumbs` (list of {name, url} with absolute URLs), `description` (the description as clean HTML without inline styles), `posted_at` (a datetime), and `shipping` structured as {origin, min_days, max_days, expedited_available}. I use parsel for scraping. Keep it under ~40 lines. Reply with ONLY the Python code in a single fenced block, no explanation before or after.
