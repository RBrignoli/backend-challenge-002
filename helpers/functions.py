"""
Model helper
"""
###
# Libraries
###

from django.utils.translation import ugettext as _

###
# Helpers
###


def choice_formatter(const):
    pretty_const = _(const.replace('_', ' ').title())
    return (const, pretty_const)
