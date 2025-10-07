# 🪟 Windows电脑部署指南

## 📋 目录
- [环境要求](#环境要求)
- [第一步：安装Git](#第一步安装git)
- [第二步：克隆项目](#第二步克隆项目)
- [第三步：安装Python](#第三步安装python)
- [第四步：安装依赖](#第四步安装依赖)
- [第五步：配置监控](#第五步配置监控)
- [第六步：运行程序](#第六步运行程序)
- [常见问题](#常见问题)

---

## 环境要求

- **操作系统**: Windows 10 或 Windows 11
- **网络**: 无需VPN（Git和Python安装可能需要良好的网络）
- **管理员权限**: 部分操作可能需要

---

## 第一步：安装Git

### 1.1 下载Git

1. 访问Git官网：https://git-scm.com/download/win
2. 下载会自动开始，等待下载完成

### 1.2 安装Git

1. 双击下载的 `Git-xxx-64-bit.exe` 安装程序
2. 安装向导设置：
   - ✅ **一路点击 "Next"** 即可
   - ⚠️ 重要选项：
     - **"Adjusting your PATH environment"** 页面：选择 **"Git from the command line and also from 3rd-party software"**
     - **"Choosing the default editor"** 页面：保持默认即可
     - 其他选项：保持默认设置

3. 点击 "Install" 开始安装
4. 安装完成后，点击 "Finish"

### 1.3 验证Git安装

1. 按 `Win + R` 打开运行窗口
2. 输入 `cmd` 或 `powershell`，按回车
3. 在命令行中输入：
   ```bash
   git --version
   ```
4. 如果显示版本号（如 `git version 2.43.0`），说明安装成功 ✅

---

## 第二步：克隆项目

### 2.1 打开PowerShell或CMD

**推荐使用PowerShell：**
1. 按 `Win + X`
2. 选择 **"Windows PowerShell"** 或 **"终端"**

**或者使用CMD：**
1. 按 `Win + R`
2. 输入 `cmd`，按回车

### 2.2 选择项目存放位置

```powershell
# 进入你想存放项目的目录，例如桌面
cd Desktop

# 或者进入文档目录
cd Documents
```

### 2.3 克隆项目

**项目现在是公开的，无需任何认证！**

```bash
git clone https://github.com/ZoeRamirie/apple-store-monitor.git
```

### 2.4 进入项目目录

```bash
cd apple-store-monitor
```

---

## 第三步：安装Python

### 3.1 下载Python

1. 访问Python官网：https://www.python.org/downloads/
2. 点击 **"Download Python 3.x.x"** （建议下载3.9或3.10版本）
3. 等待下载完成

### 3.2 安装Python

1. 双击下载的 `python-3.x.x-amd64.exe` 安装程序
2. **⚠️ 非常重要**：在安装界面底部勾选 ✅ **"Add Python to PATH"**
3. 点击 **"Install Now"**
4. 等待安装完成，点击 "Close"

### 3.3 验证Python安装

在PowerShell或CMD中输入：
```bash
python --version
```

如果显示版本号（如 `Python 3.10.0`），说明安装成功 ✅

---

## 第四步：安装依赖

### 4.1 确认在项目目录

```bash
# 确认当前在 apple-store-monitor 目录下
cd apple-store-monitor
```

### 4.2 安装Python依赖包

**⚠️ 重要：Python版本建议**
- ✅ **推荐：Python 3.11** （兼容性最好）
- ✅ 可用：Python 3.10, 3.12
- ⚠️ 谨慎：Python 3.13（太新，部分包可能不兼容）

**方法一：使用Python 3.11（最推荐）**
```bash
# 如果安装了Python 3.11
py -3.11 -m pip install -r requirements.txt
```

**方法二：使用默认Python + 国内镜像源**
```bash
# 使用清华镜像源（速度快）
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**方法三：逐个安装核心依赖**
```bash
# 如果整体安装有问题，单独安装核心包
python -m pip install requests colorama plyer tabulate
```

**说明：**
- Windows上直接使用 `pip`，不需要 `pip3`
- 如果 `pip` 命令不可用，使用 `python -m pip` 代替
- 不需要创建虚拟环境（个人电脑使用可以省略）
- 安装过程可能需要几分钟

### 4.3 处理可能的错误

**如果提示 `pip不是内部或外部命令，也不是可运行的程序或批处理文件`：**

这是正常的，使用以下命令代替：
```bash
python -m pip install -r requirements.txt
```

**如果提示pip版本过旧：**
```bash
python -m pip install --upgrade pip
```

**安装成功的标志：**
你会看到类似这样的输出：
```
Collecting requests
  Downloading requests-2.31.0-py3-none-any.whl (62 kB)
Collecting colorama
  Downloading colorama-0.4.6-py2.py3-none-any.whl (25 kB)
...
Successfully installed requests-2.31.0 colorama-0.4.6 ...
```

---

## 第五步：配置监控

### 5.1 同步系统时间

**⚠️ 重要：运行程序前，请确保电脑时间与Apple官网同步！**

1. 按 `Win + I` 打开设置
2. 点击 **"时间和语言"**
3. 点击 **"日期和时间"**
4. 启用 **"自动设置时间"**
5. 点击 **"立即同步"**

### 5.2 运行交互式配置

**方式一：使用统一启动入口（推荐）**
```bash
python start.py
```

然后按照提示：
1. 选择区域（输入 `1` 选择中国大陆，或 `2` 选择香港）
2. 选择配置方式（推荐选择交互式配置）
3. 按照引导完成配置

**方式二：直接启动中国大陆监控**
```bash
python start_cn.py
```

**方式三：直接启动香港监控**
```bash
python start_hk.py
```

### 5.3 配置示例

启动后会显示：
```
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║         🍎  Apple Store 库存监控系统 v1.1.0 🍎                    ║
║                                                                   ║
║                    版权所有：骑着大鹅追大奔                         ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

请选择监控策略：
  1. 保守策略（推荐新手）
  2. 平衡策略（推荐）⭐
  3. 积极策略
  4. 激进策略（高风险）
  5. 自定义配置
```

按照提示选择：
- **监控策略**（推荐选择 `2` 平衡策略）
- **监控产品**（选择你想监控的iPhone型号）
- **监控门店**（选择你附近的Apple Store）
- **检查间隔**（推荐使用默认15秒）

---

## 第六步：运行程序

### 6.1 启动监控

配置完成后，程序会自动开始监控。你会看到：

```
✨ 监控已启动！正在实时检查库存...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 监控产品: 2个
🏪 监控门店: 2个
⏱️  检查间隔: 15秒
🔔 桌面通知: ✅ 已启用
🔊 声音提醒: ✅ 已启用
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 正在检查库存 (1/4)...
```

### 6.2 后台运行（可选）

**方式一：使用pythonw（无窗口运行）**
```bash
pythonw start.py
```

**方式二：最小化窗口运行**
- 直接最小化PowerShell/CMD窗口
- 程序会继续在后台运行
- 有库存变化时会弹出通知

### 6.3 停止监控

在PowerShell/CMD窗口中按 `Ctrl + C` 停止程序

---

## 常见问题

### ❓ Python命令不识别

**问题：** 输入 `python` 提示不是内部或外部命令

**解决：**
1. 重新安装Python，确保勾选 ✅ "Add Python to PATH"
2. 或者手动添加环境变量：
   - 右键 "此电脑" → "属性" → "高级系统设置"
   - "环境变量" → 找到 "Path" → "编辑"
   - 添加Python安装路径（如 `C:\Users\你的用户名\AppData\Local\Programs\Python\Python310`）

### ❓ pip不是内部或外部命令

**问题：** 输入 `pip` 提示 "不是内部或外部命令，也不是可运行的程序或批处理文件"

**原因：** Python的Scripts目录没有添加到系统PATH

**解决方案一：使用python -m pip（推荐）**

即使pip命令不可用，也可以通过Python模块方式使用pip：

```bash
# 安装依赖
python -m pip install -r requirements.txt

# 升级pip
python -m pip install --upgrade pip

# 安装单个包
python -m pip install requests
```

**解决方案二：手动添加Scripts到PATH**

1. **找到Python的Scripts目录：**
   ```bash
   # 在PowerShell中运行
   python -c "import sys; print(sys.executable)"
   ```
   这会显示Python的安装路径，例如：
   ```
   C:\Users\你的用户名\AppData\Local\Programs\Python\Python310\python.exe
   ```
   Scripts目录就在同一位置：
   ```
   C:\Users\你的用户名\AppData\Local\Programs\Python\Python310\Scripts
   ```

2. **添加到环境变量：**
   - 按 `Win + R`，输入 `sysdm.cpl`，按回车
   - 点击 "高级" 标签
   - 点击 "环境变量"
   - 在 "用户变量" 中找到 "Path"，双击
   - 点击 "新建"
   - 添加 Scripts 路径（例如：`C:\Users\你的用户名\AppData\Local\Programs\Python\Python310\Scripts`）
   - 点击 "确定" 保存所有窗口
   - **重要：关闭并重新打开PowerShell/CMD**

3. **验证pip安装：**
   ```bash
   pip --version
   ```
   如果显示版本号，说明配置成功 ✅

**解决方案三：重新安装Python（最简单）**

1. 卸载当前Python：
   - 按 `Win + I` 打开设置
   - "应用" → "应用和功能"
   - 找到Python，点击"卸载"

2. 重新安装Python：
   - 下载：https://www.python.org/downloads/
   - **务必勾选** ✅ "Add Python to PATH"
   - 点击 "Install Now"

3. 安装完成后，关闭并重新打开PowerShell/CMD，验证：
   ```bash
   python --version
   pip --version
   ```

### ❓ Git克隆失败

**问题：** `fatal: unable to access`

**解决：**
1. 检查网络连接
2. 项目是公开的，不需要任何认证
3. 如果还是失败，可以直接从GitHub网页下载ZIP：
   - 访问：https://github.com/ZoeRamirie/apple-store-monitor
   - 点击绿色 "Code" 按钮
   - 选择 "Download ZIP"
   - 解压后进入目录

### ❓ 缺少模块错误

**问题：** `ModuleNotFoundError: No module named 'xxx'`

**解决：**
```bash
pip install -r requirements.txt
```

如果还是失败，单独安装缺失的模块：
```bash
pip install requests
pip install colorama
pip install beautifulsoup4
```

### ❓ 桌面通知不显示

**问题：** 程序运行正常，但没有弹出通知

**解决：**
1. 检查Windows通知设置：
   - 按 `Win + I` 打开设置
   - "系统" → "通知和操作"
   - 确保"获取来自应用和其他发送者的通知"已开启
2. 确保配置文件中 `notification_enabled` 为 `true`

### ❓ HTTP 541错误

**问题：** 程序显示 `HTTP 541` 错误

**原因：** 请求过于频繁，触发了Apple的限制

**解决：**
1. 停止程序（`Ctrl + C`）
2. 等待15-30分钟
3. 重新运行，选择更保守的策略
4. 增加检查间隔（如30秒或60秒）
5. 减少监控的产品和门店数量

### ❓ 端口占用

**问题：** 程序无法启动，提示端口被占用

**解决：**
```bash
# 查找占用端口的进程
netstat -ano | findstr :端口号

# 结束进程（替换PID为实际的进程ID）
taskkill /PID 进程ID /F
```

### ❓ 虚拟环境相关问题

**问题：** 是否需要创建虚拟环境？

**回答：**
- **个人电脑使用**：不需要，直接安装即可
- **开发或多项目**：建议使用虚拟环境

如果想使用虚拟环境：
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

---

## 🎯 快速启动速查卡

```bash
# 1. 打开PowerShell/CMD
Win + X → Windows PowerShell

# 2. 进入项目目录
cd Desktop\apple-store-monitor

# 3. 启动程序
python start.py

# 4. 选择区域和配置
按照提示操作

# 5. 停止程序
Ctrl + C
```

---

## 📞 获取帮助

如果遇到问题：
1. 查看本文档的"常见问题"部分
2. 查看项目中的其他文档
3. 检查GitHub Issues：https://github.com/ZoeRamirie/apple-store-monitor/issues

---

## 📝 版权信息

**版权所有：骑着大鹅追大奔**

---

**祝你监控顺利！🎉**

