"""
API V1: Challenges Serializers
"""
###
# Libraries
###
from rest_framework import serializers, fields
from .models import Challenges

###
# Serializers
###
class ChallengeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Challenges
        fields = ('category', 'title', 'text', 'is_super', 'score', 'URLName')