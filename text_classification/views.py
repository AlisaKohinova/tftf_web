from django.shortcuts import render
from rest_framework import generics

from django.http import HttpResponse
from django.http import JsonResponse

def index(request):
    return JsonResponse({'tftf': 'bayreuth'})