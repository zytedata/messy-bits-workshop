# Hook and close captures

Two answers to the same prompt (`prompt.md`), captured from Claude Sonnet 5
on 2026-09-10. `vanilla.py` is the prompt as-is. `with_checklist.py` is the
same prompt with the closing checklist prepended; its two `Price` attribute
names (`amount`, `currency`) and its `clean_node` call (an lxml element, no
`base_url`) were fixed afterwards, everything else is verbatim. They are shown
on the hook and close slides; `tests/test_demo.py` runs both against the
prompt's HTML, with the LLM call stubbed, so a library update cannot break a
slide silently.
