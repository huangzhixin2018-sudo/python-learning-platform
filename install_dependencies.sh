#!/bin/bash

echo "📦 安装项目依赖包..."

# 检查Python环境
if ! command -v python &> /dev/null; then
    echo "❌ Python未安装，请先安装Python"
    exit 1
fi

echo "🐍 Python版本: $(python --version)"

# 升级pip
echo "⬆️ 升级pip..."
python -m pip install --upgrade pip

# 安装依赖包
echo "📦 安装依赖包..."
pip install -r requirements-vercel.txt

# 测试安装
echo "🧪 测试依赖包安装..."
python test_dependencies.py

echo "✅ 依赖包安装完成！"
echo "💡 如果测试失败，请手动运行: pip install -r requirements-vercel.txt"
