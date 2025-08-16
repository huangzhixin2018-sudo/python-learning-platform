#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from Pythonfun.models import Article, MainCategory, SubCategory

def test_category_tree_logic():
    """测试分类树构建逻辑"""
    print("🔍 测试分类树构建逻辑")
    print("=" * 50)
    
    # 获取所有文章
    articles = Article.objects.all()
    print(f"数据库中的文章总数: {articles.count()}")
    
    # 按内容类型统计
    content_types = {}
    for article in articles:
        content_type = article.content_type
        if content_type not in content_types:
            content_types[content_type] = []
        content_types[content_type].append(article)
    
    print("\n文章内容类型分布:")
    for content_type, article_list in content_types.items():
        print(f"  {content_type}: {len(article_list)} 篇")
        for article in article_list:
            print(f"    - {article.title} (分类: {article.category.name if article.category else '无分类'})")
    
    # 测试语法类型的分类树构建
    print("\n" + "=" * 50)
    print("测试语法类型 (GR) 的分类树构建:")
    print("-" * 30)
    
    # 模拟修复后的逻辑
    model_content_type = 'GR'
    
    # 获取包含指定内容类型文章的子分类
    sub_categories_with_articles = SubCategory.objects.filter(
        article__content_type=model_content_type,
        article__is_published=True,
        is_enabled=True
    ).distinct().order_by('parent__id', 'id')
    
    print(f"包含语法文章的子分类数量: {sub_categories_with_articles.count()}")
    
    # 按主分类分组
    current_main_category = None
    current_sub_categories = []
    category_tree = []
    
    for sub_category in sub_categories_with_articles:
        if current_main_category != sub_category.parent:
            # 保存前一个主分类的数据
            if current_main_category and current_sub_categories:
                category_tree.append({
                    'main_category': current_main_category,
                    'sub_categories': current_sub_categories
                })
            
            # 开始新的主分类
            current_main_category = sub_category.parent
            current_sub_categories = []
        
        # 计算文章数量
        article_count = Article.objects.filter(
            category=sub_category,
            content_type=model_content_type,
            is_published=True
        ).count()
        sub_category.article_count = article_count
        current_sub_categories.append(sub_category)
    
    # 添加最后一个主分类的数据
    if current_main_category and current_sub_categories:
        category_tree.append({
            'main_category': current_main_category,
            'sub_categories': current_sub_categories
        })
    
    print(f"语法页面应该显示的主分类数量: {len(category_tree)}")
    
    for i, category_group in enumerate(category_tree, 1):
        main_cat = category_group['main_category']
        sub_cats = category_group['sub_categories']
        print(f"\n主分类 {i}: {main_cat.name}")
        for sub_cat in sub_cats:
            print(f"  - {sub_cat.name} (文章数量: {sub_cat.article_count})")
    
    # 测试数据结构类型
    print("\n" + "=" * 50)
    print("测试数据结构类型 (DS) 的分类树构建:")
    print("-" * 30)
    
    model_content_type = 'DS'
    
    sub_categories_with_articles = SubCategory.objects.filter(
        article__content_type=model_content_type,
        article__is_published=True,
        is_enabled=True
    ).distinct().order_by('parent__id', 'id')
    
    print(f"包含数据结构文章的子分类数量: {sub_categories_with_articles.count()}")
    
    # 按主分类分组
    current_main_category = None
    current_sub_categories = []
    category_tree = []
    
    for sub_category in sub_categories_with_articles:
        if current_main_category != sub_category.parent:
            if current_main_category and current_sub_categories:
                category_tree.append({
                    'main_category': current_main_category,
                    'sub_categories': current_sub_categories
                })
            
            current_main_category = sub_category.parent
            current_sub_categories = []
        
        article_count = Article.objects.filter(
            category=sub_category,
            content_type=model_content_type,
            is_published=True
        ).count()
        sub_category.article_count = article_count
        current_sub_categories.append(sub_category)
    
    if current_main_category and current_sub_categories:
        category_tree.append({
            'main_category': current_main_category,
            'sub_categories': current_sub_categories
        })
    
    print(f"数据结构页面应该显示的主分类数量: {len(category_tree)}")
    
    for i, category_group in enumerate(category_tree, 1):
        main_cat = category_group['main_category']
        sub_cats = category_group['sub_categories']
        print(f"\n主分类 {i}: {main_cat.name}")
        for sub_cat in sub_cats:
            print(f"  - {sub_cat.name} (文章数量: {sub_cat.article_count})")
    
    print("\n" + "=" * 50)
    print("✅ 分类树构建逻辑测试完成")

if __name__ == '__main__':
    test_category_tree_logic()
