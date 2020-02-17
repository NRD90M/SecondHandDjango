# SecondHandDjango
仿闲鱼的二手交易平台服务端，使用Django进行编写

## 运行环境
Python 3

## 注意事项
注册功能需要用到QQ邮箱,用于把验证码发给注册用户, 所以请先开通QQ邮箱的STMP功能, 然后将邮箱信息填写在[trade/utils.py](https://github.com/zstu-lly/SecondHandDjango/blob/6a69b92576dc3005e87ca6dc6d1513a3fd1c0897/trade/utils.py#L12)里面

## 第三方库
- django
- pillow

## 环境配置
``` 
依赖包安装
pip install django==3.0.2
pip install pillow==6.2.1

数据库迁移
python manage.py makemigrations trade
python manage.py migrate

创建超级用户
python manage.py createsuperuser

启动服务
python manage.py runserver
```





