"""Serves the images stored next to each article's Markdown as static files.

articles/content/<slug>/images/x.png becomes the static file articles/<slug>/images/x.png,
so collectstatic copies it into the image and whitenoise serves it like any other static
file. Only image files are exposed: the Markdown itself (including drafts) is not.
"""

from pathlib import Path, PurePosixPath

from django.conf import settings
from django.contrib.staticfiles.finders import BaseFinder
from django.contrib.staticfiles.utils import get_files
from django.core.exceptions import SuspiciousFileOperation
from django.core.files.storage import FileSystemStorage
from django.utils._os import safe_join

PREFIX = "articles"
ASSET_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".avif"}


def is_asset(path):
    return PurePosixPath(path).suffix.lower() in ASSET_SUFFIXES


class ArticleAssetsFinder(BaseFinder):
    def __init__(self, *args, **kwargs):
        self.location = Path(settings.ARTICLES_CONTENT_DIR)
        self.storage = FileSystemStorage(location=self.location)
        self.storage.prefix = PREFIX  # collectstatic puts the files under articles/

    def check(self, **kwargs):
        return []

    def find(self, path, find_all=False, **kwargs):
        find_all = find_all or kwargs.get("all", False)  # "all" before Django 5.2
        matches = []
        if path.startswith(PREFIX + "/") and is_asset(path):
            try:
                full = safe_join(self.location, path[len(PREFIX) + 1:])
            except SuspiciousFileOperation:  # outside the content folder
                full = None
            if full and Path(full).is_file():
                matches.append(full)
        if find_all:
            return matches
        return matches[0] if matches else []

    def list(self, ignore_patterns):
        if not self.location.is_dir():
            return
        for path in get_files(self.storage, ignore_patterns):
            if is_asset(path):
                yield path, self.storage
