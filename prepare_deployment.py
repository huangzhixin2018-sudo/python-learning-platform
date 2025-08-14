#!/usr/bin/env python3
"""
部署准备脚本 - 检查所有必要的组件并生成部署报告
"""
import os
import sys
import subprocess
import platform
from pathlib import Path
from datetime import datetime

def check_python_dependencies():
    """检查Python依赖"""
    print("=== Python依赖检查 ===")
    
    # 包名到导入名的映射
    package_mapping = {
        'django': 'django',
        'psycopg2': 'psycopg2',
        'dj-database-url': 'dj_database_url',
        'python-decouple': 'decouple'
    }
    
    missing_packages = []
    for package, import_name in package_mapping.items():
        try:
            __import__(import_name)
            print(f"[OK] {package}")
        except ImportError:
            print(f"[ERROR] {package} - 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n[WARNING] 缺少依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install " + " ".join(missing_packages))
        return False
    
    return True

def check_environment_variables():
    """检查环境变量"""
    print("\n=== 环境变量检查 ===")
    
    required_vars = ['DATABASE_URL']
    optional_vars = ['SECRET_KEY', 'DEBUG', 'ALLOWED_HOSTS']
    
    all_good = True
    
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            print(f"[OK] {var} - 已设置")
            if var == 'DATABASE_URL':
                # 隐藏密码显示
                safe_value = value.replace('huangzhixin2025', '***')
                print(f"    值: {safe_value}")
        else:
            print(f"[ERROR] {var} - 未设置")
            all_good = False
    
    for var in optional_vars:
        value = os.environ.get(var)
        if value:
            print(f"[OK] {var} - 已设置")
        else:
            print(f"[WARNING] {var} - 未设置（可选）")
    
    return all_good

def check_django_configuration():
    """检查Django配置"""
    print("\n=== Django配置检查 ===")
    
    try:
        BASE_DIR = Path(__file__).resolve().parent
        sys.path.append(str(BASE_DIR))
        
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
        
        import django
        django.setup()
        
        from django.conf import settings
        
        print("[OK] Django环境设置成功")
        print(f"    项目名称: {settings.SETTINGS_MODULE}")
        print(f"    调试模式: {settings.DEBUG}")
        print(f"    允许主机: {settings.ALLOWED_HOSTS}")
        
        # 检查数据库配置
        db_config = settings.DATABASES['default']
        print(f"    数据库引擎: {db_config.get('ENGINE', 'N/A')}")
        print(f"    数据库主机: {db_config.get('HOST', 'N/A')}")
        print(f"    数据库端口: {db_config.get('PORT', 'N/A')}")
        print(f"    数据库名称: {db_config.get('NAME', 'N/A')}")
        print(f"    数据库用户: {db_config.get('USER', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Django配置检查失败: {e}")
        return False

def check_static_files():
    """检查静态文件"""
    print("\n=== 静态文件检查 ===")
    
    static_dir = Path("static")
    staticfiles_dir = Path("staticfiles")
    templates_dir = Path("templates")
    
    if static_dir.exists():
        print(f"[OK] static/ 目录存在")
    else:
        print(f"[ERROR] static/ 目录不存在")
    
    if staticfiles_dir.exists():
        print(f"[OK] staticfiles/ 目录存在")
    else:
        print(f"[WARNING] staticfiles/ 目录不存在（部署时会创建）")
    
    if templates_dir.exists():
        print(f"[OK] templates/ 目录存在")
        # 检查关键模板
        key_templates = [
            "admin/登录.html",
            "admin/分类管理.html", 
            "admin/教程管理.html",
            "front/index.html"
        ]
        for template in key_templates:
            if (templates_dir / template).exists():
                print(f"    [OK] {template}")
            else:
                print(f"    [ERROR] {template}")
    else:
        print(f"[ERROR] templates/ 目录不存在")
    
    return True

def check_vercel_configuration():
    """检查Vercel配置"""
    print("\n=== Vercel配置检查 ===")
    
    vercel_json = Path("vercel.json")
    vercel_env = Path("vercel.env")
    
    if vercel_json.exists():
        print("[OK] vercel.json 存在")
    else:
        print("[ERROR] vercel.json 不存在")
    
    if vercel_env.exists():
        print("[OK] vercel.env 存在")
    else:
        print("[ERROR] vercel.env 不存在")
    
    # 检查requirements文件
    requirements_files = ["requirements.txt", "requirements-vercel.txt"]
    for req_file in requirements_files:
        if Path(req_file).exists():
            print(f"[OK] {req_file} 存在")
        else:
            print(f"[ERROR] {req_file} 不存在")
    
    return True

