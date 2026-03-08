"""
SDD Banking Kata - 领域模型
严格按照 SPEC.md 定义实现
"""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional
import uuid


class AccountType(Enum):
    SAVINGS = "SAVINGS"      # 储蓄账户
    CHECKING = "CHECKING"    # 支票账户


class AccountStatus(Enum):
    ACTIVE = "ACTIVE"        # 正常
    FROZEN = "FROZEN"        # 冻结
    CLOSED = "CLOSED"        # 已关闭


class TransactionType(Enum):
    DEPOSIT = "DEPOSIT"      # 存款
    WITHDRAW = "WITHDRAW"    # 取款
    TRANSFER = "TRANSFER"    # 转账


class TransactionStatus(Enum):
    PENDING = "PENDING"      # 处理中
    COMPLETED = "COMPLETED"  # 已完成
    FAILED = "FAILED"        # 失败


@dataclass
class Account:
    """账户模型 - 对应 SPEC.md 2.1 节"""
    owner_name: str
    balance: Decimal = field(default=Decimal("0"))
    account_type: AccountType = AccountType.SAVINGS
    account_id: str = field(default="")
    status: AccountStatus = AccountStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.account_id:
            self.account_id = f"ACC{str(uuid.uuid4().int)[:8]}"
        self.balance = Decimal(str(self.balance))

    def can_transfer(self, amount: Decimal) -> tuple[bool, Optional[str]]:
        """
        检查是否可以转出指定金额
        返回: (是否可以, 错误信息)
        """
        if self.status != AccountStatus.ACTIVE:
            return False, "E002"  # 账户已冻结
        if self.balance < amount:
            return False, "E003"  # 余额不足
        return True, None


@dataclass
class Transaction:
    """交易模型 - 对应 SPEC.md 2.2 节"""
    from_account: str
    to_account: str
    amount: Decimal
    transaction_type: TransactionType = TransactionType.TRANSFER
    transaction_id: str = field(default="")
    status: TransactionStatus = TransactionStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = field(default=None)

    def __post_init__(self):
        if not self.transaction_id:
            self.transaction_id = f"TXN{str(uuid.uuid4().int)[:12]}"
        self.amount = Decimal(str(self.amount))

    def mark_completed(self):
        """标记交易完成"""
        self.status = TransactionStatus.COMPLETED
        self.completed_at = datetime.now()

    def mark_failed(self):
        """标记交易失败"""
        self.status = TransactionStatus.FAILED
        self.completed_at = datetime.now()