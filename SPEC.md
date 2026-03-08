# SDD Banking Kata - 银行转账系统规格说明书

## 1. 项目概述

**项目名称**: SDD Banking Kata  
**项目类型**: 金融核心系统演示  
**核心功能**: 银行账户管理与转账  
**目标用户**: 银行技术人员、架构师、高管

---

## 2. 核心概念 (Domain Model)

### 2.1 账户 (Account)

| 字段 | 类型 | 说明 |
|------|------|------|
| account_id | string | 唯一账户ID (格式: ACC + 8位数字) |
| owner_name | string | 持卡人姓名 |
| balance | decimal | 账户余额 (单位: 元，精确到分) |
| account_type | enum | 账户类型: SAVINGS(储蓄), CHECKING(支票) |
| status | enum | 账户状态: ACTIVE, FROZEN, CLOSED |
| created_at | datetime | 创建时间 |

### 2.2 交易 (Transaction)

| 字段 | 类型 | 说明 |
|------|------|------|
| transaction_id | string | 交易ID (格式: TXN + 12位数字) |
| from_account | string | 转出账户ID |
| to_account | string | 转入账户ID |
| amount | decimal | 交易金额 |
| type | enum | 交易类型: DEPOSIT, WITHDRAW, TRANSFER |
| status | enum | 状态: PENDING, COMPLETED, FAILED |
| created_at | datetime | 创建时间 |
| completed_at | datetime | 完成时间 |

---

## 3. 核心业务规则 (Business Rules)

### 3.1 开户规则

1. 账户ID必须唯一，自动生成
2. 持卡人姓名不能为空
3. 初始余额不能为负数
4. 储蓄账户默认 ACTIVE 状态

### 3.2 转账规则 (核心场景)

```
RULE-001: 转账金额必须大于0
RULE-002: 转出账户必须存在且状态为 ACTIVE
RULE-003: 转入账户必须存在且状态为 ACTIVE  
RULE-004: 转出账户余额必须足够 (balance >= amount)
RULE-005: 转出账户和转入账户不能相同
RULE-006: 单笔转账金额上限为 50,000 元
RULE-007: 单日累计转账限额为 100,000 元
RULE-008: 转账金额必须是 0.01 的倍数 (精确到分)
```

### 3.3 异常处理

| 错误码 | 说明 |
|--------|------|
| E001 | 账户不存在 |
| E002 | 账户已冻结 |
| E003 | 余额不足 |
| E004 | 金额无效 |
| E005 | 超出单笔限额 |
| E006 | 超出日限额 |
| E007 | 不能转账给自己 |

---

## 4. 接口规范 (API)

### 4.1 创建账户

```yaml
POST /api/accounts
Request:
  - owner_name: string (required)
  - initial_balance: decimal (required, >= 0)
  - account_type: enum (required)

Response:
  - account_id: string
  - owner_name: string
  - balance: decimal
  - account_type: string
  - status: string
  - created_at: datetime
```

### 4.2 查询账户

```yaml
GET /api/accounts/{account_id}

Response:
  - account_id: string
  - owner_name: string
  - balance: decimal
  - account_type: string
  - status: string
  - created_at: datetime
```

### 4.3 转账

```yaml
POST /api/transfers
Request:
  - from_account: string (required)
  - to_account: string (required)
  - amount: decimal (required, > 0)

Response:
  - transaction_id: string
  - from_account: string
  - to_account: string
  - amount: decimal
  - status: string
  - created_at: datetime
```

---

## 5. 验收标准 (Acceptance Criteria)

### AC-001: 成功转账

```
Given 账户A余额为1000元，账户B余额为0元
When 从账户A转账500元到账户B
Then 账户A余额为500元
And 账户B余额为500元
And 产生一条COMPLETED状态的交易记录
```

### AC-002: 余额不足

```
Given 账户A余额为100元，账户B余额为0元
When 从账户A转账200元到账户B
Then 转账失败
And 错误码为 E003 (余额不足)
And 账户A余额仍为100元
And 账户B余额仍为0元
```

### AC-003: 单笔限额

```
Given 账户A余额为100000元，账户B余额为0元
When 从账户A转账60000元到账户B
Then 转账失败
And 错误码为 E005 (超出单笔限额)
```

### AC-004: 日累计限额

```
Given 账户A余额为200000元，账户B余额为0元
And 当日已转账80000元
When 从账户A转账30000元到账户B
Then 转账失败
And 错误码为 E006 (超出日限额)
```

---

## 6. SDD 实施要点

### 6.1 Spec-First 原则

1. 所有业务规则必须在 SPEC.md 中明确定义
2. 代码实现前必须通过规格评审
3. 规格文档是唯一的"黄金源码"

### 6.2 关键差异 - 传统 vs SDD

| 维度 | 传统方式 | SDD 方式 |
|------|----------|----------|
| 需求传递 | 自然语言文档，易丢失 | 形式化 Spec，精确无歧义 |
| 测试覆盖 | 依赖测试人员经验 | Spec 驱动自动生成测试 |
| 变更追溯 | 散落在代码注释中 | 统一从 Spec 追溯 |
| AI 辅助 | 效果不稳定 | Spec 提供准确上下文 |

---

## 7. 技术栈

- **语言**: Python 3.10+
- **测试框架**: pytest
- **验证**: pydantic
- **AI工具**: 支持 Kiro, Cursor, Claude Code

---

*本文档遵循 SDD 原则，是项目的唯一事实源*
*版本: v1.0.0 | 更新日期: 2026-03-08*