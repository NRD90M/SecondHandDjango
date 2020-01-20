from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('send_auth_code', views.send_auth_code, name='send_auth_code'),    # 往指定邮箱发送一个验证码
    path('register', views.register, name='register'),    # 注册账号
    path('login', views.login, name='login'),
    path('release_goods', views.release_goods, name='release_goods'),
    path('get_goods_info', views.get_goods_info, name='get_goods_info'),
    path('get_released_list', views.get_released_list, name='get_released_list'),
    path('upload_message', views.upload_message, name='upload_message'),
    path('get_message_list', views.get_message_list, name='get_message_list'),
]