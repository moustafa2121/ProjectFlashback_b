from rest_framework.decorators import api_view, permission_classes
import uuid, random
from django.utils import timezone
from rest_framework.exceptions import status
from .models import CookieUser, RedditDataEntry, KymDataEntry, TwitterDataEntry, UserEntryRead, ImbdbGameDataEntry, WikipediaDataEntry, ImbdbDataEntry, ImbdbShowDataEntry, ImbdbMovieDataEntry, SpotifyDataEntry
from .serializer import RedditDataEntry_ser, TwitterDataEntry_ser, KymDataEntry_ser, ImbdbGameDataEntry_ser, WikipediaDataEntry_ser, ImbdbShowDataEntry_ser, ImbdbMovieDataEntry_ser, SpotifyDataEntry_ser
from rest_framework.response import Response

class EntryWrapper:
    def __init__(self, entryType, sizePerBatch, serializer):
        self.entryType = entryType
        self.sizePerBatch = sizePerBatch
        self.serializer = serializer
        
    #fetch count is used to fetch extra data to randomize them the returned data instead of
    #just getting the top results each time
    def getData(self, excludedList, year, fetchCount=20):
        sortType = '-scoreValue'
        if self.entryType == WikipediaDataEntry or issubclass(self.entryType, ImbdbDataEntry):
            sortType = 'scoreValue'
        self.storeData = self.entryType.objects.exclude(entryId__in=excludedList).filter(year=year).order_by(sortType)[:fetchCount]
        return len(self.storeData) != 0
    
    def sliceAndRandomize(self, randomize=True):
        finalLst = list(self.serializer(self.storeData, many=True).data)
        if not randomize:
            return finalLst[:self.sizePerBatch]
        else: 
            return random.sample(finalLst, min(len(self.storeData), self.sizePerBatch))
    
#handles the entries for each entry type
entriesWrapper = [EntryWrapper(RedditDataEntry, 2, RedditDataEntry_ser),
                  EntryWrapper(TwitterDataEntry, 2, TwitterDataEntry_ser),
                  EntryWrapper(KymDataEntry, 1, KymDataEntry_ser),
                  EntryWrapper(WikipediaDataEntry, 2, WikipediaDataEntry_ser),
                  EntryWrapper(ImbdbGameDataEntry, 1, ImbdbGameDataEntry_ser),
                  EntryWrapper(ImbdbMovieDataEntry, 1, WikipediaDataEntry_ser),
                  EntryWrapper(ImbdbShowDataEntry, 1, ImbdbShowDataEntry_ser),
                  EntryWrapper(SpotifyDataEntry, 1, SpotifyDataEntry_ser),]

#@permission_classes([AllowAny])
@api_view(['GET'])
def phase1View(request, year, batch):
    year = int(year)
    if year > 2023 or year < 2000:
        return Response({"Failure": "Error"}, status=status.HTTP_400_BAD_REQUEST)
    
    #testing switches
    testingMode = False#ignores the cookies sent from the frontend
    randomize = True#sample random entries form each type
    shuffle = True#shuffle entry
    ignoreHistory = True#ignoring history means user will get the same posts each time they refresh

    #handle cookies/user
    setCookie = False
    currentUser = None
    if testingMode:
        currentUser = CookieUser.objects.get(cookie="e3d3abf1-a05a-4a97-a17e-a9c36e5a0265")
    elif request.COOKIES.get('user_id'):#if the front has a cookie, get the user or create it
        currentUser = CookieUser.objects.get_or_create(cookie=request.COOKIES.get('user_id'))[0]
    else:#if the front doesn't have a cookie, get a cookie and create a user
        currentUser = CookieUser.objects.create(cookie=str(uuid.uuid4()))
        setCookie = True
    
    #get the entries, tailored to the user
    returnValue = sauce(currentUser, int(year), int(batch), randomize=randomize,
                        shuffle=shuffle, ignoreHistory=ignoreHistory)
    response = Response(returnValue)

    #set cookie if there is a need
    if setCookie:
        response.set_cookie('user_id', currentUser.cookie, 
                        expires=timezone.now() + timezone.timedelta(days=5),
                        secure=True, httponly=True)
        
    return response


#handles retrieving the correct feed for the user
def sauce(cookieUser, year, batch, entriesWrapper=entriesWrapper, 
          randomize=True, shuffle=True, ignoreHistory=False):
    #1- get the exclusion list of the user
    if ignoreHistory and batch == 1:#delete history
        cookieUser.entriesRead.through.objects.all().delete()
    excludedList = list(map(lambda x: x[0], cookieUser.entriesRead.values_list('entryId').all()))
    
    #2- for each wrapper
    #2a- exclude list, filter by year, order_by scoreValue, slice[:feedCount]
    #2b- valid entries are those with sufficient data entries
    validEntries = [currentEntry for currentEntry in entriesWrapper if currentEntry.getData(excludedList, year)]

    #3- get random values, each entry count in proportion to feebackCount
    returnEntries = []
    for validEntry in validEntries:
        returnEntries += validEntry.sliceAndRandomize(randomize=randomize)
    if shuffle:
        random.shuffle(returnEntries)
    
    #4- associate the values with the user to avoid fetching the same data in the next batch
    [cookieUser.entriesRead.add(UserEntryRead.objects.get_or_create(entryId=entry['entryId'])[0]) for entry in returnEntries]
    
    return returnEntries