# 🍎 Apple Store 库存监控系统 - 统一版本

> **一个入口，支持香港和大陆双区域监控**

---

## ✨ 新功能：统一入口

### 主要特点

- 🌍 **双区域支持** - 香港和大陆一键切换
- 🎯 **交互式选择** - 清晰的步骤引导
- 🔒 **自动验证** - 配置和频率自动检查
- 📊 **实时摘要** - 详细的监控信息展示
- ⚡ **快速启动** - 一条命令即可开始

---

## 🚀 快速开始

### 方法1：使用统一入口（推荐）

```bash
python3 main_unified.py
```

**功能：**
- 选择监控区域（香港/大陆）
- 选择预设配置
- 自动加载和验证
- 显示详细摘要

---

### 方法2：使用快速启动脚本

```bash
./start.sh
```

**功能：**
- 菜单式选择
- 支持统一入口和原程序

---

### 方法3：使用原监控程序

```bash
python3 main.py
```

**功能：**
- 直接使用 `config.json`
- 适合自动化脚本

---

## 🌍 支持的区域

### 中国香港 (HK)

| 特性 | 值 |
|------|-----|
| **Part Number格式** | `ZA/A` |
| **示例** | `MFYP4ZA/A` |
| **门店数量** | 6家 |
| **API端点** | `fulfillment-messages` |
| **货币** | HKD |
| **预设配置** | 2个（iPhone 17 Pro Max）|

**门店列表：**
- R409 - Causeway Bay（铜锣湾）
- R428 - ifc mall（中环）
- R485 - Festival Walk（九龙塘）
- R499 - Canton Road（尖沙咀）
- R610 - New Town Plaza（沙田）
- R673 - apm Hong Kong（观塘）

**可用型号：** 12个（256GB/512GB/1TB/2TB）

---

### 中国大陆 (CN)

| 特性 | 值 |
|------|-----|
| **Part Number格式** | `CH/A` |
| **示例** | `MXUA3CH/A` |
| **门店数量** | 42+家 |
| **API端点** | `pickup-message` |
| **货币** | CNY |
| **预设配置** | 1个 |

**门店覆盖：**
- 北京、上海、深圳、广州等主要城市

---

## 📖 使用示例

### 示例1：监控香港iPhone 17 Pro Max

```bash
$ python3 main_unified.py

请选择监控区域：
  1. 中国大陆 (China Mainland)
  2. 中国香港 (Hong Kong)

请选择 (1-2): 2

✅ 已选择: 中国香港 (HK)

请选择配置方案：
  1. iPhone 17 Pro Max 优先配置（香港）
     3门店 × 3产品(256GB) = 3次/分钟
  
  2. iPhone 17 Pro Max 平衡配置（香港）
     6门店 × 6产品(256GB+512GB) = 6次/分钟
  
  3. 自定义配置

请选择 (1-3): 2

✅ 已选择: iPhone 17 Pro Max 平衡配置（香港）

监控配置摘要
======================================================================

  区域: 中国香港 (HK)
  Part Number格式: ZA/A
  
  监控门店 (6 个):
    • R409 - Causeway Bay
    • R428 - ifc mall
    ...
  
  监控产品 (6 个):
    • MFYP4ZA/A - iPhone 17 Pro Max 256GB 深墨蓝色
    ...

确认启动？(y/n): y

正在启动监控系统...
```

---

### 示例2：监控大陆门店

```bash
$ python3 main_unified.py

请选择监控区域：
  1. 中国大陆 (China Mainland)
  2. 中国香港 (Hong Kong)

请选择 (1-2): 1

✅ 已选择: 中国大陆 (CN)

请选择配置方案：
  1. 默认配置（大陆）
  2. 自定义配置

请选择 (1-2): 1

...
```

---

## 📋 配置文件

### 香港预设配置

**1. 优先配置** (`config_hongkong_promax_priority.json`)
- 3个核心门店
- 3个256GB配置
- 3次/分钟 ✅ 非常安全

**2. 平衡配置** (`config_hongkong_promax_all.json`)
- 6个全部门店
- 6个配置（256GB + 512GB）
- 6次/分钟 ✅ 安全

---

### 自定义配置

创建或编辑 `config.json`：

```json
{
  "region": "HK",
  "target_stores": ["R409", "R428"],
  "target_products": [
    {
      "part_number": "MFYP4ZA/A",
      "name": "iPhone 17 Pro Max 256GB 深墨蓝色"
    }
  ],
  "check_interval": 60,
  "notification": {
    "desktop": true,
    "sound": true,
    "log": true
  }
}
```

---

## 🎯 完整型号列表

### iPhone 17 Pro Max（香港版）

**256GB（最热门）：**
- `MFYP4ZA/A` - 深墨蓝色
- `MFYN4ZA/A` - 宇宙橙色
- `MFYM4ZA/A` - 银色

**512GB：**
- `MFYU4ZA/A` - 深墨蓝色
- `MFYT4ZA/A` - 宇宙橙色
- `MFYQ4ZA/A` - 银色

**1TB：**
- `MFYX4ZA/A` - 深墨蓝色
- `MFYW4ZA/A` - 宇宙橙色
- `MFYV4ZA/A` - 银色

**2TB：**
- `MG014ZA/A` - 深墨蓝色
- `MG004ZA/A` - 宇宙橙色
- `MFYY4ZA/A` - 银色

