#!/usr/bin/env python
"""
Vercel部署前检查脚本
"""
import os
import sys
import django
from pathlib import Path

def check_environment():
    """检查环境配置"""
    print("🔍 检查环境配置...")
    
    # 检查Python版本
    print(f"Python版本: {sys.version}")
    
    # 检查关键环境变量
    required_vars = ['DATABASE_URL', 'DJANGO_SETTINGS_MODULE']
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: {value[:50]}..." if len(value) > 50 else f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: 未设置")
            return False
    
    return True

def check_django_config():
    """检查Django配置"""
    print("\n🔍 检查Django配置...")
    
    try:
        # 设置Django环境
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings_production')
        django.setup()
        
        from django.conf import settings
        
        # 检查关键设置
        print(f"✅ DEBUG: {settings.DEBUG}")
        print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"✅ DATABASE ENGINE: {settings.DATABASES['default']['ENGINE']}")
        print(f"✅ STATIC_ROOT: {settings.STATIC_ROOT}")
        
        return True
        
    except Exception as e:
        print(f"❌ Django配置检查失败: {e}")
        return False

def check_database_connection():
    """检查数据库连接"""
    print("\n🔍 检查数据库连接...")
    
    try:
        from django.db import connection
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ 数据库连接成功: {version[0][:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def check_static_files():
    """检查静态文件"""
    print("\n🔍 检查静态文件...")
    
    static_dir = Path("static")
    if static_dir.exists():
        files = list(static_dir.rglob("*"))
        print(f"✅ 静态文件目录存在，包含 {len(files)} 个文件")
        return True
    else:
        print("❌ 静态文件目录不存在")
        return False

def check_requirements():
    """检查依赖包"""
    print("\n🔍 检查依赖包...")
    
    required_packages = [
        'django',
        'psycopg2',
        'dj_database_url',
        'whitenoise',
        'gunicorn'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}: 已安装")
        except ImportError:
            print(f"❌ {package}: 未安装")
            return False
    
    return True

def main():
    """主函数"""
    print("🚀 Vercel部署前检查")
    print("=" * 50)
    
    checks = [
        check_environment,
        check_django_config,
        check_database_connection,
        check_static_files,
        check_requirements
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有检查通过！可以安全部署到Vercel")
        return 0
    else:
        print("💥 检查失败！请修复问题后再部署")
        return 1

if __name__ == "__main__":
    sys.exit(main())
