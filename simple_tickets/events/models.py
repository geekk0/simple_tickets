from django.contrib.auth.models import User, Group
from django.db import models


class Organizer(models.Model):
    name = models.CharField(verbose_name="Organizer name", max_length=100)
    logo = models.ImageField(upload_to='Organizer_logo', null=True, blank=True)
    email = models.EmailField(verbose_name="Organizer email", null=True, blank=True)
    phone = models.CharField(verbose_name="Organizer phone", max_length=20, null=True, blank=True)
    info = models.CharField(verbose_name="Organizer info", max_length=300, null=True, blank=True)
    group = models.OneToOneField(Group, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Personnel")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Organizer'
        verbose_name_plural = 'Organizers'


class Event(models.Model):
    name = models.CharField(verbose_name="Event name", max_length=100)
    date = models.DateTimeField(verbose_name="Event date", null=True, blank=True)
    location = models.CharField(verbose_name="Event location", max_length=100, null=True, blank=True)
    description = models.TextField(verbose_name="Event description", null=True, blank=True)
    cover = models.ImageField(upload_to='event_images', null=True, blank=True, verbose_name="Cover image")
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE,
                                  null=True, blank=True, verbose_name="Organizer")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'


class EventImages(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_images', null=True, blank=True)
    image = models.ImageField(upload_to='event_images', null=True, blank=True)



