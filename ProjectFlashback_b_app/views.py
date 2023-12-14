from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
import uuid
from django.utils import timezone
from .models import CookieUser

#@permission_classes([AllowAny])
@api_view(['GET'])
def testView(request):
    setCookie = False
    #if the front has a cookie, get the user
    if request.COOKIES.get('user_id'):
        try:
            currentUser = CookieUser.objects.get(cookie=request.COOKIES.get('user_id'))
        except:
            pass
    else:#if it doesn't get a cookie and create a user
        currentUser = CookieUser.objects.create(cookie=str(uuid.uuid4()))
        setCookie = True    
    

    response = JsonResponse({"test":"test data"})
    
    
    
    if setCookie:
        response.set_cookie('user_id', currentUser.cookie, 
                        expires=timezone.now() + timezone.timedelta(days=5),
                        secure=True, httponly=True)
    return response