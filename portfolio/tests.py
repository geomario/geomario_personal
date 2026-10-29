import importlib
import os
from io import StringIO
from unittest import mock

from django.apps import apps as django_apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings

from portfolio import data
from portfolio.models import FocusArea, Post, ProfileLink, Project, TimelineEntry


def run(command):
    call_command(command, stdout=StringIO())


# Tests run with DEBUG off, where the manifest storage only knows the static files
# collected when the image was built; plain storage keeps new files from failing.
@override_settings(STORAGES={
    **settings.STORAGES,
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class IndexTests(TestCase):
    def test_renders_seeded_content(self):
        run("load_initial_data")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, data.PROJECTS[0]["name"])
        self.assertContains(response, data.WRITING[0]["title"])

    def test_cannot_be_framed(self):
        response = self.client.get("/")
        self.assertEqual(response["X-Frame-Options"], "DENY")

    def test_shows_profile_and_links_from_migration(self):
        response = self.client.get("/")
        self.assertContains(response, "<h1>Mario Ramirez</h1>", html=True)
        for link in ProfileLink.objects.all():
            self.assertContains(response, f'href="{link.url}"')
        self.assertContains(response, 'href="mailto:marm1984@gmail.com"')

    def test_hides_focus_areas_without_projects(self):
        FocusArea.objects.create(name="Empty area")
        used = FocusArea.objects.create(name="Used area")
        Project.objects.create(name="P", tag=used, desc="d")
        response = self.client.get("/")
        self.assertContains(response, 'data-filter="Used area"')
        self.assertNotContains(response, 'data-filter="Empty area"')

    def test_project_without_tag_or_url(self):
        Project.objects.create(name="Untagged", desc="d")
        response = self.client.get("/")
        self.assertContains(response, 'data-tag=""')
        self.assertNotContains(response, "None")

    def test_project_url_is_a_link(self):
        Project.objects.create(name="Linked", desc="d", url="https://example.com/repo")
        response = self.client.get("/")
        self.assertContains(response, 'href="https://example.com/repo"')


class LoadInitialDataTests(TestCase):
    def counts(self):
        return [m.objects.count() for m in (FocusArea, TimelineEntry, Project, Post)]

    def test_loads_everything_once(self):
        run("load_initial_data")
        expected = [len(data.FOCUS_AREAS), len(data.TIMELINE), len(data.PROJECTS), len(data.WRITING)]
        self.assertEqual(self.counts(), expected)
        run("load_initial_data")
        self.assertEqual(self.counts(), expected)

    def test_does_not_reseed_after_focus_areas_deleted(self):
        run("load_initial_data")
        FocusArea.objects.all().delete()
        run("load_initial_data")
        self.assertEqual(FocusArea.objects.count(), 0)
        self.assertEqual(Project.objects.count(), len(data.PROJECTS))


class ReplaceSeedTimelineTests(TestCase):
    migration = importlib.import_module("portfolio.migrations.0004_replace_seed_timeline")

    def test_replaces_placeholders_and_keeps_other_entries(self):
        for title in self.migration.PLACEHOLDER_TITLES:
            TimelineEntry.objects.create(when="x", title=title, org="o", body="b")
        TimelineEntry.objects.create(when="x", title="Added in the admin", org="o", body="b")
        self.migration.replace_placeholders(django_apps, None)
        titles = set(TimelineEntry.objects.values_list("title", flat=True))
        self.assertFalse(titles & set(self.migration.PLACEHOLDER_TITLES))
        self.assertIn("Added in the admin", titles)
        self.assertEqual(len(titles), len(self.migration.TIMELINE) + 1)

    def test_does_nothing_without_placeholders(self):
        self.migration.replace_placeholders(django_apps, None)
        self.assertFalse(TimelineEntry.objects.exists())


class UpdateProjectsTests(TestCase):
    migration = importlib.import_module("portfolio.migrations.0005_update_projects")

    def test_updates_the_original_starter_projects(self):
        behavioral = FocusArea.objects.create(name="Behavioral Data")
        research = FocusArea.objects.create(name="Research Software")
        data_infra = FocusArea.objects.create(name="Data Infrastructure")
        Project.objects.create(name="GESISSurfMobile", tag=behavioral, desc="d", order=0)
        Project.objects.create(name="mcp-server-gesis-surf", tag=research, desc="d", order=1)
        Project.objects.create(name="PreisRe", tag=data_infra, desc="d", order=2)
        Project.objects.create(name=self.migration.REMOVED, tag=research, desc="d", order=3)

        self.migration.update_projects(django_apps, None)

        projects = list(Project.objects.select_related("tag"))
        self.assertEqual([p.name for p in projects], self.migration.ORDER)
        self.assertEqual(projects[0].tag.name, "Research Software Infrastructure")
        self.assertEqual(projects[0].url, self.migration.GESIS_SURF["url"])
        self.assertEqual(projects[1].tag, research)
        self.assertIn("Accessibility API", projects[1].stack)

    def test_does_nothing_without_the_starter_projects(self):
        self.migration.update_projects(django_apps, None)
        self.assertFalse(Project.objects.exists())


class EnsureSuperuserTests(TestCase):
    env = {
        "DJANGO_SUPERUSER_USER": "admin",
        "DJANGO_SUPERUSER_EMAIL": "admin@example.com",
        # Quotes and shell characters broke the old shell-heredoc version.
        "DJANGO_SUPERUSER_PASSWORD": 'pa"ss\'$(echo x)\nword',
    }

    def test_skips_when_unset(self):
        with mock.patch.dict(os.environ, {"DJANGO_SUPERUSER_PASSWORD": ""}):
            run("ensure_superuser")
        self.assertFalse(get_user_model().objects.exists())

    def test_creates_once_with_any_password(self):
        with mock.patch.dict(os.environ, self.env):
            run("ensure_superuser")
            run("ensure_superuser")
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)
        self.assertTrue(users[0].is_superuser)
        self.assertTrue(users[0].check_password(self.env["DJANGO_SUPERUSER_PASSWORD"]))
