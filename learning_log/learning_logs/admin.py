from django.contrib import admin

# Register your models here.
# 这是在admin注册模型

from learning_logs.models import Topic, Entry

admin.site.register(Topic)
admin.site.register(Entry)