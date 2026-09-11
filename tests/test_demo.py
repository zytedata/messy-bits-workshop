import datetime
import importlib.util
import re
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

REPO_ROOT = Path(__file__).resolve().parent.parent
HOOK_HTML = re.search(
    r"```html\n(.*?)```", (REPO_ROOT / "hook/prompt.md").read_text(), re.S
).group(1)


def import_script(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_hook_product(product):
    assert product["title"] == "4-Person Dome Tent"
    assert (product["price"], product["currency"]) == (189.99, "$")
    assert product["breadcrumbs"][-1] == {
        "name": "Tents",
        "url": "https://example.com/outdoor/tents",
    }
    assert "3-season" in product["description"]
    assert "style=" not in product["description"]
    assert product["posted_at"] == datetime.datetime(2026, 8, 22)


def run(directory, script):
    result = subprocess.run(
        ["uv", "run", script],
        cwd=REPO_ROOT / directory,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout


def test_parsing_demo():
    out = run("demo", "01_parsing.py")
    assert '"name": "Trail Running Shoes"' in out  # extruct: structured data present
    assert "$84.50" in out  # parsel works on the simple template
    assert "'\\n    '" in out  # parsel silently fails on the split template
    assert "\n$92.00\n" in out  # normalize-space() rebuttal works
    assert "Price(amount=Decimal('84.50'), currency='$')" in out
    assert "Price(amount=Decimal('92.00'), currency='$')" in out  # zyte_parsers, both templates
    assert "Trail -> https://example.com/shoes/trail" in out
    assert "\n4.0\n" in out  # star icons -> rating


def test_cleaning_demo():
    out = run("demo", "02_cleaning.py")
    assert "before: 341 chars, after: 100 chars" in out  # the size number the slide quotes
    assert out.count("loadAd") == 1  # leaks in the raw ::text dump, stripped everywhere else
    assert "Café Press Coffee Maker" in out  # entities decoded


def test_normalizing_demo():
    out = run("demo", "03_normalizing.py")
    assert "Price(amount=Decimal('1299.00'), currency='US$')" in out
    assert "Price(amount=Decimal('0'), currency=None)" in out  # "Free" -> 0
    assert "datetime.datetime(2026, 8, 22, 0, 0)" in out  # "5 days ago" resolves
    assert "datetime.datetime(2026, 8, 25, 0, 0)" in out  # French relative date resolves


def test_exercise_solution():
    out = run("exercise", "solution.py")
    assert "all checks passed" in out


def test_exercise_starter_runs_before_any_todo_is_filled_in():
    # guards against a TODO edit breaking the file for everyone before the
    # workshop even starts -- starter.py must run clean with blanks as None
    out = run("exercise", "starter.py")
    assert "title: None" in out


def test_hook_vanilla_runs_on_the_prompt_html():
    product = import_script(REPO_ROOT / "hook/vanilla.py").parse_product(HOOK_HTML)
    check_hook_product(product)
    assert product["shipping"] == {
        "origin": "Reno",
        "min_days": 2,
        "max_days": 3,
        "expedited_available": True,
    }


def test_hook_with_checklist_runs_on_the_prompt_html(monkeypatch):
    shipping = {"origin": "Reno", "min_days": 2, "max_days": 3, "expedited_available": True}

    class FakeAnthropic:
        def __init__(self):
            self.messages = self

        def create(self, **kwargs):
            assert kwargs["tool_choice"] == {"type": "tool", "name": "shipping"}
            assert "business days" in kwargs["messages"][0]["content"]
            return SimpleNamespace(content=[SimpleNamespace(input=shipping)])

    monkeypatch.setitem(sys.modules, "anthropic", SimpleNamespace(Anthropic=FakeAnthropic))
    product = import_script(REPO_ROOT / "hook/with_checklist.py").extract_product(HOOK_HTML)
    check_hook_product(product)
    assert product["shipping"] == shipping


def test_slides_quote_the_hook_files_verbatim():
    # whitespace-insensitive so that slides may re-wrap lines, nothing else
    exhibits = "".join(
        "".join(path.read_text().split()) for path in (REPO_ROOT / "hook").glob("*.py")
    )
    slides = (REPO_ROOT / "slides.md").read_text()
    for block in re.findall(r"```python\n(.*?)```", slides, re.S):
        for line in block.splitlines():
            if line.strip() and not line.lstrip().startswith("#"):
                assert "".join(line.split()) in exhibits, line
