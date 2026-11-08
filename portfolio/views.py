from django.shortcuts import render

from articles.models import Article

from .models import FocusArea, Post, Project, TimelineEntry
from .site import site_context


def index(request):
    context = {
        **site_context(),
        # Only areas that have projects, so no chip filters down to nothing.
        "focus_areas": FocusArea.objects.filter(projects__isnull=False).distinct(),
        "timeline": TimelineEntry.objects.all(),
        "projects": Project.objects.select_related("tag"),
        "articles": Article.objects.filter(is_published=True),
        "writing": Post.objects.all(),
    }
    return render(request, "portfolio/index.html", context)
