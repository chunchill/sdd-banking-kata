# SDD Banking Kata

> 演示 Spec-Driven Development (SDD) 核心价值的银行转账系统

## 🎯 项目目标

通过这个Kata项目，展示 SDD（规范驱动开发）如何解决金融软件开发中的核心痛点：

- **需求零偏差** - 从意图到代码的精准传递
- **全流程可追溯** - 规格是唯一的"黄金源码"
- **AI提效闭环** - 为 AI 工具提供统一准确的上下文

## 📁 项目结构

```
sdd-banking-kata/
├── SPEC.md                 # 统一的规格文档（核心）
├── src/
│   ├── __init__.py
│   ├── models.py           # 领域模型
│   ├── services.py         # 业务逻辑
│   └── exceptions.py       # 异常定义
├── tests/
│   ├── __init__.py
│   └── test_transfer.py    # 转账业务规则测试
├── traditional/            # 对比：传统开发方式
│   └── ad-hoc-code.py
└── README.md
```

## 🚀 快速开始

### 环境要求

- Python 3.10+

### 安装

```bash
cd sdd-banking-kata
pip install -r requirements.txt
```

### 运行测试

```bash
pytest tests/ -v
```

## 📖 Kata 练习

### Level 1: 基础转账

按照 SPEC.md 中的 `AC-001` 实现转账功能。

### Level 2: 业务规则

实现 SPEC.md 第 3.2 节的全部 8 条转账规则。

### Level 3: 异常处理

按照 SPEC.md 第 3.3 节定义全部 7 种错误码。

### Level 4: AI 辅助

使用 AI 工具（如 Kiro, Cursor, Claude Code）根据 SPEC.md 自动生成代码：
1. 将 SPEC.md 完整提供给 AI
2. 让 AI 生成完整的实现代码
3. 对比 AI 生成的代码与手动编写的代码

## 🔑 核心概念

### 什么是 SDD？

SDD (Spec-Driven Development) 是一种软件开发范式，其核心思想是：

1. **Spec-First**: 在编写代码前，首先定义清晰、准确、可执行的规格说明
2. **Spec-Anchored**: 所有开发活动严格锚定在已定义的 Spec 上
3. **Spec-as-Source**: Spec 的地位超越传统源代码，成为系统的"黄金源码"

### 对比传统方式

| 维度 | 传统开发 | SDD |
|------|----------|-----|
| 需求表达 | 自然语言，易产生歧义 | 形式化规格，精确无歧义 |
| 测试生成 | 依赖人工编写 | Spec 驱动自动生成 |
| 变更追溯 | 散落在代码注释中 | 统一从 Spec 追溯 |
| AI 辅助效果 | 不稳定，依赖上下文的完整性 | Spec 提供准确上下文，效果稳定 |

## 🏦 金融场景示例

这个 Kata 模拟了一个简化但完整的银行转账系统，包含：

- 账户管理（创建、查询、状态管理）
- 转账交易（带完整的业务规则校验）
- 异常处理（7 种明确的错误类型）

这些规则直接来自银行业务实践，经过适当简化后非常适合演示 SDD 的价值。

## 📝 使用建议

### 给技术团队

1. 先仔细阅读 `SPEC.md` 的每一条规定
2. 尝试在不查看代码的情况下实现功能
3. 使用 AI 工具辅助，对比效果差异

### 给管理层

1. 关注 `SPEC.md` 中"验收标准"部分
2. 理解"需求零偏差"如何实现
3. 了解 SDD 如何提升 AI 辅助开发效率

## 🔗 相关资源

- [SDD 理念详解](./docs/sdd-intro.md)
- [AI4SE 四大范式对比](./docs/ai4se-paradigms.md)
- [Kiro 工具使用指南](./docs/kiro-usage.md)

---

**SDD Demo Project** | Created by Thoughtworks SE Team | 2026