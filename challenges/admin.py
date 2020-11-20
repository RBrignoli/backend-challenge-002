"""
Challenges admin
"""
###
# Libraries
###


###
# Inline Admin Models
###


###
# Main Admin Models
###
from django.contrib import admin

from challenges.models import ChallengeTemplate, CorporationChallenge


@admin.register(ChallengeTemplate)
class ChallengeTemplateAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'score', 'relative_week', 'relative_day']
    list_filter = ['category', 'is_super', 'relative_week',]


@admin.register(CorporationChallenge)
class CorporationChallengeAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'corporation', 'score', 'date']
    list_filter = ['category', 'corporation', 'date',]
    filter_horizontal = ['skipped_users', 'completed_users']


