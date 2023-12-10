from django.contrib import admin
from .models import Dataset, RedditDataEntry, KymDataEntry, TwitterDataEntry

# Register your models here.
admin.site.register(Dataset)
admin.site.register(RedditDataEntry)
admin.site.register(KymDataEntry)
admin.site.register(TwitterDataEntry)
