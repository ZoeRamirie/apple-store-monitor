
# 🚀 GitHub 上传速查卡

## ⚡ 最快上传方法

### Windows
```cmd
setup_git.bat
```

### macOS / Linux
```bash
./setup_git.sh
```

按照提示操作即可！

---

## 📋 手动上传步骤

### 1️⃣ 创建 GitHub 仓库
→ https://github.com/new
→ 名称: `apple-store-monitor`

### 2️⃣ 本地操作

**Windows**:
```cmd
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/你的用户名/apple-store-monitor.git
git branch -M main
git push -u origin main
```

**macOS/Linux**:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/你的用户名/apple-store-monitor.git
git branch -M main
git push -u origin main
```

### 3️⃣ 输入凭证
- Username: GitHub用户名
- Password: Personal Access Token

---

## 🔑 获取 Token

1. https://github.com/settings/tokens
2. Generate new token (classic)
3. 勾选 `repo`
4. 生成并复制

---

## ✅ 验证上传

```bash
# 检查文件数量
git ls-files | wc -l

# 应该约 40-50 个文件
```

---

## 📊 上传内容

### ✅ 会上传
- 所有 `.py` 源代码
- 所有 `.json` 数据文件
- 配置示例 `config.example.json`
- 所有文档 `.md`
- `requirements.txt`

### ❌ 不上传
- `config.json` (个人配置)
- `*.log` (日志)
- `stock_history_*.json` (历史)
- `__pycache__/` (缓存)
- `venv/` (虚拟环境)

---

## 🔄 日常更新

```bash
git add .
git commit -m "更新说明"
git push
```

---

## 📚 详细文档

- 完整指南: `项目上传GitHub完整指南.md`
- GitHub教程: `GITHUB_SETUP.md`
- 安装说明: `INSTALL.md`

---

**仓库**: `https://github.com/你的用户名/apple-store-monitor`

