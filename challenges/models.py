"""
Challenges Models
"""
###
# Libraries
###
from django.db import models
from helpers.models import TimestampModel
from helpers.functions import choice_formatter

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
    score = models.IntegerField(
        choices = SCORE_CHOICE,
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