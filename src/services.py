"""
SDD Banking Kata - 业务服务层
严格按照 SPEC.md 第3节业务规则实现
"""

from decimal import Decimal
from datetime import datetime, date
from typing import Dict, List
from collections import defaultdict

from src.models import (
    Account, Transaction, 
    AccountType, AccountStatus,
    TransactionType, TransactionStatus
)
from src.exceptions import (
    BankingException,
    AccountNotFoundError, AccountFrozenError,
    InsufficientBalanceError, InvalidAmountError,
    SingleTransferLimitError, DailyLimitError, SelfTransferError
)


# SPEC.md 定义的常量
MAX_SINGLE_TRANSFER = Decimal("50000")      # 单笔转账上限
MAX_DAILY_TRANSFER = Decimal("100000")      # 日累计转账限额
AMOUNT_PRECISION = Decimal("0.01")          # 金额精度（分）


class BankingService:
    """银行核心服务 - 实现 SPEC.md 规定的全部业务规则"""

    def __init__(self):
        # 账户存储: account_id -> Account
        self._accounts: Dict[str, Account] = {}
        
        # 交易记录: account_id -> List[Transaction]
        self._transactions: Dict[str, List[Transaction]] = defaultdict(list)
        
        # 日累计转账: account_id -> date -> amount
        self._daily_limits: Dict[str, Dict[date, Decimal]] = defaultdict(dict)

    # ==================== 账户操作 ====================

    def create_account(
        self, 
        owner_name: str, 
        initial_balance: float,
        account_type: AccountType = AccountType.SAVINGS
    ) -> Account:
        """
        创建账户 - 对应 SPEC.md 3.1 节
        
        RULE-001: 账户ID必须唯一，自动生成
        RULE-002: 持卡人姓名不能为空
        RULE-003: 初始余额不能为负数
        RULE-004: 储蓄账户默认 ACTIVE 状态
        """
        # RULE-002: 持卡人姓名不能为空
        if not owner_name or not owner_name.strip():
            raise InvalidAmountError("持卡人姓名不能为空")
        
        # RULE-003: 初始余额不能为负数
        balance = Decimal(str(initial_balance))
        if balance < 0:
            raise InvalidAmountError("初始余额不能为负数")
        
        # 创建账户
        account = Account(
            owner_name=owner_name.strip(),
            balance=balance,
            account_type=account_type,
            status=AccountStatus.ACTIVE
        )
        
        self._accounts[account.account_id] = account
        return account

    def get_account(self, account_id: str) -> Account:
        """查询账户 - 对应 SPEC.md 4.2 节"""
        if account_id not in self._accounts:
            raise AccountNotFoundError(account_id)
        return self._accounts[account_id]

    # ==================== 转账操作 ====================

    def transfer(
        self, 
        from_account_id: str, 
        to_account_id: str, 
        amount: float
    ) -> Transaction:
        """
        转账操作 - 对应 SPEC.md 3.2 节业务规则
        
        RULE-001: 转账金额必须大于0
        RULE-002: 转出账户必须存在且状态为 ACTIVE
        RULE-003: 转入账户必须存在且状态为 ACTIVE
        RULE-004: 转出账户余额必须足够
        RULE-005: 转出账户和转入账户不能相同
        RULE-006: 单笔转账金额上限为 50,000 元
        RULE-007: 单日累计转账限额为 100,000 元
        RULE-008: 转账金额必须是 0.01 的倍数
        """
        # ===== 基础验证 =====
        
        amount_dec = Decimal(str(amount))
        
        # RULE-001: 转账金额必须大于0
        if amount_dec <= 0:
            raise InvalidAmountError("转账金额必须大于0")
        
        # RULE-008: 转账金额必须是 0.01 的倍数
        if amount_dec % AMOUNT_PRECISION != 0:
            raise InvalidAmountError("转账金额必须精确到分")
        
        # RULE-005: 转出账户和转入账户不能相同
        if from_account_id == to_account_id:
            raise SelfTransferError()
        
        # ===== 账户验证 =====
        
        # RULE-002: 转出账户必须存在且状态为 ACTIVE
        from_account = self._get_active_account(from_account_id)
        
        # RULE-003: 转入账户必须存在且状态为 ACTIVE
        to_account = self._get_active_account(to_account_id)
        
        # RULE-006: 单笔转账金额上限
        if amount_dec > MAX_SINGLE_TRANSFER:
            raise SingleTransferLimitError(float(amount_dec), float(MAX_SINGLE_TRANSFER))
        
        # RULE-007: 单日累计转账限额
        today = date.today()
        today_total = self._get_daily_total(from_account_id, today)
        if today_total + amount_dec > MAX_DAILY_TRANSFER:
            raise DailyLimitError(
                float(today_total), 
                float(amount_dec), 
                float(MAX_DAILY_TRANSFER)
            )
        
        # RULE-004: 转出账户余额必须足够
        if from_account.balance < amount_dec:
            raise InsufficientBalanceError(
                from_account_id,
                float(from_account.balance),
                float(amount_dec)
            )
        
        # ===== 执行转账 =====
        
        # 创建交易记录
        transaction = Transaction(
            from_account=from_account_id,
            to_account=to_account_id,
            amount=amount_dec,
            transaction_type=TransactionType.TRANSFER
        )
        
        # 更新余额
        from_account.balance -= amount_dec
        to_account.balance += amount_dec
        
        # 标记完成
        transaction.mark_completed()
        
        # 保存记录
        self._transactions[from_account_id].append(transaction)
        self._transactions[to_account_id].append(transaction)
        
        # 更新日累计
        self._daily_limits[from_account_id][today] = today_total + amount_dec
        
        return transaction

    # ==================== 辅助方法 ====================

    def _get_active_account(self, account_id: str) -> Account:
        """获取活跃账户"""
        if account_id not in self._accounts:
            raise AccountNotFoundError(account_id)
        
        account = self._accounts[account_id]
        if account.status != AccountStatus.ACTIVE:
            raise AccountFrozenError(account_id)
        
        return account

    def _get_daily_total(self, account_id: str, day: date) -> Decimal:
        """获取指定日期的累计转账金额"""
        return self._daily_limits.get(account_id, {}).get(day, Decimal("0"))

    def get_transactions(self, account_id: str) -> List[Transaction]:
        """获取账户的所有交易记录"""
        return self._transactions.get(account_id, [])

    def get_balance(self, account_id: str) -> float:
        """获取账户余额（便捷方法）"""
        account = self.get_account(account_id)
        return float(account.balance)