---

## 📊 频率安全指南

### 计算公式

```
频率 = (门店数 × 产品数) ÷ (间隔秒数 ÷ 60)
```

### 安全级别

| 频率 | 状态 | 说明 |
|------|------|------|
| < 5次/分钟 | 🟢 非常安全 | 推荐新手使用 |
| 5-10次/分钟 | 🟢 安全 | 推荐配置 |
| 10-15次/分钟 | 🟡 接近上限 | 谨慎使用 |
| > 15次/分钟 | 🔴 危险 | 可能触发限制 |

### 推荐配置

**保守配置：**
- 1门店 × 1产品 × 60秒 = 1次/分钟 🟢

**平衡配置：**
- 3门店 × 3产品 × 60秒 = 3次/分钟 🟢
- 6门店 × 6产品 × 60秒 = 6次/分钟 🟢

**激进配置：**
- 6门店 × 12产品 × 60秒 = 12次/分钟 🟡

---

## 🗂️ 项目结构

```
applepick/
├── main_unified.py                          ← 统一入口（新）⭐
├── main.py                                  ← 原监控程序
├── start.sh                                 ← 快速启动脚本
│
├── apple_stores_hongkong.json               ← 香港门店（6家）
├── apple_stores_china.json                  ← 大陆门店（42+家）
│
├── config.json                              ← 当前配置
├── config_hongkong_promax_priority.json     ← 香港优先配置
├── config_hongkong_promax_all.json          ← 香港平衡配置
│
├── iphone17_promax_hongkong_complete.json   ← 香港iPhone型号（12个）
├── iphone17_all_models.json                 ← 大陆iPhone型号
│
├── README_统一入口.md                       ← 本文档
├── 统一入口使用指南.md                      ← 详细使用指南
├── iPhone17_ProMax_完整配置指南.md          ← iPhone配置指南
└── START_HERE.md                            ← 快速开始
```

---

## 📚 文档索引

| 文档 | 说明 | 推荐度 |
|------|------|--------|
| **START_HERE.md** | 3步快速开始 | ⭐⭐⭐⭐⭐ |
| **统一入口使用指南.md** | 详细使用说明 | ⭐⭐⭐⭐⭐ |
| **README_统一入口.md** | 本文档，项目总览 | ⭐⭐⭐⭐ |
| **iPhone17_ProMax_完整配置指南.md** | iPhone配置策略 | ⭐⭐⭐⭐ |
| **iPhone17_ProMax_型号速查卡.txt** | 型号快速查询 | ⭐⭐⭐⭐ |

---

## 🔧 功能对比

### 统一入口 vs 原程序

| 特性 | 统一入口 | 原程序 |
|------|----------|--------|
| **区域支持** | 香港 + 大陆 | 单区域 |
| **交互式** | ✅ | ❌ |
| **配置验证** | ✅ 自动 | ❌ |
| **频率计算** | ✅ 自动 | 手动 |
| **预设配置** | ✅ 多个 | ❌ |
| **适用场景** | 新手、多区域 | 自动化脚本 |

---

## ⚠️ 重要提醒

### Part Number格式

**不能混用！**

| 区域 | 格式 | 示例 |
|------|------|------|
| 香港 | `ZA/A` | `MFYP4ZA/A` |
| 大陆 | `CH/A` | `MXUA3CH/A` |

**错误示例：**
```json
{
  "region": "HK",
  "target_products": [
    {"part_number": "MXUA3CH/A"}  // ❌ 错误！香港应该用ZA/A
  ]
}
```

---

### API端点

程序会根据选择的区域自动使用正确的API端点：

| 区域 | API端点 |
|------|---------|
| 香港 | `fulfillment-messages` |
| 大陆 | `pickup-message` |

---

## 🆘 常见问题

### Q: 如何切换区域？

A: 重新运行 `python3 main_unified.py`，选择不同区域。

---

### Q: 可以同时监控两个区域吗？

A: 需要运行两个程序实例，每个配置不同区域。

---

### Q: 统一入口和原程序有什么区别？

A: 
- **统一入口**：交互式，支持双区域，自动验证
- **原程序**：直接运行，适合脚本自动化

---

### Q: 预设配置可以修改吗？

A: 可以！复制预设配置为 `config.json` 后修改。

---

### Q: 如何添加自己的门店和产品？

A: 编辑 `config.json`，修改 `target_stores` 和 `target_products`。

---

## ✅ 完成状态

- [x] 统一入口程序 ✅
- [x] 香港门店信息（6家）✅
- [x] 香港iPhone型号（12个）✅
- [x] 预设配置（2个）✅
- [x] 完整文档 ✅
- [x] 快速启动脚本 ✅

**100% 完成！** 🎉

---

## 🚀 立即开始

```bash
# 推荐：使用统一入口
python3 main_unified.py

# 或使用启动脚本
./start.sh
```

---

## 📞 相关链接

- **详细使用指南**: `统一入口使用指南.md`
- **快速开始**: `START_HERE.md`
- **iPhone配置**: `iPhone17_ProMax_完整配置指南.md`
- **型号速查**: `iPhone17_ProMax_型号速查卡.txt`

---

**创建时间：** 2025-10-06  
**版本：** 2.0（统一版本）  
**支持区域：** 香港、大陆  

**祝您使用愉快！** 🎉🍎


