from django.contrib import admin
from .models import Article, MainCategory, SubCategory, Tag

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_published', 'created_at', 'updated_at']
    list_filter = ['is_published', 'category', 'tags', 'created_at']
    search_fields = ['title', 'summary', 'content_html']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'subtitle', 'summary', 'category')
        }),
        ('内容', {
            'fields': ('content_html', 'content_code', 'code_language')
        }),
        ('分类和标签', {
            'fields': ('tags',)
        }),
        ('发布设置', {
            'fields': ('is_published', 'read_time_minutes')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def save_model(self, request, obj, form, change):
        if obj.is_published:
            obj.full_clean()
        super().save_model(request, obj, form, change)

@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_enabled']
    list_filter = ['is_enabled']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_enabled']
    list_filter = ['is_enabled', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
