# SecondHandDjango
仿闲鱼的二手交易平台服务端，使用Django进行编写

## 运行环境
Python 3

## 注意事项
用于注册功能需要用到QQ邮箱, 请先开通QQ邮箱的STMP功能, 然后将邮箱信息填写在trade/utils.py里面

## 第三方库
- django
- pillow

## 环境配置
``` 
依赖包安装
pip install django
pip install pillow

数据库迁移
python manage.py migrate

创建超级用户
python manage.py createsuperuser

启动服务
python manage.py runserver
```





