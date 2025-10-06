# 🤝 贡献指南

感谢你对 Apple Store 库存监控系统的关注！我们欢迎所有形式的贡献。

## 📋 目录

- [行为准则](#行为准则)
- [我能做什么](#我能做什么)
- [开发环境设置](#开发环境设置)
- [提交规范](#提交规范)
- [Pull Request 流程](#pull-request-流程)
- [代码规范](#代码规范)

## 🌟 行为准则

参与本项目时，请遵守以下准则：

- 尊重所有贡献者
- 接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表现出同理心

## 💡 我能做什么？

### 报告问题 (Bug Report)

发现 Bug？请：

1. 在 [Issues](https://github.com/你的用户名/apple-store-monitor/issues) 中搜索是否已有相关问题
2. 如果没有，创建新 Issue，包含：
   - 清晰的标题
   - 详细的问题描述
   - 重现步骤
   - 预期行为 vs 实际行为
   - 系统环境（OS、Python 版本）
   - 错误日志或截图

**Issue 模板**：
```markdown
## 问题描述
[描述问题]

## 重现步骤
1. ...
2. ...
3. ...

## 预期行为
[应该发生什么]

## 实际行为
[实际发生了什么]

## 环境信息
- OS: [Windows 10 / macOS 13 / Ubuntu 22.04]
- Python: [3.9.0]
- 版本: [v1.0.0]

## 错误日志
```
[粘贴错误信息]
```
```

### 功能建议 (Feature Request)

想要新功能？请：

1. 检查是否已有类似建议
2. 创建新 Issue，标记为 `enhancement`
3. 详细描述：
   - 功能用途
   - 使用场景
   - 实现建议（可选）

### 代码贡献

想要贡献代码？太棒了！请继续阅读。

## 🛠️ 开发环境设置

### 1. Fork 仓库

点击 GitHub 页面右上角的 "Fork" 按钮

### 2. 克隆你的 Fork

```bash
git clone https://github.com/你的用户名/apple-store-monitor.git
cd apple-store-monitor
```

### 3. 添加上游仓库

```bash
git remote add upstream https://github.com/原作者/apple-store-monitor.git
```

### 4. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 5. 安装依赖

```bash
pip install -r requirements.txt
```

### 6. 创建开发分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bugfix-name
```

## 📝 提交规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

### 提交消息格式

```
<类型>(<范围>): <简短描述>

<详细描述>（可选）

<相关 Issue>（可选）
```

### 类型说明

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat: 添加邮件通知功能` |
| `fix` | Bug 修复 | `fix: 修复香港API请求错误` |
| `docs` | 文档更新 | `docs: 更新README安装说明` |
| `style` | 代码格式 | `style: 格式化代码` |
| `refactor` | 代码重构 | `refactor: 重构配置加载逻辑` |
| `perf` | 性能优化 | `perf: 优化请求频率控制` |
| `test` | 测试相关 | `test: 添加单元测试` |
| `chore` | 构建/工具 | `chore: 更新依赖版本` |

### 提交示例

```bash
# 新功能
git commit -m "feat(notification): 添加邮件通知支持

- 添加 SMTP 配置
- 支持多个收件人
- 添加邮件模板

Closes #123"

# Bug 修复
git commit -m "fix(api): 修复香港API请求失败

修复了由于URL格式错误导致的API请求失败问题

Fixes #456"

# 文档更新
git commit -m "docs: 更新安装指南

添加了 Windows 用户的详细安装步骤"
```

## 🔄 Pull Request 流程

### 1. 保持分支更新

```bash
# 获取上游更新
git fetch upstream

# 合并到本地主分支
git checkout main
git merge upstream/main

# 将主分支合并到你的功能分支
git checkout feature/your-feature-name
git merge main
```

### 2. 推送到你的 Fork

```bash
git push origin feature/your-feature-name
```

### 3. 创建 Pull Request

1. 访问你的 Fork 页面
2. 点击 "Compare & pull request"
3. 填写 PR 信息：

**PR 标题格式**：
```
feat: 添加新功能描述
fix: 修复某个问题
docs: 更新文档
```

**PR 描述模板**：
```markdown
## 变更类型
- [ ] Bug 修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 性能优化
- [ ] 代码重构

## 变更说明
[详细描述你的更改]

## 测试
- [ ] 本地测试通过
- [ ] 添加了单元测试
- [ ] 更新了文档

## 相关 Issue
Closes #issue编号

## 截图（如适用）
[添加截图]

## 检查清单
- [ ] 代码符合项目规范
- [ ] 通过所有测试
- [ ] 更新了相关文档
- [ ] 添加了必要的注释
- [ ] 没有引入新的警告
```

### 4. 代码审查

- 维护者会审查你的代码
- 根据反馈进行修改
- 推送新的提交更新 PR

### 5. 合并

- PR 被批准后会合并到主分支
- 删除你的功能分支（可选）

```bash
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```

## 📐 代码规范

### Python 代码规范

遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 规范：

```python
# 好的示例
def check_store_availability(store_id: str, product_id: str) -> dict:
    """
    检查门店的产品库存
    
    Args:
        store_id: 门店 ID
        product_id: 产品 Part Number
        
    Returns:
        包含库存信息的字典
    """
    # 实现逻辑
    pass

# 避免
def check(s,p):
    # 没有文档字符串，参数名不清晰
    pass
```

### 代码风格

- **缩进**：使用 4 个空格
- **命名**：
  - 变量/函数：`snake_case`
  - 类：`PascalCase`
  - 常量：`UPPER_SNAKE_CASE`
- **导入**：
  ```python
  # 标准库
  import os
  import sys
  
  # 第三方库
  import requests
  from colorama import Fore
  
  # 本地模块
  from logger_config import setup_logger
  ```
- **行长度**：最多 100 字符（允许例外）
- **文档字符串**：所有公共函数/类都要有

### 目录结构

```
新增文件应放在合适的位置：
- 核心逻辑：根目录
- 工具脚本：保持在根目录
- 数据文件：JSON 文件在根目录
- 文档：README、INSTALL 等在根目录
```

## 🧪 测试

### 运行测试

```bash
# 如果有测试框架
python -m pytest

# 手动测试
python3 start.py
```

### 添加测试

为新功能添加测试：

```python
# test_monitor.py
def test_store_availability():
    """测试门店库存检查"""
    result = check_store_availability("R448", "MYEV3CH/A")
    assert result is not None
    assert 'available' in result
```

## 📚 文档

### 更新文档

如果你的更改影响到：

- **功能**：更新 README.md
- **安装**：更新 INSTALL.md
- **配置**：更新配置说明
- **API**：添加/更新注释和文档字符串

### 文档风格

- 使用清晰、简洁的语言
- 提供示例代码
- 添加必要的截图
- 使用 Markdown 格式

## ❓ 常见问题

### Q: 我的 PR 什么时候会被审查？

A: 通常在 1-3 天内。如果超过一周没有回应，可以友好地提醒一下。

### Q: 我不知道从哪里开始？

A: 查看标记为 `good first issue` 的 Issues，这些适合新手。

### Q: 我的修改被拒绝了怎么办？

A: 不要灰心！询问原因，根据反馈改进，或者讨论其他解决方案。

### Q: 可以同时提交多个 PR 吗？

A: 可以，但建议每个 PR 只做一件事，这样更容易审查。

## 🙏 致谢

感谢所有贡献者！你的努力让这个项目变得更好。

### 贡献者列表

<!-- 这里会自动更新贡献者 -->
查看完整列表：[Contributors](https://github.com/你的用户名/apple-store-monitor/graphs/contributors)

## 📞 联系方式

有问题？可以通过以下方式联系：

- GitHub Issues
- Email: your.email@example.com
- 讨论区：[Discussions](https://github.com/你的用户名/apple-store-monitor/discussions)

---

再次感谢你的贡献！🎉

