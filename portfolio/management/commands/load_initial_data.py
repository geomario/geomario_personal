from django.core.management.base import BaseCommand
from django.db import transaction

from portfolio import data
from portfolio.models import FocusArea, Post, Project, TimelineEntry


class Command(BaseCommand):
    help = (
        "Load initial content from portfolio.data into the database. "
        "Only runs when the database is empty so it is safe to repeat."
    )

    @transaction.atomic
    def handle(self, *args, **options):
        # Any content at all counts as "already loaded", so deleting one kind of
        # content in the admin doesn't make the next start re-add everything.
        if any(m.objects.exists() for m in (FocusArea, TimelineEntry, Project, Post)):
            self.stdout.write("Data already present — skipping load_initial_data.")
            return

        focus_map = {
            name: FocusArea.objects.create(name=name)
            for name in data.FOCUS_AREAS
        }

        for i, row in enumerate(data.TIMELINE):
            TimelineEntry.objects.create(
                when=row["when"],
                title=row["title"],
                org=row["org"],
                body=row["body"],
                order=i,
            )

        for i, p in enumerate(data.PROJECTS):
            Project.objects.create(
                name=p["name"],
                tag=focus_map.get(p["tag"]),
                desc=p["desc"],
                stack=p["stack"],
                order=i,
            )

        for i, post in enumerate(data.WRITING):
            Post.objects.create(
                title=post["title"],
                date=post["date"],
                source=post["source"],
                url=post["url"],
                excerpt=post["excerpt"],
                span=post.get("span", ""),
                order=i,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Loaded initial data: {len(focus_map)} focus areas, "
                f"{len(data.TIMELINE)} timeline entries, "
                f"{len(data.PROJECTS)} projects, {len(data.WRITING)} posts."
            )
        )
