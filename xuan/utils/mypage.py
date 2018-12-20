# 封装一个分页的函数
class Page():
    def __init__(self, page_num, total_count, url_prefix, per_page=4, max_page=7):
        """

        :param page_num: 当前页码数
        :param total_count: 数据总数
        :param url_prefix: 按标签href的前缀
        :param per_page: 每一页显示多少条数据
        :param max_page: 页面上最多显示几个页码
        """
        self.url_prefix = url_prefix
        # 每一页显示多少条数据
        self.per_page = per_page
        # 总共需要多少页码来展示
        total_page, m = divmod(total_count, per_page)
        if m:
            total_page += 1
        self.total_page = total_page

        try:
            page_num = int(page_num)
            # 如果输入的页码超过最大的页码,默认返回最后一页
            if page_num > total_page:
                page_num = total_page
        except Exception as e:
            # 如果出现一个页码数不为int类型的数则
            page_num = 1
        self.page_num = page_num

        # 定义两个变量保存数据从哪儿去到哪儿
        self.data_start = (page_num - 1) * self.per_page
        self.data_end = page_num * self.per_page

        # 页面上总共展示多少页码
        self.max_page = max_page
        if total_page < self.max_page:
            self.max_page = total_page
        halt_max_page = self.max_page // 2
        # 页面上展示的页码从哪儿开始
        page_start = page_num - halt_max_page
        # 页面上展示的页码从哪儿结束
        page_end = page_num + halt_max_page
        # 如果当前页减一半比1还小
        if page_start <= 1:
            page_start = 1
            page_end = self.max_page
        # 如果当前页加一半比总码数还大
        if page_end >= total_page:
            page_end = total_page
            page_start = total_page - self.max_page + 1
        self.page_start = page_start
        self.page_end = page_end

    @property
    def start(self):
        return self.data_start

    @property
    def end(self):
        return self.data_end

    def page_html(self):
        # 自己拼接分页的HTML代码
        html_str_list = []
        # 加上第一页
        html_str_list.append('<li><a href="{}?page=1">首页</a></li>'.format(self.url_prefix))
        # 加上一个上一页的标签
        if self.page_num <= 1:
            self.page_num = 1
            html_str_list.append('<li class="disabled"><a href="#"><span aria-hidden="true">&laquo;</span></a></li>')
        else:
            html_str_list.append(
                '<li><a href="{}?page={}"><span aria-hidden="true">&laquo;</span></a></li>'.format(self.url_prefix,
                                                                                                   self.page_num - 1))

        for i in range(self.page_start, self.page_end + 1):
            # 如果是当前页就加一个active样式
            if i == self.page_num:
                tmp = '<li class="active"><a href="{0}?page={1}">{1}</a></li>'.format(self.url_prefix, i)
            else:
                tmp = '<li><a href="{0}?page={1}">{1}</a></li>'.format(self.url_prefix, i)
            html_str_list.append(tmp)
        # 加上一个下一页的标签
        if self.page_num >= self.total_page:
            html_str_list.append('<li class="disabled"><a href=""><span aria-hidden="true">&raquo;</span></a></li>')
        else:
            html_str_list.append(
                '<li><a href="{}?page={}"><span aria-hidden="true">&raquo;</span></a></li>'.format(self.url_prefix,
                                                                                                   self.page_num + 1))
        # 加上最后一页
        html_str_list.append('<li><a href="{}?page={}">尾页</a></li>'.format(self.url_prefix, self.total_page))

        page_html = "".join(html_str_list)
        return page_html
