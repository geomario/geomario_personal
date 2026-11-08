from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    # The About page is the landing page.
    path("", views.index, name="index"),
    path("about/", RedirectView.as_view(pattern_name="index", permanent=True)),
    path("favicon.ico", views.favicon),
    path("projects/", views.projects, name="projects"),
    # Single articles are /writing/<slug>/, in the articles app.
    path("writing/", views.writing, name="writing"),
    path("publications/", views.publications, name="publications"),
    path("experience/", views.experience, name="experience"),
]
