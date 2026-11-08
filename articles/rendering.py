"""Turns an article's Markdown file into HTML for its page.

Each article is a folder, articles/content/<slug>/, holding index.md and an images/
folder. Image paths in the Markdown stay relative (images/01-hero.png), so the file also
previews correctly in an editor; here they become absolute static-file URLs, which
Medium's "Import a story" needs to fetch them.
"""

from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

import markdown
from django.conf import settings
from django.templatetags.static import static
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

# Everything after this line in index.md is left out of the page (production notes etc.).
CUT_MARKER = "<!-- not-for-publication -->"


def source_path(slug):
    return Path(settings.ARTICLES_CONTENT_DIR) / slug / "index.md"


def is_local(src):
    """True for a relative path inside the article folder, e.g. images/01-hero.png."""
    parts = urlsplit(src)
    path = PurePosixPath(parts.path)
    return bool(src) and not parts.scheme and not parts.netloc and not path.is_absolute() and ".." not in path.parts


@dataclass
class RenderedArticle:
    html: str
    images: list = field(default_factory=list)


class _ArticleTree(Treeprocessor):
    def __init__(self, md, slug, absolute_url):
        super().__init__(md)
        self.slug = slug
        self.absolute_url = absolute_url
        self.images = []

    def run(self, root):
        # The page template shows the title, so drop the Markdown's own top heading.
        first = root.find("h1")
        if first is not None:
            root.remove(first)

        for i, img in enumerate(root.iter("img")):
            src = img.get("src", "")
            if is_local(src):
                try:
                    src = self.absolute_url(static(f"articles/{self.slug}/{PurePosixPath(src)}"))
                except ValueError:
                    pass  # Not collected (manifest storage): leave the path as written.
                img.set("src", src)
            if i:  # the first image is usually at the top of the page
                img.set("loading", "lazy")
            img.set("decoding", "async")
            self.images.append(src)

        # A paragraph holding only an image is a figure.
        for p in root.iter("p"):
            if len(p) == 1 and p[0].tag == "img" and not (p.text or "").strip() and not (p[0].tail or "").strip():
                p.tag = "figure"


class _ArticleExtension(Extension):
    def __init__(self, tree):
        super().__init__()
        self.tree = tree

    def extendMarkdown(self, md):
        # After "inline" (20), which creates the <img> elements.
        md.treeprocessors.register(self.tree, "article", 15)


def render_article(slug, absolute_url=lambda url: url):
    """Render articles/content/<slug>/index.md. Raises FileNotFoundError if it is missing."""
    text = source_path(slug).read_text(encoding="utf-8")
    text = text.split(CUT_MARKER, 1)[0]
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "toc"])
    tree = _ArticleTree(md, slug, absolute_url)
    _ArticleExtension(tree).extendMarkdown(md)
    return RenderedArticle(html=md.convert(text), images=tree.images)
