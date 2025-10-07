# 🚀 GitHub 上传指南

本文档详细说明如何将项目上传到 GitHub。

## 📋 准备工作

### 1. 确保已安装 Git

#### Windows
```cmd
git --version
```
如果未安装，下载：https://git-scm.com/download/win

#### macOS
```bash
git --version
```
如果未安装：`brew install git`

#### Linux
```bash
git --version
```
如果未安装：`sudo apt install git` (Ubuntu/Debian)

### 2. 配置 Git（首次使用）

```bash
# 设置用户名
git config --global user.name "你的GitHub用户名"

# 设置邮箱
git config --global user.email "你的GitHub邮箱"

# 验证配置
git config --list
```

---

## 🌐 创建 GitHub 仓库

### 方法 A：在 GitHub 网站创建（推荐）

1. **登录 GitHub**
   - 访问 https://github.com
   - 登录你的账号

2. **创建新仓库**
   - 点击右上角 "+" > "New repository"
   - 或访问：https://github.com/new

3. **填写仓库信息**
   ```
   Repository name: apple-store-monitor
   Description: 🍎 Apple Store 库存监控工具 - 支持中国大陆和香港地区
   
   Public or Private: [选择公开或私有]
   
   ⚠️ 不要勾选：
   - Add a README file
   - Add .gitignore
   - Choose a license
   
   （因为我们本地已经有这些文件了）
   ```

4. **创建仓库**
   - 点击 "Create repository"
   - 记住仓库 URL：`https://github.com/你的用户名/apple-store-monitor.git`

---

## 📤 上传项目到 GitHub

### 步骤 1：初始化本地仓库

```bash
# 进入项目目录
cd apple-store-monitor

# 初始化 Git 仓库
git init

# 检查状态
git status
```

### 步骤 2：添加文件到暂存区

```bash
# 添加所有文件（.gitignore 会自动排除不需要的文件）
git add .

# 查看将要提交的文件
git status
```

### 步骤 3：提交到本地仓库

```bash
# 提交
git commit -m "Initial commit: Apple Store监控系统 v1.0.0"

# 查看提交历史
git log --oneline
```

### 步骤 4：连接远程仓库

```bash
# 添加远程仓库（替换为你的 GitHub 用户名）
git remote add origin https://github.com/你的用户名/apple-store-monitor.git

# 验证远程仓库
git remote -v
```

### 步骤 5：推送到 GitHub

```bash
# 首次推送（创建 main 分支）
git branch -M main
git push -u origin main
```

如果提示输入用户名和密码：
- **用户名**：你的 GitHub 用户名
- **密码**：使用 Personal Access Token（不是 GitHub 密码）

---

## 🔑 创建 GitHub Personal Access Token

GitHub 已不再支持密码认证，需要使用 Token。

### 步骤：

1. **访问 GitHub 设置**
   - 点击右上角头像 > Settings
   - 或访问：https://github.com/settings/tokens

2. **生成新 Token**
   - 左侧菜单：Developer settings > Personal access tokens > Tokens (classic)
   - 点击 "Generate new token" > "Generate new token (classic)"

3. **配置 Token**
   ```
   Note: apple-store-monitor-upload
   Expiration: 90 days (或自定义)
   
   勾选权限:
   ✅ repo (全选)
   ✅ workflow (如果需要 GitHub Actions)
   ```

4. **生成并保存**
   - 点击 "Generate token"
   - **⚠️ 立即复制 Token**（只显示一次！）
   - 保存到安全的地方

5. **使用 Token**
   
   推送时输入：
   - Username: 你的GitHub用户名
   - Password: 刚才复制的 Token（不是密码）

---

## 🔄 后续更新

### 修改代码后提交更新

```bash
# 1. 查看修改
git status

# 2. 添加修改的文件
git add .

# 3. 提交修改
git commit -m "描述你的修改内容"

# 4. 推送到 GitHub
git push
```

### 常用提交信息示例

```bash
# 新增功能
git commit -m "feat: 添加邮件通知功能"

# 修复 Bug
git commit -m "fix: 修复香港API请求错误"

# 更新文档
git commit -m "docs: 更新README安装说明"

# 性能优化
git commit -m "perf: 优化请求频率控制"

# 代码重构
git commit -m "refactor: 重构配置加载逻辑"
```

---

## 📝 完善 GitHub 仓库

