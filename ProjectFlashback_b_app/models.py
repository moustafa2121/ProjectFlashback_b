from abc import abstractclassmethod
from django.db import models

entryTypeChoices = [
    ("RE", "Reddit"),
    ("NW", "News"),
    ("ME", "Meme"),
    ("MV", "Movie"),
    ("TV", "TV Show"),
    ("SO", "Song"),
    ("GA", "Game"),
    ("AN", "Anime"),
]
  

#the dataset that BasicDataEntry belongs to.
class Dataset(models.Model):
    #this field must match the dataset numbering in the 'Kaggel datasets.xlsb'
    datasetID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

class BasicDataEntry(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.SET_NULL, 
                                null=True, default=None)
    #the exact date of the entry, the date the entry was created in the original source
    date = models.IntegerField(null=True, blank=True)
    #the year in which the entry will be displayed for (and the origin of the entry)
    #the year field might not always match the date field (i.e. memes from the 1990s are year 
    #1991 but the date is whenever were created on KYM such as 2008)
    year = models.IntegerField()
    #link to the entry
    url = models.URLField(primary_key=True)
    #todo: what if the string is longer?
    title = models.CharField(max_length=250)
    entryType = models.CharField(max_length=2, choices=entryTypeChoices)
    
    class Meta:
        abstract = True
        db_table = "BasicDataEntry"
        
    def __str__(self):
        return self.entryType + " " + self.title
        
    
class RedditDataEntry(BasicDataEntry):
    img = models.URLField()
    upvotes = models.IntegerField()
    comments = models.IntegerField()

    class Meta:
        db_table = "RedditDataEntry"

class KymDataEntry(BasicDataEntry):
    img = models.URLField()
    fav = models.IntegerField()
    views = models.IntegerField()

    class Meta:
        db_table = "KymDataEntry"
        
class TwitterDataEntry(BasicDataEntry):
    lang = models.CharField(max_length=2)
    retweetsCount = models.IntegerField()
    likesCount = models.IntegerField()
    source = models.CharField(max_length=3)
    
    class Meta:
        db_table = "TwitterDataEntry"
        

#identified by a cookie. its main purpose is to keep track what the user has been
#fetched so far to avoid duplicated
class CookieUser(models.Model):
    cookie = models.CharField(primary_key=True, max_length=200)
    entriesRead = models.ManyToManyField('UserEntryRead')

#this acts as a record to what entries have been read by a user
#note that we should be using ManyToMany relation with the BasicDataEntry but can't since it is abstract
class UserEntryRead(models.Model):
    entryUrl = models.URLField()
