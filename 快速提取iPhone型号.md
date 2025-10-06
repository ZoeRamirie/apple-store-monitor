# ⚡ 快速提取iPhone 17全系列型号 - 3分钟搞定

> **最快的方法！** 只需3步，3分钟完成

---

## 🚀 超快速提取（推荐）

### 步骤1：打开页面（30秒）

访问：https://www.apple.com/hk/shop/buy-iphone

---

### 步骤2：运行脚本（1分钟）

1. **按F12打开开发者工具**

2. **切换到Console标签**

3. **复制粘贴以下代码并按回车：**

```javascript
(function() {
    console.log('🍎 开始提取...');
    const content = document.body.innerHTML;
    const matches = content.match(/[A-Z0-9]{5,6}ZA\/A/g);
    if (!matches) {
        console.log('❌ 未找到');
        return;
    }
    const models = [...new Set(matches)];
    console.log(`✅ 找到 ${models.length} 个型号：`);
    models.forEach((m, i) => console.log(`${i+1}. ${m}`));
    
    const json = JSON.stringify({
        region: 'Hong Kong',
        models: models.map(pn => ({part_number: pn})),
        total: models.length
    }, null, 2);
    
    if (navigator.clipboard) {
        navigator.clipboard.writeText(json);
        console.log('✅ 已复制到剪贴板！');
    }
    return models;
})();
```

---

### 步骤3：保存结果（30秒）

Console会显示：
```
✅ 找到 X 个型号：
1. MFYP4ZA/A
2. MFYQ3ZA/A
3. ...
✅ 已复制到剪贴板！
```

**直接粘贴给我或保存为文件！**

---

## 📋 针对不同型号分别提取

### 方法：依次访问每个型号的页面

```
1. iPhone 17 → 运行脚本 → 复制结果
2. iPhone 17 Plus → 运行脚本 → 复制结果
3. iPhone 17 Pro → 运行脚本 → 复制结果
4. iPhone 17 Pro Max → 运行脚本 → 复制结果
```

---

## 🎯 更精确的方法（如果需要完整信息）

### 如果您已经在某个产品页面：

```javascript
// 运行这个脚本会尝试从当前页面提取产品信息
(async function() {
    // 查找所有Part Number
    const partNumbers = [...new Set(
        document.body.innerHTML.match(/[A-Z0-9]{5,6}ZA\/A/g) || []
    )];
    
    console.log(`找到 ${partNumbers.length} 个Part Number`);
    
    // 对于每个Part Number，尝试获取详细信息
    const results = [];
    
    for (const pn of partNumbers) {
        console.log(`检查 ${pn}...`);
        
        // 尝试从页面内容中查找产品名称
        const namePattern = new RegExp(`${pn}[^<>]*?([^<>]{10,100})`, 'i');
        const nameMatch = document.body.innerHTML.match(namePattern);
        
        results.push({
            part_number: pn,
            name: nameMatch ? nameMatch[1].trim() : 'Unknown'
        });
    }
    
    console.log('结果：', results);
    
    // 复制结果
    const json = JSON.stringify({
        region: 'Hong Kong',
        extracted_from: window.location.href,
        models: results,
        total: results.length
    }, null, 2);
    
    if (navigator.clipboard) {
        await navigator.clipboard.writeText(json);
        console.log('✅ 已复制到剪贴板！');
    }
    
    return results;
})();
```

---

## 💡 最简单的方式（如果不想写代码）

### 手动查看：

1. **访问产品页面**

2. **选择不同的颜色和容量**

3. **在URL或页面标题中查找Part Number**

4. **手动记录**

### 示例：

访问iPhone 17 Pro Max页面：
- 选择"深墨藍色" + "256GB"
- 在页面某处会显示：`MFYP4ZA/A`
- 记录下来

重复选择其他配置...

---

## 📊 您之前已经帮我获取过一个！

从您提供的API响应中，我们已知：

```
MFYP4ZA/A - iPhone 17 Pro Max 256GB 深墨藍色
```

**如果您能用同样的方法（选择其他配置），就能获取完整列表！**

---

## 🎯 优先级建议

### 如果时间有限，优先获取：

**iPhone 17 Pro Max（最热门）：**
- 所有颜色的256GB
- 所有颜色的512GB
- 原色钛金属的1TB

大约12-15个Part Number

**其他型号可以稍后补充**

---

## 📤 获取后告诉我

### 任何格式都可以：

**格式1：简单列表**
```
MFYP4ZA/A
MFYQ3ZA/A
MFYR2ZA/A
```

**格式2：带说明**
```
MFYP4ZA/A - 256GB 深墨藍色
MFYQ3ZA/A - 512GB 深墨藍色
```

**格式3：JSON**
```json
{
  "models": ["MFYP4ZA/A", "MFYQ3ZA/A"]
}
```

---

## 🛠️ 工具文件

我已为您创建：

| 文件 | 说明 |
|------|------|
| `浏览器Console脚本.js` | 完整的浏览器脚本 |
| `get_iphone17_models_hk.py` | Python收集工具 |
| `浏览器获取iPhone17型号指南.md` | 详细指南 |

---

## ⚡ 立即开始

```bash
# 查看完整脚本
cat 浏览器Console脚本.js

# 或运行Python工具
python3 get_iphone17_models_hk.py
```

---

**只需要3分钟，就能获取您需要的所有型号！** 🚀

**找到Part Number后，直接告诉我或粘贴给我！** 📋


