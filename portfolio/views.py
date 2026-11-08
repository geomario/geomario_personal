from django.shortcuts import render

from articles.models import Article

from .models import FocusArea, Post, Project, Publication, TimelineEntry
from .site import site_context


def writing_items():
    """Hosted articles first, then posts elsewhere, each in its admin order."""
    return [*Article.objects.filter(is_published=True), *Post.objects.all()]


def page(request, template, active, **context):
    return render(request, template, {**site_context(), "active": active, **context})


def index(request):
    """The landing page is the About page, with a badge pointing to the newest writing."""
    items = writing_items()
    return page(request, "portfolio/index.html", "about", latest=items[0] if items else None)


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


def publications(request):
    return page(request, "portfolio/publications.html", "publications", publications=Publication.objects.all())


def experience(request):
    return page(request, "portfolio/experience.html", "experience", timeline=TimelineEntry.objects.all())
