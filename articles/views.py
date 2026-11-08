import logging

from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils.safestring import mark_safe

from portfolio.site import site_context

from .models import Article
from .rendering import render_article

logger = logging.getLogger(__name__)


def detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if not article.is_published and not request.user.is_staff:
        raise Http404("No such article.")
    try:
        rendered = render_article(article.slug, request.build_absolute_uri)
    except FileNotFoundError:
        logger.error("Article %r has no content file", article.slug)
        raise Http404("No such article.")

    context = {
        **site_context(),
        "active": "writing",
        "article": article,
        # Written by the site owner and stored in the repository, not user input.
        "body": mark_safe(rendered.html),
        "canonical_url": request.build_absolute_uri(article.get_absolute_url()),
        "share_image": rendered.images[0] if rendered.images else "",
    }
    return render(request, "articles/article.html", context)
