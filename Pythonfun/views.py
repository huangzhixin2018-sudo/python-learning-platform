import json
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from .models import MainCategory, SubCategory, Article, Tag, Library, Module, OperationType, Function, Parameter

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

# ========== 页面渲染视图 ==========

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Pythonfun:category_management') # 使用URL名称进行重定向
        else:
            messages.error(request, '用户名或密码无效')
            return render(request, 'admin/登录.html', status=401)
    return render(request, 'admin/登录.html')

def index_view(request):
    """首页视图 - 显示分类树和默认第一篇文章"""
    main_categories = MainCategory.objects.filter(is_enabled=True).order_by('order')
    category_tree = []
    for main_category in main_categories:
        sub_categories = SubCategory.objects.filter(
            parent=main_category,
            is_enabled=True
        ).order_by('id')
        sub_categories_with_count = []
        for sub in sub_categories:
            article_count = Article.objects.filter(
                category=sub,
                content_type=Article.ContentType.TUTORIAL,
                is_published=True
            ).count()
            sub.article_count = article_count
            sub_categories_with_count.append(sub)
        category_tree.append({
            'main_category': main_category,
            'sub_categories': sub_categories_with_count
        })
    current_article = Article.objects.filter(
        content_type=Article.ContentType.TUTORIAL,
        is_published=True
    ).order_by('created_at').first()
    
    # 如果没有已发布的文章，且用户是管理员，尝试获取未发布的文章（用于管理员预览）
    if not current_article and request.user.is_authenticated and request.user.is_staff:
        current_article = Article.objects.filter(
            content_type=Article.ContentType.TUTORIAL,
            is_published=False
        ).order_by('created_at').first()
    context = {
        'category_tree': category_tree,
        'current_article': current_article,
    }
    return render(request, 'front/index.html', context)

def category_view(request, slug):
    """子分类文章显示视图"""
    try:
        # 获取分类树
        main_categories = MainCategory.objects.filter(is_enabled=True).order_by('order')
        category_tree = []
        for main_category in main_categories:
            sub_categories = SubCategory.objects.filter(
                parent=main_category,
                is_enabled=True
            ).order_by('id')
            sub_categories_with_count = []
            for sub in sub_categories:
                article_count = Article.objects.filter(
                    category=sub,
                    content_type=Article.ContentType.TUTORIAL,
                    is_published=True
                ).count()
                sub.article_count = article_count
                sub_categories_with_count.append(sub)
            category_tree.append({
                'main_category': main_category,
                'sub_categories': sub_categories_with_count
            })
        
        # 获取当前分类
        try:
            current_category = SubCategory.objects.get(slug=slug, is_enabled=True)
        except SubCategory.DoesNotExist:
            return render(request, 'front/404.html', {
                'error_message': f'分类 "{slug}" 不存在或已被禁用'
            }, status=404)
        
        # 获取当前分类的文章
        current_article = Article.objects.filter(
            category=current_category,
            content_type=Article.ContentType.TUTORIAL,
            is_published=True
        ).order_by('created_at').first()
        
        # 如果没有已发布的文章，且用户是管理员，尝试获取未发布的文章（用于管理员预览）
        if not current_article and request.user.is_authenticated and request.user.is_staff:
            current_article = Article.objects.filter(
                category=current_category,
                content_type=Article.ContentType.TUTORIAL,
                is_published=False
            ).order_by('created_at').first()
        
        # 构建上下文
        context = {
            'category_tree': category_tree,
            'current_category': current_category,
            'current_article': current_article,
        }
        
        # 如果没有文章，添加提示信息
        if not current_article:
            context['no_articles_message'] = f'分类 "{current_category.name}" 暂无文章'
        else:
            # 如果有文章，确保文章内容被正确处理
            if hasattr(current_article, 'content') and current_article.content:
                # 如果文章有content字段，转换为HTML
                import markdown
                current_article.content_html = markdown.markdown(current_article.content)
        
        return render(request, 'front/index.html', context)
        
    except Exception as e:
        # 记录错误并返回友好的错误页面
        print(f"Category view error: {str(e)}")
        return render(request, 'front/404.html', {
            'error_message': '加载分类页面时发生错误，请稍后重试'
        }, status=500)

@login_required
def category_management_view(request):
    return render(request, 'admin/分类管理.html')

@login_required
def article_edit_view(request):
    article_id = request.GET.get('id')
    article = None
    if article_id:
        article = get_object_or_404(Article, id=article_id)
    return render(request, 'admin/文章编辑.html', {'article': article})

@login_required
def course_management_view(request):
    return render(request, 'admin/教程管理.html')

