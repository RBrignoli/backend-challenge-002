"""
API V1: Challenges Serializers
"""
###
# Libraries
###
from rest_framework import serializers, fields
from challenges.models import CorporationChallenge
from challenges.constants import COMPLETED, SKIPPED

###
# Serializers
###
class ChallengeSerializer(serializers.ModelSerializer):


    status = serializers.SerializerMethodField()
    corporation = serializers.CharField(source='corporation.name')

    def get_status(self, instance):
        request = self.context.get('request')
        if request.user in instance.completed_users.all():
            status = COMPLETED
        elif request.user in instance.skipped_users.all():
            status = SKIPPED
        else:
            status = None
        return status


    class Meta:
        model = CorporationChallenge
        fields = ('id','category', 'title', 'text', 'is_super', 'score', 'date', 'corporation', 'status',)