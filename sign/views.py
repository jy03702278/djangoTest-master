#-*- coding:utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from models import Event
from models import Guest
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

# Create your views here.
def index(request):
    # return HttpResponse("hello django!")
    return render(request,"index.html")

def login_action(request):
    if request.method == "POST":
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        if username =='admin' and password == 'admin123':
            response =  HttpResponseRedirect('/event_manage/')
            request.session['user'] = username  #将session记录到浏览器
            return response
        else:
            return render(request,'index.html',{'error':'username or password error !'})

#【发布会管理页】的处理
#限制某个视图函数，必须先登录以后，才能访问。在函数前加上@login_required修饰符
# @login_required
def event_manage(request):
    event_list = Event.objects.all()
    username = request.session.get('user','') #读取浏览器的session
    return render(request, 'event_manage.html',{'user':username,'events':event_list})

def search_name(request):
    username = request.session.get('user','')
    search_name = request.GET.get('name','')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request,'event_manage.html',{'user':username,'events':event_list})

#【嘉宾页】的处理
def guest_manage(request):
    guest_list = Guest.objects.all()
    username = request.session.get('user', '')  # 读取浏览器的session
    paginator = Paginator(guest_list,1)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        #如果page不是整数，取第一页数据
        contacts = paginator.page(1)
    except EmptyPage:
        #如果page不在范围，取最后一页
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'guest_manage.html', {'user': username, 'guests': contacts})

#签到页面
def sign_index(request,eid):
    event = get_object_or_404(Event,id=eid)
    return render(request,'sign_index.html',{'event':event})

#签到动作
def sign_index_action(request,eid):
    event = get_object_or_404(Event,id=eid)
    phone = request.POST.get('phone','')
    print phone
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'hint': 'phone error !'})
    result = Guest.objects.filter(phone=phone,event_id=eid)
    if not result:
        return render(request, 'sign_index.html', {'event':event,'hint': 'event id or phone error !'})
    result = Guest.objects.get(phone=phone,event_id=eid)
    if result.sign:
        return render(request, 'sign_index.html', {'event':event,'hint': 'user has sign in.'})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        print result
        return render(request, 'sign_index.html', {'event':event,'hint': 'sign in success .','guest':result})

def logout(request):
    auth.logout(request)
    print "8888888"
    return HttpResponseRedirect('/index/')
