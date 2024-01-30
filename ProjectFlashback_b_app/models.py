from django.db import models

entryTypeChoices = [
    ("RE", "Reddit"),
    ("NW", "News"),
    ("ME", "Meme"),
    ("WK", "Wikipedia"),
    ("MV", "Movie"),
    ("TV", "TV Show"),
    ("SO", "Song"),
    ("GA", "Game"),
]

#the dataset that BasicDataEntry belongs to.
class Dataset(models.Model):
    #this field must match the dataset numbering in the 'Kaggel datasets.xlsb'
    datasetID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return str(self.datasetID) + " " + self.name

#A data entry is a single post/card-like entry
#example: a reddit post, a song, a movie
class BasicDataEntry(models.Model):
    entryId = models.AutoField(primary_key=True, editable=False)
    dataset = models.ForeignKey(Dataset, on_delete=models.SET_NULL, 
                                null=True, default=None)
    #the exact date of the entry, the date the entry was created in the original source
    date = models.IntegerField(null=True, blank=True)
    #the year in which the entry will be displayed for (and the origin of the entry)
    #the year field might not always match the date field (i.e. memes from the 1990s are year 
    #1991 but the date is whenever were created on KYM such as 2008)
    year = models.IntegerField()
    #link to the entry
    url = models.URLField(unique=False)
    #todo: what if the string is longer?
    title = models.CharField(max_length=250)
    entryType = models.CharField(max_length=2, choices=entryTypeChoices)
    scoreValue = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        abstract = True
        db_table = "BasicDataEntry"
        
    def __str__(self) -> str:
        return self.entryType + " " + self.title[:50]

#sub classes of BasicDataEntry
class RedditDataEntry(BasicDataEntry):
    img = models.URLField()
    class Meta:
        db_table = "RedditDataEntry"

class KymDataEntry(BasicDataEntry):
    img = models.URLField()
    class Meta:
        db_table = "KymDataEntry"
        
class TwitterDataEntry(BasicDataEntry):
    lang = models.CharField(max_length=2)
    source = models.CharField(max_length=3)
    class Meta:
        db_table = "TwitterDataEntry"
        
class WikipediaDataEntry(BasicDataEntry):
    summary = models.CharField(max_length=1000)
    img = models.URLField()
    class Meta:
        db_table = "WikipediaDataEntry"
#movies, shows, games have the same entry, however,
#we will use different models for each as it is easier when selecting for proprtions
class ImdbDataEntry(BasicDataEntry):
    summary = models.CharField(max_length=1000)
    img = models.URLField()
    class Meta:
        abstract = True
        db_table = "ImbdbDataEntry"
class ImdbGameDataEntry(ImdbDataEntry):
    class Meta:
        db_table = "ImbdbGameDataEntry"
class ImdbShowDataEntry(ImdbDataEntry):
    class Meta:
        db_table = "ImbdbShowDataEntry"
class ImdbMovieDataEntry(ImdbDataEntry):
    class Meta:
        db_table = "ImbdbMovieDataEntry"
class SpotifyDataEntry(BasicDataEntry):
    class Meta:
        db_table = "SpotifyDataEntry"
        
#identified by a cookie. its main purpose is to keep track what the user has been
#fetched so far to avoid duplicats
class CookieUser(models.Model):
    cookie = models.CharField(primary_key=True, max_length=200)
    entriesRead = models.ManyToManyField('UserEntryRead')

#this acts as a record to what entries have been read by a user
#note that we should be using ManyToMany relation with the BasicDataEntry but can't since it is abstract
class UserEntryRead(models.Model):
    entryId = models.IntegerField(primary_key=True)
    def __str__(self) -> str:
        return str(self.entryId)