# ⚡ 快速开始指南

5 分钟快速上手 Apple Store 库存监控系统！

## 🎯 适用人群

- ✅ 想快速开始使用的用户
- ✅ 不想看长篇文档的用户
- ✅ 只需要基本功能的用户

详细文档请查看 [README.md](README.md) 和 [INSTALL.md](INSTALL.md)

---

## 📦 第一步：安装

### Windows 用户

```cmd
# 1. 确保已安装 Python 3.7+
python --version

# 2. 克隆或下载项目
git clone https://github.com/你的用户名/apple-store-monitor.git
cd apple-store-monitor

# 3. 安装依赖
pip install -r requirements.txt

# 完成！
```

### macOS / Linux 用户

```bash
# 1. 确保已安装 Python 3.7+
python3 --version

# 2. 克隆或下载项目
git clone https://github.com/你的用户名/apple-store-monitor.git
cd apple-store-monitor

# 3. 安装依赖
pip3 install -r requirements.txt

# 完成！
```

---

## 🚀 第二步：启动

### 最简单的方式

```bash
# Windows
python start.py

# macOS / Linux
python3 start.py
```

### 跟随向导操作

程序会引导你完成所有配置：

```
1️⃣ 选择区域
   [1] 🇨🇳 中国大陆
   [2] 🇭🇰 中国香港
   
   → 输入数字，回车

2️⃣ 选择配置方式
   [1] 交互式配置（推荐）⭐
   [2] 使用示例配置
   
   → 输入 1，回车

3️⃣ 选择策略
   [1] 保守策略（新手推荐）
   [2] 平衡策略⭐
   [3] 积极策略
   
   → 输入数字，回车

4️⃣ 选择产品
   [1] iPhone 16 黑色 128GB - 测试用
   [2] iPhone 17 Pro Max 深墨蓝色 256GB
   ...
   
   → 输入数字（可多选：1,2,3），回车

5️⃣ 选择门店
   选择城市，然后选择门店
   
   → 输入数字，回车

6️⃣ 确认并开始
   确认配置，输入 y
   
   → 开始监控！
```

---

## 📊 第三步：查看结果

### 监控界面示例

```
╔═══════════════════════════════════════════════╗
║     🍎  Apple Store 库存监控系统  🍎          ║
╚═══════════════════════════════════════════════╝

📍 监控区域: 🇨🇳 中国大陆
📱 监控产品: 2 个
🏪 监控门店: 3 个

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[2025-10-06 20:00:00] 🔄 开始检查...

✅ 王府井 (R448)
   • iPhone 16 黑色 128GB: 有货 🎉
   • iPhone 17 Pro Max 深墨蓝色: 无货

✅ 三里屯 (R479)
   • iPhone 16 黑色 128GB: 无货
   • iPhone 17 Pro Max 深墨蓝色: 无货

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏰ 下次检查: 60秒后
按 Ctrl+C 停止监控
```

### 有货提醒

当检测到库存时：
- 🔔 **桌面通知**：系统通知弹窗
- 🔊 **声音提醒**：系统提示音
- 📝 **日志记录**：保存到文件

---

## ⚙️ 常用配置

### 快速切换区域

**监控大陆**：
```bash
python3 start_cn.py
```

**监控香港**：
```bash
python3 start_hk.py
```

### 调整检查间隔

编辑 `config.json`：
```json
{
  "check_interval": 60,  // 改为 30、120 等
  ...
}
```

### 开启/关闭通知

编辑 `config.json`：
```json
{
  "notification_enabled": true,  // 改为 false 关闭
  "sound_enabled": true,         // 改为 false 关闭
  ...
}
```

---

## 🎯 实用技巧

### 1️⃣ 后台运行

**macOS / Linux**：
```bash
nohup python3 start.py &
```

**Windows**：
```cmd
pythonw start.py
```

### 2️⃣ 查看历史记录

```bash
# 查看所有历史文件
ls stock_history_*.json

# 查看最新记录（macOS/Linux）
cat stock_history_*.json | tail -n 50
```

### 3️⃣ 只监控特定型号

直接编辑 `config.json`：
```json
{
  "target_products": [
    {
      "name": "iPhone 17 Pro Max 深墨蓝色 256GB",
      "part_number": "MFYP4CH/A"
    }
  ],
  ...
}
```

### 4️⃣ 多门店优先级

**推荐监控这些热门门店**：

**大陆**：
- R448 - 北京王府井
- R479 - 北京三里屯  
- R389 - 上海南京东路

**香港**：
- R428 - 銅鑼灣
- R485 - ifc mall
- R638 - 廣東道

---

## ❓ 遇到问题？

### HTTP 541 错误

**原因**：请求太频繁

**解决**：
1. 增加检查间隔（60秒以上）
2. 减少监控的门店数量
3. 等待 15-30 分钟

### 没有通知

**检查**：
1. `notification_enabled` 是否为 `true`
2. 系统通知设置是否允许
3. 查看终端是否有库存提示

### 无法启动

**确认**：
1. Python 版本 3.7+
2. 已安装所有依赖
3. 在正确的目录下

```bash
# 重新安装依赖
pip install -r requirements.txt --force-reinstall
```

---

## 📚 了解更多

- 📖 [完整文档](README.md)
- 🔧 [安装指南](INSTALL.md)
- 🌐 [GitHub 上传](GITHUB_SETUP.md)
- 🤝 [贡献指南](CONTRIBUTING.md)

---

## 💡 一句话总结

```bash
# 就是这么简单！
python3 start.py
```

**3 个步骤，5 分钟上手，开始监控你的 iPhone！** 🎉

---

## 🎁 进阶功能

有兴趣深入了解？

- 自定义通知方式（邮件、Telegram 等）
- 设置定时任务自动运行
- 批量监控多个配置
- API 集成到自己的项目

详见 [README.md](README.md) 的高级功能章节。

---

**祝你成功抢到心仪的 iPhone！** 🍎✨


