from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("projects/", views.projects, name="projects"),
    # Single articles are /writing/<slug>/, in the articles app.
    path("writing/", views.writing, name="writing"),
    path("experience/", views.experience, name="experience"),
]
