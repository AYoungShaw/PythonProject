from django.db import models
# 为了更改编辑器
from DjangoUeditor.models import UEditorField
# 将url转换成指定的格式
from django.core.urlresolvers import reverse


# Create your models here.
# 规划:
# 栏目：名称，网址，简介等
# 文章：标题，作者，网址，内容等
# 文章与作者是多对一的关系
# 文章与栏目是多对多的关系


class Column(models.Model):
    name = models.CharField('栏目名称', max_length=256)
    slug = models.CharField('栏目网站', max_length=256, db_index=True)
    intro = models.TextField('栏目简介', default='')
    # 是否在导航栏显示
    nav_display = models.BooleanField('导航显示', default=False)
    home_display = models.BooleanField('首页显示', default=False)

    # 将url转换成/column/slug格式
    def get_absolute_url(self):
        return reverse('column', args=(self.slug,))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '栏目'
        verbose_name_plural = '栏目'
        ordering = ['name']  # 按照哪个栏目排序


class Article(models.Model):
    # 默认地，Django会为每一个Model建一个名称为id的主键
    # id 这个是默认有的。可以自己定义一个其他的主键来覆盖它
    id = models.AutoField(primary_key=True)
    # 文章与栏目是多对多的关系，所以是多键
    column = models.ManyToManyField(Column, verbose_name='归属栏目')

    title = models.CharField('标题', max_length=256)
    slug = models.CharField('网址', max_length=200, unique=True)

    # 作者与文章是一对多的关系，所以是外键
    author = models.ForeignKey('auth.User', blank=True, null=True, verbose_name='作者')
    # 仅修改content字段, 使之能使用编辑器
    # content = models.TextField('内容', default='', blank=True)
    content = UEditorField('内容', height=300, width=1000,
                           default=u'', blank=True, imagePath="uploads/images/",
                           toolbars='besttome', filePath='uploads/files/')

    published = models.BooleanField('正式发布', default=True)
    pub_date = models.DateTimeField('发表时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)

    # 将url转换成/article/pk/slug格式
    def get_absolute_url(self):
        return reverse('article', args=(self.pk, self.slug))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '教程'
        verbose_name_plural = '教程'