def check_database_migration():
    """检查数据库迁移状态"""
    print("\n=== 数据库迁移检查 ===")
    
    try:
        BASE_DIR = Path(__file__).resolve().parent
        
        # 检查迁移状态
        result = subprocess.run([
            sys.executable, 'manage.py', 'showmigrations'
        ], capture_output=True, text=True, cwd=BASE_DIR)
        
        if result.returncode == 0:
            print("[OK] 迁移检查成功")
            print("    迁移状态:")
            for line in result.stdout.split('\n'):
                if line.strip() and ('[X]' in line or '[ ]' in line):
                    print(f"    {line}")
        else:
            print(f"[ERROR] 迁移检查失败: {result.stderr}")
            return False
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 数据库迁移检查失败: {e}")
        return False

def run_django_health_check():
    """运行Django健康检查"""
    print("\n=== Django健康检查 ===")
    
    try:
        result = subprocess.run([
            sys.executable, 'manage.py', 'check', '--deploy'
        ], capture_output=True, text=True, cwd=Path(__file__).resolve().parent)
        
        if result.returncode == 0:
            print("[OK] Django健康检查通过")
            print("    部署检查结果:")
            for line in result.stdout.split('\n'):
                if line.strip() and not line.startswith('System check'):
                    print(f"    {line}")
        else:
            print(f"[ERROR] Django健康检查失败: {result.stderr}")
            return False
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Django健康检查异常: {e}")
        return False

def generate_deployment_report(results):
    """生成部署报告"""
    print("\n" + "=" * 60)
    print("部署准备报告")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    print(f"检查项目: {total}")
    print(f"通过项目: {passed}")
    print(f"失败项目: {total - passed}")
    print(f"成功率: {(passed/total)*100:.1f}%")
    
    print("\n详细结果:")
    for check_name, result in results.items():
        status = "[OK] 通过" if result else "[ERROR] 失败"
        print(f"  {check_name}: {status}")
    
    if passed == total:
        print("\n[SUCCESS] 所有检查通过！系统准备就绪，可以部署上线！")
        print("\n部署步骤:")
        print("1. 确保Vercel环境变量已正确设置")
        print("2. 运行 'vercel --prod' 进行生产部署")
        print("3. 部署后验证网站功能")
        return True
    else:
        print(f"\n[WARNING] 有 {total - passed} 项检查失败，请修复后重试。")
        print("\n修复建议:")
        if not results.get("环境变量", True):
            print("- 检查环境变量设置")
        if not results.get("Django配置", True):
            print("- 检查Django配置文件")
        if not results.get("数据库迁移", True):
            print("- 运行数据库迁移")
        if not results.get("Python依赖", True):
            print("- 安装缺少的Python包")
        return False

def main():
    """主检查函数"""
    print("开始部署前检查...")
    print("=" * 60)
    
    # 显示系统信息
    print(f"系统信息: {platform.system()} {platform.release()}")
    print(f"Python版本: {platform.python_version()}")
    print(f"工作目录: {os.getcwd()}")
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 执行各项检查
    checks = [
        ("Python依赖", check_python_dependencies),
        ("环境变量", check_environment_variables),
        ("Django配置", check_django_configuration),
        ("静态文件", check_static_files),
        ("Vercel配置", check_vercel_configuration),
        ("数据库迁移", check_database_migration),
        ("Django健康检查", run_django_health_check),
    ]
    
    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"[ERROR] {check_name} 检查异常: {e}")
            results[check_name] = False
    
    # 生成部署报告
    deployment_ready = generate_deployment_report(results)
    
    # 保存报告到文件
    report_file = "deployment_report.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"部署准备报告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n")
        f.write(f"系统信息: {platform.system()} {platform.release()}\n")
        f.write(f"Python版本: {platform.python_version()}\n")
        f.write(f"工作目录: {os.getcwd()}\n\n")
        
        for check_name, result in results.items():
            status = "通过" if result else "失败"
            f.write(f"{check_name}: {status}\n")
        
        f.write(f"\n总计: {sum(1 for r in results.values() if r)}/{len(results)} 项检查通过\n")
        
        if deployment_ready:
            f.write("\n[SUCCESS] 系统准备就绪，可以部署上线！\n")
        else:
            f.write("\n[WARNING] 部分检查失败，请修复后重试。\n")
    
    print(f"\n部署报告已保存到: {report_file}")
    
    return deployment_ready

if __name__ == "__main__":
    main()
