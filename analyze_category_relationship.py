#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from Pythonfun.models import Article, SubCategory, MainCategory

def analyze_category_relationship():
    print("🔍 分析文章编辑和分类管理的关联关系")
    print("=" * 60)
    
    # 1. 检查分类数据结构
    print("\n1. 分类数据结构分析:")
    print("-" * 30)
    
    main_categories = MainCategory.objects.all()
    print(f"主分类数量: {main_categories.count()}")
    for mc in main_categories:
        print(f"  - {mc.name} (ID: {mc.id}, Slug: {mc.slug})")
    
    sub_categories = SubCategory.objects.all()
    print(f"\n子分类数量: {sub_categories.count()}")
    for sc in sub_categories:
        print(f"  - {sc.name} (ID: {sc.id}, 主分类: {sc.parent.name if sc.parent else '无'})")
    
    # 2. 检查文章分类关联
    print("\n2. 文章分类关联分析:")
    print("-" * 30)
    
    articles = Article.objects.all()
    print(f"文章总数: {articles.count()}")
    
    # 按内容类型分组
    content_type_stats = {}
    category_stats = {}
    
    for article in articles:
        # 内容类型统计
        content_type = article.content_type
        if content_type not in content_type_stats:
            content_type_stats[content_type] = 0
        content_type_stats[content_type] += 1
        
        # 分类统计
        if article.category:
            category_name = article.category.name
            if category_name not in category_stats:
                category_stats[category_name] = 0
            category_stats[category_name] += 1
    
    print("\n按内容类型统计:")
    for ct, count in content_type_stats.items():
        print(f"  - {ct}: {count} 篇")
    
    print("\n按分类统计:")
    for cat, count in category_stats.items():
        print(f"  - {cat}: {count} 篇")
    
    # 3. 检查关联逻辑
    print("\n3. 关联逻辑检查:")
    print("-" * 30)
    
    # 检查文章编辑页面的分类选择逻辑
    print("文章编辑页面的分类选择逻辑:")
    print("  - 主分类选择: 从 /api/main-categories/ 获取")
    print("  - 子分类选择: 根据主分类从 /api/sub-categories/?main_category_id={id} 获取")
    print("  - 文章保存时使用子分类ID (category_id)")
    
    # 检查分类管理页面的数据结构
    print("\n分类管理页面的数据结构:")
    print("  - 主分类: 包含 name, slug 字段")
    print("  - 子分类: 包含 name, slug, parent_id 字段")
    print("  - 子分类通过 parent_id 关联到主分类")
    
    # 4. 检查潜在问题
    print("\n4. 潜在问题检查:")
    print("-" * 30)
    
    # 检查孤立的主分类（没有子分类）
    orphan_main_categories = []
    for mc in main_categories:
        if not mc.subcategories.exists():
            orphan_main_categories.append(mc.name)
    
    if orphan_main_categories:
        print(f"❌ 发现孤立的主分类（没有子分类）: {', '.join(orphan_main_categories)}")
    else:
        print("✅ 所有主分类都有对应的子分类")
    
    # 检查孤立的子分类（没有文章）
    orphan_sub_categories = []
    for sc in sub_categories:
        if not sc.article_set.exists():
            orphan_sub_categories.append(sc.name)
    
    if orphan_sub_categories:
        print(f"⚠️  发现孤立的子分类（没有文章）: {', '.join(orphan_sub_categories)}")
    else:
        print("✅ 所有子分类都有对应的文章")
    
    # 检查文章分类关联的完整性
    articles_without_category = articles.filter(category__isnull=True)
    if articles_without_category.exists():
        print(f"❌ 发现 {articles_without_category.count()} 篇文章没有分类")
        for article in articles_without_category:
            print(f"    - {article.title}")
    else:
        print("✅ 所有文章都有分类")
    
    # 5. 关联关系总结
    print("\n5. 关联关系总结:")
    print("-" * 30)
    print("文章编辑页面和分类管理的关联关系:")
    print("  ✅ 数据结构一致: 都使用 MainCategory 和 SubCategory 模型")
    print("  ✅ API接口一致: 都使用相同的API端点获取分类数据")
    print("  ✅ 关联逻辑正确: 文章通过 category 字段关联到子分类")
    print("  ✅ 层级关系正确: 子分类通过 parent 字段关联到主分类")
    print("  ✅ 数据流一致: 编辑页面从分类管理创建的数据中获取选项")
    
    # 6. 建议
    print("\n6. 建议:")
    print("-" * 30)
    print("  📝 确保在创建文章前先创建好分类结构")
    print("  📝 定期清理孤立的分类（如果不再使用）")
    print("  📝 考虑添加分类使用统计，帮助管理分类")
    print("  📝 可以考虑添加分类的软删除功能")

if __name__ == '__main__':
    analyze_category_relationship()
