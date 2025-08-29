#!/usr/bin/env python
"""
创建Django超级用户
用于生产环境初始化
"""
import os
import sys
import django
from django.contrib.auth import get_user_model

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings_production')
django.setup()

def create_superuser():
    """创建超级用户"""
    User = get_user_model()
    
    # 检查是否已存在超级用户
    if User.objects.filter(is_superuser=True).exists():
        print("✅ 超级用户已存在")
        superusers = User.objects.filter(is_superuser=True)
        for user in superusers:
            print(f"   - {user.username} ({user.email})")
        return True
    
    # 创建新的超级用户
    print("🔧 创建超级用户...")
    
    # 默认超级用户信息
    username = "admin"
    email = "admin@example.com"
    password = "admin123456"
    
    try:
        # 检查用户是否已存在
        if User.objects.filter(username=username).exists():
            print(f"⚠️  用户 {username} 已存在，正在升级为超级用户...")
            user = User.objects.get(username=username)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            print(f"✅ 用户 {username} 已升级为超级用户")
        else:
            # 创建新用户
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_superuser=True,
                is_staff=True
            )
            print(f"✅ 超级用户创建成功！")
            print(f"   用户名: {username}")
            print(f"   邮箱: {email}")
            print(f"   密码: {password}")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建超级用户失败: {e}")
        return False

def list_users():
    """列出所有用户"""
    User = get_user_model()
    users = User.objects.all()
    
    print(f"\n📋 当前用户列表 ({users.count()} 个用户):")
    for user in users:
        status = "超级用户" if user.is_superuser else "普通用户"
        print(f"   - {user.username} ({user.email}) - {status}")

def main():
    """主函数"""
    print("🚀 Django超级用户管理")
    print("=" * 50)
    
    # 创建超级用户
    if create_superuser():
        # 列出所有用户
        list_users()
        
        print("\n🎉 超级用户设置完成！")
        print("💡 您可以使用以下凭据登录:")
        print("   用户名: admin")
        print("   密码: admin123456")
        print("\n⚠️  请在生产环境中及时修改密码！")
        
        return 0
    else:
        print("\n💥 超级用户创建失败！")
        return 1

if __name__ == "__main__":
    sys.exit(main())
