#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from Pythonfun.models import Article

def check_tutorial_articles():
    print("🔍 检查教程管理页面的文章显示逻辑")
    print("=" * 50)
    
    # 获取所有文章
    all_articles = Article.objects.all()
    print(f"数据库中的文章总数: {all_articles.count()}")
    
    print("\n所有文章的详细信息:")
    for article in all_articles:
        print(f"  - ID: {article.id}")
        print(f"    标题: {article.title}")
        print(f"    内容类型: {article.content_type} ({article.get_content_type_display()})")
        print(f"    分类: {article.category.name if article.category else '无分类'}")
        print(f"    发布状态: {'已发布' if article.is_published else '草稿'}")
        print()
    
    # 检查教程管理页面应该显示的文章（content_type='GR'）
    tutorial_articles = Article.objects.filter(content_type=Article.ContentType.GRAMMAR)
    print(f"\n教程管理页面应该显示的文章数量: {tutorial_articles.count()}")
    
    if tutorial_articles.exists():
        print("教程管理页面应该显示的文章:")
        for article in tutorial_articles:
            print(f"  - {article.title} (ID: {article.id})")
    else:
        print("⚠️  没有找到语法类型的文章，教程管理页面将显示为空")
    
    # 检查其他内容类型的文章
    other_articles = Article.objects.exclude(content_type=Article.ContentType.GRAMMAR)
    print(f"\n其他内容类型的文章数量: {other_articles.count()}")
    
    if other_articles.exists():
        print("其他内容类型的文章（不会在教程管理中显示）:")
        for article in other_articles:
            print(f"  - {article.title} (ID: {article.id}, 类型: {article.get_content_type_display()})")
    
    # 分析问题
    print("\n" + "=" * 50)
    print("问题分析:")
    print("教程管理页面只显示 content_type='GR'（语法类型）的文章")
    print("其他内容类型的文章（'DS'数据结构、'AI'AI编程）不会在教程管理中显示")
    print()
    print("解决方案:")
    print("1. 如果希望所有文章都在教程管理中显示，需要修改 course_api 视图")
    print("2. 如果希望只有语法文章在教程管理中显示，这是正常行为")
    print("3. 可以在文章编辑页面选择不同的内容类型来创建不同类型的文章")

if __name__ == '__main__':
    check_tutorial_articles()
