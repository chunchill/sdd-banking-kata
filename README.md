# SDD Banking Kata

> 演示 Spec-Driven Development (SDD) 核心价值的银行转账系统

## 🎯 项目目标

通过这个Kata项目，展示 SDD（规范驱动开发）如何解决金融软件开发中的核心痛点：

- **需求零偏差** - 从意图到代码的精准传递
- **全流程可追溯** - 规格是唯一的"黄金源码"
- **AI提效闭环** - 为 AI 工具提供统一准确的上下文

## 🚀 快速开始

### Kiro 编辑器打开

```bash
# 方式1: 用 Kiro 打开项目
kiro open ~/Projects/sdd-banking-kata

# 方式2: 直接在 VS Code / Cursor 中打开
code ~/Projects/sdd-banking-kata
```

### 环境要求

- Python 3.10+
- Kiro 编辑器（推荐）

### 安装依赖

```bash
cd ~/Projects/sdd-banking-kata
pip install -r requirements.txt
```

### 运行测试

```bash
pytest tests/ -v
```

---

## 📁 Kiro 项目结构

```
sdd-banking-kata/
├── .kiro/                        # Kiro 配置目录
│   └── specs/
│       └── sdd-banking-kata/     # Kiro Spec
│           ├── .config.kiro      # Kiro 项目配置
│           ├── requirements.md   # 需求规格
│           ├── design.md         # 设计文档
│           └── tasks.md          # 任务清单
├── src/                          # 源代码
│   ├── models.py                 # 领域模型
│   ├── services.py               # 业务逻辑
│   └── exceptions.py             # 异常定义
├── tests/                        # 测试用例
│   └── test_transfer.py          # 9个测试（全部通过）
├── SPEC.md                       # 统一规格文档（核心）
├── README.md                     # 本文件
└── requirements.txt              # Python 依赖
```

---

## 📖 Kiro 使用指南

### 1. 打开 Kiro 项目

在 Kiro 编辑器中打开 `~/Projects/sdd-banking-kata`，Kiro 会自动识别 `.kiro/specs/sdd-banking-kata/` 目录。

### 2. Spec 工作流

| 文件 | 用途 |
|------|------|
| `.config.kiro` | 项目配置（specId, workflowType） |
| `requirements.md` | 需求定义（Domain Model, Business Rules） |
| `design.md` | 设计文档（API, 实现细节） |
| `tasks.md` | 任务清单（进度跟踪） |

### 3. 开发流程

1. **读需求** - 查看 `requirements.md` 中的业务规则
2. **看设计** - 参考 `design.md` 中的 API 规范
3. **写代码** - 在 `src/` 目录实现
4. **跑测试** - `pytest tests/ -v` 验证

### 4. AI 辅助开发

将 `requirements.md` 内容完整提供给 Kiro/Claude/Cursor，AI 可以基于准确的 Spec 生成正确代码。

---

## 📖 Kata 练习（按验收标准）

### Level 1: 成功转账 (AC-001)

按照 requirements.md 中的 `AC-001` 实现转账功能。

**预期结果：** 9个测试全部通过 ✅

```bash
pytest tests/test_transfer.py::test_successful_transfer -v
```

### Level 2: 业务规则

实现 `requirements.md` 中的全部 8 条转账规则（RULE-001 到 RULE-008）。

### Level 3: 异常处理

实现 `requirements.md` 中定义的 7 种错误码（E001-E007）。

### Level 4: AI 辅助

使用 Kiro 根据 Spec 自动生成代码：
1. 打开 `requirements.md`
2. 让 Kiro 生成完整的 `src/services.py`
3. 对比 AI 生成的代码与现有实现

---

## 🧪 测试结果

```bash
$ pytest tests/ -v

tests/test_transfer.py::test_successful_transfer PASSED           [ 11%]
tests/test_transfer.py::test_insufficient_balance PASSED          [ 22%]
tests/test_transfer.py::test_single_transfer_limit PASSED         [ 33%]
tests/test_transfer.py::test_daily_limit PASSED                   [ 44%]
tests/test_transfer.py::test_invalid_amount_zero PASSED           [ 55%]
tests/test_transfer.py::test_invalid_amount_precision PASSED      [ 66%]
tests/test_transfer.py::test_self_transfer PASSED                 [ 77%]
tests/test_transfer.py::test_account_not_found PASSED             [ 88%]
tests/test_transfer.py::test_transfer_to_non_existent_account PASSED [100%]

============================== 9 passed in 0.02s ===============================
```

---

## 🔑 SDD 核心概念

| 概念 | 说明 |
|------|------|
| **Spec-First** | 先定义规格，再写代码 |
| **Spec-Anchored** | 所有活动锚定在 Spec 上 |
| **Spec-as-Source** | Spec 是"黄金源码" |

### 对比传统方式

| 维度 | 传统开发 | SDD |
|------|----------|-----|
| 需求表达 | 自然语言，易产生歧义 | 形式化规格，精确 |
| 测试生成 | 依赖人工 | Spec 驱动自动生成 |
| 变更追溯 | 散落各处 | 统一从 Spec 追溯 |
| AI 辅助 | 不稳定 | 上下文准确，效果稳定 |

---

## 🏦 金融场景示例

这是一个完整的银行转账系统，包含：

- **账户管理** - 创建、查询、状态管理
- **转账交易** - 8条业务规则校验
- **异常处理** - 7种明确的错误类型

这些规则来自真实银行业务，适合演示 SDD 的价值。

---

## 🔗 相关资源

- 📚 [SDD 分享 PPT](https://github.com/chunchill/sdd-banking-kata/blob/main/SPEC.md)
- 🛠️ [Kiro 官网](https://kiro.ai)
- 🤖 [Kiro Spec 模式文档](https://docs.kiro.ai)

---

**Built with Kiro + SDD** | Thoughtworks SE Team | 2026