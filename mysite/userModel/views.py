from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection # 导入connection
from django.db.models import Q
from django.db.models import F
from userModel.models import regUser
from django.contrib.auth.hashers import make_password,check_password
# 正确的导入方式
from datetime import datetime
# Create your views here.
# 接收请求数据，以执行SQL地方式插入到数据库中
def reg_withSQL(request):  
    insert_sql,ctx=getInsertRegSQLAndDict(request)  #赋值的解压缩
    if(insert_sql=="" or ctx=={}):
        return HttpResponse("<p>用户注册失败！</p>")
    try:
        with connection.cursor() as cursor:
            # cursor.execute(sql, params)
            cursor.execute(insert_sql)
        print("注册成功！") #控制台打印输出
    except Exception as e:
        print(f"插入失败: {e}")
    return render(request, "login.html")  #web页面跳转
    #return HttpResponse("<p>用户注册成功！</p>")
    #用来教学演示POST提交，不会真实提交到数据库
# 接收请求数据，以ORM的方式提交到数据库
def reg_withORM(request): 
   insert_sql,ctx=getInsertRegSQLAndDict(request)
   print("do regwithORM.......")
   if(insert_sql=="" or ctx=={}):
       return HttpResponse("<p>用户注册失败！</p>")
   try:
       regUser.objects.create(**ctx)
       print("注册成功！") #控制台打印输出
   except Exception as e:
       print(f"插入失败: {e}")
   return render(request, "login.html")
   #return HttpResponse("<p>用户注册成功！</p>")
def reg_withoutdatabase(request):  
    insert_sql,ctx=getInsertRegSQLAndDict(request)
    return HttpResponse("<p>用户注册成功！"+insert_sql+"</p>")
# 根据用户请求生成SQL语句，并返回给用户
def getInsertRegSQLAndDict(request):
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
            ctx['regdate'] =datetime.now() 
            ctx['logintimes'] =0
            strSQL="insert into usermodel_reguser(username,email,password,gender,birthdate,nativePlace,regdate,logintimes)values('%s','%s','%s','%s','%s','%s','%s',%s)"%(
                ctx['username'],ctx['email'],ctx['password'],ctx['gender'],
                ctx['birthdate'],ctx['nativePlace'],ctx['regdate'] ,ctx['logintimes']
            )   
            print(strSQL) #控制台打印输出,这个不会在WEB页输出的！！！！！！！！
    else:
         strSQL=""
    return strSQL,ctx

# 接收请求数据
def reg(request): 
    return render(request, "reg.html")
def register(request): 
    return render(request, "register.html")
# 接收请求数据
def login(request): 
    return render(request, "login.html")
# 以SQL的方式验证用户登录
def login_withSQL(request):
    request.encoding='utf-8'
    msg="<p>请<a href='/userModel/register'>注册</a></p>"+"<p><a href='/login'>返回登录</a></p>"
    ctx ={}  # 创建一个字典对象
    if request.POST:
        ctx['username'] = request.POST['username']
        try:
            # 1. 获取用户记录（使用参数化查询防止SQL注入）
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, password, is_active FROM userModel_Reguser WHERE username = %s",
                    (ctx['username'])
                )
                print("SELECT id, password, is_active FROM userModel_Reguser WHERE username = '"+ctx['username']+"'")
                row = cursor.fetchone()  #注意此时的row是 tuple类型
                print("返回行：",row) #控制台打印日志防止有问题
                # 2. 用户不存在或未激活
                if not row :  # row[2] = is_active
                    msg="<p>用户名不存在！</p>"+msg
                else:
                    user_id, hashed_password, _ = row  #解压缩变量赋值
                    # 3. 安全验证密码（防止时序攻击）
                    # 方法A：使用Django内置的check_password（推荐）
                    if check_password(request.POST['password'], hashed_password):
                            # 登录成功后的处理（如设置session）
                        request.session['user_id'] = user_id
                        msg="<p>登录成功！</p>"                
                    else:
                        msg="<p>密码验证失败！</p>"+msg
        except Exception as e:
                    # 记录错误日志
                    print(f"异常: {e}")                   
    return HttpResponse(msg) 
def login_withORM(request):  
   request.encoding='utf-8'
   ctx ={}
   if request.POST:
      ctx['username'] = request.POST['username']         
      # 1. 通过ORM获取用户
      user = regUser.get_by_username(ctx['username'])  #user的类型是什么？ 答案：regUser的一个实例
      # 2. 验证用户存在且活跃
      #if not user or not user.is_Active:
      if not user :
        return render(request, 'login.html', {'error': '用户不存在或已被禁用'})      
        # 3. 验证密码（使用ORM模型方法）
      if not check_password(request.POST['password'],user.password):
        return render(request, 'login.html', {'error': '密码不正确'})        
        # 4. 更新最后登录时间
      user.logintimes = user.logintimes+1234
      user.lastlogin = datetime.now()
      user.save(update_fields=['logintimes','lastlogin'])   #掌握ORM更新的方法
      print("login success")
      return HttpResponse("<p>登录成功！</p>")               
   else:
      return render(request, 'login.html', {'error': '请不用使用爬虫！'})      