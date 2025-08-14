# 🚀 Vercel部署指南

## 准备工作

您的Django项目已经配置好，可以部署到Vercel了！以下是部署步骤：

### 1. 安装Vercel CLI

由于PowerShell执行策略限制，您需要以管理员身份运行PowerShell并执行：

```powershell
Set-ExecutionPolicy RemoteSigned
npm install -g vercel
```

或者使用Git Bash：
```bash
npm install -g vercel
```

### 2. 登录Vercel

```bash
vercel login
```

### 3. 部署项目

在项目根目录执行：
```bash
vercel --prod
```

## 项目配置状态

✅ **数据库配置**: 已配置PostgreSQL连接池
✅ **环境变量**: 已设置DATABASE_URL
✅ **静态文件**: 已配置Whitenoise
✅ **生产设置**: 已配置settings_production.py
✅ **依赖包**: 已创建requirements-vercel.txt

## 关键配置文件

### vercel.json
```json
{
  "builds": [
    { "src": "mysite/wsgi.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "mysite/wsgi.py" }
  ],
  "env": {
    "DJANGO_SETTINGS_MODULE": "mysite.settings_production",
    "DATABASE_URL": "postgresql://postgres.gbpegvuuwljgfwimyjsw:PLMQAZ123456@aws-0-ap-northeast-1.pooler.supabase.com:6543/postgres"
  }
}
```

### 数据库配置
- **主机**: aws-0-ap-northeast-1.pooler.supabase.com
- **端口**: 6543
- **数据库**: postgres
- **用户**: postgres.gbpegvuuwljgfwimyjsw
- **SSL**: 已启用

## 部署后检查

部署成功后，请检查：

1. **网站可访问性**: 访问Vercel提供的URL
2. **数据库连接**: 确认应用能正常连接数据库
3. **静态文件**: 确认CSS/JS文件正常加载
4. **功能测试**: 测试主要功能是否正常

## 故障排除

如果部署失败，请检查：

1. **Vercel Dashboard**: 查看构建日志
2. **环境变量**: 确认DATABASE_URL正确设置
3. **依赖包**: 确认requirements-vercel.txt包含所有必要包
4. **数据库连接**: 确认PostgreSQL连接池可访问

## 成功部署后

🎉 您的Django应用将运行在Vercel上，具有：
- 自动HTTPS
- 全球CDN
- 自动扩展
- 零停机部署

## 联系支持

如果遇到问题，请：
1. 查看Vercel Dashboard的部署日志
2. 检查数据库连接状态
3. 确认所有环境变量正确设置
