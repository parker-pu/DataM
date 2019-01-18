后台 REST API
===
#### 目录结构
- **custom** 本项目自定义的一些配置文件
- **db** 数据库配置
- **datam_server** 这个文件夹下存放的是 Django 的一些配置
- **manage** 存放的是管理模块
    - 用户 Token 的认证
- **static** 存放的是一些静态文件
- **templates** 一些模版文件
- **test** 测试脚本
- **utils** 一个工具包
- **task** 任务的配置

#### 配置任务

安装相应的包
```shell
pipenv install
```

同步数据库模型
```shell
python manage.py makemigrations

python manage.py migrate
```

Docker 安装 Redis
- 安装
```shell
docker pull redis:3.2
```

- 创建数据文件夹
```shell
mkdir -p ~/redis ~/redis/data
```

- 启动 Redis
```shell
docker run -p 6379:6379 -v $PWD/data:/data  -d redis:3.2 redis-server --appendonly yes
```

#### 启动项目
启动 **celery**
- 启动 celery worker
```shell
celery worker -A datam_server -l info
```
- 启动 celery beat
```shell
celery -A datam_server beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

启动 **Django**
```shell
python manage.py runserver 0.0.0.0:8000
```