from django.urls import path

from . import views

app_name = "articles"

urlpatterns = [
    path("writing/<slug:slug>/", views.detail, name="detail"),
]
