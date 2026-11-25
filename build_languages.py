"""Сборка и предпросмотр сайта из публичной выгрузки (Python 3.11+)."""

import argparse
from copy import deepcopy
from functools import partial
from html import escape
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from posixpath import relpath
import re
import shutil
import subprocess
from tempfile import TemporaryDirectory
import tomllib
from urllib.parse import quote, urlsplit


ROOT = Path(__file__).resolve().parent
ORIGINAL = "ru"
SWITCHER_CSS = "stylesheets/kb-languages.css"
THEME_HEADER = '<div class="md-header__source">'
BODY_START = re.compile(r"<body\b[^>]*>", re.IGNORECASE)
HEAD_END = re.compile(r"</head\s*>", re.IGNORECASE)

SWITCHER_STYLES = """\
.kb-language { position: relative; margin-inline: .35rem; white-space: nowrap; }
.kb-language summary { cursor: pointer; padding: .35rem; }
.kb-language ul {
  position: absolute; inset-inline-end: 0; z-index: 2; min-width: max-content;
  margin: 0; padding: .25rem; list-style: none; border-radius: .2rem;
  background: var(--md-default-bg-color, Canvas); color: var(--md-default-fg-color, CanvasText);
  box-shadow: 0 .15rem .6rem #0004;
}
.kb-language li > * { display: block; padding: .35rem .5rem; }
.kb-language a { color: var(--md-typeset-a-color, LinkText); text-decoration: underline; }
.kb-language [aria-current] { font-weight: 700; }
.kb-language-standalone { display: flex; justify-content: flex-end; padding: .4rem 1rem 0; }
"""


def translated_nav(source, language):
    pages = sorted(
        p.relative_to(source).as_posix()
        for p in source.rglob("*.md")
        if p.is_file() and p != source / "index.md"
        and not any(part.startswith(".") for part in p.relative_to(source).parts)
    )
    # Labels come from the translated Markdown, not the (stable) Russian filenames.
    return [{language["home"]: "index.md"}, *pages]


def language_config(base, base_url, code, language, source):
    config = deepcopy(base)
    config.update(docs_dir="docs", site_dir="site", site_url=f"{base_url}{code}/")
    theme = config.setdefault("theme", {})
    theme["language"] = code
    # Zensical's instant navigation doesn't replace the surrounding header.
    # A normal load keeps the per-page language choices and locale search in sync.
    theme["features"] = [
        feature for feature in theme.get("features", [])
        if feature != "navigation.instant" and not feature.startswith("navigation.instant.")
    ]
    if code != ORIGINAL:
        config["nav"] = translated_nav(source, language)
        config["site_description"] = language.get("description")
        palette = theme.get("palette", [])
        if palette:
            labels = language.get("palette_labels", ["Light mode", "Dark mode", "System preference"])
            for entry, label in zip(palette, labels, strict=True):
                entry["toggle"]["name"] = label
    config["extra_css"] = [*base.get("extra_css", []), *language.get("extra_css", [])]
    return config


def build_locale(base, base_url, code, language, work, site):
    original_docs = ROOT / "docs"
    source = original_docs if code == ORIGINAL else ROOT / "translations" / code
    if not (source / "index.md").is_file():
        raise ValueError(f"Нет главной страницы: {source.relative_to(ROOT) / 'index.md'}")

    work.mkdir()
    docs = work / "docs"
    shutil.copytree(source, docs)
    if code != ORIGINAL:
        for css in base.get("extra_css", []):
            if urlsplit(css).scheme or css.startswith("//"):
                continue
            target = docs / css
            if target.exists():
                raise ValueError(f"{code}: общий CSS уже существует в переводе: {css}")
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(original_docs / css, target)

    config = language_config(base, base_url, code, language, source)
    # Zensical accepts mkdocs.yml; JSON is valid YAML. Preserve the parsed TOML
    # settings (including the Russian nav) without editing the export's config.
    (work / "mkdocs.yml").write_text(json.dumps(config, ensure_ascii=False), encoding="utf-8")
    print(f"Сборка /{code}/", flush=True)
    subprocess.run(["zensical", "build", "--clean", "-f", "mkdocs.yml"], cwd=work, check=True)
    (work / "site").rename(site / code)

    # Russian placeholder URLs are still deployed and redirected from their old
    # locations, but placeholders aren't destinations of the language switcher.
    stubs = set()
    if code == ORIGINAL:
        for md in source.rglob("*.md"):
            with md.open(encoding="utf-8") as f:
                if f.readline().strip() != "---" or f.readline().strip() != "kb_stub: true":
                    continue
            path = md.relative_to(source)
            if path.name in {"index.md", "README.md"}:
                stubs.add(path.with_name("index.html"))
            elif config.get("use_directory_urls", True):
                stubs.add(path.with_suffix("") / "index.html")
            else:
                stubs.add(path.with_suffix(".html"))
    return stubs


def relative_url(page, target, *, directory_urls):
    relative = quote(relpath(target.as_posix(), page.parent.as_posix()), safe="/")
    if directory_urls and target.name == "index.html":
        return relative.removesuffix("index.html") or "./"
    return relative


