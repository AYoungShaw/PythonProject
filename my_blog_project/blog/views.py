from django.shortcuts import render, get_object_or_404
# 类视图
from django.views.generic import ListView, DetailView
# 支持markdown 用pip install 安装
import markdown
# 锚点
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
# 导入评论表单
from comments.forms import CommentForm
from .models import Post, Category, Tag
# 搜索
from django.db.models import Q

# Create your views here.


# 类视图就可以不需要用index函数了
class IndexView(ListView):
    model= Post
    template_name = 'blog/index.html'
    # 模板保存的变量名
    context_object_name = 'post_list'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一行包含多少篇文章
    # 类视图已经写好了分页逻辑
    # paginator ，即Paginator的实例。
    # page_obj ，当前请求页面分页对象。
    # is_paginated，是否已分页。只有当分页后页面超过两页时才算已分页。
    # object_list，请求页面的对象列表，和post_list等价。
    # 所以在模板中循环文章列表时可以选post_list ，也可以选object_list。
    paginate_by = 10

    # 复杂分页：
    # 第1页页码，这一页需要始终显示。
    # 第1页页码后面的省略号部分。
    # 但要注意如果第1页的页码号后面紧跟着页码号2，那么省略号就不应该显示。
    # 当前页码的左边部分，比如这里的3 - 6。
    # 当前页码，比如这里的7。
    # 当前页码的右边部分，比如这里的8 - 11。
    # 最后一页页码前面的省略号部分。但要注意如果最后一页的页码号前面跟着的页码号是连续的，那么省略号就不应该显示。
    # 最后一页的页码号。
    def get_context_data(self, **kwargs):
        """
        在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
        例如 render(request, 'blog/index.html', context={'post_list': post_list})，
        这里传递了一个 {'post_list': post_list} 字典给模板。
        在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
        所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
        """

        # 首先获得父类生成的传递给模板的字典
        context = super().get_context_data(**kwargs)

        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False。
        # 由于context是一个字典，所以调用get方法从中去除某个键对应的值
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的pagination_data 方法获得显示分页导航条需要的数据
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到context中
        context.update(pagination_data)

        # 将更新后的context返回，以便listview使用这个字典中的模板变量来渲染模板
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，返回空
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第1页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第一页的页码号
        # 因为如果当前页左边的连续页码号中已经包含有第一页的页码号，此时就无需再显示第一页的页码号
        # 其他情况下第一页的页码是始终需要显示的
        # 初始值为False
        first = False

        # 标示是否需要显示最后一页的页码号
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是[1,2,3,4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此left=[]
            # 此时只要获取当前页右边的连续页码号
            # 比如分页页码列表是[1,2,3,4]，那么获取的就是right=[2,3]
            # 注意这里只获取了当前页码后连续两个页码，你可以更改数字以获取更多页码
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减1还要1
            # 说明最右边的页码号和最后一页的页码号之间还有其他页码，因此需要显示省略号。通过right_has_more来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此right=[]
            # 此时只要获取当前页左边的连续页码号
            # 比如分页页码列表是[1,2,3,4]，那么获取的就是left=[2,3]
            # 这里只获取了当前页码后连续两个页码，你也可以更改数字以获取更多页码
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0: page_number - 1]

            # 如果最左边的页码号比第2页页码号还大
            # 说明最左边的页码号和第一页的页码号之间还有其他页码，因此需要用省略号，通过left_has_more表示
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第1页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码
            # 所以需要显示第一页的页码号，通过first指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第一页，则需要获取当前页左右两边的连续页码号
            # 这里只获取当前页码前后连续两个页码，你可以更改数字获取更多页码
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0: page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第一页和第一页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data


class CategoryView(IndexView):
    # 继承IndexView，下面的就不需要了
    # model = Post
    # template_name = 'blog/index.html'
    # context_object_name = 'post_list'

    # 复写get_queryset方法，获取指定数据
    # 在类视图中，从URL
    # 捕获的命名组参数值保存在实例的kwargs属性（是一个字典）里，
    # 非命名组参数值保存在实例的args属性（是一个列表）里。
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class ArchivesView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_tiem__year=year,
                                                               created_tiem__month=month
                                                               )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 复写get方法的目的是因为每当文章被访问一次，将得将文章阅读量 +1
        # get方法返回的是一个httpResponse实例
        # 只有get方法被调用后
        # 才有self.object属性，其值为post模型实例
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量+1
        # self.object的值就是被访问的文章post
        self.object.increase_views()
        # 必须返回一个httpresp对象
        return response

    def get_object(self, queryset=None):
        # 复写get_object方法的目的是因为需要对post的body值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
                                'markdown.extensions.extra',
                                'markdown.extensions.codehilite',
                                # 'markdown.extensions.toc',
                                TocExtension(slugify=slugify),
                                ]
                )
        post.body = md.convert(post.body)
        post.toc = md.toc

        return post

    def get_context_data(self, **kwargs):
        # 复写get_context_data的目的是因为除了将post传递给模板外
        # 还需要把评论表单、post下的评论列表传递给模板
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list,
        })

        return context


class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


# def index(request):
#     post_list = Post.objects.all()
#
#     context = {'post_list': post_list}
#     return render(request, 'blog/index.html', context)


# def category(request, pk):
#     """分类试图"""
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate).order_by('-created_time')
#     context = {'post_list': post_list}
#     return render(request, 'blog/index.html', context)


# def archives(request, year, month):
#     """归档试图"""
#     post_list = Post.objects.filter(created_time__year=year,
#                                     created_time__month=month
#                                     ).order_by('-created_time')
#     context = {'post_list': post_list}
#     return render(request, 'blog/index.html', context)


# def detail(request, pk):
#     # 如果对应的pk存在时就返回post否则返回404
#     post = get_object_or_404(Post, pk=pk)
#
#     # 阅读量 +1
#     post.increase_views()
#
#     post.body = markdown.markdown(
#                 post.body, extensisons=[
#                         'markdown.extensions.extra',
#                         'markdown.extensions.codehilite',
#                         'markdown.extensions.toc',
#                         ]
#                 )
#     # 创建一个评论表单
#     form = CommentForm()
#     # 获取所有该post下所有评论
#     comment_list = post.comment_set.all()
#
#     context = {'post': post,
#                'form': form,
#                'comment_list': comment_list}
#
#     return render(request, 'blog/detail.html', context)


def search(request):
    """搜索"""
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = '请输入关键词'
        return render(request, 'blog/index.html', {'error_msg': error_msg})
    # i表示不区分大小写
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'post_list': post_list})



