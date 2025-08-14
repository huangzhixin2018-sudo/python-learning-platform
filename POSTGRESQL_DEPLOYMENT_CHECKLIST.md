# PostgreSQL部署检查清单

## 🚀 部署前检查

### 1. 环境变量配置 ✅
- [x] `DATABASE_URL` 已正确设置
- [x] 格式: `postgresql://username:password@host:port/dbname`
- [x] 当前值: `postgresql://postgres:huangzhixin2025@db.wjuaayjnetykmnyqejhi.supabase.co:5432/postgres`

### 2. 依赖包检查 ✅
- [x] `psycopg2-binary==2.9.9` 已在 requirements.txt 中
- [x] `dj-database-url==2.1.0` 已在 requirements.txt 中
- [x] `Django==5.0.7` 版本兼容

### 3. 配置文件检查 ✅
- [x] `mysite/settings.py` 已优化PostgreSQL配置
- [x] `mysite/settings_production.py` 已配置生产环境
- [x] `vercel.json` 已设置环境变量

### 4. 数据库连接测试
运行以下命令测试连接:
```bash
python test_postgres_connection.py
```

### 5. 数据库表结构准备
运行以下命令创建表结构:
```bash
python prepare_database.py
```

## 🔧 部署步骤

### 步骤1: 本地测试
```bash
# 设置环境变量
export DATABASE_URL="postgresql://postgres:huangzhixin2025@db.wjuaayjnetykmnyqejhi.supabase.co:5432/postgres"

# 测试数据库连接
python test_postgres_connection.py

# 准备数据库
python prepare_database.py

# 启动开发服务器
python manage.py runserver
```

### 步骤2: Vercel部署
1. 确保 `vercel.json` 配置正确
2. 在Vercel项目设置中添加环境变量:
   - `DATABASE_URL`: `postgresql://postgres:huangzhixin2025@db.wjuaayjnetykmnyqejhi.supabase.co:5432/postgres`
   - `DJANGO_SETTINGS_MODULE`: `mysite.settings_production`
3. 部署项目

### 步骤3: 部署后验证
1. 检查Vercel部署日志
2. 访问应用确认功能正常
3. 检查数据库连接是否稳定

## 🚨 常见问题解决

### 问题1: 数据库连接超时
**解决方案:**
- 检查防火墙设置
- 确认数据库服务器可访问
- 验证连接字符串格式

### 问题2: SSL连接错误
**解决方案:**
- 确保 `ssl_require=True` 设置正确
- 检查数据库服务器SSL配置
- 验证证书有效性

### 问题3: 权限错误
**解决方案:**
- 检查数据库用户权限
- 确认用户有创建表的权限
- 验证数据库名称是否正确

### 问题4: 连接池问题
**解决方案:**
- 调整 `conn_max_age` 参数
- 启用 `conn_health_checks`
- 监控连接数量

## 📊 性能优化建议

### 数据库连接优化
- 设置合适的 `conn_max_age` (建议600秒)
- 启用连接健康检查
- 使用连接池管理

### SSL配置优化
- 强制SSL连接 (`ssl_require=True`)
- 设置SSL模式 (`ssl_mode='require'`)
- 配置连接超时

### 监控和日志
- 启用Django日志记录
- 监控数据库连接状态
- 记录连接错误信息

## 🔍 故障排除命令

### 检查数据库状态
```bash
# 测试连接
python test_postgres_connection.py

# 检查Django配置
python manage.py check --database default

# 查看数据库表
python manage.py dbshell
```

### 查看日志
```bash
# 查看Django日志
python manage.py runserver --verbosity 2

# 查看Vercel部署日志
vercel logs
```

## 📞 技术支持

如果遇到问题，请检查:
1. 数据库服务器状态
2. 网络连接
3. 防火墙设置
4. 用户权限
5. SSL证书

---

**最后更新:** 2024年12月
**状态:** ✅ 配置完成，准备部署
