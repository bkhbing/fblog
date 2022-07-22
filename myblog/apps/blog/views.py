from django.shortcuts import render
from blog.models import Article
from blog.models import Banner
from blog.models import Category
from blog.models import Link
from blog.models import Tag

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def index(request):
    # 所有文章
    allcategory = Category.objects.all()
    # 首页推荐
    tui = Article.objects.filter(tui__id=1)[:3]#查询推荐位ID为1的文章
    # 幻灯片
    banner = Banner.objects.filter(is_active=True)[0:4]#查询所有幻灯图数据，并进行切片
    print(banner)
    # 最新文章
    allarticle = Article.objects.all().order_by('-id')[0:10]
    # 热门文章
    hot = Article.objects.all().order_by('views')[:10]#通过浏览数进行排序
    # 热门推荐
    remen = Article.objects.filter(tui__id=2)[:6]
    # 所有标签
    tags = Tag.objects.all()
    # 友情链接
    link = Link.objects.all()
    #把查询到的对象，封装到上下文
    context = {
        'tui': tui,
        'allcategory': allcategory,
        'banner':banner,
        'allarticle': allarticle,
        'hot':hot,
        'remen':remen,
        'tags':tags,
        'link':link,
    }
    #把上传文传到模板页面index.html里
    return render(request,'index.html',context)
    
    
    
    
#文章列表
def list(request,lid):
    list = Article.objects.filter(category_id=lid)#获取通过URL传进来的lid，然后筛选出对应文章
    cname = Category.objects.get(id=lid)#获取当前文章的栏目名
    remen = Article.objects.filter(tui__id=2)[:6]#右侧的热门推荐
    allcategory = Category.objects.all()#导航所有分类
    tags = Tag.objects.all()#右侧所有文章标签
    page = request.GET.get('page')#在URL中获取当前页面数
    paginator = Paginator(list, 5)#对查询到的数据对象list进行分页，设置超过5条数据就分页
    try:
        list = paginator.page(page)#获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'list.html', locals())


def show(request,sid):
    show = Article.objects.get(id=sid)#查询指定ID的文章
    allcategory = Category.objects.all()#导航上的分类
    tags = Tag.objects.all()#右侧所有标签
    remen = Article.objects.filter(tui__id=2)[:6]#右侧热门推荐
    hot = Article.objects.all().order_by('?')[:10]#内容下面的您可能感兴趣的文章，随机推荐
    previous_blog = Article.objects.filter(created_time__gt=show.created_time,category=show.category.id).first()
    netx_blog = Article.objects.filter(created_time__lt=show.created_time,category=show.category.id).last()
    show.views = show.views + 1
    show.save()
    return render(request, 'show.html', locals())

def tag(request, tag):
    list = Article.objects.filter(tags__name=tag)#通过文章标签进行查询文章
    remen = Article.objects.filter(tui__id=2)[:6]
    allcategory = Category.objects.all()
    tname = Tag.objects.get(name=tag)#获取当前搜索的标签名
    page = request.GET.get('page')
    tags = Tag.objects.all()
    paginator = Paginator(list, 5)
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'tags.html', locals())


def search(request):
    ss=request.GET.get('search')#获取搜索的关键词
    list = Article.objects.filter(title__icontains=ss)#获取到搜索关键词通过标题进行匹配
    remen = Article.objects.filter(tui__id=2)[:6]
    allcategory = Category.objects.all()
    page = request.GET.get('page')
    tags = Tag.objects.all()
    paginator = Paginator(list, 10)
    try:
        list = paginator.page(page) # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1) # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages) # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'search.html', locals())


# 关于我们
def about(request):
    allcategory = Category.objects.all()
    return render(request, 'page.html',locals())