"""
Challenges Models
"""
###
# Libraries
###
from django.db import models
from helpers.models import TimestampModel
from helpers.functions import choice_formatter
from django.core import validators

from accounts.models import Corporation, User

###
# Choices
###
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

DEFAULT_SCORE = 1,
SUPER_SCORE = 10,

SCORE_CHOICES = [
    DEFAULT_SCORE,
    SUPER_SCORE,
    ]



###
# Querysets
###


###
# Models
###


class Challenges(TimestampModel):
    category = models.CharField(
        choices=CHALLENGE_CATEGORY_CHOICES,
        verbose_name=('category'),
        max_length=32,
    )
    title = models.CharField(
        verbose_name=('title'),
        max_length=256,
        null=True,
        blank = True,
    )
    text = models.TextField(
        verbose_name=('text'),
        null = True,
        blank = True,
    )

    is_super = models.BooleanField(
        verbose_name= ('is super'),
        default= False,
        blank = True,
    )
    score = models.PositiveSmallIntegerField(
        verbose_name=('score'),
        default = DEFAULT_SCORE,
        blank = True,
    )
    URLName = models.SlugField(
        max_length=255,
        unique=True
    )

    def save(self, *args, **kwargs):
        if self.is_super:
            self.score = SUPER_SCORE
        super().save(*args, **kwargs)

    class Meta:
        abstract = True

class ChallengeTemplate(Challenges):
    relative_week = models.SmallIntegerField(
        verbose_name= ('week number'),
        validators=[validators.MaxValueValidator(10)]
    )
    relative_day = models.SmallIntegerField(
        verbose_name= ('day number'),
        validators=[validators.MaxValueValidator(7)],
        null=True,
        blank=True,
    )
    class Meta:
        constraints = [models.UniqueConstraint(fields=['category', 'relative_week', 'relative_day'],
                                               name='unique_challenge_template')]

    def __str__(self):
        if not self.is_super:
            return f'Template: {self.category.title().replace("_", " ")} - Week {self.relative_week} - Day {self.relative_day}'
        else:
            return f'Template: {self.category.title().replace("_", " ")} - Week {self.relative_week}'

class CorporationChallenge(Challenges):
    # Attributes
    date = models.DateField(
        verbose_name= ('date'),
        null=True,
        blank=True,
    )

    # Relationships
    corporation = models.ForeignKey(
        Corporation,
        verbose_name= ('corporation'),
        related_name='challenges',
        on_delete=models.CASCADE,
    )
    completed_users = models.ManyToManyField(
        User,
        verbose_name= ('completed users'),
        related_name='completed_challenges',
        blank=True,
    )
    skipped_users = models.ManyToManyField(
        User,
        related_name='skipped_challenges',
        verbose_name= ('skipped users'),
        blank=True,
    )
    parent_template = models.ForeignKey(
        ChallengeTemplate,
        verbose_name= ('parent template'),
        related_name='child_challenges',
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        if not self.is_super:
            return f'Challenge: {self.category.title().replace("_", " ")} - {self.corporation} - Date {self.date}'
        else:
            return f'Super Challenge: {self.category.title().replace("_", " ")} - {self.corporation} - Week {self.parent_template.relative_week}'
