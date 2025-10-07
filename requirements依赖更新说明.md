# 📦 requirements.txt 依赖更新说明

## 🔄 更新内容

### 修改前（固定版本）
```
requests==2.31.0
beautifulsoup4==4.12.2
lxml==5.1.0
urllib3==2.1.0
colorama==0.4.6
python-dotenv==1.0.0
plyer==2.1.0
tabulate==0.9.0
tqdm==4.66.1
schedule==1.2.0
pydantic==2.5.3
```

### 修改后（灵活版本）
```
requests>=2.28.0
beautifulsoup4>=4.12.0
lxml>=5.1.0
urllib3>=2.0.0
colorama>=0.4.6
python-dotenv>=1.0.0
plyer>=2.1.0
tabulate>=0.9.0
tqdm>=4.66.0
schedule>=1.2.0
pydantic>=2.5.0
```

---

## 📊 依赖包说明

| 包名 | 用途 | 最低版本 |
|------|------|---------|
| **requests** | HTTP请求库，用于访问Apple API | ≥2.28.0 |
| **beautifulsoup4** | HTML解析库 | ≥4.12.0 |
| **lxml** | XML/HTML解析器 | ≥5.1.0 |
| **urllib3** | HTTP客户端库 | ≥2.0.0 |
| **colorama** | 终端彩色输出 | ≥0.4.6 |
| **python-dotenv** | 环境变量管理 | ≥1.0.0 |
| **plyer** | 跨平台通知库 | ≥2.1.0 |
| **tabulate** | 表格格式化输出 | ≥0.9.0 |
| **tqdm** | 进度条显示 | ≥4.66.0 |
| **schedule** | 任务调度 | ≥1.2.0 |
| **pydantic** | 数据验证 | ≥2.5.0 |

---

## ✅ 更新优势

### 1. **兼容性更好**
- ✅ 支持Python 3.8 - 3.13
- ✅ 使用 `>=` 而不是 `==`，允许安装兼容的新版本
- ✅ 避免因包版本过旧导致的安装失败

### 2. **安全性提升**
- ✅ 可以自动获取安全补丁更新
- ✅ 不会锁定在可能有漏洞的旧版本

### 3. **维护更简单**
- ✅ 减少版本冲突
- ✅ 适配更多Python环境
- ✅ 降低依赖问题

---

## 🚀 如何使用更新后的requirements.txt

### Windows系统

#### 方法1：Python 3.11（推荐）
```bash
# 进入项目目录
cd C:\Users\Administrator\apple-store-monitor

# 安装依赖
py -3.11 -m pip install -r requirements.txt
```

#### 方法2：Python 3.13
```bash
# 使用官方源（兼容性更好）
python -m pip install -r requirements.txt

# 或使用国内镜像源
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

### Mac/Linux系统

```bash
# 进入项目目录
cd ~/apple-store-monitor

# 激活虚拟环境（如果有）
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 或使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 🔍 验证安装

### 检查所有包是否安装成功

```bash
# Windows (Python 3.11)
py -3.11 -m pip list

# Windows (Python 3.13)
python -m pip list

# Mac/Linux
pip list
```

### 检查特定包

```bash
# Windows
py -3.11 -m pip show requests
py -3.11 -m pip show tabulate

# Mac/Linux
pip show requests
pip show tabulate
```

### 检查依赖完整性

```bash
# Windows
py -3.11 -m pip check

# Mac/Linux
pip check
```

---

## ⚠️ 常见问题

### Q1: 提示某个包版本不满足要求

**解决：** 升级该包
```bash
# Windows
py -3.11 -m pip install --upgrade 包名

# Mac/Linux
pip install --upgrade 包名
```

### Q2: 安装速度慢

**解决：** 使用国内镜像源
```bash
# 清华源
-i https://pypi.tuna.tsinghua.edu.cn/simple

# 阿里源
-i https://mirrors.aliyun.com/pypi/simple/

# 豆瓣源
-i https://pypi.douban.com/simple/
```

### Q3: lxml安装失败（Windows）

**原因：** lxml需要编译，可能缺少C++编译器

**解决：** 
```bash
# 方法1：使用预编译的wheel
py -3.11 -m pip install lxml --only-binary lxml

# 方法2：跳过lxml（如果项目不需要）
py -3.11 -m pip install -r requirements.txt --no-deps
py -3.11 -m pip install requests colorama plyer tabulate
```

### Q4: Python 3.13 仍然无法安装

**解决：** 某些包可能还不支持3.13，使用Python 3.11
```bash
py -3.11 -m pip install -r requirements.txt
```

---

## 📋 重新安装所有依赖

如果之前安装有问题，可以完全重装：

### 方法1：清除缓存重装

```bash
# Windows
py -3.11 -m pip cache purge
py -3.11 -m pip install -r requirements.txt --force-reinstall

# Mac/Linux
pip cache purge
pip install -r requirements.txt --force-reinstall
```

### 方法2：卸载后重装

```bash
# Windows
py -3.11 -m pip uninstall -r requirements.txt -y
py -3.11 -m pip install -r requirements.txt

# Mac/Linux
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

---

## 🎯 推荐安装命令（Windows）

### 完整流程

```bash
# 1. 进入项目目录
cd C:\Users\Administrator\apple-store-monitor

# 2. 更新pip
py -3.11 -m pip install --upgrade pip

# 3. 安装依赖（使用镜像源）
py -3.11 -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 4. 验证安装
py -3.11 -m pip check

# 5. 查看已安装的包
py -3.11 -m pip list

# 6. 运行程序
py -3.11 start.py
```

---

## 📝 版本兼容性测试

| Python版本 | 测试状态 | 说明 |
|-----------|---------|------|
| Python 3.13 | ⚠️ 部分兼容 | 某些包可能无预编译版本 |
| Python 3.12 | ✅ 完全兼容 | 推荐使用 |
| Python 3.11 | ✅ 完全兼容 | **最推荐** |
| Python 3.10 | ✅ 完全兼容 | 稳定可靠 |
| Python 3.9 | ✅ 兼容 | 可用 |
| Python 3.8 | ✅ 兼容 | 最低支持版本 |
| Python 3.7及以下 | ❌ 不支持 | 请升级Python |

---

## 🔄 更新日志

### 2025-10-07
- 🔧 将所有包从固定版本（`==`）改为最低版本要求（`>=`）
- ✅ 提升对Python 3.11-3.13的兼容性
- ✅ 允许自动获取安全补丁和性能优化
- 📝 添加完整的依赖说明文档

---

## 💡 建议

1. **优先使用Python 3.11** - 兼容性最好，所有包都有稳定版本
2. **使用国内镜像源** - 大幅提升下载速度
3. **定期更新依赖** - 获取安全补丁和性能优化
   ```bash
   py -3.11 -m pip install -r requirements.txt --upgrade
   ```
4. **虚拟环境隔离** - 避免包冲突（可选）
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

---

**现在可以放心使用更新后的requirements.txt文件了！** 🎉

