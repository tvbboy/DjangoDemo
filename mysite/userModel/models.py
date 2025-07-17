from django.db import models
# Create your models here.
class regUser(models.Model):
    logintimes = models.IntegerField(default=0,null=False)
    username = models.CharField(max_length=20)
    qq = models.CharField(max_length=20,null=True)
    email= models.EmailField()
    password = models.CharField(max_length=256)
    gender= models.CharField(max_length=10)
    birthdate= models.DateField()
    nativePlace= models.CharField(max_length=20)
    regdate= models.DateTimeField()
    is_Active = models.BooleanField(default=True,null=True)
    lastlogin= models.DateTimeField() #课程一开始没有这个字段，临时增加这个字段，一方面是有了新的需求，一方面让同学们锻炼django的Migrate
    @classmethod    # 伪代码注入技术
    #采用ORM的方式，根据用户输入username获取一行记录object,避免写SQL语句的低效和不安全
    def get_by_username(cls, username):
        try:
            return cls.objects.get(username=username)
        except cls.DoesNotExist:
            return None