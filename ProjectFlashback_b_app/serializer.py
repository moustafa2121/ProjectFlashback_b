from rest_framework import serializers
from .models import RedditDataEntry, KymDataEntry, TwitterDataEntry, ImdbGameDataEntry, WikipediaDataEntry, ImdbShowDataEntry, ImdbMovieDataEntry, SpotifyDataEntry

        
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
   
class WikipediaDataEntry_ser(serializers.ModelSerializer):
    class Meta:
        model = WikipediaDataEntry
        exclude = ('year', 'scoreValue','dataset',)
        
class ImbdbGameDataEntry_ser(serializers.ModelSerializer):
    class Meta:
        model = ImdbGameDataEntry
        exclude = ('year', 'scoreValue','dataset',)
class ImbdbShowDataEntry_ser(serializers.ModelSerializer):
    class Meta:
        model = ImdbShowDataEntry
        exclude = ('year', 'scoreValue','dataset',)
class ImbdbMovieDataEntry_ser(serializers.ModelSerializer):
    class Meta:
        model = ImdbMovieDataEntry
        exclude = ('year', 'scoreValue','dataset',)
class SpotifyDataEntry_ser(serializers.ModelSerializer):
    class Meta:
        model = SpotifyDataEntry
        exclude = ('year', 'scoreValue','dataset',)