from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from konfera.models.abstract import KonferaModel
from konfera.settings import TALK_LANGUAGE, TALK_LANGUAGE_DEFAULT, TALK_DURATION as TALK_DURATION_SETTING

from .track import Track


class Talk(KonferaModel):
    CFP = 'cfp'
    DRAFT = 'draft'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    WITHDRAWN = 'withdrawn'

    TALK_STATUS = (
        (CFP, _('Call For Proposals')),
        (DRAFT, _('Draft')),
        (APPROVED, _('Approved')),
        (REJECTED, _('Rejected')),
        (WITHDRAWN, _('Withdrawn')),
    )

    TALK = 'talk'
    WORKSHOP = 'workshop'
    BREAK = 'break'

    TALK_TYPE = (
        (TALK, _('Talk')),
        (WORKSHOP, _('Workshop')),
        (BREAK, _('Break')),
    )

    TALK_DURATION = TALK_DURATION_SETTING

    title = models.CharField(max_length=256)
    abstract = models.TextField(help_text=_('Abstract will be published in the schedule.'))
    type = models.CharField(choices=TALK_TYPE, max_length=32, default=TALK)
    status = models.CharField(choices=TALK_STATUS, max_length=32)
    language = models.CharField(choices=TALK_LANGUAGE, max_length=2, default=TALK_LANGUAGE_DEFAULT)
    duration = models.IntegerField(choices=TALK_DURATION, help_text=_('Talk duration in minutes.'), default=30)
    primary_speaker = models.ForeignKey(
        'Speaker',
        related_name='primary_speaker_talks',
        verbose_name=_('Primary speaker'),
    )
    secondary_speaker = models.ForeignKey(
        'Speaker',
        related_name='secondary_speaker_talks',
        verbose_name=_('Secondary speaker'),
        blank=True,
        null=True,
    )
    event = models.ForeignKey('Event')

    ordering = models.IntegerField('Ordering number', help_text=_('A number that helps to order talks (ASC).'))
    track = models.ForeignKey('Track')

    def __str__(self):
        return self.title

    def clean(self):
        if hasattr(self, 'primary_speaker') and hasattr(self, 'secondary_speaker') \
                and self.primary_speaker == self.secondary_speaker:
            msg = _('%(primary)s have to be different than %(secondary)s.') % {
                'primary': self._meta.get_field('primary_speaker').verbose_name,
                'secondary': self._meta.get_field('secondary_speaker').verbose_name
            }

            raise ValidationError({'primary_speaker': msg, 'secondary_speaker': msg})

        room = self.track.room
        for track in room.tracks:
            start = track.start
            if self.track.start < start and self.track.end + timedelta(minutes=self.duration) < start:
                raise ValidationError({'duration': _('Tracks in the room overlap.')})
