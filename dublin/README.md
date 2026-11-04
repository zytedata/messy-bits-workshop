# Dublin notebooks via Docker

Requires Docker only. From this folder:

    docker compose up --build

Open http://localhost:8888 (no token). Stop with Ctrl+C.

Optional, for `hook/with_checklist.ipynb`:

    ANTHROPIC_API_KEY=sk-ant-... docker compose up
