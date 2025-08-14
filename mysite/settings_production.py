"""
生产环境配置文件
适用于Vercel部署
"""

import os

# 只导入基础设置，不导入数据库配置
from .settings import (
    BASE_DIR, SECRET_KEY, INSTALLED_APPS, MIDDLEWARE, ROOT_URLCONF, TEMPLATES,
    WSGI_APPLICATION, AUTH_PASSWORD_VALIDATORS, LANGUAGE_CODE, TIME_ZONE,
    USE_I18N, USE_TZ, STATIC_URL, DEFAULT_AUTO_FIELD, LOGIN_URL, LOGIN_REDIRECT_URL
)

# 生产环境设置
DEBUG = False

# 安全设置
SECURE_SSL_REDIRECT = False  # Vercel会自动处理HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# 允许的主机
ALLOWED_HOSTS = [
    '.vercel.app',
    '.now.sh',
    'localhost',
    '127.0.0.1',
    '*'
]

# 静态文件配置
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# 数据库配置 - 必须使用PostgreSQL
import dj_database_url

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("生产环境必须设置DATABASE_URL环境变量")

# 验证数据库URL格式
if not (DATABASE_URL.startswith('postgresql://') or DATABASE_URL.startswith('postgres://')):
    raise ValueError("生产环境必须使用PostgreSQL数据库")

# 生产环境PostgreSQL配置
DATABASES = {
    'default': dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,  # 连接池最大存活时间
        conn_health_checks=True,  # 启用连接健康检查
        ssl_require=True  # 强制SSL连接
    )
}

print(f"[OK] 生产环境使用PostgreSQL数据库: {DATABASE_URL[:50]}...")
print(f"[INFO] 数据库引擎: {DATABASES['default']['ENGINE']}")
print(f"[INFO] 数据库主机: {DATABASES['default']['HOST']}")
print(f"[INFO] 数据库端口: {DATABASES['default']['PORT']}")
print(f"[INFO] 数据库名称: {DATABASES['default']['NAME']}")

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
