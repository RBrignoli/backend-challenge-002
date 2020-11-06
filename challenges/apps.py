"""
Challenges Apps
"""
###
# Libraries
###
from django.apps import AppConfig


###
# Config
###
class ChallengesConfig(AppConfig):
    name = 'challenges'

    def ready(self):
        import challenges.signals
