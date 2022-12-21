import json

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, HttpResponse, redirect


# @login_required
def index(request):
    data = {}
    # 获取群组id
    data["qq_group_num"] = request.GET.get('num')

    # 获取cookie
    # cookies = request.COOKIES
    # sessionid = cookies["sessionid"]
    try:
        data["username"] = request.session["username"]
        data["session"] = request.session.session_key
    except:
        pass

    return render(request, "index.html", data)


def register(request):
    if request.method == "GET":
        return render(request, "register.html")

    message = {}
    message["error"] = ""
    username = request.POST.get("username")
    password = request.POST.get("password")
    email = request.POST.get("email")

    user = None
    if User.objects.filter(username=username).count() > 0:
        message["success"] = "202"
        message["error"] = "用户名已存在"
    else:
        user = User.objects.create_user(username=username, password=password, email=email)

    if user is not None:
        if user:
            message["success"] = "200"
            message["error"] = "注册成功"
            auth.login(request, user)
        else:
            message["success"] = "201"
            message["error"] = "未正确输入信息"

    return JsonResponse(message, content_type="application/json;charset=utf-8")


def login(request):
    if request.method == "GET":
        return render(request, "login.html")

    message = {}
    message["success"] = ""
    message["error"] = ""
    username = request.POST.get("username")
    password = request.POST.get("password")
    # 将username存入session中
    request.session["username"] = username
    user = auth.authenticate(username=username, password=password)

    if user:
        auth.login(request, user)
        message["success"] = "200"
        # return HttpResponseRedirect("/index/")
    else:
        message["success"] = "201"
        message["error"] = "用户名或密码错误"
    return JsonResponse(message, json_dumps_params={'ensure_ascii': False})


def logout(request):
    if request.method == "POST":
        request.session.flush()
        request.session["username"] = None
        message = {}
        message["success"] = "200"
        return JsonResponse(message, json_dumps_params={'ensure_ascii': False})
