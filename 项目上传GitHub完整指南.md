# 🚀 Apple Store 监控系统 - GitHub 上传完整指南

本文档详细说明如何将此项目上传到 GitHub，适用于所有操作系统。

## 📋 目录

1. [准备工作检查](#准备工作检查)
2. [文件说明](#文件说明)
3. [上传步骤](#上传步骤)
4. [验证上传](#验证上传)
5. [后续维护](#后续维护)

---

## ✅ 准备工作检查

### 已完成的准备工作

- [x] **`.gitignore`** - 配置完成，敏感文件已排除
- [x] **`README.md`** - 项目主文档，支持跨平台
- [x] **`LICENSE`** - MIT 开源协议
- [x] **`INSTALL.md`** - 详细安装指南
- [x] **`GITHUB_SETUP.md`** - GitHub 上传指南
- [x] **`CONTRIBUTING.md`** - 贡献者指南
- [x] **`QUICKSTART.md`** - 快速开始指南
- [x] **`requirements.txt`** - 依赖列表完整
- [x] **自动化脚本** - `setup_git.sh` 和 `setup_git.bat`

### 系统要求

| 项目 | Windows | macOS | Linux |
|------|---------|-------|-------|
| Git | ✅ 必需 | ✅ 必需 | ✅ 必需 |
| Python 3.7+ | ✅ 必需 | ✅ 必需 | ✅ 必需 |
| GitHub 账号 | ✅ 必需 | ✅ 必需 | ✅ 必需 |

---

## 📁 文件说明

### 会上传到 GitHub 的文件

#### 核心代码（21 个文件）

```
✅ start.py                           - 统一启动入口
✅ start_cn.py                        - 大陆快速启动
✅ start_hk.py                        - 香港快速启动
✅ main.py                            - 主程序
✅ apple_store_monitor_enhanced.py   - 核心监控逻辑
✅ interactive_config.py             - 大陆交互式配置
✅ interactive_config_hk.py          - 香港交互式配置
✅ logger_config.py                  - 日志配置
✅ notifier.py                       - 通知模块
✅ auto_get_part_numbers.py          - 自动获取产品型号
✅ get_iphone17_models_hk.py         - 获取香港型号
✅ scan_valid_stores.py              - 扫描有效门店
✅ select_models.py                  - 选择型号工具
✅ setup_monitor.py                  - 监控设置工具
✅ rate_calculator.py                - 频率计算器
```

#### 数据文件（5 个文件）

```
✅ apple_stores_china.json           - 大陆门店数据（48家）
✅ apple_stores_hongkong.json        - 香港门店数据（6家）
✅ iphone17_all_models.json          - iPhone 17 全型号（大陆）
✅ iphone17_promax_hongkong_complete.json - iPhone 17 Pro Max（香港）
✅ iphone16_hongkong.json            - iPhone 16 测试型号（香港）
```

#### 配置示例（6 个文件）

```
✅ config.example.json               - 基础配置示例
✅ config_safe.json                  - 安全配置示例
✅ config_hongkong_example.json      - 香港配置示例
✅ config_hongkong_promax_all.json   - 香港全产品配置
✅ config_hongkong_promax_priority.json - 香港优先配置
✅ config_shenzhen_nearby.json       - 深圳周边配置
```

#### 文档文件（8 个文件）

```
✅ README.md                         - 项目主文档 ⭐
✅ LICENSE                           - MIT 开源协议
✅ INSTALL.md                        - 安装指南
✅ QUICKSTART.md                     - 快速开始
✅ GITHUB_SETUP.md                   - GitHub 上传指南
✅ CONTRIBUTING.md                   - 贡献指南
✅ requirements.txt                  - Python 依赖
✅ .gitignore                        - Git 忽略规则
```

#### 自动化脚本（3 个文件）

```
✅ setup_git.sh                      - macOS/Linux Git 初始化
✅ setup_git.bat                     - Windows Git 初始化
✅ start.sh                          - 快速启动脚本
```

**总计：约 43 个核心文件**

### 不会上传的文件（已在 .gitignore 中配置）

```
❌ config.json                       - 用户个人配置
❌ *.log                             - 所有日志文件
❌ monitor.log                       - 监控日志
❌ stock_history_*.json              - 所有历史记录
❌ __pycache__/                      - Python 缓存
❌ venv/                             - 虚拟环境
❌ *.xlsx                            - Excel 文件
❌ *.backup                          - 备份文件
❌ temp_*.txt                        - 临时文件
❌ test_*.py                         - 测试文件（开发用）
```

### 开发文档（可选择性上传）

以下文档是开发过程记录，可以选择：
- 全部上传（完整记录）
- 移到 `docs/` 目录上传（整理后）
- 不上传（仅保留本地）

```
📄 开发记录文档（约 30+ 个）：
   - 香港API修复完成报告.md
   - 随机打散策略实施完成.md
   - 跨系列选择和iPhone16集成完成报告.md
   - 输入缓冲问题修复说明.md
   - 等等...
```

**建议**：这些开发文档可以移到单独的 `dev-docs/` 目录，然后在 `.gitignore` 中添加：
```
# 开发文档（可选）
# dev-docs/
```

---

## 🚀 上传步骤

### 方式一：一键自动上传（推荐）⭐

#### Windows 用户

```cmd
# 双击运行或在命令提示符中执行
setup_git.bat
```

#### macOS / Linux 用户

```bash
# 在终端中执行
./setup_git.sh
```

脚本会自动完成：
1. ✅ 检查 Git 安装
2. ✅ 配置 Git 用户信息
3. ✅ 初始化本地仓库
4. ✅ 添加文件到暂存区
5. ✅ 创建首次提交
6. ✅ 连接远程仓库
7. ✅ 推送到 GitHub

### 方式二：手动上传

#### 步骤 1：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 填写信息：
   ```
   Repository name: apple-store-monitor
   Description: 🍎 Apple Store 库存监控工具 - 支持中国大陆和香港地区
   Public 或 Private: [自选]
   
   ⚠️ 不要勾选：
   [ ] Add a README file
   [ ] Add .gitignore
   [ ] Choose a license
   ```
3. 点击 "Create repository"
4. 复制仓库 URL

#### 步骤 2：本地 Git 操作

**Windows (CMD/PowerShell)**:
```cmd
cd 项目目录

REM 初始化仓库
git init

REM 添加文件
git add .

REM 提交
git commit -m "Initial commit: Apple Store库存监控系统 v1.0.0"

REM 连接远程仓库（替换为你的 URL）
git remote add origin https://github.com/你的用户名/apple-store-monitor.git

REM 设置主分支
git branch -M main

REM 推送到 GitHub
git push -u origin main
```

**macOS / Linux (Terminal)**:
```bash
cd 项目目录

# 初始化仓库
git init

# 添加文件
git add .

# 提交
git commit -m "Initial commit: Apple Store库存监控系统 v1.0.0"

# 连接远程仓库（替换为你的 URL）
git remote add origin https://github.com/你的用户名/apple-store-monitor.git

# 设置主分支
git branch -M main

# 推送到 GitHub
git push -u origin main
```

#### 步骤 3：认证

推送时会要求输入：
- **Username**: 你的 GitHub 用户名
- **Password**: **Personal Access Token**（不是 GitHub 密码！）

**获取 Token**：
1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token" > "Generate new token (classic)"
3. Note: `apple-store-monitor-upload`
4. Expiration: `90 days`
5. 勾选：`repo` (全部)
6. 点击 "Generate token"
7. **立即复制 Token**（只显示一次）

### 方式三：GitHub Desktop（图形化）

1. **下载安装**
   - Windows/macOS: https://desktop.github.com
   - 登录 GitHub 账号

2. **添加项目**
   - File > Add Local Repository
   - 选择项目文件夹
   - 或：Create New Repository

3. **发布到 GitHub**
   - 点击 "Publish repository"
   - 填写仓库名和描述
   - 选择 Public/Private
   - 点击 "Publish"

完成！

---

## ✅ 验证上传

### 1. 检查 GitHub 仓库

访问：`https://github.com/你的用户名/apple-store-monitor`

应该看到：
- ✅ README.md 正确显示
- ✅ 所有源代码文件
- ✅ 文件数量约 43 个
- ✅ 没有敏感文件（config.json、*.log）

### 2. 检查文件数量

```bash
# 本地检查将要上传的文件
git ls-files | wc -l

# 应该显示约 40-50 个文件
```

### 3. 检查忽略规则

```bash
# 查看被忽略的文件
git status --ignored

# 确认 config.json、*.log 等在忽略列表中
```

### 4. 克隆测试（可选）

```bash
# 克隆到新目录测试
cd /tmp
git clone https://github.com/你的用户名/apple-store-monitor.git test-clone
cd test-clone

# 安装依赖
pip install -r requirements.txt

# 测试运行
python3 start.py

# 应该能正常启动
```

---

## 🔄 后续维护

### 日常更新流程

```bash
# 1. 修改代码
# ...

# 2. 查看修改
git status
git diff

# 3. 添加修改
git add .

# 4. 提交
git commit -m "feat: 添加新功能"

# 5. 推送
git push
```

### 提交信息规范

```bash
# 新功能
git commit -m "feat: 添加邮件通知功能"

# Bug 修复
git commit -m "fix: 修复香港API请求错误"

# 文档更新
git commit -m "docs: 更新README安装说明"

# 性能优化
git commit -m "perf: 优化请求频率控制"

# 代码重构
git commit -m "refactor: 重构配置加载逻辑"
```

### 拉取最新代码

```bash
# 获取并合并最新代码
git pull origin main

# 或分步操作
git fetch origin
git merge origin/main
```

### 创建 Release

1. 在 GitHub 仓库页面点击 "Releases"
2. 点击 "Create a new release"
3. 填写：
   - Tag: `v1.0.0`
   - Title: `v1.0.0 - 初始发布`
   - Description: 列出主要功能
4. 点击 "Publish release"

---

## 📊 项目统计

### 代码统计

```bash
# 统计代码行数
find . -name "*.py" | xargs wc -l

# 统计文件数量
find . -type f -name "*.py" | wc -l
```

### 仓库大小

预计上传大小：
- **源代码**: ~500 KB
- **数据文件**: ~50 KB
- **文档**: ~200 KB
- **总计**: < 1 MB

非常轻量，适合快速克隆！

---

## ❓ 常见问题

### Q1: 推送失败，提示 403 错误

**原因**: Token 权限不足或已过期

**解决**:
1. 重新生成 Token
2. 确保勾选了 `repo` 权限
3. 更新本地凭证

### Q2: 文件太大无法上传

**检查**:
```bash
# 查找大文件（>10MB）
find . -type f -size +10M

# 如果有，添加到 .gitignore
echo "大文件名" >> .gitignore
```

### Q3: 想要重新上传

```bash
# 删除 .git 目录
rm -rf .git

# 重新初始化
git init
git add .
git commit -m "Initial commit"
git remote add origin <URL>
git push -u origin main -f
```

### Q4: 不小心上传了敏感文件

```bash
# 从历史中删除
git rm --cached 敏感文件
git commit -m "移除敏感文件"
git push

# 如果已在历史中，需要清理历史
git filter-branch --index-filter 'git rm --cached --ignore-unmatch 敏感文件' HEAD
git push -f
```

---

## 🎯 检查清单

上传前最后检查：

- [ ] `.gitignore` 已配置
- [ ] `README.md` 已完善
- [ ] `requirements.txt` 已更新
- [ ] `config.json` 不在上传列表
- [ ] 历史记录 `*.json` 不在上传列表
- [ ] 日志文件 `*.log` 不在上传列表
- [ ] 所有源代码已包含
- [ ] 数据文件已包含
- [ ] 配置示例已包含
- [ ] 文档完整
- [ ] LICENSE 已添加
- [ ] GitHub 仓库已创建
- [ ] 本地测试通过

---

## 🎉 完成

恭喜！你的项目已成功上传到 GitHub！

**下一步**:

1. ⭐ **完善仓库**
   - 添加 About 描述
   - 添加 Topics 标签
   - 设置仓库主页

2. 📢 **推广项目**
   - 分享到社交媒体
   - 邀请朋友 Star
   - 收集用户反馈

3. 🔄 **持续维护**
   - 修复 Bug
   - 添加新功能
   - 更新文档

---

**仓库链接**: `https://github.com/你的用户名/apple-store-monitor`

**祝你的项目获得更多 Star！** ⭐✨


