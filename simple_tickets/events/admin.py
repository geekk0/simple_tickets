from django.contrib import admin

from .models import Organizer, Event, EventImages

admin.site.register(Organizer)
admin.site.register(Event)
admin.site.register(EventImages)
