# 思维空间 - Python学习网站

一个现代化的Python学习网站，提供教程管理、分类管理和文章编辑功能。

## 🚀 功能特性

- **教程管理**: 支持主分类和子分类的层级管理
- **文章编辑**: 集成TinyMCE富文本编辑器
- **代码编辑**: 集成Monaco代码编辑器
- **函数库系统**: 完整的Python函数库查询和管理
- **函数查询**: 支持按库、模块、操作类型等条件查询
- **响应式设计**: 现代化的UI设计，支持移动端
- **权限管理**: 基于Django的认证系统
- **RESTful API**: 完整的后端API支持

## 🛠️ 技术栈

- **后端**: Django 5.2.3
- **前端**: HTML5, CSS3, JavaScript
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **编辑器**: TinyMCE, Monaco Editor
- **部署**: Gunicorn + Nginx

## 📁 项目结构

```
mysite/
├── mysite/                 # Django项目配置
│   ├── settings.py        # 开发环境配置
│   ├── settings_prod.py   # 生产环境配置
│   ├── urls.py            # 主URL配置
│   └── wsgi.py            # WSGI配置
├── Pythonfun/             # 主应用
│   ├── models.py          # 数据模型
│   ├── views.py           # 视图函数
│   ├── urls.py            # 应用URL配置
│   └── admin.py           # 管理后台配置
├── templates/              # 模板文件
│   ├── admin/             # 管理后台模板
│   └── front/             # 前台页面模板
├── static/                 # 静态文件
├── requirements.txt        # Python依赖
├── gunicorn.conf.py       # Gunicorn配置
├── deploy.sh              # 部署脚本
└── README.md              # 项目说明
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip
- 虚拟环境工具

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd mysite
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate     # Windows
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **数据库迁移**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **创建超级用户**
   ```bash
   python manage.py createsuperuser
   ```

6. **启动开发服务器**
   ```bash
   python manage.py runserver
   ```

7. **访问网站**
   - 前台页面: http://127.0.0.1:8000/
   - 管理后台: http://127.0.0.8000/admin/

### 使用部署脚本

```bash
chmod +x deploy.sh
./deploy.sh
```

## 🔧 配置说明

### 开发环境

使用 `mysite/settings.py` 配置文件，包含：
- DEBUG = True
- 开发数据库配置
- 开发环境安全设置

### 生产环境

使用 `mysite/settings_prod.py` 配置文件，包含：
- DEBUG = False
- 生产环境安全设置
- 日志配置
- 缓存配置

## 📚 使用指南

### 管理后台

1. **分类管理**: 创建和管理主分类、子分类
2. **文章管理**: 创建、编辑、发布文章
3. **教程管理**: 管理教程内容和发布状态

### 前台页面

1. **首页**: 显示分类树和默认文章
2. **分类页面**: 按分类显示相关文章
3. **文章详情**: 完整的文章内容展示

## 🚀 部署

### 使用Gunicorn

```bash
gunicorn -c gunicorn.conf.py mysite.wsgi:application
```

### 使用Nginx

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location /static/ {
        alias /path/to/your/staticfiles/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔒 安全配置

- 生产环境必须设置 `SECRET_KEY`
- 启用HTTPS
- 配置防火墙规则
- 定期更新依赖包

## 📝 开发规范

- 遵循PEP 8代码规范
- 使用有意义的变量和函数名
- 添加适当的注释和文档
- 编写单元测试

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

本项目采用MIT许可证。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 邮箱: your-email@example.com
- 项目Issues: [GitHub Issues](https://github.com/yourusername/mysite/issues)

---

**思维空间** - 探索数据科学的无限可能 🚀
