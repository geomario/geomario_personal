"""Adds the first hosted article, Practical Packet Analysis chapter 1, as a draft.

Its text and images are in articles/content/packet-analysis-chapter-1/. It starts
unpublished so it can be checked on the live site (staff only) before going public;
publish it from /admin. The values are copied here because migrations must not change
later; edit the article in the admin afterwards.
"""

import datetime

from django.db import migrations

ARTICLE = {
    "slug": "packet-analysis-chapter-1",
    "title": "I Read 7 Pages of a Packet Analysis Book and It Changed How I Think About My Phone",
    "date": datetime.date(2026, 11, 8),
    "excerpt": (
        "A mobile researcher's notes on Chapter 1 of Practical Packet Analysis, and why the "
        "OSI model is the vocabulary you need before you build anything."
    ),
    "span": "feature",
    "is_published": False,
}


def add_article(apps, schema_editor):
    Article = apps.get_model("articles", "Article")
    Article.objects.get_or_create(slug=ARTICLE["slug"], defaults=ARTICLE)


def remove_article(apps, schema_editor):
    apps.get_model("articles", "Article").objects.filter(slug=ARTICLE["slug"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_article, remove_article),
    ]
