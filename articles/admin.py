from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "is_published", "has_content", "span", "order")
    list_editable = ("is_published", "order")
    list_filter = ("is_published",)
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}

    @admin.display(boolean=True, description="Content file")
    def has_content(self, obj):
        return obj.has_content
