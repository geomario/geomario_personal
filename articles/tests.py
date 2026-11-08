import datetime
import shutil
import tempfile
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from articles.finders import ArticleAssetsFinder
from articles.models import Article
from articles.rendering import CUT_MARKER, is_local, render_article

# Tests run with DEBUG off, where the manifest storage only knows the static files
# collected when the image was built (same reason as in portfolio/tests.py).
PLAIN_STATIC = {
    **settings.STORAGES,
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

SAMPLE = f"""# Sample title

Intro paragraph with **bold** text.

![A diagram](images/diagram.png)

| a | b |
|---|---|
| 1 | 2 |

{CUT_MARKER}

## Production notes

Secret manifest.
"""


class ContentDirTestCase(TestCase):
    """Uses a temporary articles/content folder."""

    def setUp(self):
        super().setUp()
        self.content = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.content)
        override = override_settings(ARTICLES_CONTENT_DIR=self.content, STORAGES=PLAIN_STATIC)
        override.enable()
        self.addCleanup(override.disable)

    def write(self, slug="sample", text=SAMPLE):
        folder = self.content / slug
        (folder / "images").mkdir(parents=True)
        (folder / "index.md").write_text(text, encoding="utf-8")
        (folder / "images" / "diagram.png").write_bytes(b"\x89PNG")
        return folder

    def article(self, slug="sample", **fields):
        values = {"title": "Sample title", "date": datetime.date(2026, 11, 8), "excerpt": "Short summary."}
        values.update(fields)
        return Article.objects.create(slug=slug, **values)


class RenderingTests(ContentDirTestCase):
    def test_renders_markdown_and_leaves_out_production_notes(self):
        self.write()
        html = render_article("sample").html
        self.assertIn("<strong>bold</strong>", html)
        self.assertIn("<table>", html)
        self.assertNotIn("Production notes", html)
        self.assertNotIn("Secret manifest", html)

    def test_drops_the_markdown_title(self):
        self.write()
        self.assertNotIn("Sample title", render_article("sample").html)

    def test_local_images_become_absolute_figures(self):
        self.write()
        rendered = render_article("sample", lambda url: "https://example.com" + url)
        src = "https://example.com/static/articles/sample/images/diagram.png"
        self.assertIn(f'src="{src}"', rendered.html)
        self.assertIn("<figure>", rendered.html)
        self.assertEqual(rendered.images, [src])

    def test_external_images_are_left_alone(self):
        self.write(text="![x](https://cdn.example.com/x.png)\n")
        self.assertIn('src="https://cdn.example.com/x.png"', render_article("sample").html)

    def test_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            render_article("nope")

    def test_is_local(self):
        self.assertTrue(is_local("images/a.png"))
        for src in ("", "/static/a.png", "https://x.org/a.png", "//x.org/a.png", "../a.png", "images/../../a.png"):
            self.assertFalse(is_local(src), src)


class FinderTests(ContentDirTestCase):
    def test_finds_images_only(self):
        folder = self.write()
        finder = ArticleAssetsFinder()
        self.assertEqual(finder.find("articles/sample/images/diagram.png"), str(folder / "images" / "diagram.png"))
        self.assertEqual(finder.find("articles/sample/index.md"), [])
        self.assertEqual(finder.find("articles/../sample/images/diagram.png"), [])
        self.assertEqual(finder.find("portfolio/css/style.css"), [])
        listed = [path for path, storage in finder.list([])]
        self.assertEqual(listed, ["sample/images/diagram.png"])


class DetailViewTests(ContentDirTestCase):
    def test_published_article(self):
        self.write()
        article = self.article(is_published=True)
        response = self.client.get("/writing/sample/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Sample title</h1>", html=True)
        self.assertContains(response, f'<link rel="canonical" href="http://testserver{article.get_absolute_url()}">')
        self.assertContains(
            response, 'property="og:image" content="http://testserver/static/articles/sample/images/diagram.png"'
        )
        self.assertNotContains(response, "Draft")
        self.assertNotContains(response, "noindex")

    def test_draft_is_hidden_from_visitors(self):
        self.write()
        self.article()
        self.assertEqual(self.client.get("/writing/sample/").status_code, 404)

    def test_draft_is_visible_to_staff(self):
        self.write()
        self.article()
        staff = get_user_model().objects.create_user("editor", password="x", is_staff=True)
        self.client.force_login(staff)
        response = self.client.get("/writing/sample/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Draft")
        self.assertContains(response, 'name="robots" content="noindex"')

    def test_missing_content_file_is_not_found(self):
        self.article(is_published=True)
        with self.assertLogs("articles.views", "ERROR"):
            self.assertEqual(self.client.get("/writing/sample/").status_code, 404)

    def test_unknown_slug_is_not_found(self):
        self.assertEqual(self.client.get("/writing/nope/").status_code, 404)

    def test_links_to_the_medium_copy(self):
        self.write()
        self.article(is_published=True, medium_url="https://medium.com/@me/sample")
        self.assertContains(self.client.get("/writing/sample/"), 'href="https://medium.com/@me/sample"')


class WritingTabTests(ContentDirTestCase):
    def test_shows_published_articles_only(self):
        self.article(slug="live", title="Live article", is_published=True)
        self.article(slug="draft", title="Draft article")
        response = self.client.get("/")
        self.assertContains(response, 'href="/writing/live/"')
        self.assertContains(response, "Live article")
        self.assertNotContains(response, "Draft article")


@override_settings(STORAGES=PLAIN_STATIC)
class PacketAnalysisArticleTests(TestCase):
    """The real article added by migration 0002."""

    slug = "packet-analysis-chapter-1"

    def test_added_as_a_draft(self):
        article = Article.objects.get(slug=self.slug)
        self.assertFalse(article.is_published)
        self.assertTrue(article.has_content)

    def test_renders_with_all_images_present(self):
        rendered = render_article(self.slug)
        self.assertNotIn("Image manifest", rendered.html)
        self.assertEqual(len(rendered.images), 8)
        finder = ArticleAssetsFinder()
        for src in rendered.images:
            self.assertTrue(src.startswith(f"/static/articles/{self.slug}/images/"), src)
            self.assertTrue(finder.find(src[len("/static/"):]), f"missing image: {src}")
