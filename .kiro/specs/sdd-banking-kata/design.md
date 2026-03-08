# Design - SDD Banking Kata

## API Specification

### 4.1 Create Account

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

### 4.2 Get Account

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

### 4.3 Transfer

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

## Implementation Design

### Technology Stack

- **Language**: Python 3.10+
- **Testing**: pytest
- **Validation**: pydantic

### Project Structure

```
src/
├── models.py       # Account, Transaction classes
├── services.py     # BankingService
├── exceptions.py   # Custom exceptions
└── __init__.py

tests/
├── test_transfer.py  # All AC test cases
└── __init__.py
```

### Key Classes

#### Account
- Auto-generates account_id in format ACCxxxxxxxx
- Supports balance operations
- Status management (ACTIVE/FROZEN/CLOSED)

#### Transaction  
- Auto-generates transaction_id in format TXNxxxxxxxxxxxx
- Tracks status (PENDING → COMPLETED/FAILED)

#### BankingService
- `create_account()` - Create new account
- `get_account()` - Query account by ID
- `transfer()` - Execute transfer with all rules validation

### Error Handling

All errors raise custom exceptions with error codes:
- `AccountNotFoundError` (E001)
- `AccountFrozenError` (E002)
- `InsufficientBalanceError` (E003)
- `InvalidAmountError` (E004)
- `SingleTransferLimitError` (E005)
- `DailyLimitError` (E006)
- `SelfTransferError` (E007)

---

## SDD Implementation Notes

### Spec-First Principles

1. All business rules must be defined in requirements.md
2. Code implementation only after spec review
3. Spec document is the "Single Source of Truth"

### Traditional vs SDD

| Aspect | Traditional | SDD |
|--------|-------------|-----|
| Requirements | Natural language, ambiguous | Formal spec, precise |
| Testing | Manual, experience-dependent | Spec-driven auto-generation |
| Traceability | Scattered in code comments | Unified from spec |
| AI Assistance | Unstable, context-dependent | Spec provides accurate context |

---

*Version: 1.0.0 | Updated: 2026-03-08*