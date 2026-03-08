# Tasks - SDD Banking Kata

## Implementation Tasks

### Phase 1: Foundation

- [x] 1.1 Create project structure
- [x] 1.2 Set up .kiro configuration
- [x] 1.3 Write requirements.md
- [x] 1.4 Write design.md
- [ ] 1.5 Initialize git repository

### Phase 2: Domain Models

- [x] 2.1 Implement Account class
- [x] 2.2 Implement Transaction class
- [x] 2.3 Define enums (AccountType, AccountStatus, TransactionType, TransactionStatus)
- [ ] 2.4 Add validation to models

### Phase 3: Business Logic

- [x] 3.1 Implement BankingService
- [x] 3.2 Create account functionality
- [x] 3.3 Transfer functionality with all 8 rules
- [ ] 3.4 Daily limit tracking logic

### Phase 4: Error Handling

- [x] 4.1 Define BankingException base class
- [x] 4.2 Implement all 7 error types
- [ ] 4.3 Add error code mapping

### Phase 5: Testing

- [x] 5.1 AC-001: Successful transfer test
- [x] 5.2 AC-002: Insufficient balance test
- [x] 5.3 AC-003: Single transfer limit test
- [x] 5.4 AC-004: Daily limit test
- [x] 5.5 Additional edge case tests

### Phase 6: Documentation

- [x] 6.1 Create SPEC.md (single source of truth)
- [x] 6.2 Write README.md
- [ ] 6.3 Add code comments
- [ ] 6.4 Generate API documentation

---

## Progress

- [x] Domain Models
- [x] Business Logic  
- [x] Error Handling
- [x] Core Tests (9 tests passing)
- [ ] GitHub push

**Status**: Core implementation complete, ready for Kiro editor.

---

## Notes for Kiro Editor

1. Open the project folder in Kiro
2. Kiro will auto-detect `.kiro/specs/sdd-banking-kata/`
3. Use requirements.md as the source of truth
4. Design.md contains API and implementation details
5. Python code is in `src/` directory
6. Tests are in `tests/` directory

**Run Tests**: `pytest tests/ -v`