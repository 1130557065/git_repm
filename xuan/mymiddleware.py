from django.utils.deprecation import MiddlewareMixin
from blog import models
class MyAuth(MiddlewareMixin):
    """
    中间件有五种方法
        process_request
        process_view
        process_exception
        process_template_response
        process_response
    """

    def process_requset(self,request):
        user_id  = request.session.get("user_id")
        if user_id:

            # 把登录的用户赋值为用户名,
            user_obj = models.Userinfo.objects.filter(id=user_id).first()
            request.user = user_obj
            print(request.user.name)

        else:
            # 如果没有登录,默认赋值为匿名用户
            request.user = {"name":"未登录 游客"}
            print(request.user.name)
