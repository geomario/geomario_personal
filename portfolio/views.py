from django.shortcuts import render

from .models import FocusArea, Post, Project, TimelineEntry


def index(request):
    context = {
        "focus_areas": list(FocusArea.objects.values_list("name", flat=True)),
        "timeline": list(TimelineEntry.objects.values("when", "title", "org", "body")),
        "projects": list(
            Project.objects.select_related("tag").values(
                "name", "tag__name", "desc", "stack"
            )
        ),
        "writing": list(
            Post.objects.values("title", "date", "source", "url", "excerpt", "span")
        ),
    }
    # Normalize keys so the existing template (which expects p.tag, not p.tag__name)
    # keeps working unchanged.
    for p in context["projects"]:
        p["tag"] = p.pop("tag__name")
    return render(request, "portfolio/index.html", context)
