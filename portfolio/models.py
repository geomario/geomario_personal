from django.db import models


class FocusArea(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class TimelineEntry(models.Model):
    when = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    org = models.CharField(max_length=200)
    body = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Project(models.Model):
    name = models.CharField(max_length=200)
    tag = models.ForeignKey(
        FocusArea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
    )
    desc = models.TextField()
    stack = models.JSONField(default=list)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class Post(models.Model):
    class Span(models.TextChoices):
        SQUARE = "", "Square (1x1)"
        FEATURE = "feature", "Feature (2x2)"
        WIDE = "wide", "Wide (2x1)"
        TALL = "tall", "Tall (1x2)"

    title = models.CharField(max_length=200)
    date = models.CharField(max_length=50)
    source = models.CharField(max_length=200)
    url = models.URLField()
    excerpt = models.TextField()
    span = models.CharField(
        max_length=10, choices=Span.choices, default=Span.SQUARE, blank=True
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title