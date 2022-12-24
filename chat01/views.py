import json

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from chat01.models import contactors

from chat01.models import *

User = get_user_model()


def index(request):
    data = {}

    # 登录状态
    if request.user.is_authenticated:
        # 获取当前用户名
        username = str(request.user)
        user_id = User.objects.get(username=username).id
        # 获取好友数据
        friend = contactors.objects.filter(user_id=user_id)
        # 获取群组数据
        groups = group.objects.filter(user_id=user_id)
        data["groups"] = []
        for item in groups:
            data["groups"].append([item.group_id_id, item.group_id.group_name])

        # 获取cookie
        cookies = request.COOKIES
        sessionid = cookies["sessionid"]

        #读取聊天记录
        historys = []
        historys.append(message.objects.filter(Q(talker_type=1) &(Q(user_id=user_id) | Q(talker_id_id=user_id))).order_by('create_time'))

        for i in data["groups"]:
            historys.append(message.objects.filter(Q(talker_type=2) & Q(talker_id=i[0])).order_by('create_time'))

        data["history"] = []
        for history in historys:
            for item in history:
                data["history"].append([item.user_id_id,item.user_id.username,item.talker_type,item.talker_id_id,item.talker_id.username,item.create_time,item.content])
                # print([item.user_id_id,item.user_id.username,item.talker_type,item.talker_id_id,item.talker_id.username,item.create_time,item.content])


        # 数据
        data["username"] = username
        data["user_id"] = user_id
        data["session"] = sessionid
        data["contactors"] = []
        for item in friend:
            data["contactors"].append([item.friend_id.id, item.friend_id.username])



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


def addTalker(request):
    if request.method == "POST":
        message = {}
        if request.POST.get("talker"):
            if request.POST.get("talker_type") == "1":

                user_id = request.POST.get("user_id")

                # 是否能找到该联系人
                try:
                    friend_id = User.objects.get(username=request.POST.get("talker")).id
                except:
                    message["success"] = "204"
                    return JsonResponse(message, json_dumps_params={'ensure_ascii': False})

                # 如果已经是好友了
                if contactors.objects.filter(user_id=user_id, friend_id=friend_id).count() > 0:
                    message["success"] = "203"
                else:
                    db_contactors = contactors(
                        user_id=user_id,
                        friend_id_id=friend_id,
                    )
                    db_contactors.save()
                    db_contactors = contactors(
                        user_id=friend_id,
                        friend_id_id=user_id,
                    )
                    db_contactors.save()
                    message["success"] = "200"

            elif request.POST.get("talker_type") == "2":
                user_id = request.POST.get("user_id")

                # 是否能找到该群组
                try:
                    group_id = group_list.objects.get(group_name=request.POST.get("talker")).group_id
                except:
                    message["success"] = "204"
                    return JsonResponse(message, json_dumps_params={'ensure_ascii': False})

                # 如果已经在群组里了
                if group.objects.filter(user_id=user_id, group_id_id=group_id).count() > 0:
                    message["success"] = "203"
                else:
                    db_group = group(
                        user_id=user_id,
                        group_id_id=group_id,
                    )
                    db_group.save()
                    message["success"] = "200"

        elif request.POST.get("talker") == "":
            message["success"] = "202"
        else:
            message["success"] = "201"
        return JsonResponse(message, json_dumps_params={'ensure_ascii': False})


def create_group(request):
    if request.method == "POST":
        message = {}

        message["success"] = "201"

        group_name = request.POST.get("group_name")

        if request.POST.get("group_name") == "":
            message["success"] = "202"
        elif group_list.objects.filter(group_name=group_name).count() > 0:
            message["success"] = "203"
        else:
            db_group = group_list(
                group_name=group_name,
            )
            db_group.save()
            message["success"] = "200"

        return JsonResponse(message, json_dumps_params={'ensure_ascii': False})
