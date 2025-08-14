#!/usr/bin/env python
"""
PostgreSQL数据库表创建脚本
适用于Vercel部署
"""

import os
import sys
import django
from pathlib import Path

# 添加项目根目录到Python路径
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.core.management import execute_from_command_line

def create_tables():
    """创建数据库表"""
    print("🔄 正在创建PostgreSQL数据库表...")
    
    try:
        # 运行数据库迁移
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ 数据库表创建成功！")
        
        # 创建超级用户（可选）
        print("👤 是否创建超级用户？(y/n): ", end="")
        choice = input().lower().strip()
        
        if choice == 'y':
            execute_from_command_line(['manage.py', 'createsuperuser'])
            print("✅ 超级用户创建成功！")
        
    except Exception as e:
        print(f"❌ 创建数据库表失败: {e}")
        return False
    
    return True

if __name__ == '__main__':
    create_tables()
