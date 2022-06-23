from django.shortcuts import render
from rest_framework import generics

from django.http import HttpResponse
from django.http import JsonResponse

import requests

def weapon_type(word):
    obj = requests.get(f'http://api.conceptnet.io/c/en/{word}?rel=/r/UsedFor&limit=1000').json()
    for i in obj['edges']:
        if ('UsedFor' and 'shoot' in str(i)) or ('DerivedFrom' and 'bow' in str(i)):
            return 'range'
        elif ('UsedFor' and ('stabbing' or 'cutting' or 'fencing' or 'cut firewood')) in str(i) or ('IsA' and 'sword' in str(i)):
            return 'melee'
    return 'other'

def index(request, user_input=None):
    return JsonResponse(
        {"recognizedWord": user_input,
        "type": weapon_type(user_input)}
    )