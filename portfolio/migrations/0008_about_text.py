"""Fills in the About page text, so it reaches production with the redesign.

Only an empty About field is filled, so text written in /admin is never replaced. The text
is copied here because migrations must not change later; edit it in the admin afterwards.
"""

from django.db import migrations

ABOUT = """I'm a research software engineer at GESIS – Leibniz Institute for the Social Sciences. \
I design and develop tools that capture behavioural data from web browsing and mobile apps, \
and I build the analyses and machine-learning models that turn those traces into findings \
researchers can trust.

Lately, we have been designing AI infrastructure for our research and building it into our \
work. That includes MCP servers that let AI agents query and work with research data within \
clear limits, so computational social scientists can use these tools without losing control \
of their data. We are also building with agents that work together through A2A, the open \
protocol for agent-to-agent communication.

Part of my work is helping lead the Computational Social Science department at GESIS into \
this next stage: taking our research software infrastructure to agents and open agent \
protocols such as MCP and A2A.

I got here by a winding path. I started in geophysics, monitoring geothermal wells and \
modelling what the sensors told us. Then I built data platforms and software in open \
finance and legal tech, where I led the software development and data science department. \
The thread through all of it: collect data carefully, build systems that keep it reliable, \
and turn it into decisions and peer-reviewed findings."""


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
