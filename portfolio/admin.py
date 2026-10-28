from django.contrib import admin

from .models import FocusArea, Post, Project, TimelineEntry


@admin.register(FocusArea)
class FocusAreaAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(TimelineEntry)
class TimelineEntryAdmin(admin.ModelAdmin):
    list_display = ("when", "title", "org", "order")
    list_editable = ("order",)
    search_fields = ("title", "org")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "tag", "order")
    list_editable = ("order",)
    list_filter = ("tag",)
    search_fields = ("name", "desc")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "source", "span", "order")
    list_editable = ("order", "span")
    list_filter = ("span",)
    search_fields = ("title", "source")
