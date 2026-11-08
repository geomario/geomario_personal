"""Context shared by every page: the profile for the footer and the profile links."""

from .models import Profile, ProfileLink


def site_context():
    return {
        "profile": Profile.objects.first(),
        "links": ProfileLink.objects.all(),
    }
