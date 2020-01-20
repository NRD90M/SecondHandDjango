from django.contrib import admin

# Register your models here.
from .models import User, Goods, Category, Message

admin.site.register(User)
admin.site.register(Goods)
admin.site.register(Category)
admin.site.register(Message)