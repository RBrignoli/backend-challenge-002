"""
Accounts Models
"""
###
# Libraries
###
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.postgres.fields import ArrayField

from helpers.firebase import unsubscribe_from_topic, subscribe_to_topic


###
# Choices
###
MALE = 'male'
FEMALE = 'female'
OTHER = 'other'

GENDER_CHOICES = [
    (MALE, _(MALE)),
    (FEMALE, _(FEMALE)),
    (OTHER, _(OTHER)),
]


###
# Querysets
###


###
# Models
###
class UserProfile(AbstractUser):

    height = models.CharField(
        max_length= 255,
        verbose_name=_('height'),
        help_text=_('in metres'),
        null=True,
    )
    weight = models.CharField(
        max_length = 255,
        verbose_name=_('weight'),
        help_text=_('in kgs'),
        null=True,
    )
    date_of_birth = models.DateField(
        verbose_name=_('date of birth'),
        null=True,
    )
    gender = models.CharField(
        choices=GENDER_CHOICES,
        verbose_name=_('gender'),
        max_length=8,
        default=OTHER
    )

    def __str___(self):
        return (self.title)

class User(AbstractUser):
    email = models.EmailField(
        verbose_name =_('email adress'),
        unique = True,
    )

    name = models.CharField(
        verbose_name=_('name'),
        max_length=64,
        null=True,
    )
    corporate = models.ForeignKey(
        Corporation,
        verbose_name=_('corporate'),
        related_name='users',
        on_delete=models.CASCADE,
        null=True,
    )
    has_generated_report = models.BooleanField(
        verbose_name=_('has generated end of program report'),
        default=False,
    )

    # Firebase
    firebase_device_tokens = ArrayField(
        models.CharField(max_length=256),
        verbose_name=_('firebase device tokens'),
        default=list,
        null=True,
        blank=True,
    )

    topics = ArrayField(
        base_field=models.CharField(max_length=256, choices=CHALLENGE_CATEGORY_CHOICES, ),
        verbose_name=_('topics'),
        default=list,
        null=True,
        blank=True,
    )
    __initial_topics = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_topics = self.topics

    def save(self, **kwargs):
        super().save(**kwargs)

        if self.firebase_device_tokens:
            unsubscribe_from = set(self.__initial_topics) - set(self.topics)
            for topic in unsubscribe_from:
                unsubscribe_from_topic(self.firebase_device_tokens, topic)

            subscribe_to = set(self.topics) - set(self.__initial_topics)
            for topic in subscribe_to:
                subscribe_to_topic(self.firebase_device_tokens, topic)

    def __str__(self):
        return self.email

    class Meta:
        constraints = [models.UniqueConstraint(fields=['name', 'corporate'], name='unique_named_user')]



class ChangeEmailRequest(models.Model):
    # Helpers
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('uuid'),
    )

    # User model
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='change_email_request',
        verbose_name=_('user'),
    )

    # Email
    email = models.EmailField(verbose_name=_('email'))


class Corporate():

    name = models.CharField(
        verbose_name='name',
        max_lenght=30,
        unique=True,
    )
    start_date = models.DateField(
        verbose_name = ('start date'),
        null = True,
        blank = True,
    )

    has_started_program = models.BooleanField(
        verbose_name= ('has started program'),
        default= False,
        editable= False,
    )
    def __str__(self):
        return self.name