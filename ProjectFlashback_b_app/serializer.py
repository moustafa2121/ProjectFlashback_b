from rest_framework import serializers
from .models import RedditDataEntry, KymDataEntry, TwitterDataEntry

        
class RedditDataEntry_ser(serializers.ModelSerializer):
    class Meta:
        model = RedditDataEntry
        fields = '__all__'
        
class KymDataEntry_ser(serializers.ModelSerializer):
    class Meta:
        model = KymDataEntry
        fields = '__all__'
        
class TwitterDataEntry_ser(serializers.ModelSerializer):
    class Meta:
        model = TwitterDataEntry
        fields = '__all__'