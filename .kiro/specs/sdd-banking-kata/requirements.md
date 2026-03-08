# Requirements - SDD Banking Kata

## 1. Project Overview

**Project Name**: SDD Banking Kata  
**Type**: Financial Core System Demo  
**Core Function**: Bank Account Management & Transfers  
**Target Users**: Bank IT, Architects, Executives

---

## 2. Domain Model

### 2.1 Account

| Field | Type | Description |
|-------|------|-------------|
| account_id | string | Unique ID (format: ACC + 8 digits) |
| owner_name | string | Account holder name |
| balance | decimal | Balance (unit: yuan, precision: cent) |
| account_type | enum | SAVINGS, CHECKING |
| status | enum | ACTIVE, FROZEN, CLOSED |
| created_at | datetime | Creation timestamp |

### 2.2 Transaction

| Field | Type | Description |
|-------|------|-------------|
| transaction_id | string | Unique ID (format: TXN + 12 digits) |
| from_account | string | Source account ID |
| to_account | string | Target account ID |
| amount | decimal | Transaction amount |
| type | enum | DEPOSIT, WITHDRAW, TRANSFER |
| status | enum | PENDING, COMPLETED, FAILED |
| created_at | datetime | Creation timestamp |
| completed_at | datetime | Completion timestamp |

---

## 3. Business Rules

### 3.1 Account Creation

1. Account ID must be unique, auto-generated
2. Owner name cannot be empty
3. Initial balance cannot be negative
4. Default status is ACTIVE

### 3.2 Transfer Rules

```
RULE-001: Amount must be greater than 0
RULE-002: Source account must exist and be ACTIVE
RULE-003: Target account must exist and be ACTIVE
RULE-004: Source account must have sufficient balance
RULE-005: Cannot transfer to same account
RULE-006: Single transfer limit is 50,000 yuan
RULE-007: Daily cumulative limit is 100,000 yuan
RULE-008: Amount must be multiple of 0.01 (cents)
```

### 3.3 Error Codes

| Code | Description |
|------|-------------|
| E001 | Account not found |
| E002 | Account frozen |
| E003 | Insufficient balance |
| E004 | Invalid amount |
| E005 | Exceeds single transfer limit |
| E006 | Exceeds daily limit |
| E007 | Cannot transfer to self |

---

## 4. Acceptance Criteria

### AC-001: Successful Transfer

```
Given Account A has 1000 yuan, Account B has 0 yuan
When Transfer 500 yuan from A to B
Then Account A has 500 yuan
And Account B has 500 yuan
And Transaction status is COMPLETED
```

### AC-002: Insufficient Balance

```
Given Account A has 100 yuan, Account B has 0 yuan
When Transfer 200 yuan from A to B
Then Transfer fails
And Error code is E003
And Account A still has 100 yuan
And Account B still has 0 yuan
```

### AC-003: Single Transfer Limit

```
Given Account A has 100000 yuan, Account B has 0 yuan
When Transfer 60000 yuan from A to B
Then Transfer fails
And Error code is E005
```

### AC-004: Daily Limit

```
Given Account A has 200000 yuan, Account B has 0 yuan
And Already transferred 80000 yuan today
When Transfer 30000 yuan from A to B
Then Transfer fails
And Error code is E006
```