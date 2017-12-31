from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.template.context import RequestContext

from django.forms.formsets import formset_factory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from bootstrap_toolkit.widgets import BootstrapUneditableInput
from django.contrib.auth.decorators import login_required

from .forms import LoginForm


# Create your views here.


def login(request):
    """
    1、判断必填项用户名和密码是否为空，如果为空，提示'用户名和密码为必填项'的错误信息
    2、判断用户名和密码是否正确，如果错误，提示'用户名或密码错误'的错误信息
    3、登录成功后，进行主页(index.html)
    """
    if request.method == 'GET':
        form = LoginForm()
        return render_to_response('login.html', RequestContext(request, {'form': form,}))
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return render_to_response('index.html', RequestContext(request))
            else:
                return render_to_response('login.html', RequestContext(request, {'form': form, 'password_is_wrong': True}))
        else:
            return render_to_response('login.html', RequestContext(request, {'form': form,}))

