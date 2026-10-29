from django.shortcuts import render

from .models import FocusArea, Post, Profile, ProfileLink, Project, TimelineEntry


def index(request):
    context = {
        "profile": Profile.objects.first(),
        "links": ProfileLink.objects.all(),
        # Only areas that have projects, so no chip filters down to nothing.
        "focus_areas": FocusArea.objects.filter(projects__isnull=False).distinct(),
        "timeline": TimelineEntry.objects.all(),
        "projects": Project.objects.select_related("tag"),
        "writing": Post.objects.all(),
    }
    return render(request, "portfolio/index.html", context)
