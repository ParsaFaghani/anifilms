from django.shortcuts import render
from anim.models import anim
from rest_framework import generics, permissions
from .serializers import animeSerializer
from django.db.models import Count,Avg,Q

class AnimeListView(generics.ListAPIView):
    queryset = anim.objects.annotate(average_ratings=Avg('ratings__average')).filter(accepted=True)
    serializer_class = animeSerializer
    http_method_names = ['get']

