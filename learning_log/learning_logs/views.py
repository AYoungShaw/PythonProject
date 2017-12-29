from django.shortcuts import render

# 重定向的库
from django.http import HttpResponseRedirect

from django.core.urlresolvers import reverse
# 对用户访问限制库
from django.contrib.auth.decorators import login_required

# 限制直接通过url来访问别的用户的主题
from django.http import HttpResponseRedirect, Http404


from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.


def index(request):
    """学习笔记的主页"""
    # 参数：
    # request, template_name, context = None
    return render(request, 'learning_logs/index.html')


# 访问限制
@login_required
def topics(request):
    """显示所有的主题"""
    # # 用时间进行排序获取所有Topic
    # topics = Topic.objects.order_by('date_added')
    # 只显示用户自己的主题
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    # 用字典保存所有的主题
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


# 访问限制
@login_required
# topic_id接收正则表达式 (?P<topic_id>\d+)获取到的值。
def topic(request, topic_id):
    """显示单个主题及其所有的条目"""
    # 通过id获取单个主题
    topic = Topic.objects.get(id=topic_id)
    # 确认请求的主题属于当前用户
    if topic.owner != request.user:
        raise Http404
    # 减号是按降序排序
    entries = topic.entry_set.order_by('-date_added')
    # 存入到字典中
    context = {'topic': topic, 'entries': entries}
    # 这个字典中的信息就可以在模板中使用了
    # 如果是单个变量值就可以直接拿出来使用，如果是列表形式的，就可以for循环获取
    return render(request, 'learning_logs/topic.html', context)


# 访问限制
@login_required
# 处理两种情形：
# 1、刚进入new_topic网页；
# 2、对提交的表单数据进行处理，并将用户重定向到网页topics
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交的数据，创建一个表单
        # 返回一个空表单没什么问题
        form = TopicForm()
    else:
        # POST提交的数据，对数据进行处理
        # 用户输入的数据在request.POST中
        form = TopicForm(request.POST)
        # 检查是否有效
        if form.is_valid():
            # form.save()
            # 将新主题关联到当前用户
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            # 重定向-> reverse()根据指定的URL模型确定URL
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


# 访问限制
@login_required
def new_entry(request, topic_id):
    """在特定的主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # 未提交数据，创建一个空表单
        form = EntryForm()
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # 将表单信息存入到new_entry中，而不是存储到数据库中
            new_entry = form.save(commit=False)
            topic.owner = request.user
            new_entry.topic = topic
            new_entry.save()
            # args 主要是包含URL中的所有实参
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                                args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


# 访问限制
@login_required
def edit_entry(request, entry_id):
    """编辑既有的条目"""
    # 通过entry_id获取这个条目的
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # 通过对比请求的用户是不是同一个来使修改能正确
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        # 初次请求，使用当期条目填充表单
        form = EntryForm(instance=entry)
    else:
        # POST提交的数据，使用当期条目填充表单
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                                args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)




