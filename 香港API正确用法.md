# 🎯 香港API正确用法 - 重要发现

> **感谢用户提供的真实API地址！**  
> **发现时间：** 2025-10-06

---

## ✨ 用户发现的真实API

### 实际URL

```
https://www.apple.com/hk-zh/shop/fulfillment-messages?
fae=true
&little=false
&parts.0=MFYP4ZA/A
&mts.0=regular
&mts.1=sticky
&fts=true
```

---

## 🔍 关键发现

### 1. API端点不同！

**我们之前使用的（错误）：**
```
https://www.apple.com/hk/shop/retail/pickup-message
```

**实际应该用的（正确）：**
```
https://www.apple.com/hk-zh/shop/fulfillment-messages
```

**关键差异：**
- ✅ `hk-zh` 而不是 `hk`（语言标识）
- ✅ `fulfillment-messages` 而不是 `retail/pickup-message`
- ✅ 复数 `messages` 不是单数 `message`

---

### 2. Part Number格式不同！

**我们之前认为的：**
```
香港：ZP/A结尾（例如：MXUA3ZP/A）
```

**实际可能是：**
```
香港：ZA/A结尾（例如：MFYP4ZA/A）
```

**重要：** 需要验证ZA/A和ZP/A的区别
- ZA/A = 香港？
- ZP/A = 其他地区？

---

### 3. 不需要门店编号参数！

**重大发现：**

用户URL中没有 `store=XXX` 参数！

这意味着：
- ✅ 这个API返回**所有门店**的库存信息
- ✅ 不需要逐个门店查询
- ✅ 一次请求就能获取所有数据
- ✅ 更高效、更快、频率更低！

---

### 4. 新的参数

用户URL包含的参数：

```
fae=true           # 未知含义
little=false       # 未知含义
parts.0=MFYP4ZA/A  # 产品编号
mts.0=regular      # 销售类型
mts.1=sticky       # 销售类型
fts=true           # fulfillment store?
```

---

## 🛠️ 需要更新的地方

### 1. 增强版监控器

**当前代码（错误）：**
```python
REGIONS = {
    'HK': {
        'api_url': 'https://www.apple.com/hk/shop/retail/pickup-message',
    }
}
```

**应该改为（正确）：**
```python
REGIONS = {
    'HK': {
        'api_url': 'https://www.apple.com/hk-zh/shop/fulfillment-messages',
    }
}
```

---

### 2. 请求参数

**当前参数（错误）：**
```python
params = {
    'pl': 'true',
    'parts.0': part_number,
    'store': store_number  # 不需要！
}
```

**应该改为（正确）：**
```python
params = {
    'fae': 'true',
    'little': 'false',
    'parts.0': part_number,
    'mts.0': 'regular',
    'mts.1': 'sticky',
    'fts': 'true'
    # 不需要store参数！
}
```

---

### 3. Part Number格式

**需要验证：**
- 香港是用 ZA/A 还是 ZP/A？
- 或者两者都支持？

**建议：**
- 在文档中明确说明
- 提供获取Part Number的方法

---

## 📊 优势分析

### 新API的优势

| 特性 | 旧API | 新API（正确） |
|------|-------|---------------|
| **端点** | retail/pickup-message | fulfillment-messages ✅ |
| **门店查询** | 需要逐个指定 | 一次返回所有 ✅ |
| **请求次数** | 每门店1次 | 所有门店1次 ✅ |
| **频率** | 高 | 低 ✅ |
| **效率** | 慢 | 快 ✅ |

### 频率降低计算

**旧方式（错误）：**
```
4个香港门店 = 4次请求
频率：4次/轮
```

**新方式（正确）：**
```
所有香港门店 = 1次请求
频率：1次/轮（降低75%！）
```

---

## 🎯 立即行动

### 1. 验证API响应（需要等待频率限制解除）

```bash
# 等待一段时间后再测试
sleep 60
python3 test_hongkong_api.py
```

---

### 2. 更新监控器代码

需要修改：
- `apple_store_monitor_enhanced.py`
- 香港区域的API配置
- 请求参数
- 响应解析

---

### 3. 测试Part Number格式

验证以下哪个正确：
- `MFYP4ZA/A`（ZA/A）✅ 用户提供
- `MFYP4ZP/A`（ZP/A）❓ 待验证

---

## 🔧 修复计划

### 阶段1：理解API（当前）

- ✅ 发现正确的API端点
- ✅ 了解不需要门店参数
- ⏳ 等待API限制解除
- ⏳ 测试实际响应

---

### 阶段2：更新代码

- [ ] 修改API端点配置
- [ ] 更新请求参数
- [ ] 修改响应解析逻辑
- [ ] 从响应中提取所有门店

---

### 阶段3：测试验证

- [ ] 测试香港API
- [ ] 验证门店编号
- [ ] 确认库存查询
- [ ] 完整测试监控

---

## 💡 重要提示

### Part Number格式

**用户提供的：** `MFYP4ZA/A`

这可能是：
- iPhone的某个型号
- ZA/A = 香港地区代码

**需要确认：**
1. ZA/A 是否是香港的标准格式
2. 是否所有产品都用ZA/A
3. ZP/A 和 ZA/A 的区别

---

### API限制

**当前问题：**
- 我们触发了HTTP 541（频率限制）
- 需要等待一段时间才能继续测试

**建议：**
- 等待30-60分钟
- 或使用不同的网络/IP
- 或直接在浏览器中测试

---

## 🌐 浏览器测试方法

### 最准确的验证方式

1. **打开浏览器**
2. **访问：** https://www.apple.com/hk/shop/buy-iphone
3. **选择型号并查看提货**
4. **F12开发者工具 → Network**
5. **查找 fulfillment-messages 请求**
6. **复制完整的请求URL和响应**

这样可以：
- ✅ 看到真实的请求格式
- ✅ 看到真实的响应结构
- ✅ 获取真实的门店列表
- ✅ 确认Part Number格式

---

## 📝 需要收集的信息

从浏览器测试中，我们需要：

1. **完整的请求URL**
   - 所有参数
   - 参数值的含义

2. **响应JSON结构**
   - 门店列表在哪个字段
   - 门店编号字段名
   - 库存状态字段名

3. **真实的门店编号**
   - 是否是R428、R485等
   - 或者是其他格式

4. **Part Number格式**
   - 确认ZA/A还是ZP/A
   - 不同产品的格式

---

## ✅ 总结

### 用户的重要贡献

**发现了：**
1. ✅ 正确的API端点（`hk-zh/fulfillment-messages`）
2. ✅ 不需要门店参数（一次返回所有）
3. ✅ 真实的Part Number格式（ZA/A）
4. ✅ 新的请求参数（fae, fts等）

### 这改变了什么

**之前的问题：**
- ❌ 使用错误的API端点
- ❌ 需要逐个查询门店
- ❌ Part Number格式可能错误

**现在的理解：**
- ✅ 使用正确的API端点
- ✅ 一次查询所有门店
- ✅ 频率大幅降低
- ✅ 效率大幅提升

### 下一步

1. **等待API限制解除**（30-60分钟）
2. **测试真实API响应**
3. **提取真实门店编号**
4. **更新监控器代码**
5. **完整测试验证**

---

**更新时间：** 2025-10-06  
**状态：** ⏳ 等待API限制解除，准备测试  
**感谢：** 用户提供的关键信息！

**🎉 这是一个重大突破！**


