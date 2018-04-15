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