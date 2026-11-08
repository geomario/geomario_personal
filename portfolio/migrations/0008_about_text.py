"""Fills in the About page text, so it reaches production with the redesign.

Only an empty About field is filled, so text written in /admin is never replaced. The text
is copied here because migrations must not change later; edit it in the admin afterwards.
"""

from django.db import migrations

ABOUT = """I'm a research software engineer at GESIS – Leibniz Institute for the Social Sciences. \
I design tools that capture behavioural data from web browsing and mobile apps, and build the \
analyses and machine-learning models that turn those traces into findings researchers can trust.

Lately, we have been bringing AI infrastructure into our research: MCP servers that let AI \
agents work with research data within clear limits, and agents that collaborate through A2A. \
Part of my work is helping lead the Computational Social Science department at GESIS into \
this next stage.

Before GESIS, I worked in geophysics, then built data platforms and software in open finance \
and legal tech, where I led the software development and data science department."""


def fill_about(apps, schema_editor):
    apps.get_model("portfolio", "Profile").objects.filter(about="").update(about=ABOUT)


def clear_about(apps, schema_editor):
    apps.get_model("portfolio", "Profile").objects.filter(about=ABOUT).update(about="")


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0007_profile_about"),
    ]

    operations = [
        migrations.RunPython(fill_about, clear_about),
    ]
