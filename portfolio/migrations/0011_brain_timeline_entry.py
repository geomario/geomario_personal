"""Adds the BRAIN (market research) role to the timeline, between the University of Cologne
and Finerio Connect entries.

Only touches databases that already have a timeline, such as production; a fresh database
gets the entry from portfolio/data.py via load_initial_data. Entries from that position on
move down one place. The values are copied here because migrations must not change later.
"""

from django.db import migrations
from django.db.models import F

ENTRY = {
    "when": "Market research",
    "title": "Co-Lead, Data Infrastructure & Machine Learning",
    "org": "BRAIN",
    "location": "Mexico City (remote)",
    "body": (
        "Co-led the design and build of the company's entire market research "
        "infrastructure, from data collection to the pipelines and machine-learning "
        "models behind its consumer, shopper and brand studies, turning research data "
        "into insights for clients."
    ),
}


def add_entry(apps, schema_editor):
    TimelineEntry = apps.get_model("portfolio", "TimelineEntry")
    if not TimelineEntry.objects.exists() or TimelineEntry.objects.filter(org=ENTRY["org"]).exists():
        return
    finerio = TimelineEntry.objects.filter(org="Finerio Connect").order_by("order", "id").first()
    position = finerio.order if finerio else TimelineEntry.objects.count()
    TimelineEntry.objects.filter(order__gte=position).update(order=F("order") + 1)
    TimelineEntry.objects.create(order=position, **ENTRY)


def remove_entry(apps, schema_editor):
    apps.get_model("portfolio", "TimelineEntry").objects.filter(
        org=ENTRY["org"], title=ENTRY["title"]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0010_gesis_surf_paper"),
    ]

    operations = [
        migrations.RunPython(add_entry, remove_entry),
    ]
