# PostgreSQL 数据库配置指南

## 🎯 概述

本项目已配置支持PostgreSQL数据库，使用`dj_database_url`包来解析连接字符串。配置支持自动回退到SQLite数据库（本地开发）。

## 🔧 配置步骤

### 1. 环境变量配置

#### 本地开发环境
创建 `local.env` 文件（已创建）：
```bash
# 本地开发环境配置
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL数据库连接配置
DATABASE_URL=postgresql://postgres:huangzhixin2025@db.wjuaayjnetykmnyqejhi.supabase.co:5432/postgres

# Django设置模块
DJANGO_SETTINGS_MODULE=mysite.settings
```

#### Vercel生产环境
更新 `vercel.env` 文件（已更新）：
```bash
# 数据库配置 - 使用PostgreSQL
DATABASE_URL=postgresql://postgres:huangzhixin2025@db.wjuaayjnetykmnyqejhi.supabase.co:5432/postgres
```

### 2. 替换密码

**重要**: 数据库密码已配置为 `huangzhixin2025`

### 3. 加载环境变量

#### 方法1: 使用python-decouple（推荐）
```bash
# 安装依赖
pip install python-decouple

# 运行Django
python manage.py runserver
```

#### 方法2: 手动设置环境变量
```bash
# Windows PowerShell
$env:DATABASE_URL="postgresql://postgres:huangzhixin2025@db.wjuaayjnetykmnyqejhi.supabase.co:5432/postgres"

# Windows CMD
set DATABASE_URL=postgresql://postgres:huangzhixin2025@db.wjuaayjnetykmnyqejhi.supabase.co:5432/postgres

# Linux/Mac
export DATABASE_URL="postgresql://postgres:huangzhixin2025@db.wjuaayjnetykmnyqejhi.supabase.co:5432/postgres"
```

## 🧪 测试数据库连接

运行测试脚本：
```bash
python test_postgres_connection.py
```

## 📊 数据库迁移

### 1. 创建PostgreSQL表
```bash
python create_postgres_tables.py
```

### 2. 运行Django迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. 创建超级用户
```bash
python manage.py createsuperuser
```

## 🔍 配置验证

### 成功标志
- Django启动时显示 "✅ 使用PostgreSQL数据库"
- 测试脚本显示 "✅ 数据库连接成功"
- 可以正常访问Django管理界面

### 故障排除
- 检查密码是否正确
- 确认网络连接（防火墙设置）
- 验证Supabase数据库是否运行
- 检查PostgreSQL驱动是否正确安装

## 🚀 部署到Vercel

1. 在Vercel项目设置中添加环境变量：
   - `DATABASE_URL`: 你的PostgreSQL连接字符串
   - `SECRET_KEY`: Django安全密钥
   - `DEBUG`: False

2. 部署时Vercel会自动使用PostgreSQL数据库

## 📝 注意事项

- 生产环境请设置强密码
- 定期备份数据库
- 监控数据库连接性能
- 使用SSL连接（生产环境）

## 🔗 相关文件

- `mysite/settings.py` - Django数据库配置
- `vercel.json` - Vercel部署配置
- `requirements.txt` - 项目依赖
- `test_postgres_connection.py` - 连接测试脚本
