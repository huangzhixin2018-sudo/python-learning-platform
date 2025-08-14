#!/usr/bin/env python
"""
推送到GitHub仓库
"""
import os
import subprocess
import sys

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"✅ {description}成功")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ {description}失败")
            if result.stderr:
                print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ {description}出错: {e}")
        return False

def main():
    """主函数"""
    print("🚀 推送到GitHub仓库")
    print("=" * 50)
    
    # 检查Git状态
    if not run_command("git status", "检查Git状态"):
        return False
    
    # 检查是否有未提交的更改
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print("⚠️  发现未提交的更改，正在提交...")
        if not run_command("git add .", "添加所有文件"):
            return False
        if not run_command('git commit -m "🚀 更新项目配置"', "提交更改"):
            return False
    
    # 获取用户输入的GitHub仓库URL
    print("\n📝 请输入GitHub仓库URL:")
    print("格式: https://github.com/用户名/仓库名.git")
    print("例如: https://github.com/yourusername/python-learning-platform.git")
    
    repo_url = input("GitHub仓库URL: ").strip()
    
    if not repo_url:
        print("❌ 请输入有效的GitHub仓库URL")
        return False
    
    # 添加远程仓库
    if not run_command(f"git remote add origin {repo_url}", "添加远程仓库"):
        # 如果远程仓库已存在，更新它
        if not run_command(f"git remote set-url origin {repo_url}", "更新远程仓库"):
            return False
    
    # 强制推送到GitHub
    print("\n🚀 正在推送到GitHub...")
    if not run_command("git push -u origin main --force", "强制推送到GitHub"):
        return False
    
    print("\n🎉 代码推送成功！")
    print(f"🌐 仓库地址: {repo_url.replace('.git', '')}")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n💡 手动推送步骤:")
        print("1. 在GitHub上创建新仓库")
        print("2. 运行: git remote add origin https://github.com/用户名/仓库名.git")
        print("3. 运行: git push -u origin main --force")