def switcher(code, page, languages, counterparts, directory_urls):
    language = languages[code]
    items = []
    alternates = []
    for other, translation in languages.items():
        name = f'<span lang="{other}">{escape(translation["name"])}</span>'
        href = (
            escape(relative_url(code / page, other / page, directory_urls=directory_urls), quote=True)
            if other in counterparts else None
        )
        if other == code:
            item = f'<span aria-current="page">{name}</span>'
        elif href is not None:
            item = f'<a href="{href}" hreflang="{other}">{name}</a>'
        else:
            item = f'<span>{name} — {escape(language["unavailable"])}</span>'
        items.append(f"<li>{item}</li>")
        if href is not None and code in counterparts and len(counterparts) > 1:
            alternates.append(f'<link rel="alternate" hreflang="{other}" href="{href}">')

    menu = (
        '<details class="kb-language">'
        f'<summary aria-label="{escape(language["selector"] + ": " + language["name"], quote=True)}">'
        f'{escape(language["name"])}</summary><ul>{"".join(items)}</ul></details>'
    )
    return menu, "\n".join(alternates)


def decorate_locale(site, code, languages, pages, counterparts, directory_urls):
    stylesheet = site / code / SWITCHER_CSS
    stylesheet.parent.mkdir(exist_ok=True)
    with stylesheet.open("x", encoding="utf-8") as css:
        css.write(SWITCHER_STYLES)

    for page in sorted(pages):
        path = site / code / page
        markup = path.read_text(encoding="utf-8")
        head = HEAD_END.search(markup)
        if not head:
            continue  # HTML fragments are resources, not standalone pages.
        menu, alternates = switcher(code, page, languages, counterparts.get(page, ()), directory_urls)
        href = relative_url(code / page, code / Path(SWITCHER_CSS), directory_urls=directory_urls)
        pos = head.start()
        markup = f'{markup[:pos]}<link rel="stylesheet" href="{escape(href, quote=True)}">\n{alternates}\n{markup[pos:]}'
        if THEME_HEADER in markup:
            markup = markup.replace(THEME_HEADER, f"{menu}\n    {THEME_HEADER}", 1)
        else:
            # Zensical copies standalone HTML (e.g. the roadmap) as-is.
            body = BODY_START.search(markup, pos)
            if not body:
                continue
            pos = body.end()
            markup = f'{markup[:pos]}<header class="kb-language-standalone">{menu}</header>{markup[pos:]}'
        path.write_text(markup, encoding="utf-8")


def write_redirects(site, pages, languages, directory_urls):
    reserved = {code.casefold() for code in languages}
    for page in sorted(pages):
        if len(page.parts) > 1 and page.parts[0].casefold() in reserved:
            raise ValueError(f"Старый путь занят языковым разделом: {page}")
        href = relative_url(page, ORIGINAL / page, directory_urls=directory_urls)
        alias = site / page
        alias.parent.mkdir(parents=True, exist_ok=True)
        alias.write_text(
            '<!doctype html>\n<html lang="ru"><meta charset="utf-8">\n'
            '<meta name="robots" content="noindex">\n<title>Страница переехала</title>\n'
            '<script>\n'
            f'const destination = new URL({json.dumps(href)}, location.href);\n'
            'destination.search = location.search;\ndestination.hash = location.hash;\n'
            'location.replace(destination.href);\n</script>\n'
            f'<p><a href="{escape(href, quote=True)}">Открыть страницу на новом адресе</a></p></html>\n',
            encoding="utf-8",
        )


def build():
    with (ROOT / "zensical.toml").open("rb") as config:
        base = tomllib.load(config)["project"]
    base_url = base["site_url"].rstrip("/") + "/"
    directory_urls = base.get("use_directory_urls", True)
    languages = json.loads((ROOT / "languages.json").read_text(encoding="utf-8"))
    if ORIGINAL not in languages:
        raise ValueError(f"В languages.json нужен язык {ORIGINAL}")
    if any(not re.fullmatch(r"[a-z]{2,3}(?:-[A-Za-z0-9]{2,8})*", code) for code in languages):
        raise ValueError("В languages.json допустимы языковые коды Zensical, например ru, en, zh")

    output = ROOT / "site"
    with TemporaryDirectory(prefix=".languages-", dir=ROOT) as workspace:
        work = Path(workspace)
        site = work / "site"
        site.mkdir()
        pages = {}
        counterparts = {}
        for code, language in languages.items():
            stubs = build_locale(base, base_url, code, language, work / code, site)
            locale = site / code
            pages[code] = {p.relative_to(locale) for p in locale.rglob("*.html") if p.is_file()} - {Path("404.html")}
            for page in pages[code] - stubs:
                counterparts.setdefault(page, set()).add(code)

        for code in languages:
            decorate_locale(site, code, languages, pages[code], counterparts, directory_urls)
        write_redirects(site, pages[ORIGINAL], languages, directory_urls)
        shutil.copy2(site / ORIGINAL / "404.html", site / "404.html")
        urls = (f"<sitemap><loc>{escape(base_url + code + '/sitemap.xml')}</loc></sitemap>" for code in languages)
        (site / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</sitemapindex>\n",
            encoding="utf-8",
        )
        if output.exists():
            shutil.rmtree(output)
        site.rename(output)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serve", action="store_true", help="после сборки открыть предпросмотр на порту 8000")
    args = parser.parse_args()
    try:
        site = build()
    except subprocess.CalledProcessError as error:
        parser.exit(error.returncode)
    except (KeyError, OSError, ValueError) as error:
        parser.exit(1, f"Ошибка сборки: {error}\n")
    if args.serve:
        handler = partial(SimpleHTTPRequestHandler, directory=site)
        with ThreadingHTTPServer(("127.0.0.1", 8000), handler) as server:
            print("Предпросмотр: http://127.0.0.1:8000/", flush=True)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass


if __name__ == "__main__":
    main()
