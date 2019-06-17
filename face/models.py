from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.


class User(AbstractUser):
    image = models.TextField(verbose_name='图片字节流', blank=True)
    # picture = models.TextField(verbose_name='图片字节流', blank=True)
    # meta信息，即后台栏目名

    class Meta:
        verbose_name = "学生信息"
        verbose_name_plural = verbose_name

    # 重载__str__方法，打印实例会打印username，username为继承自AbstractUser
    def __str__(self):
        return self.username


class Note(models.Model):
    content = models.TextField(verbose_name='记事本内容')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='使用者')
    time = models.DateTimeField(default=datetime.now, verbose_name='记录时间')

