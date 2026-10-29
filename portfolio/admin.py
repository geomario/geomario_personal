from django.contrib import admin

from .models import FocusArea, Post, Profile, ProfileLink, Project, TimelineEntry


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "role")

    # There is exactly one profile: it can be edited, not added twice or deleted.
    def has_add_permission(self, request):
        return not Profile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ProfileLink)
class ProfileLinkAdmin(admin.ModelAdmin):
    list_display = ("kind", "url", "order")
    list_editable = ("url", "order")


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
    list_display = ("name", "tag", "url", "order")
    list_editable = ("order",)
    list_filter = ("tag",)
    search_fields = ("name", "desc")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "source", "span", "order")
    list_editable = ("order", "span")
    list_filter = ("span",)
    search_fields = ("title", "source")
