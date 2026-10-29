"""Updates the starter projects: adds GESIS Surf and the doctoral research, rewrites the
mobile app and MCP server cards, removes the cross-retailer clustering paper and puts the
projects in a new order.

Only touches databases that still have the original starter projects (production): a
fresh database has no projects yet at this point and gets them from portfolio/data.py.
The values are copied here because migrations must not change when data.py does.
"""

from django.db import migrations

REMOVED = "Cross-Retailer Behavioural Clustering"
OLD_MOBILE_NAME = "GESISSurfMobile"
MCP_NAME = "mcp-server-gesis-surf"

GESIS_SURF = {
    "name": "GESIS Surf",
    "desc": (
        "The open-source research infrastructure behind the GESIS Surf panel: a browser "
        "extension sends windows, tabs, domains, clicks, scrolls and page HTML to a Django "
        "REST backend, where Celery processes it, PostgreSQL stores it and Elasticsearch "
        "makes it searchable, with ELK monitoring for long-running studies."
    ),
    "stack": ["Django REST", "PostgreSQL", "Celery", "Elasticsearch", "Browser extension"],
    "url": "https://github.com/gesiscss/gesis_surf_backend",
}
MOBILE = {
    "name": "GESIS Surf Mobile",
    "desc": (
        "Brings GESIS Surf to smartphones: a cross-platform React Native app that captures "
        "how participants browse and use apps, through VPN-based packet inspection on "
        "Android and iOS and the Accessibility API, so studies can follow behaviour across "
        "desktop and mobile."
    ),
    "stack": ["React Native", "Expo", "TypeScript", "VPN packet inspection", "Accessibility API"],
}
MCP = {
    "desc": (
        "Connects AI agents to the GESIS Surf infrastructure through the Model Context "
        "Protocol: a TypeScript server that lets LLM tools query the panel's PostgreSQL data "
        "and make tightly scoped updates (no inserts or deletes, a WHERE clause required, "
        "protected tables, validated inputs). Built with Spec-Driven Development."
    ),
    "stack": ["TypeScript", "MCP", "PostgreSQL", "Zod"],
}
SEGMENTS = {
    "name": "Dynamic Shopper Segments",
    "desc": (
        "Doctoral research on behaviour across many retailers: visits are clustered into "
        "behavioural states, shoppers are grouped by how they move between those states over "
        "time with Markov chains, and Fisher information measures how stable the groups are, "
        "separating seasonal swings from real shifts."
    ),
    "stack": ["Python", "Clustering", "Markov chains", "Fisher information"],
}
ORDER = [
    "GESIS Surf",
    "GESIS Surf Mobile",
    MCP_NAME,
    "Dynamic Shopper Segments",
    "PreisRe",
]


def update_projects(apps, schema_editor):
    FocusArea = apps.get_model("portfolio", "FocusArea")
    Project = apps.get_model("portfolio", "Project")
    removed = Project.objects.filter(name=REMOVED)
    if not removed.exists():
        return
    removed.delete()

    infrastructure, _ = FocusArea.objects.get_or_create(name="Research Software Infrastructure")
    research_software, _ = FocusArea.objects.get_or_create(name="Research Software")
    modeling, _ = FocusArea.objects.get_or_create(name="Modeling & Machine Learning")
    Project.objects.get_or_create(
        name=GESIS_SURF["name"], defaults={**GESIS_SURF, "tag": infrastructure}
    )
    Project.objects.get_or_create(name=SEGMENTS["name"], defaults={**SEGMENTS, "tag": modeling})
    Project.objects.filter(name=OLD_MOBILE_NAME).update(**MOBILE, tag=research_software)
    Project.objects.filter(name=MCP_NAME).update(**MCP)
    for order, name in enumerate(ORDER):
        Project.objects.filter(name=name).update(order=order)


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0004_replace_seed_timeline"),
    ]

    operations = [
        migrations.RunPython(update_projects, migrations.RunPython.noop),
    ]
