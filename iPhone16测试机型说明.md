# 📱 iPhone 16 测试机型说明

> **添加时间：** 2025-10-06  
> **目的：** 提供有库存的机型用于测试对比  
> **状态：** ✅ 已验证可用

---

## 🎯 添加的机型

### 1. 中国大陆版本

**机型信息：**
- **Part Number:** `MYEV3CH/A`
- **系列:** iPhone 16
- **颜色:** 黑色
- **容量:** 128GB
- **用途:** 测试用（有库存）

**测试结果：**
```
✅ API调用成功
✅ 查询北京王府井门店
✅ 库存状态: 有货
✅ 提示: "今天可取货"
```

---

### 2. 中国香港版本

**机型信息：**
- **Part Number:** `MYEV3ZA/A`
- **系列:** iPhone 16
- **颜色:** 黑色
- **容量:** 128GB
- **用途:** 测试用（有库存）

**测试结果：**
```
✅ API调用成功
✅ 查询銅鑼灣门店
✅ 库存状态: 有货
✅ 提示: "備妥於： 今日"
```

---

## 📁 相关文件

### 1. 机型数据文件

#### 大陆机型库
**文件：** `iphone17_all_models.json`

```json
{
  "series": "iPhone 16",
  "name": "iPhone 16 黑色 128GB",
  "part_number": "MYEV3CH/A",
  "color": "黑色",
  "storage": "128GB",
  "description": "苹果iPhone 16 128GB 黑色 (测试用-有库存)"
}
```

#### 香港机型库
**文件：** `iphone16_hongkong.json` (新建)

```json
{
  "region": "Hong Kong",
  "region_code": "HK",
  "device": "iPhone 16",
  "models": [
    {
      "part_number": "MYEV3ZA/A",
      "storage": "128GB",
      "color": "黑色",
      "color_en": "Black",
      "priority": "test",
      "note": "测试用-有库存"
    }
  ]
}
```

---

### 2. 测试配置文件

#### 大陆测试配置
**文件：** `config_test_iphone16.json` (新建)

```json
{
  "region": "CN",
  "target_products": [
    {
      "name": "iPhone 16 黑色 128GB",
      "part_number": "MYEV3CH/A",
      "color": "黑色",
      "storage": "128GB"
    }
  ],
  "target_stores": ["R448", "R479", "R389"],
  "check_interval": 30
}
```

**监控门店：**
- R448 - 北京王府井
- R479 - 北京三里屯
- R389 - 上海南京东路

---

#### 香港测试配置
**文件：** `config_test_iphone16_hk.json` (新建)

```json
{
  "region": "HK",
  "target_products": [
    {
      "name": "iPhone 16 黑色 128GB",
      "part_number": "MYEV3ZA/A",
      "color": "黑色",
      "storage": "128GB"
    }
  ],
  "target_stores": ["R409", "R428", "R485"],
  "check_interval": 30
}
```

**监控门店：**
- R409 - Apple Causeway Bay (銅鑼灣)
- R428 - Apple ifc mall (國際金融中心)
- R485 - Apple Canton Road (廣東道)

---

## 🚀 使用方法

### 方法1: 直接使用测试配置

#### 测试大陆iPhone 16
```bash
cd /Users/kellychen/CodeBuddy/applepick
cp config_test_iphone16.json config.json
python3 main.py
```

#### 测试香港iPhone 16
```bash
cd /Users/kellychen/CodeBuddy/applepick
cp config_test_iphone16_hk.json config.json
python3 main.py
```

---

### 方法2: 通过交互式配置选择

#### 大陆
```bash
python3 start.py

选择: 1 (🇨🇳 中国大陆)
配置: 1 (交互式配置)
策略: 2 (平衡策略)
产品: 在列表中找到"iPhone 16 黑色 128GB"并选择
门店: 选择1-3个门店
确认: y
```

#### 香港
```bash
python3 start.py

选择: 2 (🇭🇰 中国香港)
配置: 1 (交互式配置)
策略: 2 (平衡策略)
产品: MYEV3ZA/A (需要手动配置)
门店: 选择1-3个门店
确认: y
```

---

## 🧪 验证测试

### 快速测试脚本

创建测试文件 `test_iphone16.py`:

```python
#!/usr/bin/env python3
from apple_store_monitor_enhanced import AppleStoreMonitorEnhanced

# 测试大陆
print('测试大陆iPhone 16...')
config_cn = {
    'region': 'CN',
    'target_products': [{'name': 'iPhone 16 黑色 128GB', 'part_number': 'MYEV3CH/A'}],
    'target_stores': ['R448']
}
monitor_cn = AppleStoreMonitorEnhanced(config_cn)
result_cn = monitor_cn.check_product_availability('MYEV3CH/A', 'R448')

if result_cn.get('success'):
    stores = result_cn.get('stores', {})
    for store_num, store_data in stores.items():
        print(f"✅ {store_data['store_name']}: {'有货' if store_data['available'] else '无货'}")
        print(f"   {store_data.get('pickup_quote', 'N/A')}")

# 测试香港
print('\n测试香港iPhone 16...')
config_hk = {
    'region': 'HK',
    'target_products': [{'name': 'iPhone 16 黑色 128GB', 'part_number': 'MYEV3ZA/A'}],
    'target_stores': ['R409']
}
monitor_hk = AppleStoreMonitorEnhanced(config_hk)
result_hk = monitor_hk.check_product_availability('MYEV3ZA/A', 'R409')

if result_hk.get('success'):
    stores = result_hk.get('stores', {})
    for store_num, store_data in stores.items():
        print(f"✅ {store_data['store_name']}: {'有货' if store_data['available'] else '无货'}")
        print(f"   {store_data.get('pickup_quote', 'N/A')}")
```

