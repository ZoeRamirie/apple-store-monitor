# 🍎 Apple Store 库存监控系统

一个强大的 Apple Store 线下门店库存实时监控工具，支持中国大陆和香港地区，帮助你第一时间发现 iPhone 等产品的库存变化。

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com)

## ✨ 主要功能

- 🌏 **双区域支持**：支持中国大陆和香港地区的 Apple Store
- 📱 **多产品监控**：支持 iPhone 16/17 全系列产品
- 🏪 **多门店监控**：可同时监控多个 Apple Store 门店
- 🎯 **智能交互配置**：友好的交互式配置向导
- 🔄 **实时监控**：自动检查库存变化并通知
- 🛡️ **防限流策略**：内置随机延迟和请求打散机制
- 💾 **历史记录**：自动保存库存变化历史
- 🔔 **多种通知**：支持桌面通知和声音提醒

## 📋 系统要求

### 支持的操作系统

| 操作系统 | 版本要求 | 状态 |
|---------|---------|------|
| 🪟 Windows | Windows 10/11 | ✅ 完全支持 |
| 🍎 macOS | macOS 10.14+ | ✅ 完全支持 |
| 🐧 Linux | Ubuntu 18.04+ / Debian 10+ | ✅ 完全支持 |

### Python 版本

- **Python 3.7 或更高版本**
- 推荐使用 Python 3.9 或 3.10

### 依赖库

所有依赖都列在 `requirements.txt` 中，主要包括：

- `requests` - HTTP 请求库
- `colorama` - 彩色终端输出
- `beautifulsoup4` - HTML 解析（可选）
- 其他辅助库

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/你的用户名/apple-store-monitor.git
cd apple-store-monitor
```

### 2. 安装 Python（如果还没安装）

#### Windows

1. 下载 Python：https://www.python.org/downloads/
2. 安装时勾选 **"Add Python to PATH"**
3. 打开命令提示符，验证安装：
   ```cmd
   python --version
   ```

#### macOS

```bash
# 使用 Homebrew 安装（推荐）
brew install python3

# 或者从官网下载安装包
# https://www.python.org/downloads/macos/
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### 3. 创建虚拟环境（推荐）

#### Windows

```cmd
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 运行程序

```bash
python3 start.py
```

## 📖 使用指南

### 统一启动入口（推荐）

```bash
python3 start.py
```

这个命令会启动交互式配置向导，引导你完成：
1. 选择监控区域（大陆 / 香港）
2. 选择配置方式（交互式 / 使用示例）
3. 配置监控参数

### 快速启动脚本

#### 大陆区域

```bash
python3 start_cn.py
```

#### 香港区域

```bash
python3 start_hk.py
```

### 交互式配置

程序提供了友好的交互式配置界面：

```
📊 步骤1: 选择监控策略
  1. 保守策略（推荐新手）
  2. 平衡策略（推荐）⭐
  3. 积极策略
  4. 激进策略（高风险）
  5. 自定义配置

📱 步骤2: 选择监控产品
  1. iPhone 16 标准版 - 测试用
  2. iPhone 17 标准版
  3. iPhone 17 Pro
  4. iPhone 17 Pro Max

🏪 步骤3: 选择监控门店
  （根据城市选择门店）

✅ 步骤4: 确认配置
```

## ⚙️ 配置说明

### 配置文件

项目使用 JSON 格式的配置文件：

- `config.example.json` - 示例配置（可复制修改）
- `config.json` - 实际使用的配置（自动生成）

### 配置示例

```json
{
  "region": "CN",
  "target_products": [
    {
      "name": "iPhone 16 黑色 128GB",
      "part_number": "MYEV3CH/A"
    }
  ],
  "target_stores": ["R448", "R479"],
  "check_interval": 60,
  "notification_enabled": true,
  "sound_enabled": true
}
```

### 配置参数说明

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `region` | 监控区域 | `CN` (大陆) / `HK` (香港) |
| `target_products` | 监控的产品列表 | 产品对象数组 |
| `target_stores` | 监控的门店 ID | 门店 ID 数组 |
| `check_interval` | 检查间隔（秒） | 30-300 |
| `notification_enabled` | 启用通知 | `true` / `false` |
| `sound_enabled` | 启用声音 | `true` / `false` |

## 🔍 产品型号说明

### Part Number 格式

- **中国大陆**：`CH/A` 结尾（如：`MYEV3CH/A`）
- **中国香港**：`ZA/A` 结尾（如：`MYEV3ZA/A`）

### 获取 Part Number

#### 方法 1：使用自动工具

```bash
# 大陆产品
python3 auto_get_part_numbers.py

