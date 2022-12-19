from django.shortcuts import render, HttpResponse, redirect


def index(request):
    qq_group_num = request.GET.get('num')
    return render(request,"index.html",{"qq_group_num":qq_group_num})

def user_list(request):
    return render(request,"user_list.html")

def user_add(request):
    return HttpResponse("user_add")

def login(request):
    message = {}
    message["msg"]=""
    if request.method == "GET":
        return render(request, "login.html")

    username = request.POST.get("user")
    password = request.POST.get("pwd")

    if username=="admin" and password=="admin":
        return redirect("https://baidu.com")
    else:
        message["msg"]="用户名或密码错误"
        return render(request, "login.html", message)

