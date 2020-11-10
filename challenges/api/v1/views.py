"""
API V1: Challenges Views
"""
from rest_framework import viewsets, permissions


from challenges.api.v1.serializers import ChallengeSerializer

from challenges.models import Challenges
###
# Filters
###


###
# Viewsets
###

class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenges.objects.order_by('-created_at')
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated, ]
