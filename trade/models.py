from django.db import models

# Create your models here.


# 用户类
class User(models.Model):
    username = models.CharField(max_length=20, default='')    # 用户名
    profile = models.CharField(max_length=50, default='')     # 自我描述
    head_portrait = models.ImageField(verbose_name='头像', upload_to='portraits', null=True, blank=True)
    email = models.EmailField(verbose_name='电子邮件', primary_key=True)
    password = models.CharField(verbose_name='密码', max_length=20)

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(verbose_name='类别名称', max_length=10)

    def __str__(self):
        return self.name


# 发布的商品类别
class Goods(models.Model):
    belong_to_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='商品拥有者', related_name='所属用户')
    description = models.CharField(verbose_name='商品描述', max_length=100)
    display_image = models.ImageField(verbose_name='展示图片', upload_to='display_images')
    price = models.FloatField(verbose_name='价格')
    express_fee = models.FloatField(verbose_name='快递费')
    category = models.ForeignKey(Category, verbose_name='商品类别', on_delete=models.CASCADE, default=None, blank=True)

    def __str__(self):
        return 'pk:' + str(self.pk) + "-" + self.description + '-' + str(self.price)


# 注意这是消息，不是留言
class Message(models.Model):
    content = models.CharField(max_length=20, verbose_name='消息内容', default='')
    belong_to_goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='所属商品')
    belong_to_sender = models.ForeignKey(User, verbose_name='发送方', on_delete=models.CASCADE, related_name='sender')
    belong_to_receiver = models.ForeignKey(User, verbose_name='接收方', on_delete=models.CASCADE, related_name='receiver')
    create_time = models.DateTimeField(auto_now_add=True)    # 创建时间

    def __str__(self):
        return self.belong_to_sender.username + "对" + self.belong_to_receiver.username + "说:" + self.content


