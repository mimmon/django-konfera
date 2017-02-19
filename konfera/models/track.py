from datetime import timedelta

from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.utils.translation import ugettext_lazy as _

from konfera.models.abstract import KonferaModel
from konfera.models.room import Room


class Track(KonferaModel):
    room = models.ForeignKey('Room', related_name='tracks')
    title = models.CharField(max_length=128)
    start = models.DateTimeField()
    # event = models.ForeignKey('Event', related_name='schedules')
    # description = models.TextField(
    #     blank=True,
    #     help_text=_('Description will be displayed, only if there is no related talk, eg. coffee break, lunch etc...'))
    # talk = models.ForeignKey('Talk', blank=True, null=True, related_name='scheduled_talks')

    @property
    def end(self):
        minutes = sum(talk.duration for talk in self.talks.objects.all())
        return self.start + timedelta(minutes=minutes)

    def append_talk(self):
        pass

    def insert_talk(self):
        pass