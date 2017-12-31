from django.shortcuts import render, get_object_or_404, redirect

from blog.models import Post

from .models import Comment
from .forms import CommentForm

# Create your views here.


def post_comment(request, post_pk):
    # 先获取被评论的文章，
    post = get_object_or_404(Post, pk=post_pk)
    # 判断是否是post请求
    if request.method == 'POST':
        # 用户提交的数据在request.POST中, 是一个类字典对象
        form = CommentForm(request.POST)

        # 判断是否合法
        if form.is_valid():
            # commit=False的作用是仅仅利用表单的数据生成Comment模型类的实例
            comment = form.save(commit=False)
            # 将评论与文章关联
            comment.post = post
            # 最终保存到数据库
            comment.save()
            # 重定向到post详情页
            return redirect(post)
        else:
            # 检查数据不合法，重新渲染详情页，并且渲染表单的错误
            # 获取这篇文章下的全部评论
            comment_list = post.comment_set.all()
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request, 'blog/detail.html', context)
    # 不是post请求，说明用户没有提交数据，重定向到文章详情页
    return redirect(post)
