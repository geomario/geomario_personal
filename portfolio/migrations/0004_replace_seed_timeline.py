"""Replaces the original placeholder timeline with the real career entries.

Only touches databases that still have the four placeholder entries (matched by title),
such as production: anything added or edited in the admin stays. A fresh database has no
timeline yet at this point and gets the new entries from portfolio/data.py instead, via
load_initial_data. The entries are copied here because migrations must not change when
data.py does.
"""

from django.db import migrations

PLACEHOLDER_TITLES = [
    "Geosciences → self-taught engineering",
    "Engineering leadership",
    "Visiting researcher",
    "Software Research Engineer & PhD Candidate",
]

TIMELINE = [
    (
        "Energy research",
        "Research Associate, Applied Geophysics & Geothermal Energy",
        "E.ON Energy Research Center",
        "Monitored geothermal wells with fibre-optic temperature sensing, built the PostgreSQL "
        "databases behind it, and turned the data into predictive models and numerical "
        "reservoir simulations.",
    ),
    (
        "Legal tech",
        "Head of Software Development & Data Science",
        "GeoLegalTech GmbH",
        "Joined as a senior full-stack and data science developer, then led the company's "
        "software development and data science.",
    ),
    (
        "Open finance",
        "Senior Full Stack & Data Developer",
        "Finerio Connect",
        "Built and secured data connections to banks' APIs with Python on AWS Lambda, keeping "
        "open-finance data accurate, current and protected.",
    ),
    (
        "Research",
        "Senior Research Software Engineer",
        "GESIS – Leibniz Institute for the Social Sciences",
        "Building the software and algorithms that collect and model digital behavioural data "
        "from web and mobile, and supporting researchers from study design to publication, "
        "with open science as the default.",
    ),
    (
        "Behavioral analytics",
        "Doctoral Researcher, IT & Business Analytics",
        "University of Cologne",
        "How people go from first click to purchase: modelling browsing and buying behaviour "
        "to uncover shopper segments and the decision points that drive conversion.",
    ),
]


def replace_placeholders(apps, schema_editor):
    TimelineEntry = apps.get_model("portfolio", "TimelineEntry")
    placeholders = TimelineEntry.objects.filter(title__in=PLACEHOLDER_TITLES)
    if not placeholders.exists():
        return
    placeholders.delete()
    for order, (when, title, org, body) in enumerate(TIMELINE):
        TimelineEntry.objects.create(when=when, title=title, org=org, body=body, order=order)


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0003_initial_profile"),
    ]

    operations = [
        migrations.RunPython(replace_placeholders, migrations.RunPython.noop),
    ]
