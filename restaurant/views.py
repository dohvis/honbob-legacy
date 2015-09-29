from django.shortcuts import render
from django.http import HttpResponse
from restaurant.models import Restaurant
from json import dumps

def serializer(request):
    min_x = request.GET['min_x']
    min_y = request.GET['min_y']
    max_x = request.GET['max_x']
    max_y = request.GET['max_y']

    x = list(Restaurant.objects.filter(x__range=(min_x,max_x)))
    y = list(Restaurant.objects.filter(y__range=(min_y,max_y)))
    res = []
    for rest in list(set(x+y)):
        dic = {}
        dic['x'] = rest.x
        dic['y'] = rest.y
        dic['title'] = rest.title
        res.append(dic)
    return HttpResponse(dumps(res), content_type="application/json")


