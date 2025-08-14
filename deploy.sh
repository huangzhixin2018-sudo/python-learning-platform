#!/bin/bash

# 思维空间项目部署脚本

echo "🚀 开始部署思维空间项目..."

# 检查Python版本
python_version=$(python3 --version 2>&1)
echo "Python版本: $python_version"

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo "⬆️  升级pip..."
pip install --upgrade pip

# 安装依赖
echo "📚 安装项目依赖..."
pip install -r requirements.txt

# 收集静态文件
echo "📁 收集静态文件..."
python manage.py collectstatic --noinput

# 执行数据库迁移
echo "🗄️  执行数据库迁移..."
python manage.py makemigrations
python manage.py migrate

# 创建超级用户（如果不存在）
echo "👤 检查超级用户..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('超级用户创建成功: admin/admin123')
else:
    print('超级用户已存在')
"

# 设置权限
echo "🔐 设置文件权限..."
chmod +x manage.py
chmod +x gunicorn.conf.py

# 创建日志目录
echo "📝 创建日志目录..."
mkdir -p logs
chmod 755 logs

echo "✅ 部署完成！"
echo ""
echo "📋 部署信息:"
echo "   项目名称: 思维空间"
echo "   管理后台: http://localhost:8000/admin/"
echo "   前台页面: http://localhost:8000/"
echo "   超级用户: admin / admin123"
echo ""
echo "🚀 启动命令:"
echo "   开发环境: python manage.py runserver"
echo "   生产环境: gunicorn -c gunicorn.conf.py mysite.wsgi:application"
echo ""
echo "⚠️  注意: 生产环境请修改 settings_prod.py 中的配置"
