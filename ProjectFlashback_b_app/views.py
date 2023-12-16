from doctest import testmod
from rest_framework.decorators import api_view, permission_classes
import uuid, math, random
from django.utils import timezone
from .models import CookieUser, RedditDataEntry, KymDataEntry, TwitterDataEntry, UserEntryRead
from .serializer import RedditDataEntry_ser, TwitterDataEntry_ser, KymDataEntry_ser
from rest_framework.response import Response

class EntryWrapper:
    def __init__(self, entryType, portion, serializer):
        self.entryType = entryType
        self.portion = portion
        self.serializer = serializer
        
    def getData(self, excludedList, year, feedCount):
        self.storeData = self.entryType.objects.exclude(entryId__in=excludedList).filter(year=year).order_by('-scoreValue')[:feedCount]
        return len(self.storeData) == feedCount
    
    def sliceAndRandomize(self, size, randomize=True):
        if not randomize:
            return list(self.serializer(self.storeData, many=True).data)[:size]
        else:
            return random.sample(list(self.serializer(self.storeData, many=True).data), size)
    
#handles the entries for each entry type
entriesWrapper = [EntryWrapper(RedditDataEntry, 2, RedditDataEntry_ser),
                  EntryWrapper(TwitterDataEntry, 2, TwitterDataEntry_ser),
                  EntryWrapper(KymDataEntry, 1, KymDataEntry_ser)]


#@permission_classes([AllowAny])
@api_view(['GET'])
def testView(request, year, batch):
    #testing switches
    testingMode = False#ignores the cookies sent from the frontend
    randomize = False#sample random entries form each type
    shuffle = False#shuffle entry types
    ignoreHistory = True#ignoring history means user will get the same posts each time they refresh
    
    #todo: year limit
    #todo: year, region, and ignoreHistory input

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
    returnValue = sauce(currentUser, year, int(batch), feedCount=10, randomize=randomize,
                        shuffle=shuffle, ignoreHistory=ignoreHistory)
    response = Response(returnValue)

    #set cookie if there is a need
    if setCookie:
        response.set_cookie('user_id', currentUser.cookie, 
                        expires=timezone.now() + timezone.timedelta(days=5),
                        secure=True, httponly=True)
        
    return response


#handles retrieving the correct feed for the user
def sauce(cookieUser, year, batch, entriesWrapper=entriesWrapper,feedCount=20, 
          randomize=True, shuffle=True, ignoreHistory=False):
    #1- get the exclusion list of the user
    if ignoreHistory and batch == 1:#delete history
        cookieUser.entriesRead.through.objects.all().delete()
    excludedList = list(map(lambda x: x[0], cookieUser.entriesRead.values_list('entryId').all()))
    
    #2- for each wrapper
    #2a- exclude list, filter by year, order_by scoreValue, slice[:feedCount]
    #2b- valid entries are those with sufficient data entries
    validEntries = [currentEntry for currentEntry in entriesWrapper if currentEntry.getData(excludedList, year, feedCount)]

    #3- get random values, each entry count in proportion to feebackCount
    sumOfPortions = sum([i.portion for i in validEntries])
    portions = [math.ceil((i/sumOfPortions)*feedCount) for i in [entry.portion for entry in validEntries]]
    returnEntries = []
    for validEntry, portion in zip(validEntries, portions):
        returnEntries+=validEntry.sliceAndRandomize(portion, randomize=randomize)
    if shuffle:
        random.shuffle(returnEntries)
    returnEntries = returnEntries[:feedCount]
    
    #4- associate the values with the user
    [cookieUser.entriesRead.add(UserEntryRead.objects.get_or_create(entryId=entry['entryId'])[0]) for entry in returnEntries]
    
    return returnEntries    