def tutorial_detail_view(request, pk):
    tutorial = get_object_or_404(Article, pk=pk)
    is_admin = request.user.is_authenticated and request.user.is_staff
    if not tutorial.is_published and not is_admin:
        return render(request, 'front/404.html', {'error_message': '教程不存在或未发布'})

    related_tutorials = Article.objects.filter(
        category=tutorial.category, content_type=Article.ContentType.TUTORIAL, is_published=True
    ).exclude(pk=pk)[:5]
    
    context = {
        'tutorial': tutorial,
        'related_tutorials': related_tutorials,
        'is_admin': is_admin
    }
    return render(request, 'front/tutorial_detail.html', context)

# ========== API 视图 ==========

@require_http_methods(["GET", "POST"])
def main_category_api(request):
    if request.method == 'GET':
        page = request.GET.get('page', 1)
        page_size = 10
        
        categories = MainCategory.objects.all().order_by('order')
        
        # 添加分页
        paginator = Paginator(categories, page_size)
        try:
            categories_page = paginator.page(page)
        except EmptyPage:
            categories_page = paginator.page(paginator.num_pages)
        
        data = {
            'items': list(categories_page.object_list.values('id', 'name', 'slug', 'order', 'is_enabled')),
            'current_page': categories_page.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count
        }
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        try:
            main_category = MainCategory.objects.create(
                name=data['name'],
                slug=data['slug'],
                order=data.get('order', 0),
                is_enabled=data.get('is_enabled', True)
            )
            return JsonResponse({
                'status': 'success', 
                'message': 'Main category created successfully', 
                'id': main_category.id
            }, status=201)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def main_category_detail_api(request, pk):
    main_category = get_object_or_404(MainCategory, pk=pk)
    if request.method == 'GET':
        data = {
            'id': main_category.id,
            'name': main_category.name,
            'order': main_category.order,
            'is_enabled': main_category.is_enabled
        }
        return JsonResponse(data)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        main_category.name = data.get('name', main_category.name)
        main_category.slug = data.get('slug', main_category.slug)
        main_category.order = data.get('order', main_category.order)
        main_category.is_enabled = data.get('is_enabled', main_category.is_enabled)
        main_category.save()
        return JsonResponse({'status': 'success', 'message': 'Main category updated successfully'})
    elif request.method == 'DELETE':
        main_category.delete()
        return JsonResponse({'status': 'success', 'message': 'Main category deleted successfully'})

@csrf_exempt
@require_http_methods(["GET", "POST"])
def sub_category_api(request):
    if request.method == 'GET':
        main_category_id = request.GET.get('main_category_id')
        page = request.GET.get('page', 1)
        page_size = 10 # Assuming a default page size

        categories = SubCategory.objects.all()
        if main_category_id:
            categories = categories.filter(parent_id=main_category_id)

        # Add pagination
        paginator = Paginator(categories, page_size)
        try:
            categories_page = paginator.page(page)
        except EmptyPage:
            categories_page = paginator.page(paginator.num_pages)

        data = {
            'items': [{
                'id': cat.id,
                'name': cat.name,
                'slug': cat.slug,
                'parent_id': cat.parent.id if cat.parent else None,
                'parent_name': cat.parent.name if cat.parent else None,
                'is_enabled': cat.is_enabled
            } for cat in categories_page.object_list],
            'current_page': categories_page.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count
        }
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        parent_id = data.get('parent_id')
        parent_category = get_object_or_404(MainCategory, pk=parent_id) if parent_id else None
        sub_category = SubCategory.objects.create(
            name=data['name'],
            slug=data['slug'],
            parent=parent_category,
            is_enabled=data.get('is_enabled', True)
        )
        return JsonResponse({'status': 'success', 'message': 'Sub category created successfully', 'id': sub_category.id}, status=201)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def sub_category_detail_api(request, pk):
    sub_category = get_object_or_404(SubCategory, pk=pk)
    if request.method == 'GET':
        data = {
            'id': sub_category.id,
            'name': sub_category.name,
            'parent_id': sub_category.parent.id if sub_category.parent else None,
            'is_enabled': sub_category.is_enabled
        }
        return JsonResponse(data)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        sub_category.name = data.get('name', sub_category.name)
        if 'parent_id' in data:
            parent_id = data.get('parent_id')
            if parent_id:
                sub_category.parent = get_object_or_404(MainCategory, pk=parent_id)
            else:
                sub_category.parent = None
        sub_category.is_enabled = data.get('is_enabled', sub_category.is_enabled)
        sub_category.save()
        return JsonResponse({'status': 'success', 'message': 'Sub category updated successfully'})
    elif request.method == 'DELETE':
        sub_category.delete()
        return JsonResponse({'status': 'success', 'message': 'Sub category deleted successfully'})

