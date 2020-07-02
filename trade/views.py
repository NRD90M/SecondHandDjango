# coding=utf-8
from django.http import HttpResponse
import json
from .utils import send_email
from .models import User, Goods, Category, Message
import uuid
import base64
import os
from django.conf import settings


# Create your views here.
def index(request):
    ret_result = {"code": 200, "msg": "请求成功", "result": []}
    goods_list = Goods.objects.all().filter(is_sold=False)

    for i, goods in enumerate(goods_list):
        obj_info = {}
        obj_info['price'] = goods.price
        obj_info['desc'] = goods.description
        obj_info['category'] = goods.category.name
        obj_info['image'] = goods.display_image.url
        obj_info['product_id'] = goods.pk    # 主键
        obj_info['user'] = goods.belong_to_user.email    # 把所属用户的邮箱
        ret_result["result"].append(obj_info)
    print(ret_result)
    return HttpResponse(json.dumps(ret_result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def send_auth_code(request):
    # 接收两个参数，一个邮箱账号，一个验证码
    print(request.body, request.POST)
    try:
        data = json.loads(request.body)
    except:
        data = request.POST

    print("请求参数:", data)
    email = data['email']
    code = data['code']
    print("接收到发送验证码的请求:", email, code)
    user = User.objects.filter(email=email).first()  # 先尝试获取这个用户
    if user:  # 如果这个用户已经注册了
        result = {"ret": 2, "desc": "用户已经注册过了,请直接登录"}
        print("用户已经注册过了")
    else:
        ret_code, ret_desc = send_email("验证码", code, email)
        if ret_code != 0:
            result = {"ret": ret_code, "desc": '邮件发送失败:'+ret_desc}
        else:
            result = {"ret": ret_code, "desc": "验证码已发送到您的邮箱,请及注意查收"}

    return HttpResponse(json.dumps(result), content_type="application/json")


def register(request):
    result = {"ret": 0, "desc": "success"}
    # 接收两个参数，一个邮箱账号，一个验证码
    if request.method == "POST":
        data = json.loads(request.body)
        print("请求参数:", data)
        email = data['email']
        password = data['password']
        print("接收到注册的请求:", email, password)
        user = User.objects.filter(email=email).first()   # 先尝试获取这个用户
        if user:    # 如果这个用户已经注册了
            result = {"ret": 1, "desc": "User is already registered"}
            print("用户已经注册过了")
        else:
            user = User.objects.create(username=email, profile="这个人很懒,没有简介", email=email, password=password)
            user.save()
            print("新用户注册成功")
            result = {"ret": 0, "desc": "Create new user successfully"}
    else:
        result['ret'] = 1
        result['desc'] = 'Only accept post requests'
        print("请求方式错误")

    return HttpResponse(json.dumps(result), content_type="application/json")


def login(request):
    data = json.loads(request.body)
    print("请求参数:", data)
    email = data['email']
    password = data['password']
    print("接收到发送验证码的请求:", email, password)
    user = User.objects.filter(email=email).first()  # 先尝试获取这个用户
    if not user:  # 如果这个用户已经注册了
        result = {"ret": 1, "desc": "这个邮箱没有注册过"}
        print("这个邮箱没有注册过")
    else:
        if password == user.password:
            result = {"ret": 0, "desc": "登录成功", "username": user.username, "head_portrait": 'https://cn.bing.com/images/search?q=%e5%8f%b2%e5%8a%aa%e6%af%94&id=24A7A8B8F4DB11EDE45E5B08DD820E41A0CF6F3A&FORM=IQFRBA'}# user.head_portrait.url}
            print("密码校验成功")
        else:
            result = {"ret": 1, "desc": "密码错误"}
            print("密码错误")

    return HttpResponse(json.dumps(result), content_type="application/json")


def release_goods(request):
    # print(request.body)
    if request.method == 'POST':
        ret_result = "成功接收到了图片"
        data = request.POST
        # 当data中有pk时，进行更新
        if data['image'] != '':
            user = User.objects.filter(email=data['user']).first()
            if not user:
                ret_result = "成功接收到了图片, 但是不存在这个用户"
            else:
                goods = Goods()
                # 先设置一个默认的类别
                category = Category.objects.all().first()     # 随便整一个类别
                if not category:
                    category = Category(name="拿外卖")
                    category.save()

                goods.description = data['desc']
                goods.price = float(data['price'])
                goods.belong_to_user = user
                goods.express_fee = data['express_fee']
                goods.category = category
                image_filename = uuid.uuid4().hex + '.jpg'
                root_dir = 'display_images/'
                abs_path = os.path.join(settings.MEDIA_ROOT, os.path.join(root_dir, image_filename))
                rel_path = os.path.join(root_dir, image_filename)
                print(abs_path, rel_path)

                # print(isinstance(data['image'], six.string_types))
                try:
                    decoded_file = base64.b64decode(data['image'])
                    with open(abs_path, 'wb') as f:
                        f.write(decoded_file)
                    goods.display_image = rel_path
                    goods.save()
                    ret_result = str(goods.pk)
                except Exception as e:
                    print(e)


        else:
            ret_result = "上传的图片为空"
    else:
        ret_result = "请使用post请求方式"
    print(ret_result)
    return HttpResponse(ret_result)


def get_goods_info(request):
    # 接收两个参数，一个邮箱账号，一个验证码
    if request.method == 'GET':
        pk = 1

    else:
        print(request.body, request.POST)
        try:
            data = json.loads(request.body)
        except:
            data = request.POST

        # print("请求参数:", data)
        pk = data['pk']

    print("请求商品的pk:", pk)
    goods = Goods.objects.filter(pk=pk).first()

    if goods:
        # 存在这个商品
        user = goods.belong_to_user    # 拿出来这个用户user.head_portrait.url
        result = {"ret_code": 0, "info": {"user_head_portrait": '/media/portraits/10060471_105425187390_2_J2ykXM6.jpg', "username": user.username,
                                          "email": user.email,     # 把邮箱传回去用于校验这个是不是自己发布的商品
                                          "location": "浙江杭州", "price": goods.price, "desc": goods.description,
                                          "display_image": goods.display_image.url}}
    else:
        result = {"ret_code": 1, "info": "不存在这个商品"}

    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def get_released_list(request):
    # 接收两个参数，一个邮箱账号，一个验证码
    if request.method == 'GET':
        email = "13777893886@163.com"

    else:
        print(request.body, request.POST)
        try:
            data = json.loads(request.body)
        except:
            data = request.POST

        # print("请求参数:", data)
        email = data['email']

    print("请求用户发布的商品列表:", email)
    user = User.objects.filter(email=email).filter().first()
    if user:
        result = {"ret_code": 0, "user_info": "用户存在", "info": []}
        goods_list = Goods.objects.filter(belong_to_user=user)    # 取出该用户发布的所有商品
        for goods in goods_list:
            goods_info = dict()
            goods_info['imageUrl'] = goods.display_image.url
            goods_info['desc'] = goods.description
            goods_info['price'] = goods.price
            goods_info['message_count'] = 0    # 留言数量
            goods_info['browse_count'] = 0     # 浏览数量
            goods_info['pk'] = goods.pk        # 主键
            result['info'].append(goods_info)
    else:
        result = {"ret_code": 1, "user_info": "该用户不存在"}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def get_served_list(request):
    # 接收两个参数，一个邮箱账号，一个验证码
    if request.method == 'GET':
        email = "13777893886@163.com"

    else:
        print(request.body, request.POST)
        try:
            data = json.loads(request.body)
        except:
            data = request.POST

        # print("请求参数:", data)
        email = data['email']

    print("请求用户发布的商品列表:", email)
    user = User.objects.filter(email=email).filter().first()
    if user:
        result = {"ret_code": 0, "user_info": "用户存在", "info": []}
        goods_list = Goods.objects.filter(labour=user)    # 取出该用户发布的所有商品
        for goods in goods_list:
            goods_info = dict()
            goods_info['imageUrl'] = goods.display_image.url
            goods_info['desc'] = goods.description
            goods_info['price'] = goods.price
            goods_info['message_count'] = 0    # 留言数量
            goods_info['browse_count'] = 0     # 浏览数量
            goods_info['pk'] = goods.pk        # 主键
            result['info'].append(goods_info)
    else:
        result = {"ret_code": 1, "user_info": "该用户不存在"}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")

# 接收聊天消息
def upload_message(request):
    try:
        data = json.loads(request.body)
    except:
        data = request.POST

    print(data)
    pk = data['pk']
    content = data['content']
    senderEmail = data['sender']
    receiverEmail = data['receiver']
    goods = Goods.objects.filter(pk=pk).first()
    sender = User.objects.filter(email=senderEmail).first()     # 发送者
    receiver = User.objects.filter(email=receiverEmail).first()

    message = Message()
    message.belong_to_sender = sender
    message.belong_to_receiver = receiver
    message.belong_to_goods = goods
    message.content = content
    message.save()
    result = {"info": "消息上传成功"}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def get_message_list(request):
    if request.method == 'GET':
        email = "13777893886@163.com"
    else:
        try:
            data = json.loads(request.body)
        except:
            data = request.POST

        email = data['email']

    user = User.objects.filter(email=email).first()
    message_list = Message.objects.filter(belong_to_sender=user)
    result = {"ret_code": 0, "info": [], "pks": []}
    for message in message_list:
        goods_pk = str(message.belong_to_goods.pk)
        if goods_pk not in result["pks"]:
            result["pks"].append(goods_pk)
            info_item = {}
            # 先把这个商品给找出来
            goods = Goods.objects.filter(pk=goods_pk).first()
            info_item["pk"] = goods_pk
            info_item["imageUrl"] = goods.display_image.url
            info_item["owner_username"] = goods.belong_to_user.username
            info_item["owner_head_portrait"] = goods.belong_to_user.head_portrait.url
            info_item["last_message"] = Message.objects.filter(belong_to_goods=goods).order_by('-create_time').first().content
            result["info"].append(info_item)

    print(result)
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def give_service(request):
    try:
        data = json.loads(request.body)
    except:
        data = request.POST

    # print("请求参数:", data)
    pk = data['pk']
    labour_id = data['labour']    # 办事的人的id
    print("请求商品的pk:", pk)
    goods = Goods.objects.filter(pk=pk).first()

    if goods:
        labour = User.objects.filter(username=labour_id).first()
        if labour:
            goods.labour = labour
            goods.is_sold = True
            goods.save()
            result = {"ret_code": 0, "info": "商品拍下成功"}
        else:
            result = {"ret_code": 1, "info": "商品服务者不存在"}
    else:
        result = {"ret_code": 1, "info": "不存在这个商品"}

    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
