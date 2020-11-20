"""
Accounts admin
"""
###
# Libraries
###
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . import models
from collections import defaultdict

from django.utils.timezone import timedelta
from django.contrib import admin
from django.utils.translation import ugettext as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from challenges.models import CorporationChallenge, ChallengeTemplate
from . import models


###
# Inline Admin Models
###

class UserProfileAdmin(admin.StackedInline):
    model = models.UserProfile
    fk_name = "user"

###
# Main Admin Models
###


@admin.register(models.ChangeEmailRequest)
class ChangeEmailRequestAdmin(admin.ModelAdmin):
    list_display = ('email',)
    readonly_fields = ('uuid',)


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'corporate',)
    inlines = (UserProfileAdmin,)
    fieldsets = (
        (_('Authentication'), {'fields': ('email', 'password', 'corporate',)}),
        (_('Personal Information'), {'fields': ('name', 'has_generated_report',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )



@admin.register(models.Corporation)
class CorporationAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'has_started_program', 'created_at')
    list_filter = ('has_started_program',)
    actions = ['start_program', 'generate_report']

    def start_program(self, request, queryset):
        success_count = 0
        fails_messages = defaultdict(list)
        for corporation in queryset:
            # If the corporation doesn't have a start date yet
            if not corporation.start_date:
                fails_messages["don't have a start date yet."].append(corporation.name)
                continue

            # If the program was already started
            elif corporation.has_started_program:
                fails_messages["have already started the program."].append(corporation.name)
                continue

            else:
                corporation_challenges = []
                for template in ChallengeTemplate.objects.all():
                    obj = CorporationChallenge(
                        category=template.category,
                        title=template.title,
                        text=template.text,
                        score=template.score,
                        URLName=template.URLName,
                        is_super=template.is_super,
                        corporation=corporation,
                        parent_template=template,

                    )
                    if not template.is_super:
                        delta = timedelta(days=(template.relative_day - 1) + 7 * (template.relative_week - 1))
                        obj.date = corporation.start_date + delta

                    corporation_challenges.append(obj)
                CorporationChallenge.objects.bulk_create(corporation_challenges)
                corporation.has_started_program = True
                corporation.save(update_fields=['has_started_program'])
                success_count += 1

        # Error handling

        final_error_message = '. '.join([f'{", ".join(value)} {key}' for key, value in fails_messages.items()])

        # Deliver message to user
        message = f'{success_count} program(s) started. ' + final_error_message
        self.message_user(request, message)

    start_program.short_description = 'Start program on corporation'



