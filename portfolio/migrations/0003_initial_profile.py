"""Creates the profile and profile links, so they exist on every database (including
production) without typing them into the admin. Runs once; edit them in /admin later."""

from django.db import migrations

PROFILE = {
    "name": "Mario Ramirez",
    "role": "Systems Architect & Senior Research Software Engineer",
    "intro": (
        "I build data platforms end to end (collection, pipelines, APIs, infrastructure) and turn "
        "the data into decisions and peer-reviewed findings. From geophysics to open finance, legal "
        "tech and market research; formerly Head of Software & Data Science, now at GESIS and a "
        "doctoral researcher at the University of Cologne."
    ),
    "availability": "Data platforms · Machine learning · Systems architecture",
    "location": "Aachen, Germany",
    "organisation": "GESIS – Leibniz Institute for the Social Sciences",
    "email": "marm1984@gmail.com",
}

LINKS = [
    ("github", "https://github.com/geomario"),
    ("linkedin", "https://www.linkedin.com/in/geomario/"),
    ("orcid", "https://orcid.org/0009-0005-0960-4745"),
    ("researchgate", "https://www.researchgate.net/profile/Mario-Ramirez-Munoz"),
    ("medium", "https://geomario1984.medium.com/"),
]


def create_profile(apps, schema_editor):
    Profile = apps.get_model("portfolio", "Profile")
    ProfileLink = apps.get_model("portfolio", "ProfileLink")
    if not Profile.objects.exists():
        Profile.objects.create(**PROFILE)
    for order, (kind, url) in enumerate(LINKS):
        ProfileLink.objects.get_or_create(kind=kind, defaults={"url": url, "order": order})


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0002_profile_links_project_url"),
    ]

    operations = [
        migrations.RunPython(create_profile, migrations.RunPython.noop),
    ]
