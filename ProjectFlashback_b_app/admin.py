from django.contrib import admin
from .models import Dataset, RedditDataEntry, KymDataEntry, TwitterDataEntry, UserEntryRead, CookieUser

# Register your models here.
admin.site.register(Dataset)
admin.site.register(RedditDataEntry)
admin.site.register(KymDataEntry)
admin.site.register(TwitterDataEntry)
admin.site.register(UserEntryRead)
admin.site.register(CookieUser)
