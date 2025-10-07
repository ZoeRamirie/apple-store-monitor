@echo off
chcp 65001 >nul
REM Apple Store Monitor - Git 初始化和 GitHub 上传脚本
REM 适用于 Windows

echo ╔═══════════════════════════════════════════════════════════════════╗
echo ║                                                                   ║
echo ║         🚀 Git 初始化和 GitHub 上传助手                           ║
echo ║                                                                   ║
echo ╚═══════════════════════════════════════════════════════════════════╝
echo.

REM 检查是否已安装 Git
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ 错误: 未检测到 Git
    echo.
    echo 请先安装 Git:
    echo   访问: https://git-scm.com/download/win
    pause
    exit /b 1
)

git --version
echo.

REM 检查 Git 配置
git config user.name >nul 2>nul
if %errorlevel% neq 0 (
    echo 📝 Git 用户配置
    echo.
    set /p username="请输入你的 GitHub 用户名: "
    git config --global user.name "%username%"
    echo ✅ 用户名已设置: %username%
    echo.
)

git config user.email >nul 2>nul
if %errorlevel% neq 0 (
    set /p email="请输入你的 GitHub 邮箱: "
    git config --global user.email "%email%"
    echo ✅ 邮箱已设置: %email%
    echo.
)

REM 显示当前配置
echo 📋 当前 Git 配置:
for /f "delims=" %%i in ('git config user.name') do echo   用户名: %%i
for /f "delims=" %%i in ('git config user.email') do echo   邮箱: %%i
echo.

REM 检查是否已初始化
if exist .git (
    echo ⚠️  检测到已初始化的 Git 仓库
    set /p reinit="是否重新初始化? (y/N): "
    if /i "%reinit%"=="y" (
        rmdir /s /q .git
        echo ✅ 已清除旧仓库
    ) else (
        echo ℹ️  保持现有仓库
    )
)

REM 初始化 Git 仓库
if not exist .git (
    echo.
    echo 🔧 初始化 Git 仓库...
    git init
    echo ✅ Git 仓库初始化完成
)

echo.
echo 📦 添加文件到暂存区...
git add .

echo.
echo 💾 提交到本地仓库...
git commit -m "Initial commit: Apple Store库存监控系统 v1.0.0" -m "✨ 功能特性:" -m "- 支持中国大陆和香港地区" -m "- 交互式配置向导" -m "- 多产品多门店监控" -m "- 防限流机制" -m "- 跨平台支持 (Windows/macOS/Linux)" -m "- 桌面通知和声音提醒" -m "" -m "📚 文档:" -m "- README.md - 项目说明" -m "- INSTALL.md - 安装指南" -m "- GITHUB_SETUP.md - GitHub上传指南" -m "" -m "🛡️ 安全:" -m "- .gitignore 已配置" -m "- 敏感信息已排除"

echo.
echo ✅ 本地提交完成
echo.

REM GitHub 仓库信息
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 📌 下一步: 创建 GitHub 仓库并上传
echo.
echo 1️⃣  在 GitHub 创建新仓库:
echo    - 访问: https://github.com/new
echo    - Repository name: apple-store-monitor
echo    - Description: 🍎 Apple Store 库存监控工具
echo    - Public 或 Private (自选)
echo    - ⚠️  不要添加 README, .gitignore, LICENSE
echo.
echo 2️⃣  创建完成后，获取仓库 URL
echo.

set /p repo_url="请输入 GitHub 仓库 URL (例: https://github.com/username/apple-store-monitor.git): "

if "%repo_url%"=="" (
    echo.
    echo ⚠️  未输入仓库 URL，跳过远程推送
    echo.
    echo 你可以稍后手动执行:
    echo   git remote add origin ^<仓库URL^>
    echo   git branch -M main
    echo   git push -u origin main
    pause
    exit /b 0
)

echo.
echo 🔗 添加远程仓库...
git remote remove origin 2>nul
git remote add origin "%repo_url%"
echo ✅ 远程仓库已添加: %repo_url%

echo.
echo 🌿 设置主分支为 main...
git branch -M main

echo.
echo 📤 推送到 GitHub...
echo.
echo ⚠️  注意:
echo   - Username: 输入你的 GitHub 用户名
echo   - Password: 输入 Personal Access Token (不是密码!)
echo.
echo   如何获取 Token:
echo   1. 访问: https://github.com/settings/tokens
echo   2. Generate new token (classic)
echo   3. 勾选 'repo' 权限
echo   4. 生成并复制 Token
echo.

git push -u origin main
if %errorlevel% equ 0 (
    echo.
    echo ╔═══════════════════════════════════════════════════════════════════╗
    echo ║                                                                   ║
    echo ║         ✅ 成功上传到 GitHub！                                    ║
    echo ║                                                                   ║
    echo ╚═══════════════════════════════════════════════════════════════════╝
    echo.
    echo 🎉 项目已成功上传到 GitHub
    echo.
    echo 📍 仓库地址: %repo_url%
    echo.
    echo 🌟 下一步:
    echo   1. 访问你的 GitHub 仓库
    echo   2. 添加仓库描述和主题标签
    echo   3. 邀请朋友 Star ⭐
    echo   4. 分享给更多人使用
    echo.
) else (
    echo.
    echo ❌ 推送失败
    echo.
    echo 常见问题:
    echo   1. 检查仓库 URL 是否正确
    echo   2. 确保使用了 Personal Access Token
    echo   3. 检查网络连接
    echo.
    echo 详细帮助请查看: GITHUB_SETUP.md
    pause
    exit /b 1
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 📚 更多信息:
echo   - 查看 README.md 了解项目详情
echo   - 查看 INSTALL.md 了解安装步骤
echo   - 查看 GITHUB_SETUP.md 了解更多 Git/GitHub 操作
echo.
pause




