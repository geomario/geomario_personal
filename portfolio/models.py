from django.db import models


class Profile(models.Model):
    """The site owner's details for the hero and footer. There is only one."""

    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    intro = models.TextField(help_text="Short introduction on the home page.")
    about = models.TextField(
        blank=True,
        help_text="Longer text for the About page; an empty line starts a new paragraph. "
        "Leave empty to show the introduction there.",
    )
    availability = models.CharField(
        max_length=200,
        blank=True,
        help_text="Short line above the name, e.g. what you are open to. Leave empty to hide it.",
    )
    location = models.CharField(max_length=100, blank=True)
    organisation = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class ProfileLink(models.Model):
    """A profile elsewhere (GitHub, LinkedIn...), shown with its logo."""

    class Kind(models.TextChoices):
        GITHUB = "github", "GitHub"
        LINKEDIN = "linkedin", "LinkedIn"
        ORCID = "orcid", "ORCID"
        RESEARCHGATE = "researchgate", "ResearchGate"
        MEDIUM = "medium", "Medium"

    kind = models.CharField(max_length=20, choices=Kind.choices, unique=True)
    url = models.URLField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.get_kind_display()

    @property
    def icon_template(self):
        return f"portfolio/icons/{self.kind}.svg"


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
    location = models.CharField(
        max_length=100, blank=True, help_text="Shown after the organisation, e.g. Cologne."
    )
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
    url = models.URLField(
        blank=True, help_text="Repository, paper or demo. Leave empty if there is none."
    )
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


class Publication(models.Model):
    """A paper or preprint on the Publications page."""

    class Status(models.TextChoices):
        PUBLISHED = "published", "Published"
        UNDER_REVIEW = "under_review", "Under review"
        PREPRINT = "preprint", "Preprint"

    title = models.CharField(max_length=300)
    authors = models.CharField(
        max_length=500, help_text="As on the paper, e.g. Mario Alberto Ramirez, Frank Mangold, Sebastian Stier."
    )
    venue = models.CharField(
        max_length=200,
        blank=True,
        help_text="Journal or conference, e.g. SoftwareX. While under review, the one it was submitted to.",
    )
    year = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PUBLISHED)
    url = models.URLField(
        help_text="Where to read it: the DOI or journal page, or the preprint (arXiv) while under review."
    )
    code_url = models.URLField(blank=True, help_text="Repository with the code, if any.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-year", "id"]

    def __str__(self):
        return self.title
