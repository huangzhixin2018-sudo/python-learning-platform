# PowerShell部署脚本
Write-Host "🚀 开始部署到Vercel..." -ForegroundColor Green

# 检查是否安装了Vercel CLI
try {
    vercel --version | Out-Null
    Write-Host "✅ Vercel CLI已安装" -ForegroundColor Green
} catch {
    Write-Host "❌ Vercel CLI未安装，正在安装..." -ForegroundColor Yellow
    npm install -g vercel
}

# 检查是否已登录Vercel
try {
    vercel whoami | Out-Null
    Write-Host "✅ 已登录Vercel" -ForegroundColor Green
} catch {
    Write-Host "🔐 请先登录Vercel账户..." -ForegroundColor Yellow
    vercel login
}

# 检查Python环境
Write-Host "🐍 检查Python环境..." -ForegroundColor Cyan
python --version

# 安装依赖包
Write-Host "📦 安装依赖包..." -ForegroundColor Cyan
pip install -r requirements-vercel.txt

# 检查Django项目
Write-Host "🔍 检查Django项目..." -ForegroundColor Cyan
python manage.py check

# 收集静态文件
Write-Host "📁 收集静态文件..." -ForegroundColor Cyan
python manage.py collectstatic --noinput

# 部署项目
Write-Host "📦 正在部署项目..." -ForegroundColor Cyan
vercel --prod

Write-Host "✅ 部署完成！" -ForegroundColor Green
Write-Host "🌐 您的应用已部署到Vercel" -ForegroundColor Green
Write-Host "📝 如果遇到问题，请检查Vercel Dashboard的部署日志" -ForegroundColor Yellow

