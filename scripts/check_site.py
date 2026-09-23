"""Check built-site local links and fragment targets using the Python standard library."""
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import unquote, urljoin, urlsplit


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'a' and attrs.get('name'):
            self.ids.add(attrs['name'])
        for key in ('href', 'src'):
            if attrs.get(key):
                self.links.append(attrs[key])


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site').resolve()
    pages = {p: Page(p.read_text()) for p in root.rglob('*.html')}
    if not pages:
        raise SystemExit(f'No built HTML pages found in {root}')
    errors = set()
    checked = 0
    for source, page in pages.items():
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
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
