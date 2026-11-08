"""Adds the GESIS Surf paper (preprint, submitted to SoftwareX) to Publications.

The values are copied here because migrations must not change later; edit the entry in
/admin afterwards, e.g. to mark it published and point it to the DOI.
"""

from django.db import migrations

PAPER = {
    "title": (
        "GESIS Surf: An Open-Source Infrastructure for Privacy-Preserving Longitudinal "
        "Web Browsing Data Collection"
    ),
    "authors": "Mario Alberto Ramirez, Frank Mangold, Sebastian Stier",
    "venue": "SoftwareX",
    "year": 2026,
    "status": "under_review",
    "url": "https://arxiv.org/abs/2610.41441",
    "code_url": "https://github.com/gesiscss/gesis_surf_extension",
}


def add_paper(apps, schema_editor):
    Publication = apps.get_model("portfolio", "Publication")
    Publication.objects.get_or_create(url=PAPER["url"], defaults=PAPER)


def remove_paper(apps, schema_editor):
    apps.get_model("portfolio", "Publication").objects.filter(url=PAPER["url"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0009_publication"),
    ]

    operations = [
        migrations.RunPython(add_paper, remove_paper),
    ]
