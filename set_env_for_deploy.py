#!/usr/bin/env python
"""
设置Vercel部署环境变量
"""
import os

# 设置Vercel部署环境变量
os.environ['DATABASE_URL'] = 'postgresql://postgres.gbpegvuuwljgfwimyjsw:PLMQAZ123456@aws-0-ap-northeast-1.pooler.supabase.com:6543/postgres'
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings_production'
os.environ['DEBUG'] = 'False'
os.environ['SECRET_KEY'] = 'w9t-u5+q#qs7xjt)^fa$r9we^$%cixnv4$^^n#2e5m2!9a0glp'
os.environ['ALLOWED_HOSTS'] = '.vercel.app,.now.sh,localhost,127.0.0.1'

print("✅ 环境变量已设置:")
print(f"DATABASE_URL: {os.environ['DATABASE_URL'][:50]}...")
print(f"DJANGO_SETTINGS_MODULE: {os.environ['DJANGO_SETTINGS_MODULE']}")
print(f"DEBUG: {os.environ['DEBUG']}")

# 运行部署前检查
print("\n🚀 运行部署前检查...")
exec(open('pre_deploy_check.py', encoding='utf-8').read())
