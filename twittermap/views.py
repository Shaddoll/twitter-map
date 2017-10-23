from django.shortcuts import render_to_response
from django.http import HttpResponse
from search import SearchEngine
import json

# Create your views here.

g_Se = SearchEngine()

def home(request):
    return render_to_response("index.html")

def search(request):
    keyword = request.GET.get('keyword', '')
    tweets = g_Se.search(keyword)
    return HttpResponse(json.dumps({"keyword": keyword, "tweets": tweets}))

def search_range(request):
    lat = request.GET.get('lat', '')
    lon = request.GET.get('lon', '')
    tweets = g_Se.search_range(lat, lon)
    return HttpResponse(json.dumps({"tweets": tweets}))