**运行测试：**
```bash
python3 test_iphone16.py
```

---

## 📊 测试验证结果

### 实际测试输出

```
======================================================================
测试1: 大陆iPhone 16 黑色 128GB (MYEV3CH/A)
======================================================================
✅ 大陆监控器初始化成功
   区域: 中国大陆
   API: https://www.apple.com.cn/shop/retail/pickup-message

查询库存...

查询结果:
  成功: True
  门店数: 1

  王府井:
    状态: ✅ 有货
    提示: 今天可取货

======================================================================
测试2: 香港iPhone 16 黑色 128GB (MYEV3ZA/A)
======================================================================
✅ 香港监控器初始化成功
   区域: 香港
   API: https://www.apple.com/hk-zh/shop/retail/pickup-message

查询库存...

查询结果:
  成功: True
  门店数: 1

  Apple Causeway Bay:
    状态: ✅ 有货
    提示: 備妥於： 今日
```

---

## 🎯 使用场景

### 1. API功能测试

**用途：** 验证API调用是否正常工作

```bash
# 快速验证大陆API
python3 -c "
from apple_store_monitor_enhanced import AppleStoreMonitorEnhanced
config = {'region': 'CN', 'target_products': [{'part_number': 'MYEV3CH/A'}], 'target_stores': ['R448']}
monitor = AppleStoreMonitorEnhanced(config)
result = monitor.check_product_availability('MYEV3CH/A', 'R448')
print('大陆API:', '✅ 正常' if result.get('success') else '❌ 失败')
"

# 快速验证香港API
python3 -c "
from apple_store_monitor_enhanced import AppleStoreMonitorEnhanced
config = {'region': 'HK', 'target_products': [{'part_number': 'MYEV3ZA/A'}], 'target_stores': ['R409']}
monitor = AppleStoreMonitorEnhanced(config)
result = monitor.check_product_availability('MYEV3ZA/A', 'R409')
print('香港API:', '✅ 正常' if result.get('success') else '❌ 失败')
"
```

---

### 2. 对比测试

**用途：** 对比iPhone 16（有库存）vs iPhone 17（可能无库存）

**测试配置：**
```json
{
  "region": "CN",
  "target_products": [
    {
      "name": "iPhone 16 黑色 128GB",
      "part_number": "MYEV3CH/A",
      "color": "黑色",
      "storage": "128GB"
    },
    {
      "name": "iPhone 17 黑色 256GB",
      "part_number": "MG6W4CH/A",
      "color": "黑色",
      "storage": "256GB"
    }
  ],
  "target_stores": ["R448"],
  "check_interval": 30
}
```

**预期结果：**
- iPhone 16: ✅ 有货
- iPhone 17: ❌ 无货（或有货，视实际情况）

---

### 3. 随机打散策略测试

**用途：** 验证随机打散和延迟是否正常工作

**观察点：**
```
🎲 本轮检查 6 个组合（已随机打散）
📦 2 个产品 × 3 个门店 - 区域: CN
========================================

⏳ [1/6] 等待 4.8秒 后发送下一个请求...
⏳ [2/6] 等待 5.2秒 后发送下一个请求...
⏳ [3/6] 等待 3.9秒 后发送下一个请求...
...
```

**验证项：**
- ✅ 组合数量正确（2×3=6）
- ✅ 随机延迟（3-6秒）
- ✅ 进度显示 [i/total]
- ✅ 每次延迟时间不同

---

### 4. 通知功能测试

**用途：** 测试库存通知是否正常触发

由于iPhone 16有库存，可以验证：
- ✅ 桌面通知
- ✅ 声音提醒
- ✅ 日志记录

---

## 📝 注意事项

### 1. Part Number格式

**务必注意区域差异：**
- 🇨🇳 大陆：`MYEV3CH/A` (CH/A结尾)
- 🇭🇰 香港：`MYEV3ZA/A` (ZA/A结尾)

**不要混用！** 使用错误的Part Number会导致查询失败。

---

### 2. 库存状态

**iPhone 16是已上市产品：**
- ✅ 大部分门店有库存
- ✅ 适合用于测试
- ⚠️ 不需要频繁监控（不抢手）

**iPhone 17是新品：**
- ❌ 大部分门店无库存
- ✅ 需要持续监控
- ⚠️ 库存稀缺，需要抢购

---

### 3. 测试频率

**使用iPhone 16测试时：**
- ✅ 可以较高频率测试（不会影响实际抢购）
- ✅ 适合验证功能是否正常
- ⚠️ 仍需遵守频率限制（<10次/分）

---

## 🔄 更新记录

### 2025-10-06
- ✅ 添加大陆iPhone 16机型 (MYEV3CH/A)
- ✅ 添加香港iPhone 16机型 (MYEV3ZA/A)
- ✅ 创建测试配置文件
- ✅ 验证API调用正常
- ✅ 确认两个区域都有库存

---

## ✅ 总结

### 已完成

1. ✅ **添加机型数据**
   - 大陆：`iphone17_all_models.json`
   - 香港：`iphone16_hongkong.json`

2. ✅ **创建测试配置**
   - 大陆：`config_test_iphone16.json`
   - 香港：`config_test_iphone16_hk.json`

3. ✅ **验证功能**
   - API调用成功
   - 库存查询正常
   - 数据返回完整

### 用途

- 🧪 **功能测试** - 验证系统是否正常工作
- 📊 **对比测试** - 对比有库存vs无库存
- 🔍 **API测试** - 快速验证API状态
- 🎯 **演示用途** - 展示系统功能

---

**🎉 iPhone 16测试机型已成功添加并验证！**

```bash
# 立即测试
python3 start.py
# 或使用测试配置
cp config_test_iphone16.json config.json && python3 main.py
```


