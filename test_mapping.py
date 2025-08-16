#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from Pythonfun.models import SubCategory, MainCategory

def test_content_type_mapping():
    print("🔍 测试内容类型映射逻辑")
    print("=" * 50)
    
    # 导入Article模型
    from Pythonfun.models import Article
    
    # 1. 检查数据库中的实际内容类型值
    print("\n1. 数据库中的内容类型值:")
    content_types = Article.objects.values_list('content_type', flat=True).distinct()
    for ct in content_types:
        print(f"  - '{ct}'")
    
    # 2. 检查模型定义
    print("\n2. 模型定义的内容类型:")
    for choice in Article.ContentType.choices:
        print(f"  - {choice[0]} -> {choice[1]}")
    
    # 3. 模拟前端映射逻辑
    print("\n3. 前端映射逻辑测试:")
    
    # 读取时的映射（从数据库到前端）
    read_mapping = {
        'AI': 'ai-programming',
        'DS': 'data-structure', 
        'GR': 'grammar'
    }
    
    # 保存时的映射（从前端到数据库）
    save_mapping = {
        'grammar': 'GR',
        'data-structure': 'DS',
        'ai-programming': 'AI'
    }
    
    print("  读取映射 (数据库 -> 前端):")
    for db_value, frontend_value in read_mapping.items():
        print(f"    '{db_value}' -> '{frontend_value}'")
    
    print("  保存映射 (前端 -> 数据库):")
    for frontend_value, db_value in save_mapping.items():
        print(f"    '{frontend_value}' -> '{db_value}'")
    
    # 4. 验证映射的一致性
    print("\n4. 映射一致性验证:")
    for db_value in content_types:
        if db_value in read_mapping:
            frontend_value = read_mapping[db_value]
            if frontend_value in save_mapping:
                back_to_db = save_mapping[frontend_value]
                if back_to_db == db_value:
                    print(f"  ✅ '{db_value}' -> '{frontend_value}' -> '{back_to_db}' (一致)")
                else:
                    print(f"  ❌ '{db_value}' -> '{frontend_value}' -> '{back_to_db}' (不一致)")
            else:
                print(f"  ❌ 前端值 '{frontend_value}' 在保存映射中不存在")
        else:
            print(f"  ❌ 数据库值 '{db_value}' 在读取映射中不存在")
    
    # 5. 检查实际文章的内容类型
    print("\n5. 实际文章的内容类型:")
    articles = Article.objects.all()
    for article in articles:
        print(f"  - '{article.title}' -> '{article.content_type}'")
    
    # 6. 检查是否有无效的内容类型
    print("\n6. 内容类型有效性检查:")
    valid_types = ['GR', 'DS', 'AI']
    for article in articles:
        if article.content_type not in valid_types:
            print(f"  ❌ 文章 '{article.title}' 有无效内容类型: '{article.content_type}'")
        else:
            print(f"  ✅ 文章 '{article.title}' 内容类型有效: '{article.content_type}'")

if __name__ == '__main__':
    test_content_type_mapping()
