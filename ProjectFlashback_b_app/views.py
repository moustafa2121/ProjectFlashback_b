from rest_framework.decorators import api_view, permission_classes
import uuid, math, random
from django.utils import timezone
from .models import CookieUser, RedditDataEntry, KymDataEntry, TwitterDataEntry
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
    
    def sliceAndRandomize(self, size):
        return random.sample(list(self.serializer(self.storeData, many=True).data), size)
    
#handles the entries for each entry type
entriesWrapper = [EntryWrapper(RedditDataEntry, 2, RedditDataEntry_ser),
                  EntryWrapper(TwitterDataEntry, 2, TwitterDataEntry_ser),
                  EntryWrapper(KymDataEntry, 1, KymDataEntry_ser)]


testingMode = True
#@permission_classes([AllowAny])
@api_view(['GET'])
def testView(request, year):
    #todo: year limit

    #handle cookies/user
    setCookie = False
    currentUser = None
    if testingMode:
        currentUser = CookieUser.objects.get(cookie="e3d3abf1-a05a-4a97-a17e-a9c36e5a0265")
    elif request.COOKIES.get('user_id'):#if the front has a cookie, get the user
        try:
            currentUser = CookieUser.objects.get(cookie=request.COOKIES.get('user_id'))
        except:
            pass
    else:#if it doesn't get a cookie and create a user
        currentUser = CookieUser.objects.create(cookie=str(uuid.uuid4()))
        setCookie = True
    
    print("current user: ", currentUser)

    #get the entries, tailored to the user
    returnValue = sauce(currentUser, year)
    response = Response(returnValue)

    #set cookie if there is a need
    if setCookie:
        response.set_cookie('user_id', currentUser.cookie, 
                        expires=timezone.now() + timezone.timedelta(days=5),
                        secure=True, httponly=True)
        
    return response



#handles retrieving the correct feed for the user
def sauce(cookieUser, year, entriesWrapper=entriesWrapper, feedCount=20):
    #1- get the exclusion list of the user
    #excludeList = testExcludeList
    excludedList = list(map(lambda x: x[0], cookieUser.entriesRead.values_list('entryId').all()))
    print("excludedList: ", excludedList)
    
    #2- for each wrapper
    #2a- exclude list, filter by year, order_by scoreValue, slice[:feedCount]
    #2b- valid entries are those with sufficient data entries
    validEntries = [currentEntry for currentEntry in entriesWrapper if currentEntry.getData(excludedList, year, feedCount)]

    #3- get random values, each entry count in proportion to feebackCount
    sumOfPortions = sum([i.portion for i in validEntries])
    portions = [math.ceil((i/sumOfPortions)*feedCount) for i in [entry.portion for entry in validEntries]]
    returnEntries = []
    for validEntry, portion in zip(validEntries, portions):
        returnEntries+=validEntry.sliceAndRandomize(portion)
    random.shuffle(returnEntries)
    returnEntries = returnEntries[:feedCount]
  
    #4- associate the values with the user
    

    return returnEntries