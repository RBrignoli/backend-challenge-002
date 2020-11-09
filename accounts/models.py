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


###
# Choices
###


###
# Querysets
###


###
# Models
###
class User(AbstractUser):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

    GENDER_CHOICES = [
        (MALE, _(MALE)),
        (FEMALE, _(FEMALE)),
        (OTHER, _(OTHER)),
    ]

    height = models.CharField(
        verbose_name=_('height'),
        help_text=_('in metres'),
        null=True,
    )
    weight = models.CharField(
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
