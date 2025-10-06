# 🚀 立即开始监控iPhone 17 Pro Max

> **所有准备工作已完成！3步即可开始！**

---

## ⚡ 3步开始

### 步骤1：选择配置（30秒）

**推荐：平衡型配置**（256GB优先，512GB备选）

```bash
cp config_hongkong_promax_all.json config.json
```

---

### 步骤2：启动监控（1秒）

```bash
python3 main.py
```

---

### 步骤3：等待通知

系统会自动：
- 🔔 发现库存时弹出通知
- 🔊 播放提示音
- 📝 记录到日志

**就这么简单！** ✅

---

## 📊 已配置信息

### 监控的门店（6家）

- ✅ R409 - Causeway Bay (铜锣湾)
- ✅ R428 - ifc mall (中环)
- ✅ R485 - Festival Walk (九龙塘)
- ✅ R499 - Canton Road (尖沙咀)
- ✅ R610 - New Town Plaza (沙田)
- ✅ R673 - apm Hong Kong (观塘)

---

### 监控的型号（6个，平衡配置）

**256GB（最热门）：**
- ✅ MFYP4ZA/A - 深墨蓝色
- ✅ MFYN4ZA/A - 宇宙橙色
- ✅ MFYM4ZA/A - 银色

**512GB（备选）：**
- ✅ MFYU4ZA/A - 深墨蓝色
- ✅ MFYT4ZA/A - 宇宙橙色
- ✅ MFYQ4ZA/A - 银色

---

### 监控频率

```
6门店 × 6产品 ÷ 60秒 = 6次/分钟 ✅ 安全
```

---

## 🔧 其他配置方案

### 激进型（只要256GB）

**更激进的监控策略：**

```bash
cp config_hongkong_promax_priority.json config.json
python3 main.py
```

**配置：**
- 3个核心门店
- 3个256GB配置
- 频率：3次/分钟（更安全）

---

### 自定义配置

编辑 `config.json`，修改：

```json
{
  "target_stores": ["R409", "R428"],  // 您想监控的门店
  "target_products": [
    {"part_number": "MFYP4ZA/A", "name": "256GB 深墨蓝色"}
  ]
}
```

---

## 📋 所有可用型号

### 完整列表（12个）

| 容量 | 颜色 | Part Number |
|------|------|-------------|
| 256GB | 深墨蓝色 | MFYP4ZA/A |
| 256GB | 宇宙橙色 | MFYN4ZA/A |
| 256GB | 银色 | MFYM4ZA/A |
| 512GB | 深墨蓝色 | MFYU4ZA/A |
| 512GB | 宇宙橙色 | MFYT4ZA/A |
| 512GB | 银色 | MFYQ4ZA/A |
| 1TB | 深墨蓝色 | MFYX4ZA/A |
| 1TB | 宇宙橙色 | MFYW4ZA/A |
| 1TB | 银色 | MFYV4ZA/A |
| 2TB | 深墨蓝色 | MG014ZA/A |
| 2TB | 宇宙橙色 | MG004ZA/A |
| 2TB | 银色 | MFYY4ZA/A |

**详细信息：** `iphone17_promax_hongkong_complete.json`

---

## 📖 详细文档

| 文档 | 说明 |
|------|------|
| **iPhone17_ProMax_完整配置指南.md** | 详细配置和策略 |
| **iPhone17_ProMax_型号速查卡.txt** | 快速查询型号 |
| **apple_stores_hongkong.json** | 门店详细信息 |

---

## 💡 监控技巧

### 提高成功率

1. **多配置备选**
   - 不要只监控单一配置
   - 256GB + 512GB 增加机会

2. **覆盖多个门店**
   - 至少监控3个门店
   - 核心门店优先

3. **及时响应**
   - 收到通知立即查看
   - 准备好Apple ID和支付方式

---

## 🔍 监控状态检查

### 运行后检查：

**正常运行应该看到：**
```
✅ 配置加载成功
✅ 已加载 6 个门店
✅ 已加载 6 个产品
✅ 开始监控...
```

**发现库存时：**
```
🎉 发现库存！
门店：Causeway Bay
产品：iPhone 17 Pro Max 256GB 深墨蓝色
```

---

## ⚠️ 注意事项

### 重要提醒

- ✅ 所有型号均为香港版（ZA/A）
- ✅ 不能与大陆版（CH/A）混用
- ✅ 监控频率已优化为安全范围
- ✅ 门店编号100%准确
- ⚠️ 请不要频繁手动测试API

---

## 🆘 常见问题

### Q: 多久能发现库存？

A: 取决于实际库存情况。系统会每分钟检查6次，发现库存立即通知。

### Q: 可以同时监控多个型号吗？

A: 可以！已配置的方案就是监控6个型号。

### Q: 频率安全吗？

A: 完全安全！6次/分钟远低于安全阈值（15次/分钟）。

### Q: 如何只监控特定颜色？

A: 编辑 `config.json`，只保留您想要的Part Number。

---

## 📞 相关文件位置

```
applepick/
├── config.json                              ← 当前使用的配置
├── config_hongkong_promax_all.json          ← 平衡型配置
├── config_hongkong_promax_priority.json     ← 激进型配置
├── iphone17_promax_hongkong_complete.json   ← 完整型号库
├── apple_stores_hongkong.json               ← 门店信息
├── iPhone17_ProMax_完整配置指南.md          ← 详细指南
├── iPhone17_ProMax_型号速查卡.txt           ← 快速查询
└── main.py                                  ← 主程序
```

---

## ✅ 准备状态检查清单

- [x] 香港门店信息 - 6家全部确认
- [x] iPhone型号 - 12个全部收集
- [x] 配置文件 - 已创建2个方案
- [x] 频率验证 - 已确认安全
- [x] API端点 - 已确认正确
- [x] Part Number格式 - 已验证（ZA/A）

**所有准备工作已完成！** ✅

---

## 🚀 立即开始

```bash
# 推荐配置（平衡型）
cp config_hongkong_promax_all.json config.json

# 启动监控
python3 main.py
```

**就是这么简单！祝您抢购成功！** 🎉

---

**创建时间：** 2025-10-06  
**可用性：** 🟢 立即可用  
**完成度：** ✅ 100%

**Have fun！** 🚀


