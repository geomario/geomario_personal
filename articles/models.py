from django.db import models
from django.urls import reverse

from portfolio.models import Post

from .rendering import source_path


class Article(models.Model):
    """An article hosted on this site.

    The details below are edited in /admin; the text is Markdown in the repository at
    articles/content/<slug>/index.md, with its images next to it in images/.
    """

    slug = models.SlugField(
        unique=True,
        help_text="The page address (/writing/<slug>/) and the folder name in articles/content/.",
    )
    title = models.CharField(max_length=200)
    date = models.DateField()
    excerpt = models.TextField(help_text="Shown on the Writing tile and as the page's description.")
    span = models.CharField(
        max_length=10,
        choices=Post.Span.choices,
        default=Post.Span.SQUARE,
        blank=True,
        help_text="Tile size on the Writing tab.",
    )
    medium_url = models.URLField(
        blank=True, help_text="The Medium copy, once imported. Shown as a link at the end of the article."
    )
    is_published = models.BooleanField(
        default=False, help_text="Drafts are only visible to staff who are logged in to /admin."
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("articles:detail", args=[self.slug])

    @property
    def has_content(self):
        return source_path(self.slug).is_file()
