from django import template

from simple_tickets.events.models import Organizer

register = template.Library()


@register.filter
def has_organizer_group(user):
    """
    Checks if the given user belongs to any group related to any organizer object.
    """
    return user.groups.filter(name__in=Organizer.objects.all().values_list('group__name', flat=True)).exists()
