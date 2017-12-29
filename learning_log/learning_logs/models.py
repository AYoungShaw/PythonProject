from django.db import models
# 只显示与当前用户相关联的数据
from django.contrib.auth.models import User

# Create your models here.
# 在setting.py 中添加项目


class Topic(models.Model):
    """用户学习的主题"""
    # 由字符或文本组成的数据，需要定义长度
    text = models.CharField(max_length=200)
    # 记录日期和时间，设置为True 设置为当期时间
    date_added = models.DateTimeField(auto_now_add=True)
    # 添加外键
    owner = models.ForeignKey(User)

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text


class Entry(models.Model):
    """学到的有关主题的具体知识"""
    # 定义外键，关联到Topic主题
    topic = models.ForeignKey(Topic)
    # 文本字段，不需要限制长度
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 定义复数形式
        verbose_name_plural = 'entries'
        # verbose_name 定义别名

    def __str__(self):
        """返回模型的字符串表示"""
        # 如果文本长度小于50就全部显示
        if len(self.text) < 50:
            return self.text
        else:
            return self.text[:50] + '...'

