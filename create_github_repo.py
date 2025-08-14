#!/usr/bin/env python
"""
创建GitHub仓库并推送代码
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
    print("🚀 创建GitHub仓库并推送代码")
    print("=" * 50)
    
    # 仓库名称
    repo_name = "python-learning-platform"
    repo_description = "思维空间 - Python学习网站，提供教程管理、分类管理和文章编辑功能"
    
    print(f"📝 仓库名称: {repo_name}")
    print(f"📝 仓库描述: {repo_description}")
    print()
    
    # 检查是否安装了GitHub CLI
    if not run_command("gh --version", "检查GitHub CLI"):
        print("❌ 请先安装GitHub CLI: https://cli.github.com/")
        print("或者手动在GitHub上创建仓库")
        return False
    
    # 检查是否已登录GitHub
    if not run_command("gh auth status", "检查GitHub登录状态"):
        print("❌ 请先登录GitHub: gh auth login")
        return False
    
    # 创建GitHub仓库
    create_cmd = f'gh repo create {repo_name} --description "{repo_description}" --public --source=. --remote=origin --push'
    if not run_command(create_cmd, "创建GitHub仓库"):
        print("❌ 创建仓库失败，请手动创建")
        return False
    
    print("\n🎉 GitHub仓库创建成功！")
    print(f"🌐 仓库地址: https://github.com/$(gh api user --jq .login)/{repo_name}")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n💡 手动创建步骤:")
        print("1. 访问 https://github.com/new")
        print("2. 仓库名称: python-learning-platform")
        print("3. 描述: 思维空间 - Python学习网站")
        print("4. 选择Public")
        print("5. 不要初始化README、.gitignore或license")
        print("6. 创建仓库后，运行以下命令:")
        print("   git remote add origin https://github.com/用户名/python-learning-platform.git")
        print("   git push -u origin main")
