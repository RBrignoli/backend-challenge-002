"""
API V1: Challenges Urls
"""
###
# Libraries
###
from django.conf.urls import url, include
from rest_framework_nested import routers


###
# Routers
###
from challenges.api.v1.views import CorporationChallengeViewSet, CorporationLeaderboardViewSet

""" Main router """
router = routers.SimpleRouter()
router.register(r'challenges', CorporationChallengeViewSet)
router.register(r'leaderboard', CorporationLeaderboardViewSet, basename='leaderboard')


###
# URLs
###
urlpatterns = [
    url(r'^', include(router.urls)),
]
