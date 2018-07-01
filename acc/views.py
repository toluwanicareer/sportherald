from django.shortcuts import render
from django.views import View
from django.conf import settings
import requests
from .models import Profile
from django.contrib.auth.models import User
import json
from django.contrib.auth import login, logout
import pdb
from django.http import HttpResponseRedirect, Http404


# Create your views here.


class handleCode(View):

    def get(self,request, *args, **kwargs):
        access_token=request.GET.get('access_token')
        url='https://steemconnect.com/api/oauth2/token'
        me_url='https://steemconnect.com/api/me'
        #data={'code':code, 'client_secret':settings.CLIENT_SECRET}
        #response=requests.post(url, data=data)
        #response=response.json()
        #username=response.get('username')
        #refresh_token=response.get('refresh_token')
        #access_token=response.get('access_token')
        headers={'Authorization': access_token}
        me_response=requests.get(me_url,headers=headers)
        me_response=me_response.json()
        #pdb.set_trace()
        username=me_response.get('account').get('name')
        posting_key=me_response.get('account').get('posting').get('key_auths')[0][0]
        active_key=me_response.get('account').get('active').get('key_auths')[0][0]
        memo_key=me_response.get('account').get('memo_key')

        try:
            user=User.objects.get(username=username)
            profile=Profile.objects.get(user=user)
            #profile.refresh_token=refresh_token
            profile.access_token=access_token
            profile.save()
        except User.DoesNotExist:
            user=User.objects.create_user(username=username)
            profile=Profile.objects.create(posting_key=posting_key, active_key=active_key,
                                           memo_key=memo_key, user=user, access_token=access_token)
        user=login(request, user)
        request.session['access_token'] = access_token
        return HttpResponseRedirect('/')


        #request.session['access_token']=response.get('access_token')
        #pdb.set_trace()

        #sportherald.pythonanywhere.com


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return Http404('Invalid url')

