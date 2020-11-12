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
from helpers.models import TimestampModel
from helpers.functions import choice_formatter



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

TRUST_MORE_STRESS_LESS = 'trust_more_and_stress_less'
HAVE_REFRESHING_REST = 'have_refreshing_rest'
ENJOY_SUNLIGHT = 'enjoy_sunlight'
NUTRITION = 'nutrition'
EXERCISE = 'exercise'
WATER = 'water'
LIVE_TEMPERATELY = 'live_temperately'
INVEST_IN_OTHERS = 'invest_in_others'
FRESH_AIR = 'fresh_air'
EDUCATION = 'education'
SUPER_CHALLENGE = 'super_challenge'

CHALLENGE_TYPE_CHOICES = [
    TRUST_MORE_STRESS_LESS,
    HAVE_REFRESHING_REST,
    ENJOY_SUNLIGHT,
    NUTRITION,
    EXERCISE,
    WATER,
    LIVE_TEMPERATELY,
    INVEST_IN_OTHERS,
    FRESH_AIR,
    EDUCATION,
    ]
CHALLENGE_CATEGORY_CHOICES = [
    choice_formatter(TRUST_MORE_STRESS_LESS),
    choice_formatter(HAVE_REFRESHING_REST),
    choice_formatter(ENJOY_SUNLIGHT),
    choice_formatter(NUTRITION),
    choice_formatter(EXERCISE),
    choice_formatter(WATER),
    choice_formatter(LIVE_TEMPERATELY),
    choice_formatter(INVEST_IN_OTHERS),
    choice_formatter(FRESH_AIR),
    choice_formatter(EDUCATION),
    choice_formatter(SUPER_CHALLENGE),
]


###
# Querysets
###


###
# Models
###
class Corporation(TimestampModel):

    name = models.CharField(
        verbose_name=('name'),
        max_length=64,
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

class UserProfile(TimestampModel):

    height = models.CharField(
        max_length= 255,
        verbose_name=('height'),
        help_text=('in metres'),
        null=True,
    )
    weight = models.CharField(
        max_length = 255,
        verbose_name=('weight'),
        help_text=('in kgs'),
        null=True,
    )
    date_of_birth = models.DateField(
        verbose_name=('date of birth'),
        null=True,
    )
    gender = models.CharField(
        choices=GENDER_CHOICES,
        verbose_name=('gender'),
        max_length=8,
        default=OTHER
    )

    def __str___(self):
        return (self.title)

class User(AbstractUser):
    email = models.EmailField(
        verbose_name = ('email adress'),
        unique = True,
    )

    name = models.CharField(
        verbose_name= ('name'),
        max_length=64,
        null=True,
    )
    has_generated_report = models.BooleanField(
        verbose_name= ('has generated end of program report'),
        default=False,
    )

    topics = ArrayField(
        base_field=models.CharField(max_length=256, choices=CHALLENGE_CATEGORY_CHOICES, ),
        verbose_name=_('topics'),
        default=list,
        null=True,
        blank=True,
    )
    corporate = models.ForeignKey(
        Corporation,
        verbose_name = ('corporate'),
        related_name = ('users'),
        on_delete = models.CASCADE,
        null = True,
    )

    __initial_topics = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_topics = self.topics

    def save(self, **kwargs):
        super().save(**kwargs)

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


