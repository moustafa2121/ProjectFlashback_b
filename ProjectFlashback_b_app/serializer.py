from rest_framework import serializers
from .models import RedditDataEntry, KymDataEntry, TwitterDataEntry

        
class RedditDataEntry_ser(serializers.ModelSerializer):
    class Meta:
        model = RedditDataEntry
        exclude = ('year', 'scoreValue','dataset',)
        
class KymDataEntry_ser(serializers.ModelSerializer):
    class Meta:
        model = KymDataEntry
        exclude = ('year', 'scoreValue','dataset',)
        
class TwitterDataEntry_ser(serializers.ModelSerializer):
    class Meta:
        model = TwitterDataEntry
        exclude = ('year', 'scoreValue','dataset',)