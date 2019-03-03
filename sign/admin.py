#-*- coding:utf-8 -*-

from django.contrib import admin\

#发布会表和嘉宾表同样可以通过admin后台管理
from sign.models import Event,Guest

class EventAdmin(admin.ModelAdmin):
    list_display = ['id','name','status']

#admin后台，guest内容的界面展示，可以展示下面列表的字段信息。
class GuestAdmin(admin.ModelAdmin):
    list_display = ['realname','phone','email','sign']
    search_fields = ['realname'] #创建一个字段的搜索栏
    list_filter = ['phone']      #创建一个字段的过滤器
# Register your models here.
admin.site.register(Event)
admin.site.register(Guest,GuestAdmin)