### 1. 添加仓库描述

在 GitHub 仓库页面：
- 点击 "About" 旁边的齿轮图标
- 填写：
  ```
  Description: 🍎 Apple Store 库存监控工具 - 实时监控 iPhone 等产品库存，支持中国大陆和香港地区
  Website: (如果有)
  Topics: apple, iphone, stock-monitor, python, automation
  ```

### 2. 添加 README 徽章

在 `README.md` 顶部已经包含了徽章：

```markdown
[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
```

### 3. 创建 Release

发布第一个版本：

1. 在 GitHub 仓库页面，点击 "Releases"
2. 点击 "Create a new release"
3. 填写信息：
   ```
   Tag version: v1.0.0
   Release title: v1.0.0 - 初始发布
   
   Description:
   ## ✨ 新功能
   - 支持中国大陆和香港地区监控
   - 交互式配置向导
   - 多产品多门店监控
   - 防限流机制
   - 跨平台支持（Windows/macOS/Linux）
   
   ## 📦 安装
   详见 [INSTALL.md](INSTALL.md)
   ```

4. 点击 "Publish release"

---

## 🔒 保护敏感信息

### 确保不上传敏感文件

`.gitignore` 已经配置好，确保以下文件不会上传：

```
config.json          # 个人配置
*.log               # 日志文件
stock_history_*.json # 历史记录
__pycache__/        # Python 缓存
venv/               # 虚拟环境
```

### 检查是否有敏感信息

```bash
# 查看将要提交的文件
git status

# 查看某个文件的内容
git show :文件名

# 如果不小心添加了敏感文件
git rm --cached 文件名
git commit -m "移除敏感文件"
git push
```

---

## 🌟 推广你的项目

### 1. 添加 Star

让朋友给你的项目点 Star：
- 访问仓库页面
- 点击右上角 "Star" 按钮

### 2. 分享到社交媒体

分享链接：
```
https://github.com/你的用户名/apple-store-monitor
```

### 3. 完善文档

- 添加更多使用示例
- 录制演示视频
- 收集用户反馈

---

## ❓ 常见问题

### Q1: 推送时提示权限错误

```bash
# 检查远程仓库 URL
git remote -v

# 如果是 HTTPS，确保使用了正确的 Token
# 如果是 SSH，确保配置了 SSH Key
```

### Q2: 推送太慢

```bash
# 检查仓库大小
du -sh .git

# 如果有大文件，检查 .gitignore
# 移除大文件历史（慎用）
git filter-branch --tree-filter 'rm -f 大文件' HEAD
```

### Q3: 想要更改仓库名

在 GitHub 仓库页面：
1. Settings > Repository name
2. 输入新名称
3. 点击 "Rename"

本地更新：
```bash
git remote set-url origin https://github.com/你的用户名/新仓库名.git
```

### Q4: 如何删除某次提交

```bash
# 撤销最后一次提交（保留修改）
git reset --soft HEAD^

# 撤销最后一次提交（删除修改）
git reset --hard HEAD^

# 强制推送（谨慎使用）
git push -f
```

---

## 📚 Git 常用命令速查

```bash
# 查看状态
git status

# 查看历史
git log --oneline --graph

# 查看差异
git diff

# 撤销修改
git checkout -- 文件名

# 创建分支
git branch 分支名
git checkout 分支名

# 合并分支
git checkout main
git merge 分支名

# 拉取更新
git pull

# 克隆仓库
git clone 仓库URL
```

---

## ✅ 完成检查清单

上传前确认：

- [ ] `.gitignore` 文件已创建
- [ ] `README.md` 已完善
- [ ] `LICENSE` 文件已添加
- [ ] `requirements.txt` 已更新
- [ ] 敏感信息已删除
- [ ] 代码已测试通过
- [ ] 文档已更新
- [ ] GitHub 仓库已创建
- [ ] 首次提交已完成
- [ ] 推送到 GitHub 成功

---

## 🎉 完成！

恭喜！你的项目已经成功上传到 GitHub。

**仓库地址**：
```
https://github.com/你的用户名/apple-store-monitor
```

**下一步**：
- 完善项目文档
- 添加更多功能
- 收集用户反馈
- 持续维护更新

---

**问题反馈**：
- GitHub Issues: https://github.com/你的用户名/apple-store-monitor/issues
- Email: your.email@example.com




