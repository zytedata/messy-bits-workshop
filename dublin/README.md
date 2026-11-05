# Dublin notebooks via Docker

Requires Docker only. From this folder:

    docker compose up --build

Open http://localhost:8888 (no token). Stop with Ctrl+C.

Optional, for `hook/with_checklist.ipynb`:

    ANTHROPIC_API_KEY=sk-ant-... docker compose up

# Scrapy + Jev demo (`scrapy_project/`)

Runs locally, not in Docker. From the repo root:

    uv sync --python-preference only-managed
    export TYPESAFE_API_TOKEN=<your key>
    cd dublin/scrapy_project
    ../../.venv/bin/scrapy crawl messy

Without `TYPESAFE_API_TOKEN` the Jev addon disables itself (warning "No API key found") and the crawl runs unchecked.

`--python-preference only-managed` avoids pyenv Pythons built without zstd (`No module named '_zstd'`).
