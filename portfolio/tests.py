import os
from io import StringIO
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from portfolio import data
from portfolio.models import FocusArea, Post, Project, TimelineEntry


def run(command):
    call_command(command, stdout=StringIO())


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
