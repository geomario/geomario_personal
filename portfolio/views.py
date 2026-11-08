from django.shortcuts import render

from articles.models import Article

from .models import FocusArea, Post, Project, TimelineEntry
from .site import site_context

HOME_TILES = 4


def writing_items():
    """Hosted articles first, then posts elsewhere, each in its admin order."""
    return [*Article.objects.filter(is_published=True), *Post.objects.all()]


def page(request, template, active, **context):
    return render(request, template, {**site_context(), "active": active, **context})


def index(request):
    return page(
        request,
        "portfolio/index.html",
        "home",
        latest=writing_items()[:HOME_TILES],
        timeline=TimelineEntry.objects.all(),
    )


def about(request):
    return page(request, "portfolio/about.html", "about")


def projects(request):
    return page(
        request,
        "portfolio/projects.html",
        "projects",
        # Only areas that have projects, so no chip filters down to nothing.
        focus_areas=FocusArea.objects.filter(projects__isnull=False).distinct(),
        projects=Project.objects.select_related("tag"),
    )


def writing(request):
    return page(request, "portfolio/writing.html", "writing", items=writing_items())


def experience(request):
    return page(request, "portfolio/experience.html", "experience", timeline=TimelineEntry.objects.all())
