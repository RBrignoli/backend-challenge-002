"""
API V1: Challenges Views
"""
from rest_framework import viewsets, permissions
from datetime import datetime
from math import ceil
from django.db.models import Sum, Q
from django.utils import timezone
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet


from challenges.api.v1.serializers import ChallengeSerializer
from challenges.models import CorporationChallenge

from challenges.models import Challenges
###
# Filters
###


###
# Viewsets
###

class CorporationChallengeViewSet(viewsets.ModelViewSet):
    queryset = CorporationChallenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def filter_queryset(self, queryset):
        queryset = queryset.filter(corporation=self.request.user.corporate)

        if self.action == 'list':
            str_date = self.request.query_params.get('date', None)
            try:
                date = datetime.strptime(str_date, '%Y-%m-%d').date()
                if date > timezone.now().date():
                    date = timezone.now().date()
            except (ValueError, TypeError):
                date = timezone.now().date()
            date_relative_week = int((date - self.request.user.corporate.start_date).days / 7) + 1
            queryset = queryset.filter(
                (Q(date=date) | Q(is_super=True)) & Q(parent_template__relative_week=date_relative_week))
        else:
            date = timezone.now().date()
            date_relative_week = int((date - self.request.user.corporate.start_date).days / 7) + 1

            queryset = queryset.filter(
                Q(date__lte=date) | Q(is_super=True) & Q(parent_template__relative_week__lte=date_relative_week))
        return queryset

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, ])
    def complete(self, request, **kwargs):
        challenge = self.get_object()
        if not challenge.is_super and challenge.date > timezone.now().date():
            return Response({'error': 'You cannot complete a challenge before it starts.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if request.user in challenge.completed_users.all():
            return Response({'error': 'You already completed this challenge.'}, status=status.HTTP_400_BAD_REQUEST)

        challenge.completed_users.add(request.user)
        if challenge.skipped_users.filter(id=request.user.id).exists():
            challenge.skipped_users.remove(request.user)

        return Response(self.get_serializer(challenge).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, ])
    def skip(self, request, **kwargs):
        challenge = self.get_object()
        if not challenge.is_super and challenge.date > timezone.now().date():
            return Response({'error': 'You cannot skip a challenge before it starts.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if request.user in challenge.skipped_users.all():
            return Response({'error': 'You already skipped this challenge.'}, status=status.HTTP_400_BAD_REQUEST)

        challenge.skipped_users.add(request.user)
        if challenge.completed_users.filter(id=request.user.id).exists():
            challenge.completed_users.remove(request.user)

        return Response(self.get_serializer(challenge).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, ])
    def uncomplete(self, request, **kwargs):
        challenge = self.get_object()
        if not challenge.completed_users.filter(id=request.user.id).exists():
            return Response({'error': 'You cannot uncomplete a challenge you didn\'t complete.'},
                            status=status.HTTP_400_BAD_REQUEST)

        challenge.completed_users.remove(request.user)
        return Response(self.get_serializer(challenge).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, ])
    def unskip(self, request, **kwargs):
        challenge = self.get_object()
        if not challenge.skipped_users.filter(id=request.user.id).exists():
            return Response({'error': 'You cannot unskip a challenge you didn\'t complete.'},
                            status=status.HTTP_400_BAD_REQUEST)

        challenge.skipped_users.remove(request.user)
        return Response(self.get_serializer(challenge).data, status=status.HTTP_200_OK)


class CorporationLeaderboardViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        corporation = request.user.corporate

        # Handle user stats
        user_completed_challenges = request.user.completed_challenges
        total_score = user_completed_challenges.aggregate(Sum('score')).get('score__sum') or 0
        today_score = user_completed_challenges.filter(date=timezone.now().today()).aggregate(Sum('score')).get(
            'score__sum') or 0
        relative_week = ceil(((timezone.now().today().date() - corporation.start_date).days + 1) / 7)
        week_score = user_completed_challenges.filter(parent_template__relative_week=relative_week).aggregate(
            Sum('score')).get('score__sum') or 0
        user_score = {
            'total': total_score,
            'today': today_score,
            'week': week_score,
        }

        # Handle leaderboard
        leaderboard = []
        for user in corporation.users.all():
            leaderboard.append({
                "name": user.name,
                "score": user.completed_challenges.aggregate(Sum('score')).get('score__sum') or 0
            })

        payload = {
            'user_score': user_score,
            'leaderboard': leaderboard,
        }

        return Response(payload, status=status.HTTP_200_OK)

