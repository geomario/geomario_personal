"""Updates the starter projects: adds GESIS Surf, renames and redescribes the mobile app,
removes the cross-retailer clustering paper and puts the projects in a new order.

Only touches databases that still have the original starter projects (production): a
fresh database has no projects yet at this point and gets them from portfolio/data.py.
The values are copied here because migrations must not change when data.py does.
"""

from django.db import migrations

REMOVED = "Cross-Retailer Behavioural Clustering"
OLD_MOBILE_NAME = "GESISSurfMobile"

GESIS_SURF = {
    "name": "GESIS Surf",
    "desc": (
        "Open-source infrastructure for collecting web browsing behaviour in social science "
        "studies: a browser extension feeding a Django REST backend that records windows, "
        "tabs, domains, clicks, scrolls and page HTML, with Celery for async processing, "
        "Elasticsearch for search and an ELK stack for monitoring."
    ),
    "stack": ["Django REST", "PostgreSQL", "Celery", "Elasticsearch", "Browser extension"],
    "url": "https://github.com/gesiscss/gesis_surf_backend",
}
MOBILE = {
    "name": "GESIS Surf Mobile",
    "desc": (
        "Cross-platform React Native app for mobile studies, using VPN-based packet "
        "inspection on Android and iOS plus the Accessibility API."
    ),
    "stack": ["React Native", "TypeScript", "VPN packet inspection", "Accessibility API"],
}
ORDER = ["GESIS Surf", "GESIS Surf Mobile", "mcp-server-gesis-surf", "PreisRe"]


def update_projects(apps, schema_editor):
    FocusArea = apps.get_model("portfolio", "FocusArea")
    Project = apps.get_model("portfolio", "Project")
    removed = Project.objects.filter(name=REMOVED)
    if not removed.exists():
        return
    removed.delete()

    infrastructure, _ = FocusArea.objects.get_or_create(name="Research Software Infrastructure")
    research_software, _ = FocusArea.objects.get_or_create(name="Research Software")
    Project.objects.get_or_create(
        name=GESIS_SURF["name"], defaults={**GESIS_SURF, "tag": infrastructure}
    )
    Project.objects.filter(name=OLD_MOBILE_NAME).update(**MOBILE, tag=research_software)
    for order, name in enumerate(ORDER):
        Project.objects.filter(name=name).update(order=order)


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0004_replace_seed_timeline"),
    ]

    operations = [
        migrations.RunPython(update_projects, migrations.RunPython.noop),
    ]
