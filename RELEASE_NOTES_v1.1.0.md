# 🚀 Apple Store 库存监控系统 v1.1.0

**发布日期：** 2025-10-07  
**版权所有：** 骑着大鹅追大奔

---

## 📋 版本亮点

### ✨ Windows全面支持
- 🪟 完整的Windows部署指南
- 🐍 支持Python 3.8-3.13多版本
- 🛠️ pip问题完整解决方案
- 📚 详细的故障排查文档

### ⚡ 性能优化
- 请求延迟：**3-6秒** → **1.5-2.5秒** （提升50%+）
- 检查间隔：统一为 **15秒**
- 请求频率：更精准的计算公式

### 📦 依赖管理改进
- requirements.txt 灵活版本约束（`>=` 替代 `==`）
- 完美支持 Python 3.13 最新版本
- 可及时获取安全补丁更新

---

## 🎯 主要更新

### 新增功能

#### 1. Windows部署支持
- ✅ 《Windows部署指南.md》- 完整部署流程
- ✅ 《pip命令问题解决方案.md》- pip常见问题
- ✅ 《pip安装无反应问题排查.md》- 安装故障排查

#### 2. 文档体系完善
- ✅ CHANGELOG.md - 版本更新日志
- ✅ requirements依赖更新说明
- ✅ 版本发布总结
- ✅ 版权信息添加说明

#### 3. 用户体验提升
- ✅ 所有启动页面显示版本号（v1.1.0）
- ✅ 添加版权信息展示
- ✅ 优化配置摘要的频率计算

---

### Bug修复

| 问题 | 修复 |
|------|------|
| 请求频率计算不准确 | ✅ 修正计算公式，考虑随机延迟 |
| Python 3.13依赖安装失败 | ✅ 更新requirements.txt版本策略 |
| 启动页面缺少版本号 | ✅ 所有入口添加版本号显示 |

---

### 性能优化

| 项目 | v1.0.0 | v1.1.0 | 提升 |
|------|--------|--------|------|
| 请求延迟 | 3-6秒 | 1.5-2.5秒 | ⬆️ 50%+ |
| 检查间隔 | 60秒 | 15秒 | ⬆️ 75% |
| 响应速度 | - | - | ⬆️ 显著提升 |

---

## 📚 新增文档

1. **Windows部署指南.md** - Windows完整部署流程
2. **pip命令问题解决方案.md** - pip常见问题及解决方案
3. **pip安装无反应问题排查.md** - 安装故障排查指南
4. **requirements依赖更新说明.md** - 依赖包详细说明
5. **requirements更新完成报告.md** - 依赖更新总结
6. **CHANGELOG.md** - 版本更新日志
7. **版本发布总结_v1.1.0.md** - v1.1.0发布总结
8. **版权信息添加报告.md** - 版权信息说明
9. **版本号显示修复报告.md** - 版本号修复说明

---

## 🔧 技术细节

### 依赖包版本策略调整

**修改前（v1.0.0）：**
```
requests==2.31.0      # 固定版本
colorama==0.4.6
plyer==2.1.0
```

**修改后（v1.1.0）：**
```
requests>=2.28.0      # 灵活版本
colorama>=0.4.6
plyer>=2.1.0
tabulate>=0.9.0       # 新增
```

### 请求频率计算优化

**v1.0.0：**
```python
frequency = (products * stores / interval) * 60  # 不准确
```

**v1.1.0：**
```python
requests_per_check = products * stores
avg_request_time = requests_per_check * 2.0  # 考虑随机延迟
total_cycle_time = avg_request_time + interval
frequency = (requests_per_check / total_cycle_time) * 60  # 精确计算
```

---

## 📥 安装指南

### Windows系统

#### 方法1：使用Python 3.11（推荐）
```bash
# 1. 克隆项目
git clone https://github.com/ZoeRamirie/apple-store-monitor.git

# 2. 进入目录
cd apple-store-monitor

# 3. 安装依赖
py -3.11 -m pip install -r requirements.txt

# 4. 运行程序
py -3.11 start.py
```

#### 方法2：使用Python 3.13
```bash
# 使用国内镜像源
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
python start.py
```

---

### Mac/Linux系统

```bash
# 1. 克隆项目
git clone https://github.com/ZoeRamirie/apple-store-monitor.git

# 2. 进入目录
cd apple-store-monitor

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行程序
python start.py
```

---

## 🔄 升级指南

### 从v1.0.0升级

```bash
# 1. 拉取最新代码
git pull origin main

# 2. 更新依赖
pip install -r requirements.txt --upgrade

# 3. 运行程序
python start.py
```

---

## 📊 Python版本兼容性

| Python版本 | 兼容状态 | 说明 |
|-----------|---------|------|
| **3.13** | ✅ 兼容 | 需使用镜像源或官方PyPI |
| **3.12** | ✅ 完美 | 推荐使用 |
| **3.11** | ✅ 完美 | **最推荐** ⭐ |
| **3.10** | ✅ 完美 | 稳定可靠 |
| **3.9** | ✅ 兼容 | 可用 |
| **3.8** | ✅ 兼容 | 最低支持版本 |
| **≤3.7** | ❌ 不支持 | 请升级Python |

---

## 🐛 已知问题

### 1. macOS通知问题
**问题：** `ModuleNotFoundError: No module named 'pyobjus'`

**解决：**
```bash
# 方法1
pip install pyobjus

# 方法2（推荐）
pip install pyobjc-framework-UserNotifications
```

### 2. Windows pip命令不可用
**问题：** `pip不是内部或外部命令`

**解决：**
```bash
# 使用 python -m pip 代替
python -m pip install -r requirements.txt
```

详见：《pip命令问题解决方案.md》

---

## 🎯 下一步计划 (v1.2.0)

- [ ] Web界面支持
- [ ] 更多通知方式（邮件、Telegram）
- [ ] 库存趋势分析
- [ ] 自动预约功能
- [ ] Docker容器化部署

---

## 📞 获取帮助

### 文档资源
- 📖 [README.md](README.md) - 项目介绍
- 📋 [CHANGELOG.md](CHANGELOG.md) - 更新日志
- 🪟 [Windows部署指南.md](Windows部署指南.md) - Windows部署
- 🛠️ [pip命令问题解决方案.md](pip命令问题解决方案.md) - pip问题

### 问题反馈
- GitHub Issues: https://github.com/ZoeRamirie/apple-store-monitor/issues
- 项目主页: https://github.com/ZoeRamirie/apple-store-monitor

---

## 🙏 致谢

感谢所有使用和支持本项目的用户！

特别感谢：
- Python社区
- GitHub平台
- 所有贡献者

---

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

---

## 👤 作者

**版权所有：骑着大鹅追大奔**

---

## ⭐ Star历史

如果这个项目对你有帮助，请给个Star ⭐️

[![Star History](https://img.shields.io/github/stars/ZoeRamirie/apple-store-monitor?style=social)](https://github.com/ZoeRamirie/apple-store-monitor)

---

**下载 [v1.1.0](https://github.com/ZoeRamirie/apple-store-monitor/archive/refs/tags/v1.1.0.zip) 开始使用！** 🚀