@csrf_exempt
@require_http_methods(["GET", "POST"])
def article_api(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        data = [{
            'id': article.id,
            'title': article.title,
            'subtitle': article.subtitle,
            'summary': article.summary,
            'read_time_minutes': article.read_time_minutes,
            'is_published': article.is_published,
            'created_at': article.created_at.isoformat(),
            'updated_at': article.updated_at.isoformat(),
            'category_name': article.category.name if article.category else None,
            'tags': [tag.name for tag in article.tags.all()]
        } for article in articles]
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        article = Article.objects.create(
            title=data['title'],
            subtitle=data.get('subtitle', ''),
            summary=data.get('summary', ''),
            content_html=data.get('content_html', ''),
            content_code=data.get('content_code', ''),
            code_language=data.get('code_language', ''),
            content_type=data.get('content_type', Article.ContentType.TUTORIAL),
            read_time_minutes=data.get('read_time_minutes', 5),
            is_published=data.get('is_published', False)
        )
        if data.get('category_id'):
            article.category = get_object_or_404(SubCategory, pk=data.get('category_id'))
        article.save()
        if data.get('tags'):
            article.tags.set(Tag.objects.filter(name__in=data.get('tags')))
        return JsonResponse({'status': 'success', 'message': 'Article created successfully', 'id': article.id}, status=201)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def article_detail_api(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        data = {
            'id': article.id,
            'title': article.title,
            'subtitle': article.subtitle,
            'summary': article.summary,
            'read_time_minutes': article.read_time_minutes,
            'content_html': article.content_html,
            'content_code': article.content_code,
            'code_language': article.code_language,
            'category_id': article.category.id if article.category else None,
            'tags': [tag.name for tag in article.tags.all()],
        }
        return JsonResponse(data)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        article.title = data.get('title', article.title)
        article.subtitle = data.get('subtitle', article.subtitle)
        article.summary = data.get('summary', article.summary)
        article.read_time_minutes = data.get('read_time_minutes', article.read_time_minutes)

        article.content_html = data.get('content_html', article.content_html)
        article.content_code = data.get('content_code', article.content_code)
        article.code_language = data.get('code_language', article.code_language)
        if data.get('category_id'):
            article.category = get_object_or_404(SubCategory, pk=data.get('category_id'))
        article.save()
        article.tags.set(Tag.objects.filter(name__in=data.get('tags', [])))
        return JsonResponse({'status': 'success', 'message': 'Article updated successfully'})

@csrf_exempt
@require_http_methods(["GET", "POST"])
def course_api(request):
    if request.method == 'GET':
        page = request.GET.get('page', 1)
        page_size = 10 # Assuming a default page size

        courses = Article.objects.filter(content_type=Article.ContentType.TUTORIAL)

        # Add pagination
        paginator = Paginator(courses, page_size)
        try:
            courses_page = paginator.page(page)
        except EmptyPage:
            courses_page = paginator.page(paginator.num_pages)

        data = {
            'items': [{
                'id': course.id,
                'title': course.title,
                'subtitle': course.subtitle,
                'summary': course.summary,
                'read_time_minutes': course.read_time_minutes,
                'is_published': course.is_published,
                'created_at': course.created_at.isoformat(),
                'updated_at': course.updated_at.isoformat(),
                'category_name': course.category.name if course.category else None,
                'tags': [tag.name for tag in course.tags.all()]
            } for course in courses_page.object_list],
            'current_page': courses_page.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count
        }
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        course = Article.objects.create(
            title=data['title'],
            subtitle=data.get('subtitle', ''),
            summary=data.get('summary', ''),
            read_time_minutes=data.get('read_time_minutes', 0),
            content_html=data.get('content_html', ''),
            content_code=data.get('content_code', ''),
            code_language=data.get('code_language', ''),
            content_type=Article.ContentType.TUTORIAL,
            is_published=data.get('is_published', False)
        )
        if data.get('category_id'):
            course.category = get_object_or_404(SubCategory, pk=data.get('category_id'))
        course.save()
        if data.get('tags'):
            course.tags.set(Tag.objects.filter(name__in=data.get('tags')))
        return JsonResponse({'status': 'success', 'message': 'Course created successfully', 'id': course.id}, status=201)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def course_detail_api(request, pk):
    course = get_object_or_404(Article, pk=pk, content_type=Article.ContentType.TUTORIAL)
    if request.method == 'GET':
        data = {
            'id': course.id,
            'title': course.title,
            'subtitle': course.subtitle,
            'summary': course.summary,
            'read_time_minutes': course.read_time_minutes,
            'content_html': course.content_html,
            'content_code': course.content_code,
            'code_language': course.code_language,
            'category_id': course.category.id if course.category else None,
            'category_name': course.category.name if course.category else None,
            'tags': [tag.name for tag in course.tags.all()],
            'is_published': course.is_published,
        }
        return JsonResponse(data)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        course.title = data.get('title', course.title)
        course.subtitle = data.get('subtitle', course.subtitle)
        course.summary = data.get('summary', course.summary)
        course.read_time_minutes = data.get('read_time_minutes', course.read_time_minutes)

        course.content_html = data.get('content_html', course.content_html)
        course.content_code = data.get('content_code', course.content_code)
        course.code_language = data.get('code_language', course.code_language)
        if data.get('category_id'):
            course.category = get_object_or_404(SubCategory, pk=data.get('category_id'))
        course.save()
        course.tags.set(Tag.objects.filter(name__in=data.get('tags', [])))
        return JsonResponse({'status': 'success', 'message': 'Course updated successfully'})
    elif request.method == 'DELETE':
        try:
            # 记录删除的教程信息用于日志
            course_title = course.title
            course_id = course.id
            
            # 删除教程
            course.delete()
            
            return JsonResponse({
                'status': 'success', 
                'message': f'教程 "{course_title}" 已成功删除',
                'deleted_id': course_id
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'删除教程失败: {str(e)}'
            }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def course_publish_api(request, pk):
    """发布/取消发布教程API"""
    try:
        course = get_object_or_404(Article, pk=pk, content_type=Article.ContentType.TUTORIAL)
        data = json.loads(request.body)
        
        # 支持多种请求格式
        action = data.get('action')
        is_published = data.get('is_published')
        
        if action == 'publish':
            course.is_published = True
            course.save()
            return JsonResponse({
                'status': 'success', 
                'message': f'教程 "{course.title}" 发布成功！'
            })
        elif action == 'unpublish':
            course.is_published = False
            course.save()
            return JsonResponse({
                'status': 'success', 
                'message': f'教程 "{course.title}" 已取消发布'
            })
        elif is_published is not None:
            course.is_published = is_published
            course.save()
            return JsonResponse({
                'status': 'success', 
                'message': 'Course publish status updated successfully'
            })
        else:
            return JsonResponse({
                'status': 'error', 
                'message': 'Invalid request: missing action or is_published field'
            }, status=400)
            
    except Exception as e:
        return JsonResponse({
            'status': 'error', 
            'message': f'发布失败: {str(e)}'
        }, status=500)

# ========== 导航栏页面视图 ==========

def function_library_view(request):
    """函数库页面视图"""
    return render(request, 'front/函数库.html')

def function_query_view(request):
    """函数查询页面视图"""
    return render(request, 'front/函数查询.html')

def data_structure_view(request):
    """数据结构页面视图"""
    return render(request, 'front/数据结构.html')

def statement_view(request):
    """语句页面视图"""
    return render(request, 'front/语句.html')

def project_view(request):
    """项目页面视图"""
    return render(request, 'front/项目.html')

def create_superuser_view(request):
    """创建超级用户页面视图"""
    return render(request, 'admin/create_superuser.html')

def reset_password_view(request):
    """重置密码页面视图"""
    return render(request, 'admin/reset_password.html')

@csrf_exempt
@require_http_methods(["POST"])
def create_superuser_api(request):
    """创建超级用户的API端点"""
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # 检查是否已存在超级用户
        if User.objects.filter(is_superuser=True).exists():
            return JsonResponse({
                'success': False,
                'message': '超级用户已存在'
            })
        
        # 创建超级用户
        username = "admin"
        email = "admin@example.com"
        password = "admin123456"
        
        # 检查用户是否已存在
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            message = f"用户 {username} 已升级为超级用户"
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_superuser=True,
                is_staff=True
            )
            message = f"超级用户创建成功！用户名: {username}, 密码: {password}"
        
        return JsonResponse({
            'success': True,
            'message': message,
            'username': username,
            'password': password
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'创建超级用户失败: {str(e)}'
        })

@csrf_exempt
@require_http_methods(["POST"])
def reset_admin_password_api(request):
    """重置管理员密码的API端点"""
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # 查找admin用户
        try:
            user = User.objects.get(username='admin')
        except User.DoesNotExist:
            # 如果admin用户不存在，创建一个
            user = User.objects.create_user(
                username='admin',
                email='admin@example.com',
                password='admin123456',
                is_superuser=True,
                is_staff=True,
                is_active=True
            )
            message = "admin用户创建成功"
        else:
            # 重置密码
            user.set_password('admin123456')
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.save()
            message = "admin用户密码已重置"
        
        return JsonResponse({
            'success': True,
            'message': message,
            'username': 'admin',
            'password': 'admin123456'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'重置密码失败: {str(e)}'
        })

# ========== 函数库相关API视图 ==========

@require_http_methods(["GET"])
def function_library_api(request):
    """函数库数据API"""
    try:
        # 获取所有库
        libraries = Library.objects.all()
        data = {}
        
        for library in libraries:
            library_data = {
                'name': library.library_name_cn,
                'modules': []
            }
            
            # 获取库下的所有模块
            modules = library.modules.all()
            for module in modules:
                module_data = {
                    'name': module.module_name,
                    'description': module.description or '',
                    'items': []
                }
                
                # 获取模块下的所有函数
                functions = module.functions.all()
                for function in functions:
                    function_data = {
                        'type': 'function',
                        'name': function.function_name,
                        'semantic': function.description_cn or function.description or '',
                        'operation': function.operation_type.operation_name_cn if function.operation_type else '',
                        'input': function.parameters_text or '',
                        'output': function.return_value_cn or function.return_value or ''
                    }
                    module_data['items'].append(function_data)
                
                library_data['modules'].append(module_data)
            
            data[library.library_name] = library_data
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def function_query_api(request):
    """函数查询API"""
    try:
        # 获取查询参数
        library_name = request.GET.get('library')
        module_name = request.GET.get('module')
        function_name = request.GET.get('function')
        operation_type = request.GET.get('operation_type')
        search = request.GET.get('search', '').lower()
        
        # 构建查询
        functions = Function.objects.select_related('module', 'module__library', 'operation_type')
        
        if library_name:
            functions = functions.filter(module__library__library_name=library_name)
        
        if module_name:
            functions = functions.filter(module__module_name=module_name)
        
        if function_name:
            functions = functions.filter(function_name__icontains=function_name)
        
        if operation_type:
            functions = functions.filter(operation_type__operation_name_cn=operation_type)
        
        if search:
            functions = functions.filter(
                models.Q(function_name__icontains=search) |
                models.Q(description__icontains=search) |
                models.Q(description_cn__icontains=search)
            )
        
        # 序列化数据
        data = []
        for function in functions:
            function_data = {
                'id': function.function_id,
                'library_name': function.module.library.library_name_cn,
                'module_name': function.module.module_name,
                'function_name': function.function_name,
                'function_name_cn': function.function_name_cn,
                'description': function.description_cn or function.description,
                'operation_type': function.operation_type.operation_name_cn if function.operation_type else '',
                'syntax': function.syntax,
                'parameters': function.parameters_text,
                'return_value': function.return_value_cn or function.return_value,
                'example': function.example_cn or function.example,
                'availability': function.availability,
                'version_added': function.version_added,
                'parameters_detail': []
            }
            
            # 获取参数详细信息
            for param in function.parameters.all():
                param_data = {
                    'name': param.parameter_name,
                    'name_cn': param.parameter_name_cn,
                    'data_type': param.data_type,
                    'is_required': param.is_required,
                    'default_value': param.default_value,
                    'description': param.description_cn or param.description
                }
                function_data['parameters_detail'].append(param_data)
            
            data.append(function_data)
        
        return JsonResponse(data, safe=False)
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def function_libraries_list_api(request):
    """获取库列表API"""
    try:
        libraries = Library.objects.all()
        data = [{
            'id': library.library_id,
            'name': library.library_name,
            'name_cn': library.library_name_cn,
            'description': library.description,
            'is_builtin': library.is_builtin,
            'is_standard': library.is_standard
        } for library in libraries]
        
        return JsonResponse(data, safe=False)
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def function_modules_list_api(request):
    """获取模块列表API"""
    try:
        library_id = request.GET.get('library_id')
        modules = Module.objects.select_related('library')
        
        if library_id:
            modules = modules.filter(library_id=library_id)
        
        data = [{
            'id': module.module_id,
            'name': module.module_name,
            'description': module.description,
            'library_name': module.library.library_name_cn,
            'is_builtin': module.is_builtin
        } for module in modules]
        
        return JsonResponse(data, safe=False)
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def function_operation_types_api(request):
    """获取操作类型列表API"""
    try:
        operation_types = OperationType.objects.all()
        data = [{
            'id': op.operation_type_id,
            'name': op.operation_name,
            'name_cn': op.operation_name_cn,
            'description': op.description
        } for op in operation_types]
        
        return JsonResponse(data, safe=False)
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)