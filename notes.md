因为涉及跟数据库的交互，我参考了一下其他的 一些项目，把登录和注册的实现写在后端代码里了（后端代码尚未经过测试）。

这先作为一个前后端数据传送的参考吧。

前端login method：

```javascript
login() {
      this.$refs.validate((valid)=>{
        if(valid){
          var data=Qs.stringify({"username":this.loginForm.username,"password":this.loginForm.password})
          // 向后端发送请求
          axios.post("http://localhost:8000",data).then(
            function(resp) {
              const flag=resp.data.request['flag']
              if(flag=='yes')
                this.$router.push("/home")
              else
                alert(resp.data.request['msg'])
            }
          )
        }
        else
          alert("出现错误，请重试")
      })
    }
```

后端views.py里login功能

```python
def login(request):
    username = request.POST.get("username")
	password = request.POST.get("password")
	try:
		user = models.User.objects.get(username=username)
	except:
		date = {'flag': 'no', "msg" : "unregisterd"}
	if password == user.password:
		date_msg = "success"
		date_flag = "yes"
	else:
		date_msg = "wrong password"
		date_flag = "no"
	date = {'flag':date_flag,'msg': date_msg}

	return JsonResponse({'request': date})
​	
```

```python
def register(request):
    username = request.POST.get("username")
    mail_address = request.POST.get("email")
    password = request.POST.get("password")
    try:
        user = models.User.objects.filter(mail_address=mail_address)
        date = {'flag': 'no', "msg" : "email existed"}
    except:
        user.save()
        date = {'flag': 'yes', "msg" : "success"}
		
	return JsonResponse({'request':date})
        
```

