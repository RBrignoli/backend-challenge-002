"""
Challenges Models
"""
###
# Libraries
###
from django.db import models
from helpers.models import TimestampModel
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
    EDUCATION
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
    EDUCATION
    ]

class Challenges(TimestampModel):
    category = models.CharField(
        choices=CHALLENGE_TYPE_CHOICES,
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
        verbose_name=_('is super'),
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

    def __str__(self):
        return self.title