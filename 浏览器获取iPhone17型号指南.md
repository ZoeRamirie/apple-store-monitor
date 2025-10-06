# 📱 如何获取iPhone 17全系列香港版Part Number

> **关键：** 香港和大陆的Part Number不同！  
> **香港：** XXXXXZA/A  
> **大陆：** XXXXXCH/A

---

## 🎯 目标

获取iPhone 17全系列（17, 17 Plus, 17 Pro, 17 Pro Max）所有配置的香港Part Number

---

## 📋 方法1：从购买页面提取（推荐）⭐⭐⭐⭐⭐

### 步骤：

1. **访问Apple香港官网**
   ```
   https://www.apple.com/hk/shop/buy-iphone
   ```

2. **选择iPhone 17 Pro Max**

3. **F12打开开发者工具**

4. **对于每个颜色选项：**
   - 点击选择颜色
   - 对于每个容量选项：
     - 点击选择容量
     - 在Network中查找API请求
     - 或在Elements中查看HTML，搜索"ZA/A"

5. **记录Part Number**

### 示例流程：

```
iPhone 17 Pro Max
├─ 原色钛金属
│  ├─ 256GB → Part Number: ?????ZA/A
│  ├─ 512GB → Part Number: ?????ZA/A
│  └─ 1TB   → Part Number: ?????ZA/A
├─ 白色钛金属
│  ├─ 256GB → Part Number: ?????ZA/A
│  └─ ...
└─ ...
```

---

## 🔍 方法2：从页面源代码提取（快速）⭐⭐⭐⭐

### 步骤：

1. **访问产品页面**

2. **右键 → 查看网页源代码**

3. **Ctrl+F 搜索 "ZA/A"**

4. **提取所有匹配的Part Number**

### 搜索技巧：

```javascript
// 在浏览器Console中运行
document.body.innerHTML.match(/[A-Z0-9]{5,6}ZA\/A/g)
```

会返回页面中所有ZA/A格式的Part Number

---

## 🌐 方法3：从JSON配置文件提取（最完整）⭐⭐⭐⭐⭐

### 步骤：

1. **访问产品页面**

2. **F12 → Network标签**

3. **刷新页面（F5）**

4. **查找以下类型的请求：**
   - `product-config.json`
   - `skus.json`
   - `fulfillment-messages`
   - 包含"config"或"product"的JSON文件

5. **在Response中查找所有Part Number**

### 示例：

可能会看到这样的结构：
```json
{
  "products": [
    {
      "partNumber": "MFYP4ZA/A",
      "name": "iPhone 17 Pro Max 256GB",
      "color": "..."
    }
  ]
}
```

---

## 📊 需要收集的信息

### iPhone 17系列完整配置

| 型号 | 颜色 | 容量 | Part Number |
|------|------|------|-------------|
| iPhone 17 | 黑色 | 128GB | ?????ZA/A |
| iPhone 17 | 黑色 | 256GB | ?????ZA/A |
| iPhone 17 | 白色 | 128GB | ?????ZA/A |
| ... | ... | ... | ... |
| iPhone 17 Pro Max | 深墨藍色 | 256GB | MFYP4ZA/A ✅ |
| ... | ... | ... | ... |

---

## 🛠️ 自动化方法（高级）

### 使用浏览器Console批量提取

```javascript
// 1. 打开产品页面
// 2. F12 → Console
// 3. 运行以下代码：

// 提取所有Part Number
const partNumbers = new Set();
const content = document.body.innerHTML;
const matches = content.match(/[A-Z0-9]{5,6}ZA\/A/g);
if (matches) {
    matches.forEach(pn => partNumbers.add(pn));
}

// 显示结果
console.log('找到的Part Number:');
console.log([...partNumbers]);

// 导出为JSON
copy(JSON.stringify([...partNumbers], null, 2));
console.log('已复制到剪贴板！');
```

---

## 📋 数据收集模板

### 复制以下模板填写：

```
iPhone 17:
  - 黑色 128GB: _____ZA/A
  - 黑色 256GB: _____ZA/A
  - 黑色 512GB: _____ZA/A
  - 白色 128GB: _____ZA/A
  ...

iPhone 17 Plus:
  - 黑色 128GB: _____ZA/A
  ...

iPhone 17 Pro:
  - 原色钛金属 128GB: _____ZA/A
  ...

iPhone 17 Pro Max:
  - 原色钛金属 256GB: _____ZA/A
  - 原色钛金属 512GB: _____ZA/A
  - 原色钛金属 1TB: _____ZA/A
  - 深墨藍色 256GB: MFYP4ZA/A ✅ (已知)
  ...
```

---

## ⚡ 快速收集流程（10分钟）

### 最快的方法：

1. **访问** https://www.apple.com/hk/shop/buy-iphone

2. **选择iPhone 17 Pro Max**

3. **打开Console，运行上面的JavaScript代码**

4. **复制结果**

5. **重复步骤2-4，换成其他型号**

6. **汇总所有Part Number**

---

## 📤 提供给我的方式

### 方式1：列表格式

```
MFYP4ZA/A
MFYQ3ZA/A
MFYR2ZA/A
...
```

### 方式2：JSON格式

```json
{
  "iPhone 17 Pro Max": [
    {
      "color": "深墨藍色",
      "storage": "256GB",
      "partNumber": "MFYP4ZA/A"
    }
  ]
}
```

### 方式3：直接告诉我

"我找到了以下Part Number: ..."

---

## 🎯 为什么需要完整的型号列表？

### 监控的灵活性

有了完整列表后，您可以：

1. **同时监控多个型号**
   ```json
   {
     "target_products": [
       {"part_number": "MFYP4ZA/A", "name": "256GB 深墨藍色"},
       {"part_number": "MFYQ3ZA/A", "name": "512GB 深墨藍色"},
       {"part_number": "MFYR2ZA/A", "name": "1TB 深墨藍色"}
     ]
   }
   ```

2. **覆盖更多备选**
   - 主选颜色无货时，自动检查其他颜色
   - 主选容量无货时，自动检查其他容量

3. **提高抢到概率**
   - 监控更多型号 = 更多机会

---

## 🔧 工具支持

### 我已为您创建：

**脚本：** `get_iphone17_models_hk.py`

**功能：**
- 帮助收集Part Number
- 验证格式
- 生成配置文件

**使用：**
```bash
python3 get_iphone17_models_hk.py
```

---

## ✅ 检查清单

- [ ] 访问Apple香港官网
- [ ] 选择iPhone 17各型号
- [ ] 记录所有颜色配置的Part Number
- [ ] 记录所有容量配置的Part Number
- [ ] 验证格式（应该是ZA/A结尾）
- [ ] 提供给我或保存到文件

---

## 💡 提示

### 不需要每个配置都要

如果太多配置：
- **优先获取您关心的型号**
- **至少获取每个系列的几个主流配置**
- **可以先收集Pro Max系列（最热门）**

### 示例最小集合

```
iPhone 17 Pro Max:
  - 原色钛金属 256GB
  - 原色钛金属 512GB
  - 深墨藍色 256GB
  - 黑色钛金属 256GB
```

---

**创建时间：** 2025-10-06  
**目的：** 获取iPhone 17全系列香港Part Number  
**重要性：** 🔴 高 - 不同地区Part Number不同

**请帮忙收集您关心的型号的Part Number！** 🙏


