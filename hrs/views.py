# Create your views here.
from django.http.response import JsonResponse
from django.shortcuts import render
from hrs.get_h import down

depts_list = [
    {'no': 10, 'name': '财务部', 'location': '北京'},
    {'no': 20, 'name': '研发部', 'location': '成都'},
    {'no': 30, 'name': '销售部', 'location': '上海'},
]


def index(request):
    return render(request, 'index.html', {'depts_list': depts_list})

def downing(request):
    """好评"""
    down()
    data = {'code': 200, 'hint': '操作成功'}
    return JsonResponse(data)

