## 在线教育Django实战 遇到的坑及解决方案

自学地址：[[Django+xadmin打造在线教育平台](http://www.cnblogs.com/derek1184405959/p/8590360.html)](http://www.cnblogs.com/derek1184405959/p/8590360.html)



开发环境：

　　　　python:  3.6.4

　　　　Django: 2.0.2

后台管理：xadmin



建立虚拟环境 使用virtualenv进行创建 并且在虚拟环境进行项目开发，这个好处不用我明说了，老司机都明白；不知道怎么使用虚拟环境的请自行百度吧！



使用source进行环境切换  关闭虚拟环境请使用deactivate

```python
benedeMacBook-Pro:Desktop bene$ source xadminDjangoEnv/bin/activate
```

> 顺便说一下，使用虚拟环境创建后会自动给你创建python安装包，所以这个虚拟环境创建成功就可以使用pip进行包安装了

推荐使用pycharm进行项目开发，可以指定开发环境和自己创建虚拟环境，在python开发中非常好用，推荐！！！



#### 问题1: 在进行指定数据库mysql进行项目开发的时候，遇到mysql报错`pymysql.err.InternalError: (1049, "Unknown database 'shengxianonline'")`

这个问题是因为我们指定了自己的数据库方式，必须要自己去对应的数据库（mysql，mongdb等待）创建数据库，所以这里我们执行一下命令，

```mysql
mysql> CREATE DATABASE `onlineEducation` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
Query OK, 1 row affected (0.00 sec)
```

成功了！然后继续下一步就OK了！ 这里必须说明的是我们在Django中对模型进行创建的时候使用了utf-8格式的字符编码，所以这里我在创建数据库的时候指定了库的编码格式。不然会引起编码错误！不信你可以试试！



#### 问题2	在对app模型创建完成后进行数据库迁移，执行`python manage.py makemigrations`命令后提示   city = models.ForeignKey(CityDict, verbose_name='所在城市', on_delete=models.CASCADE)  NameError: name 'CityDict' is not defined

在项目中完成后并没有任何提示错误的信息，结果迁移提示这个数据库模型并未定义，所以我猜测是位置没写对，在修改前的位置是

```python 
class CourseOrg(models.Model):
    name = models.CharField("机构名称",max_length=50)
    desc = models.TextField("机构描述")
    click_nums = models.IntegerField("点击数",default=0)
    fav_nums = models.IntegerField("收藏数",default=0)
    image = models.ImageField("封面图",upload_to="org/%Y%m",max_length=100)
    address = models.CharField("机构地址",max_length=150)
    city = models.ForeignKey(CityDict, verbose_name='所在城市', on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name



# 注意这个位置
class CityDict(models.Model):
    name = models.CharField('城市',max_length=20)
    desc = models.CharField('描述',max_length=200)
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '城市'
        verbose_name_plural= verbose_name
```

修改后的位置

```python
class CityDict(models.Model):
    name = models.CharField('城市',max_length=20)
    desc = models.CharField('描述',max_length=200)
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '城市'
        verbose_name_plural= verbose_name
        
        

class CourseOrg(models.Model):
    name = models.CharField("机构名称",max_length=50)
    desc = models.TextField("机构描述")
    click_nums = models.IntegerField("点击数",default=0)
    fav_nums = models.IntegerField("收藏数",default=0)
    image = models.ImageField("封面图",upload_to="org/%Y%m",max_length=100)
    address = models.CharField("机构地址",max_length=150)
    city = models.ForeignKey(CityDict, verbose_name='所在城市', on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name
```

再次运行命令

```python
(xadminDjangoEnv) benedeMacBook-Pro:onlineEducation bene$ python manage.py makemigrations
Migrations for 'course':
  course/migrations/0001_initial.py
    - Create model Course
    - Create model CourseResource
    - Create model Lesson
    - Create model Video
Migrations for 'operation':
  operation/migrations/0001_initial.py
    - Create model CourseComments
    - Create model UserAsk
    - Create model UserCourse
    - Create model UserFavorite
    - Create model UserMessage
Migrations for 'organization':
  organization/migrations/0001_initial.py
    - Create model CityDict
    - Create model CourseOrg
    - Create model Teacher
Migrations for 'users':
  users/migrations/0004_banner_emailverifyrecord.py
    - Create model Banner
    - Create model EmailVerifyRecord
(xadminDjangoEnv) benedeMacBook-Pro:onlineEducation bene$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, course, operation, organization, sessions, users
Running migrations:
  Applying course.0001_initial... OK
  Applying operation.0001_initial... OK
  Applying organization.0001_initial... OK
  Applying users.0004_banner_emailverifyrecord... OK
(xadminDjangoEnv) benedeMacBook-Pro:onlineEducation bene$ 
```

完美成功了！！！所以说有时候书写位置很重要，在上一个模型未创建的时候一定不要去引用它，以免引起不必要的错误！



在虚拟环境中使用 `requirements.txt`

```
pip freeze > requirements.txt
```

安装货升级包后，一定要更新这个文件！！！



在部署的时候使用这个可以一键安装包依赖

```
pip install -r requirements.txt
```



#### 问题3  安装xadmin过程中出现的问题

推荐查看[官方文档安装方法](https://xadmin.readthedocs.io/en/latest/quickstart.html)

[问题解决方法集锦](http://www.lybbn.cn/data/bbsdatas.php?lybbs=50) 基本上包含了所有遇到的安装问题 



#### 查找和替换技巧

使用command+f 进行字符串查找，如果需要把查找的字符串替换为另一个字符串，使用command+r  然后选择replace all 就OK了



#### 问题4 打开指定页面的时候提示`raise TemplateDoesNotExist(', '.join(template_name_list), chain=chain)django.template.exceptions.TemplateDoesNotExist: index.html`

这个原因是因为模版没有找到，意思就是没有一个正确的路径进行模版渲染，所以这里需要在setting.py中进行模版路径指定

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],# 添加这句话就OK了
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```



#### 问题5 在进行app申明时报错  

```python
  File "/Users/bene/Desktop/onlineEducation/onlineEducation/apps/operation/models.py", line 4, in <module>
    from users.models import UserProfile
  File "/Users/bene/Desktop/onlineEducation/onlineEducation/apps/users/models.py", line 8, in <module>
    class UserProfile(AbstractUser):
  File "/Users/bene/Desktop/xadminDjangoEnv/lib/python3.6/site-packages/django/db/models/base.py", line 108, in __new__
    "INSTALLED_APPS." % (module, name)
RuntimeError: Model class users.models.UserProfile doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS.
Performing system checks...

```

提示很明确，在使用`users.models import UserProfile`等这样的方法是 找不到users的申明，需要去INSTALLED_APPS处修改apps申明,因为我这里是把所有的app放在了一个apps的目录下，所以我这里的修改方案是

1. settings.py处申明

   ```python
    sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
       
       
    INSTALLED_APPS= ['apps.users',  # 用户
    'apps.course',  # 课程
    'apps.organization',  # 机构
    'apps.operation',  # 提问
    ]
   ```

2. apps.py修改名称

   ```python
   class UsersConfig(AppConfig):
       name = 'apps.users'
       verbose_name = "用户"
   ```

3. 在所有引用的地方这样去导入文件

   ```python
   from apps.users.models import UserProfile
   from apps.users.forms import LoginForm
   ```

   重新编译一下就好了！！



#### 问题6 在xadmin后台进行数据添加的时候报错

```python
IndexError at /xadmin/organization/courseorg/add/
list index out of range
Request Method:	GET
Request URL:	http://127.0.0.1:8000/xadmin/organization/courseorg/add/
Django Version:	2.0.2
Exception Type:	IndexError
Exception Value:	
list index out of range
Exception Location:	/Users/bene/Desktop/xadminDjangoEnv/lib/python3.6/site-packages/xadmin-2.0.1-py3.6.egg/xadmin/widgets.py in render, line 80
Python Executable:	/Users/bene/Desktop/xadminDjangoEnv/bin/python
Python Version:	3.6.3
Python Path:	
['/Users/bene/Desktop/onlineEducation/onlineEducation/apps',
 '/Users/bene/Desktop/onlineEducation/onlineEducation',
 '/Users/bene/Desktop/xadminDjangoEnv/lib/python36.zip',
 '/Users/bene/Desktop/xadminDjangoEnv/lib/python3.6',
 '/Users/bene/Desktop/xadminDjangoEnv/lib/python3.6/lib-dynload',
 '/Users/bene/anaconda3/lib/python3.6',
 '/Users/bene/Desktop/xadminDjangoEnv/lib/python3.6/site-packages',
 '/Users/bene/Desktop/xadminDjangoEnv/lib/python3.6/site-packages/XlsxWriter-1.0.4-py3.6.egg',
 '/Users/bene/Desktop/xadminDjangoEnv/lib/python3.6/site-packages/xadmin-2.0.1-py3.6.egg',
 '/Users/bene/Desktop/xadminDjangoEnv/lib/python3.6/site-packages',
 '/Users/bene/Desktop/xadminDjangoEnv/lib/python3.6/site-packages/odf',
 '/Users/bene/Desktop/xadminDjangoEnv/lib/python3.6/site-packages/odf',
 '/Users/bene/Desktop/xadminDjangoEnv/lib/python3.6/site-packages/odf',
 '/Users/bene/Desktop/xadminDjangoEnv/lib/python3.6/site-packages/odf',
 '/Users/bene/Desktop/xadminDjangoEnv/lib/python3.6/site-packages/odf',
 '/Users/bene/Desktop/xadminDjangoEnv/lib/python3.6/site-packages/odf',
 '/Users/bene/Desktop/xadminDjangoEnv/lib/python3.6/site-packages/odf']
Server time:	星期二, 24 四月 2018 23:56:09 +0800
```

可以看到问题已经定位到widgets.py 第80行代码处，第80行的源码为

```python
input_html = [ht for ht in super(AdminSplitDateTime, self).render(name, value, attrs).split('\n') if ht != '']
        # return input_html
        return mark_safe('<div class="datetime clearfix"><div class="input-group date bootstrap-datepicker"><span class="input-group-addon"><i class="fa fa-calendar"></i></span>%s'
                         '<span class="input-group-btn"><button class="btn btn-default" type="button">%s</button></span></div>'
                         '<div class="input-group time bootstrap-clockpicker"><span class="input-group-addon"><i class="fa fa-clock-o">'
                         '</i></span>%s<span class="input-group-btn"><button class=
```

对标签进行拆分的时候使用了`\n`，这个导致了`out of index range`，说明这种方式拆分是有问题的，在网上找了一下解决方法，把split那行代码修改为如下

```python
#修改前
input_html = [ht for ht in super(AdminSplitDateTime, self).render(name, value, attrs).split('\n') if ht != '']
#修改后
input_html = [ht for ht in super(AdminSplitDateTime, self).render(name, value, attrs).split('/><') if ht != '']
input_html[0] = input_html[0] + "/>"
input_html[1] = "<" + input_html[1]
```

再运行就可以了！！！