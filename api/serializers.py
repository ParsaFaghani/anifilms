from rest_framework import serializers
from anim.models import anim

class animeSerializer(serializers.ModelSerializer):
    class Meta:
        model = anim
        fields = ('name_english', 'name_farsi','name_Japanese','name_Japanese','description','trailer','photo','added_by','status','seasion','max_episod','publication_year')

