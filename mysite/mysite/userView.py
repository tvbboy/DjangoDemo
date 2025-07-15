from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection # 导入connection
from django.db.models import Q
from django.db.models import F
from userModel.models import regUser
from django.contrib.auth.hashers import make_password,check_password

# 正确的导入方式
from datetime import datetime
# 接收请求数据
def reg(request): 
    return render(request, "reg.html")
# 接收请求数据
def login(request): 
    return render(request, "login.html")
# 接收请求数据
def login_do(request):  
    request.encoding='utf-8'
    ctx ={}
    if request.POST:
        ctx['username'] = request.POST['username']
         # 使用make_password函数加密密码
        encrypted_password = make_password(request.POST['password'])
        ctx['password'] = encrypted_password
        findUser = regUser.objects.filter(Q(username=ctx['username'])\
                                          & Q(password=ctx['password']))
        if findUser:
            # 更新所有对象的某个字段，例如增加1
            regUser.objects.update(logintimes=F('logintimes') + 99)            
            return HttpResponse("<p>登录成功！</p>")
        else:
            return HttpResponse("<p>用户名或密码错误！</p>") 
        ##掌握续航的语法
        strSQL="select * from usermodel_reguser where username='%s' and password='%s'"%\
            (ctx['username'],ctx['password'])
     
                                       
    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    #listTest = Test.objects.all()
        
    # filter相当于SQL中的WHERE，可设置条件过滤结果
   
    

    # 获取单个对象
    #response3 = regUser.objects.get(id=1) 
    
    
   
def login_do1(request):
    request.encoding='utf-8'
    msg="<p>请<a href='/userModel/register'>注册</a></p>"+"<p><a href='/login'>返回登录</a></p>"
    ctx ={}  # 创建一个字典对象
    if request.POST:
        ctx['username'] = request.POST['username']
        encrypted_password = make_password(request.POST['password'])
        ctx['password'] = encrypted_password
        strSql=""
        # 1. 获取用户记录（使用参数化查询防止SQL注入）
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, password, is_active FROM userModel_Reguser WHERE username = %s",
                (ctx['username'])
            )
           # strSql="SELECT id, password, is_active FROM userModel_Reguser WHERE username = '"+ctx['username']+"'"
            row = cursor.fetchone()
        # 2. 用户不存在或未激活
        if not row or not row[2]:  # row[2] = is_active
          msg="<p>用户名不存在！</p>"+strSql+msg
        else:
            user_id, hashed_password, _ = row
            # 3. 安全验证密码（防止时序攻击）
            try:
                # 方法A：使用Django内置的check_password（推荐）
                if check_password(request.POST['password'], hashed_password):
                    # 登录成功后的处理（如设置session）
                    request.session['user_id'] = user_id
                    msg="<p>登录成功！</p>"
                   
                else:
                    msg="<p>密码错误！</p>"+strSql+msg
            except Exception as e:
                # 记录错误日志
                print(f"Password check failed: {e}")
                msg="<p>密码验证失败！</p>"+strSql+msg
    return HttpResponse(msg) 
 # 接收请求数据
def reg_do(request):  
    request.encoding='utf-8'
    ctx ={}
    if request.POST:
        ctx['username'] = request.POST['username']
        ctx['email'] = request.POST['email']
        encrypted_password = make_password(request.POST['password'])
        ctx['password'] = encrypted_password
        #ctx['password'] = request.POST['password']
        ctx['gender'] = request.POST['gender']
        ctx['birthdate'] = request.POST['birthdate']
        ctx['nativePlace'] = request.POST['nativePlace']
        ctx['regdate'] = datetime.now()
        regUser.objects.create(**ctx)
        return render(request, "login.html")
        #return HttpResponse("<p>用户注册成功！</p>")
        strSQL="insert into tblUser(username,email,password,gender,birthdate,nativePlace)values(\
        '%s','%s','%s','%s','%s','%s')"%(ctx['username'],ctx['email'],ctx['password'],\
                                         ctx['gender'],ctx['birthdate'],ctx['nativePlace']
        )   
        #return render(request, "login.html", ctx)
        #return HttpResponse(strSQL)
        
        # test1 = regUser(username=ctx['username'])
        # test1.save()
        
        
