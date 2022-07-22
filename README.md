# fblog
django中文网博客教程

# 部署

```shell
pip install -r requirements.txt
# 迁移数据库
python manage.py makemigrations
python manage.py migrate
# 创建管理用户
python manage.py createsuperuser
# 默认使用8000端口
python manage.py runserver
```
