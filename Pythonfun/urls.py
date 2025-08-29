from django.urls import path
from . import views

app_name = 'Pythonfun'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.index_view, name='index'),
    path('category/<str:slug>/', views.category_view, name='category'),
    path('manage/category-management/', views.category_management_view, name='category_management'),
    path('manage/article-edit/', views.article_edit_view, name='article_edit'),
    path('manage/course-management/', views.course_management_view, name='course_management'),
    
    # 前台页面路由
    path('tutorial/<int:pk>/', views.tutorial_detail_view, name='tutorial_detail'),
    
    # API 路由 - 分类管理
    path('api/main-categories/', views.main_category_api, name='main_category_api'),
    path('api/main-categories/<int:pk>/', views.main_category_detail_api, name='main_category_detail_api'),
    path('api/sub-categories/', views.sub_category_api, name='sub_category_api'),
    path('api/sub-categories/<int:pk>/', views.sub_category_detail_api, name='sub_category_detail_api'),
    
    # API 路由 - 文章管理
    path('api/articles/', views.article_api, name='article_api'),
    path('api/articles/<int:pk>/', views.article_detail_api, name='article_detail_api'),
    
    # API 路由 - 教程管理
    path('api/courses/', views.course_api, name='course_api'),
    path('api/courses/<int:pk>/', views.course_detail_api, name='course_detail_api'),
    path('api/courses/<int:pk>/publish/', views.course_publish_api, name='course_publish_api'),
    
    # 导航栏页面路由
    path('function-library/', views.function_library_view, name='function_library'),
    path('function-query/', views.function_query_view, name='function_query'),
    path('data-structure/', views.data_structure_view, name='data_structure'),
    path('ai-programming/', views.ai_programming_view, name='ai_programming'),
    path('project/', views.project_view, name='project'),
    
    # 系统管理页面
    path('create-superuser/', views.create_superuser_view, name='create_superuser'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    
    # 系统管理API
    path('api/create-superuser/', views.create_superuser_api, name='create_superuser_api'),
    path('api/reset-admin-password/', views.reset_admin_password_api, name='reset_admin_password_api'),
    
    # 函数管理页面路由
    path('manage/function-management/', views.function_management_view, name='function_management'),
    
    # 函数库相关API路由
    path('api/function-library/', views.function_library_api, name='function_library_api'),
    path('api/function-query/', views.function_query_api, name='function_query_api'),
    path('api/function-libraries/', views.function_libraries_list_api, name='function_libraries_list_api'),
    path('api/function-modules/', views.function_modules_list_api, name='function_modules_list_api'),
    path('api/function-operation-types/', views.function_operation_types_api, name='function_operation_types_api'),
    
    # 函数管理API路由
    path('api/upload-functions/', views.upload_functions_api, name='upload_functions'),
    path('api/function-stats/', views.get_function_stats_api, name='get_function_stats'),
    path('api/table-structure/', views.get_table_structure_api, name='get_table_structure'),
    path('api/export-functions/', views.export_functions_api, name='export_functions'),
    path('api/download-template/', views.download_template_api, name='download_template'),
]