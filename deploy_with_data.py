#!/usr/bin/env python
"""
部署脚本 - 确保函数库数据正确迁移到生产环境
"""

import os
import sys
import django
import subprocess

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"\n=== {description} ===")
    print(f"执行命令: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ 成功")
        if result.stdout:
            print(f"输出: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 失败: {e}")
        if e.stdout:
            print(f"标准输出: {e.stdout}")
        if e.stderr:
            print(f"错误输出: {e.stderr}")
        return False

def main():
    """主部署流程"""
    print("🚀 开始部署Python学习平台...")
    
    # 1. 检查环境
    print("\n=== 检查环境 ===")
    print(f"Python版本: {sys.version}")
    print(f"当前目录: {os.getcwd()}")
    
    # 2. 安装依赖
    if not run_command("pip install -r requirements.txt", "安装Python依赖"):
        return False
    
    # 3. 设置Django环境
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings_production')
    django.setup()
    
    # 4. 数据库迁移
    if not run_command("python manage.py makemigrations", "创建数据库迁移"):
        return False
    
    if not run_command("python manage.py migrate", "应用数据库迁移"):
        return False
    
    # 5. 收集静态文件
    if not run_command("python manage.py collectstatic --noinput", "收集静态文件"):
        return False
    
    # 6. 检查数据
    print("\n=== 检查数据库数据 ===")
    try:
        from Pythonfun.models import Library, Module, OperationType, Function, Parameter
        
        library_count = Library.objects.count()
        module_count = Module.objects.count()
        operation_count = OperationType.objects.count()
        function_count = Function.objects.count()
        parameter_count = Parameter.objects.count()
        
        print(f"✅ 数据库数据检查完成:")
        print(f"   - 库数量: {library_count}")
        print(f"   - 模块数量: {module_count}")
        print(f"   - 操作类型数量: {operation_count}")
        print(f"   - 函数数量: {function_count}")
        print(f"   - 参数数量: {parameter_count}")
        
        if function_count == 0:
            print("⚠️  警告: 没有函数数据，可能需要重新导入Excel数据")
            return False
            
    except Exception as e:
        print(f"❌ 数据检查失败: {e}")
        return False
    
    # 7. 系统检查
    if not run_command("python manage.py check --deploy", "Django系统检查"):
        return False
    
    print("\n🎉 部署完成！")
    print("✅ 所有步骤执行成功")
    print("🌐 可以访问: https://python-learning-platform-omega.vercel.app")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
