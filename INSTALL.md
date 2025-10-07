# 📦 安装指南

本文档提供详细的安装步骤，适用于不同操作系统。

## 📋 目录

- [Windows 安装](#windows-安装)
- [macOS 安装](#macos-安装)
- [Linux 安装](#linux-安装)
- [验证安装](#验证安装)
- [常见问题](#常见问题)

---

## 🪟 Windows 安装

### 步骤 1: 安装 Python

1. **下载 Python**
   - 访问 [Python 官网](https://www.python.org/downloads/)
   - 下载 Python 3.9 或更高版本
   - 推荐下载：Python 3.10.x (稳定版)

2. **安装 Python**
   - 运行下载的安装程序
   - ⚠️ **重要**：勾选 **"Add Python to PATH"**
   - 点击 "Install Now"
   - 等待安装完成

3. **验证 Python 安装**
   
   打开命令提示符（CMD）：
   ```cmd
   python --version
   ```
   
   应该显示：`Python 3.x.x`

### 步骤 2: 安装 Git（可选，用于克隆项目）

1. 下载 [Git for Windows](https://git-scm.com/download/win)
2. 运行安装程序，使用默认设置
3. 验证安装：
   ```cmd
   git --version
   ```

### 步骤 3: 获取项目

#### 方法 A：使用 Git（推荐）

```cmd
git clone https://github.com/你的用户名/apple-store-monitor.git
cd apple-store-monitor
```

#### 方法 B：下载 ZIP

1. 访问项目 GitHub 页面
2. 点击 "Code" > "Download ZIP"
3. 解压到目标文件夹
4. 打开命令提示符，进入项目文件夹

### 步骤 4: 创建虚拟环境

```cmd
python -m venv venv
venv\Scripts\activate
```

激活成功后，命令提示符前会显示 `(venv)`

### 步骤 5: 安装依赖

```cmd
pip install -r requirements.txt
```

### 步骤 6: 运行程序

```cmd
python start.py
```

---

## 🍎 macOS 安装

### 步骤 1: 安装 Homebrew（如果还没安装）

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 步骤 2: 安装 Python

```bash
# 安装 Python 3
brew install python3

# 验证安装
python3 --version
```

### 步骤 3: 安装 Git

```bash
# Git 通常已预装，如果没有：
brew install git

# 验证
git --version
```

### 步骤 4: 获取项目

```bash
# 克隆项目
git clone https://github.com/你的用户名/apple-store-monitor.git
cd apple-store-monitor
```

### 步骤 5: 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate
```

### 步骤 6: 安装依赖

```bash
pip install -r requirements.txt
```

### 步骤 7: 运行程序

```bash
python3 start.py
```

---

## 🐧 Linux 安装

### Ubuntu / Debian

#### 步骤 1: 更新系统

```bash
sudo apt update
sudo apt upgrade -y
```

#### 步骤 2: 安装 Python 和工具

```bash
# 安装 Python 3 和 pip
sudo apt install python3 python3-pip python3-venv git -y

# 验证安装
python3 --version
pip3 --version
```

#### 步骤 3: 安装通知支持（可选）

```bash
# 桌面通知支持
sudo apt install libnotify-bin -y
```

#### 步骤 4: 获取项目

```bash
git clone https://github.com/你的用户名/apple-store-monitor.git
cd apple-store-monitor
```

#### 步骤 5: 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 步骤 6: 安装依赖

```bash
pip install -r requirements.txt
```

#### 步骤 7: 运行程序

```bash
python3 start.py
```

### CentOS / RHEL / Fedora

```bash
# 安装 Python 3
sudo yum install python3 python3-pip git -y
# 或者 (Fedora)
sudo dnf install python3 python3-pip git -y

# 其他步骤与 Ubuntu 相同
```

---

## ✅ 验证安装

### 1. 检查 Python 版本

```bash
python3 --version
# 应该显示 Python 3.7 或更高版本
```

### 2. 检查依赖安装

```bash
pip list | grep requests
pip list | grep colorama
```

### 3. 测试运行

```bash
python3 start.py
```

应该看到交互式配置界面：

```
╔═══════════════════════════════════════════════╗
║                                               ║
║     🍎  Apple Store 库存监控系统  🍎          ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

---

## ❓ 常见问题

### Q1: Windows 提示 "python 不是内部或外部命令"

**原因**：Python 未添加到系统 PATH

**解决**：
1. 重新安装 Python，确保勾选 "Add Python to PATH"
2. 或手动添加到 PATH：
   - 右键 "此电脑" > 属性 > 高级系统设置
   - 环境变量 > 系统变量 > Path
   - 添加 Python 安装路径（如：`C:\Python310\`）

### Q2: pip install 报错

**问题 1**：网络问题

```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**问题 2**：权限问题

```bash
# Windows（以管理员身份运行 CMD）
pip install -r requirements.txt

# macOS/Linux
pip install --user -r requirements.txt
```

### Q3: 虚拟环境激活失败

**Windows PowerShell 报错**：

```powershell
# 以管理员身份运行 PowerShell
Set-ExecutionPolicy RemoteSigned

# 然后激活虚拟环境
venv\Scripts\activate
```

**macOS/Linux 报错**：

```bash
# 确保使用正确的命令
source venv/bin/activate

# 检查文件是否存在
ls venv/bin/activate
```

### Q4: 无法安装某些依赖

**lxml 安装失败（Windows）**：

1. 下载预编译包：https://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml
2. 安装：`pip install 下载的文件.whl`

**lxml 安装失败（Linux）**：

```bash
sudo apt install python3-dev libxml2-dev libxslt-dev
pip install lxml
```

### Q5: macOS 提示权限问题

```bash
# 不要使用 sudo
# 使用虚拟环境或用户安装
pip install --user -r requirements.txt
```

---

## 🔄 更新项目

### 使用 Git 更新

```bash
# 进入项目目录
cd apple-store-monitor

# 拉取最新代码
git pull origin main

# 更新依赖
pip install -r requirements.txt --upgrade
```

### 手动更新

1. 下载最新版本的 ZIP
2. 备份你的 `config.json`
3. 替换旧文件
4. 恢复 `config.json`
5. 重新安装依赖

---

## 🆘 获取帮助

如果遇到问题：

1. 查看 [README.md](README.md) 的常见问题部分
2. 查看 [GitHub Issues](https://github.com/你的用户名/apple-store-monitor/issues)
3. 提交新的 Issue

---

## ✨ 下一步

安装完成后，查看：

- 📖 [使用指南](README.md#使用指南)
- ⚙️ [配置说明](README.md#配置说明)
- 🏪 [门店信息](README.md#门店信息)

**开始监控**：

```bash
python3 start.py
```

祝你成功抢到心仪的 iPhone！🎉




