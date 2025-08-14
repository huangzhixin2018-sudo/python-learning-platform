# 🚀 Vercel部署检查清单

## ✅ 代码和依赖检查

### 1. 依赖文件检查
- [x] `requirements.txt` 已生成并包含所有依赖
- [x] `requirements-vercel.txt` 包含生产环境依赖
- [x] 所有关键依赖已安装：
  - [x] Django==5.2.3
  - [x] dj-database-url==2.1.0
  - [x] psycopg2==2.9.10
  - [x] python-decouple==3.8
  - [x] django-cors-headers==4.7.0
  - [x] django-storages==1.14.2
  - [x] whitenoise==6.9.0

### 2. 代码检查
- [x] 本地运行 `python manage.py check` - 无错误
- [x] 代码无语法错误
- [x] 项目配置正确

### 3. 静态文件检查
- [x] 运行 `python manage.py collectstatic --noinput` - 成功
- [x] 静态文件已收集到 `staticfiles/` 目录

## ✅ 配置检查

### 1. 数据库配置
- [x] `settings.py` 支持PostgreSQL和SQLite
- [x] 使用环境变量管理数据库连接
- [x] 生产环境强制使用PostgreSQL
- [x] 本地开发使用SQLite

### 2. 静态文件配置
- [x] `STATIC_ROOT` 配置正确
- [x] `STATICFILES_DIRS` 配置正确
- [x] Vercel静态文件托管配置

### 3. 安全设置
- [x] 生产环境 `DEBUG = False`
- [x] `ALLOWED_HOSTS` 包含Vercel域名
- [x] `SECRET_KEY` 使用环境变量管理
- [x] 启用所有安全中间件
- [x] HTTPS重定向配置
- [x] 安全Cookie设置
- [x] HSTS配置

### 4. 环境变量配置
- [x] `DATABASE_URL` - PostgreSQL连接字符串
- [x] `SECRET_KEY` - Django密钥
- [x] `DEBUG` - 生产环境设为False
- [x] `ALLOWED_HOSTS` - 允许的主机列表

## ✅ Vercel配置

### 1. 部署配置
- [x] `vercel.json` 配置正确
- [x] WSGI入口点配置正确
- [x] Python运行时配置正确
- [x] 环境变量配置正确
- [x] 函数超时设置

### 2. WSGI配置
- [x] `mysite/wsgi.py` 导出 `app` 变量
- [x] Django设置模块路径正确
- [x] 支持Vercel serverless环境

## 🚀 部署步骤

### 1. 环境准备
```bash
# 安装依赖
pip install -r requirements-vercel.txt

# 检查项目
python manage.py check

# 收集静态文件
python manage.py collectstatic --noinput
```

### 2. 数据库设置
- 注册PostgreSQL服务（Neon、Supabase、Railway等）
- 获取数据库连接字符串
- 在Vercel Dashboard中设置 `DATABASE_URL`

### 3. 环境变量设置
在Vercel Dashboard中设置：
```
DATABASE_URL=postgresql://username:password@host:port/database_name
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=.vercel.app,.now.sh
```

### 4. 部署
```bash
# 部署到Vercel
vercel --prod

# 部署完成后创建数据库表
python create_postgres_tables.py
```

## 🔍 部署后检查

### 1. 功能测试
- [ ] 网站可以正常访问
- [ ] 数据库连接正常
- [ ] 静态文件加载正常
- [ ] 管理后台可以访问

### 2. 性能检查
- [ ] 页面加载速度
- [ ] 数据库查询性能
- [ ] 静态文件CDN性能

### 3. 安全检查
- [ ] HTTPS正常工作
- [ ] 安全头设置正确
- [ ] 错误信息不泄露敏感数据

## 📝 注意事项

1. **数据库限制**：Vercel不支持SQLite，必须使用PostgreSQL
2. **文件存储**：Vercel是无状态环境，不支持文件上传存储
3. **环境变量**：确保所有敏感信息都通过环境变量管理
4. **静态文件**：Vercel会自动处理静态文件，无需额外配置
5. **超时限制**：Vercel函数有30秒超时限制

## 🆘 常见问题

### 1. 数据库连接错误
- 检查 `DATABASE_URL` 格式是否正确
- 确认PostgreSQL服务是否正常运行
- 检查网络连接和防火墙设置

### 2. 静态文件404
- 确认 `STATIC_ROOT` 配置正确
- 检查 `collectstatic` 是否成功运行
- 验证Vercel静态文件配置

### 3. 环境变量未生效
- 确认环境变量名称正确
- 检查Vercel Dashboard设置
- 重新部署项目

---

**🎉 项目已准备好部署到Vercel！**
