# chatsite

结构：Django+websocket+AJAX



## 使用

### 目录结构

```
│  manage.py
│
├─chat01
│  │  admin.py
│  │  apps.py
│  │  consumers.py
│  │  models.py
│  │  tests.py
│  │  views.py
│  │  __init__.py
│  │
│  ├─migrations
│  │      0001_initial.py
│  │      __init__.py
│  │
│  ├─static
│  │  ├─css
│  │  │      animate.min.css
│  │  │      bootstrap.min.css
│  │  │      bootstrap.min.css.map
│  │  │      font-awesome.min.css
│  │  │      index.css
│  │  │      login_style.css
│  │  │      register_style.css
│  │  │      style.css
│  │  │
│  │  ├─fonts
│  │  │      fontawesome-webfont.eot
│  │  │      fontawesome-webfont.svg
│  │  │      fontawesome-webfont.ttf
│  │  │      fontawesome-webfont.woff
│  │  │      fontawesome-webfont.woff2
│  │  │      FontAwesome.otf
│  │  │
│  │  ├─img
│  │  │      logo.jpeg
│  │  │
│  │  ├─js
│  │  │      bootstrap.min.js
│  │  │      jquery.min-3.6.2.js
│  │  │
│  │  └─plugins
│  └─templates
│          index.html
│          login.html
│          register.html
│
└─chatsite
        asgi.py
        routings.py
        settings.py
        urls.py
        wsgi.py
        __init__.py
```



### 拷贝项目到本地

```
git clone https://github.com/pang-juzhong/chatsite.git
```

### 创建数据库

```
cd 你的项目位置

python manger.py makemigrations
python manager.py migrate
```

### 安装依赖

```
cd 你的项目位置

pip install -r requirements.txt
```

### 运行项目

```
cd 你的项目位置

#运行
python manage.py runserver 8000
```