# 香港产品
python3 get_iphone17_models_hk.py
```

#### 方法 2：手动查找

1. 访问 Apple 官网
2. 选择产品型号
3. 在浏览器开发者工具中查找 Part Number

详见：[浏览器获取iPhone17型号指南.md](浏览器获取iPhone17型号指南.md)

## 🏪 门店信息

### 数据文件

- `apple_stores_china.json` - 中国大陆 48 家门店
- `apple_stores_hongkong.json` - 香港 6 家门店

### 门店 ID 示例

#### 中国大陆

| 门店 ID | 门店名称 | 城市 |
|---------|---------|------|
| R448 | 王府井 | 北京 |
| R479 | 三里屯 | 北京 |
| R389 | 南京东路 | 上海 |

#### 香港

| 门店 ID | 门店名称 | 地区 |
|---------|---------|------|
| R428 | 銅鑼灣 | 香港岛 |
| R485 | ifc mall | 中环 |
| R638 | 廣東道 | 尖沙咀 |

## 🛡️ 防限流说明

### API 请求策略

系统内置了多层防限流机制：

1. **随机延迟**：每次请求间隔 3-6 秒
2. **请求打散**：随机顺序发送请求
3. **频率控制**：建议不超过 10 次/分钟
4. **智能等待**：根据策略自动调整间隔

### 推荐策略

| 策略 | 门店数 | 产品数 | 请求频率 | 风险 |
|------|--------|--------|---------|------|
| 保守 | 1-2 | 1-2 | ~5次/分钟 | ✅ 极低 |
| 平衡 | 2-3 | 2-3 | ~10次/分钟 | ✅ 低 |
| 积极 | 3-4 | 3-4 | ~15次/分钟 | ⚠️ 中 |
| 激进 | 5+ | 5+ | ~25次/分钟 | ❌ 高 |

⚠️ **注意**：过于频繁的请求可能导致 IP 被临时封禁（HTTP 541）

## 🔔 通知功能

### 桌面通知

程序会在检测到库存变化时发送桌面通知：

- **Windows**：系统通知中心
- **macOS**：通知中心
- **Linux**：libnotify / notify-send

### 声音提醒

可以启用声音提醒（需要安装音频库）：

```bash
# macOS/Linux
pip install playsound

# Windows
# 系统自带支持
```

## 📂 项目结构

```
apple-store-monitor/
├── start.py                    # 统一启动入口 ⭐
├── start_cn.py                 # 大陆快速启动
├── start_hk.py                 # 香港快速启动
├── main.py                     # 主程序
├── apple_store_monitor_enhanced.py  # 核心监控逻辑
├── interactive_config.py       # 大陆交互式配置
├── interactive_config_hk.py    # 香港交互式配置
├── logger_config.py            # 日志配置
├── notifier.py                 # 通知模块
├── requirements.txt            # 依赖列表
├── config.example.json         # 配置示例
├── apple_stores_china.json     # 大陆门店数据
├── apple_stores_hongkong.json  # 香港门店数据
├── iphone17_all_models.json    # iPhone 17 型号数据
└── README.md                   # 项目说明
```

## ❓ 常见问题

### Q1: 提示 HTTP 541 错误怎么办？

**原因**：请求过于频繁，触发了 Apple 的 API 限制。

**解决方法**：
1. 增加检查间隔（`check_interval`）
2. 减少监控的门店和产品数量
3. 选择更保守的策略
4. 等待一段时间（通常 15-30 分钟）

### Q2: 如何在后台运行？

#### macOS / Linux

```bash
# 使用 nohup
nohup python3 start.py &

# 或使用 screen
screen -S monitor
python3 start.py
# Ctrl+A, D 分离会话
```

#### Windows

```cmd
# 使用 pythonw（无窗口运行）
pythonw start.py

# 或创建 VBS 脚本隐藏窗口
```

### Q3: 没有收到通知怎么办？

**检查清单**：
1. 确认配置文件中 `notification_enabled` 为 `true`
2. macOS：检查系统偏好设置 > 通知
3. Windows：检查通知设置
4. Linux：确保安装了 `libnotify` 或 `notify-send`

### Q4: 如何添加新产品？

1. **自动获取**：
   ```bash
   python3 auto_get_part_numbers.py
   ```

2. **手动添加**：
   编辑 `iphone17_all_models.json` 或 `iphone16_hongkong.json`

3. **交互式配置**：
   运行 `python3 start.py` 选择交互式配置

### Q5: 支持其他地区吗？

目前仅支持：
- 🇨🇳 中国大陆
- 🇭🇰 中国香港

其他地区需要修改 API 端点和数据格式。

## 🔧 高级功能

### 自定义通知

编辑 `notifier.py` 可以自定义通知方式：

```python
def custom_notify(message):
    # 添加你的通知逻辑
    # 例如：发送邮件、Telegram、微信等
    pass
```

### 定时任务

使用系统的定时任务功能：

#### macOS / Linux (crontab)

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天早上9点运行）
0 9 * * * cd /path/to/project && python3 start.py
```

#### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器和操作
4. 操作：运行 `python.exe start.py`

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/你的用户名/apple-store-monitor.git
cd apple-store-monitor

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行测试
python3 -m pytest  # 如果有测试
```

## 📝 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## ⚠️ 免责声明

- 本工具仅供学习和个人使用
- 请遵守 Apple 的服务条款和 robots.txt
- 请勿用于商业用途或恶意爬取
- 频繁请求可能导致 IP 被封禁，请合理使用
- 作者不对使用本工具造成的任何后果负责

## 🙏 致谢

- Apple Inc. - 提供 API
- 所有贡献者和用户

## 📮 联系方式

- Issues: [GitHub Issues](https://github.com/你的用户名/apple-store-monitor/issues)
- Email: your.email@example.com

---

**⭐ 如果这个项目对你有帮助，请给一个 Star！**

## 📅 更新日志

### v1.0.0 (2025-10-06)

- ✨ 初始版本发布
- ✅ 支持中国大陆和香港地区
- ✅ 交互式配置向导
- ✅ 多产品多门店监控
- ✅ 防限流机制
- ✅ 桌面通知和声音提醒
- ✅ 跨平台支持（Windows/macOS/Linux）
