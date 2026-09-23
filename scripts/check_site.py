"""Check built-site links, fragments, and unrendered Markdown tables."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urljoin, urlsplit


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.in_main = False
        self.paragraph = None
        self.unrendered_tables = []
        self.table_count = 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        if tag == 'main':
            self.in_main = True
        if self.in_main and tag == 'table':
            self.table_count += 1
        if self.in_main and tag == 'p':
            self.paragraph = []
        if tag == 'br' and self.paragraph is not None:
            self.paragraph.append('\n')
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'a' and attrs.get('name'):
            self.ids.add(attrs['name'])
        for key in ('href', 'src'):
            if attrs.get(key):
                self.links.append(attrs[key])

    def handle_data(self, data):
        if self.paragraph is not None:
            self.paragraph.append(data)

    def handle_endtag(self, tag):
        if tag == 'p' and self.paragraph is not None:
            text = ''.join(self.paragraph)
            # Kramdown smart punctuation converts raw table dashes to en/em dashes.
            if re.search(r'\|\s*:?[-–—]{2,}:?\s*\|', text):
                self.unrendered_tables.append(' '.join(text.split())[:120])
            self.paragraph = None
        if tag == 'main':
            self.in_main = False


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site').resolve()
    pages = {p: Page(p.read_text()) for p in root.rglob('*.html')}
    if not pages:
        raise SystemExit(f'No built HTML pages found in {root}')
    errors = set()
    checked = 0
    for source, page in pages.items():
        for index, snippet in enumerate(page.unrendered_tables, start=1):
            errors.add(f'{source.relative_to(root)}: unrendered table {index}: {snippet}')
        source_url = '/' + source.relative_to(root).as_posix()
        for href in page.links:
            parts = urlsplit(href)
            if parts.scheme not in ('', 'http', 'https'):
                continue
            if parts.netloc and parts.netloc != 'lunyang.github.io':
                continue
            resolved = urlsplit(urljoin(source_url, href))
            target = root / unquote(resolved.path).lstrip('/')
            if target.is_dir():
                target /= 'index.html'
            checked += 1
            if not target.is_file():
                errors.add(f'{source.relative_to(root)}: missing {href}')
            elif resolved.fragment and target in pages:
                fragment = unquote(resolved.fragment)
                if fragment not in pages[target].ids:
                    errors.add(f'{source.relative_to(root)}: missing fragment {href}')
    for error in sorted(errors):
        print(error)
    print(f'{len(pages)} HTML pages; {checked} internal references; {len(errors)} errors')
    print(f'{sum(p.table_count for p in pages.values())} rendered content tables; '
          f'{sum(len(p.unrendered_tables) for p in pages.values())} unrendered tables')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
