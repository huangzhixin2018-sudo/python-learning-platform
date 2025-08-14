#!/usr/bin/env python3
"""
数据库准备脚本
用于创建必要的数据库表结构和初始数据
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_database():
    """设置数据库"""
    print("🔧 开始设置数据库...")
    
    try:
        # 设置Django环境
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
        django.setup()
        
        print("✅ Django环境设置完成")
        
        # 运行数据库迁移
        print("📊 运行数据库迁移...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("✅ 数据库迁移完成")
        
        # 创建超级用户（如果不存在）
        print("👤 检查超级用户...")
        try:
            from django.contrib.auth.models import User
            if not User.objects.filter(is_superuser=True).exists():
                print("⚠️  未找到超级用户，请手动创建:")
                print("   python manage.py createsuperuser")
            else:
                print("✅ 超级用户已存在")
        except Exception as e:
            print(f"⚠️  检查超级用户时出错: {e}")
        
        # 检查模型
        print("🔍 检查数据模型...")
        try:
            from Pythonfun.models import Category, Article
            
            # 检查分类表
            category_count = Category.objects.count()
            print(f"   📂 分类数量: {category_count}")
            
            # 检查文章表
            article_count = Article.objects.count()
            print(f"   📄 文章数量: {article_count}")
            
            # 如果没有数据，创建示例数据
            if category_count == 0:
                print("📝 创建示例分类...")
                Category.objects.create(
                    name="Python基础",
                    description="Python编程基础知识",
                    order=1
                )
                Category.objects.create(
                    name="数据结构",
                    description="Python数据结构详解",
                    order=2
                )
                print("✅ 示例分类创建完成")
            
        except Exception as e:
            print(f"⚠️  检查模型时出错: {e}")
        
        print("\n🎉 数据库设置完成!")
        return True
        
    except Exception as e:
        print(f"❌ 数据库设置失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 数据库准备工具")
    print("=" * 50)
    
    # 检查环境变量
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        print(f"📝 检测到DATABASE_URL: {database_url[:50]}...")
        
        if 'postgresql://' in database_url or 'postgres://' in database_url:
            print("✅ 使用PostgreSQL数据库")
        else:
            print("⚠️  建议使用PostgreSQL数据库")
    else:
        print("⚠️  未检测到DATABASE_URL环境变量")
    
    # 设置数据库
    success = setup_database()
    
    if success:
        print("\n💡 下一步操作:")
        print("   1. 运行 'python manage.py runserver' 启动开发服务器")
        print("   2. 访问 http://localhost:8000/admin/ 管理后台")
        print("   3. 部署到Vercel前确保环境变量配置正确")
    else:
        print("\n❌ 数据库设置失败，请检查错误信息")

if __name__ == '__main__':
    main()
