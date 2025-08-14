"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``app``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# 强制设置生产环境设置
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings_production'

# 确保DATABASE_URL环境变量被设置（如果vercel.json没有正确传递）
if 'DATABASE_URL' not in os.environ:
    os.environ['DATABASE_URL'] = 'postgresql://postgres.gbpegvuuwljgfwimyjsw:PLMQAZ123456@aws-0-ap-northeast-1.pooler.supabase.com:6543/postgres'

app = get_wsgi_application()
