from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from blog import models, forms
from django.contrib import auth
from geetest import GeetestLib

# Create your views here.

# 首页的视图函数
def index(request):
    #查询所有的文章列表
    # article_list = models.Article.objects.all()
    # 从URL去参数
    page_num = request.GET.get("page")

    # 总数据是多少
    total_count = models.Article.objects.all().count()

    """
        #从URL去参数
        page_num = request.GET.get("page")
        #每一页显示多少条数据
        per_page = 10
        #总页码数是多少
        total_count = models.Book.objects.all().count()
        #总共需要多少页码展示
        # total_count // per_page
        total_page, m = divmod(total_count,per_page)
        if m:
            total_page += 1
        # 如果出现一个不正常的页码就默认为1
        try:
            page_num = int(page_num)
            # 如果超过当前页码数 则为最当前
            if page_num > total_page:
                page_num = total_page
        except Exception as e:
            # 当输入一个页码不是正经数字的时候,默认返回第一页数据
            page_num = 1
        # 页面上总共展示多少页码
        max_page = 11
        if total_page < max_page:
            max_page = total_page

        data_start = (page_num - 1) * 10
        data_end = page_num * 10

        half_max_page = max_page // 2
        #页面上展示的页码从哪儿开始
        page_start = page_num - half_max_page
        #页面上展示的页码到哪儿结束
        page_end = page_num + half_max_page

        #如果当前页减一半比1还小
        if page_start <=1 :
            page_start = 1
            page_end = max_page
        #如果当前页加一半比总页码数还大
        if page_end >= total_page:
            page_end = total_page
            page_start = total_page - max_page + 1

        all_book = models.Book.objects.all()[data_start:data_end]
        # 自己拼接分页的HTML代码
        html_str_list = []
        #加上第一页
        html_str_list.append('<li><a href="/books/?page=1">首页</a></li>')
        #加上一个上一页的标签
        if page_num <=1:
            page_num = 1
            html_str_list.append('<li class="disabled"><a href="#"><span aria-hidden="true">&laquo;</span></a></li>')
        else:
            html_str_list.append('<li><a href="/books/?page={}"><span aria-hidden="true">&laquo;</span></a></li>'.format(page_num-1))

        for i in range(page_start,page_end+1):
            # 如果是当前页就加一个active样式
            if i == page_num:
                tmp = '<li class="active"><a href="/books/?page={0}">{0}</a></li>'.format(i)
            else:
                tmp = '<li><a href="/books/?page={0}">{0}</a></li>'.format(i)
            html_str_list.append(tmp)
        # 加上一个下一页的标签
        if page_num >= total_page :
            html_str_list.append('<li class="disabled"><a href=""><span aria-hidden="true">&raquo;</span></a></li>')
        else:
            html_str_list.append('<li><a href="/books/?page={}"><span aria-hidden="true">&raquo;</span></a></li>'.format(page_num+1))
        #加上最后一页
        html_str_list.append('<li><a href="/books/?page={}">尾页</a></li>'.format(total_page))
        page_html = "".join(html_str_list)
        return render(request,"books.html",{"books": all_book, "page_html": page_html})
        """
    from utils.mypage import Page
    page_obj = Page(page_num, total_count, url_prefix="/index/", per_page=5, max_page=7)
    ret = models.Article.objects.all()[page_obj.start:page_obj.end]

    page_html = page_obj.page_html()

    return render(request, "index.html", {"article_list": ret, "page_html": page_html})
# 注册
def register(request):
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}
        form_obj = forms.RegForm(request.POST)
        # 做校验
        if form_obj.is_valid():
            # 校验通过,去数据库创建一个新的用户
            form_obj.cleaned_data.pop("re_password")  # 添加用户前先把确认密码字段删除
            avatar_img = request.FILES.get("avatar")
            models.UserInfo.objects.create_user(**form_obj.cleaned_data, avatar=avatar_img)
            ret["msg"] = "/index/"
            return JsonResponse(ret)
        else:
            print(form_obj.errors)
            ret["status"] = 1
            ret["msg"] = form_obj.errors
            print(ret)
            print("=" * 12)
            return JsonResponse(ret)

    # 生成一个Form对象
    form_obj = forms.RegForm()
    print(form_obj.fields)
    return render(request, "register.html", {"form_obj": form_obj})

# 使用极验验证码验证登录
def login(request):
    # if request.is_ajax():  # 如果是AJAX请求
    if request.method == "POST":
        # 初始化一个给AJAX返回的数据
        ret = {"status": 0, "msg": ""}
        # 从提交过来的数据中 取到用户名和密码
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        # 获取极验 滑动验证码相关的参数
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]

        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            # 验证码正确
            # 利用auth模块做用户名和密码的校验
            user = auth.authenticate(username=username, password=pwd)
            if user:
                # 用户名密码正确
                # 给用户做登录
                auth.login(request, user)  # 将登录用户赋值给 request.user
                ret["msg"] = "/index/"
            else:
                # 用户名密码错误
                ret["status"] = 1
                ret["msg"] = "用户名或密码错误！"
        else:
            ret["status"] = 1
            ret["msg"] = "验证码错误"
        return JsonResponse(ret)
    return render(request, "login.html")

# 请在官网申请ID使用，示例ID不可使用
# pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
# pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"
pc_geetest_id = "ffd294642512d2fd95e3f0666daa9f76"
pc_geetest_key = "de6f1e9d2a20f8487941082ba8282ce9"

# 处理极验 获取验证码的视图
def get_geetest(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)

#注销登录
def logout(request):
    auth.logout(request)
    return redirect("/index/")

