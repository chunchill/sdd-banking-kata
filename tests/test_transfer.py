"""
SDD Banking Kata - 测试
对应 SPEC.md 第5节验收标准
"""

import pytest
from decimal import Decimal
from datetime import date

from src.services import BankingService
from src.models import AccountType, TransactionStatus
from src.exceptions import (
    AccountNotFoundError, AccountFrozenError,
    InsufficientBalanceError, InvalidAmountError,
    SingleTransferLimitError, DailyLimitError, SelfTransferError
)


@pytest.fixture
def banking_service():
    """创建银行服务实例"""
    return BankingService()


@pytest.fixture
def two_accounts(banking_service):
    """创建两个测试账户"""
    acc_a = banking_service.create_account(
        owner_name="张三",
        initial_balance=1000,
        account_type=AccountType.SAVINGS
    )
    acc_b = banking_service.create_account(
        owner_name="李四",
        initial_balance=0,
        account_type=AccountType.SAVINGS
    )
    return acc_a, acc_b


# ==================== AC-001: 成功转账 ====================

def test_successful_transfer(banking_service, two_accounts):
    """
    AC-001: 成功转账
    
    Given 账户A余额为1000元，账户B余额为0元
    When 从账户A转账500元到账户B
    Then 账户A余额为500元
    And 账户B余额为500元
    And 产生一条COMPLETED状态的交易记录
    """
    acc_a, acc_b = two_accounts
    
    # 执行转账
    transaction = banking_service.transfer(
        from_account_id=acc_a.account_id,
        to_account_id=acc_b.account_id,
        amount=500
    )
    
    # 验证余额
    assert banking_service.get_balance(acc_a.account_id) == 500
    assert banking_service.get_balance(acc_b.account_id) == 500
    
    # 验证交易状态
    assert transaction.status == TransactionStatus.COMPLETED
    assert transaction.from_account == acc_a.account_id
    assert transaction.to_account == acc_b.account_id
    assert transaction.amount == Decimal("500")


# ==================== AC-002: 余额不足 ====================

def test_insufficient_balance(banking_service, two_accounts):
    """
    AC-002: 余额不足
    
    Given 账户A余额为100元，账户B余额为0元
    When 从账户A转账200元到账户B
    Then 转账失败
    And 错误码为 E003 (余额不足)
    And 账户A余额仍为100元
    And 账户B余额仍为0元
    """
    acc_a, acc_b = two_accounts
    
    # 修改余额
    acc_a.balance = Decimal("100")
    
    # 尝试转账
    with pytest.raises(InsufficientBalanceError) as exc_info:
        banking_service.transfer(
            from_account_id=acc_a.account_id,
            to_account_id=acc_b.account_id,
            amount=200
        )
    
    assert exc_info.value.error_code == "E003"
    
    # 验证余额未变
    assert banking_service.get_balance(acc_a.account_id) == 100
    assert banking_service.get_balance(acc_b.account_id) == 0


# ==================== AC-003: 单笔限额 ====================

def test_single_transfer_limit(banking_service, two_accounts):
    """
    AC-003: 单笔限额
    
    Given 账户A余额为100000元，账户B余额为0元
    When 从账户A转账60000元到账户B
    Then 转账失败
    And 错误码为 E005 (超出单笔限额)
    """
    acc_a, acc_b = two_accounts
    
    acc_a.balance = Decimal("100000")
    
    with pytest.raises(SingleTransferLimitError) as exc_info:
        banking_service.transfer(
            from_account_id=acc_a.account_id,
            to_account_id=acc_b.account_id,
            amount=60000
        )
    
    assert exc_info.value.error_code == "E005"


# ==================== AC-004: 日累计限额 ====================

def test_daily_limit(banking_service, two_accounts):
    """
    AC-004: 日累计限额
    
    Given 账户A余额为200000元，账户B余额为0元
    And 当日已转账80000元
    When 从账户A转账30000元到账户B
    Then 转账失败
    And 错误码为 E006 (超出日限额)
    """
    acc_a, acc_b = two_accounts
    
    acc_a.balance = Decimal("200000")
    
    # 模拟当日已转账 80000
    from src.services import MAX_SINGLE_TRANSFER
    # 先转 80000 (分成两笔)
    banking_service.transfer(acc_a.account_id, acc_b.account_id, 50000)
    banking_service.transfer(acc_a.account_id, acc_b.account_id, 30000)
    
    # 重置以便测试
    acc_a.balance = Decimal("200000")
    
    # 尝试再转 30000
    with pytest.raises(DailyLimitError) as exc_info:
        banking_service.transfer(
            from_account_id=acc_a.account_id,
            to_account_id=acc_b.account_id,
            amount=30000
        )
    
    assert exc_info.value.error_code == "E006"


# ==================== 其他规则测试 ====================

def test_invalid_amount_zero(banking_service, two_accounts):
    """RULE-001: 金额必须大于0"""
    acc_a, acc_b = two_accounts
    
    with pytest.raises(InvalidAmountError):
        banking_service.transfer(
            from_account_id=acc_a.account_id,
            to_account_id=acc_b.account_id,
            amount=0
        )


def test_invalid_amount_precision(banking_service, two_accounts):
    """RULE-008: 金额必须精确到分"""
    acc_a, acc_b = two_accounts
    
    with pytest.raises(InvalidAmountError):
        banking_service.transfer(
            from_account_id=acc_a.account_id,
            to_account_id=acc_b.account_id,
            amount=100.001  # 不是分倍数
        )


def test_self_transfer(banking_service, two_accounts):
    """RULE-005: 不能转账给自己"""
    acc_a, _ = two_accounts
    
    with pytest.raises(SelfTransferError):
        banking_service.transfer(
            from_account_id=acc_a.account_id,
            to_account_id=acc_a.account_id,
            amount=100
        )


def test_account_not_found(banking_service):
    """E001: 账户不存在"""
    with pytest.raises(AccountNotFoundError):
        banking_service.get_account("ACC00000000")


def test_transfer_to_non_existent_account(banking_service, two_accounts):
    """转出到不存在的账户"""
    acc_a, _ = two_accounts
    
    with pytest.raises(AccountNotFoundError):
        banking_service.transfer(
            from_account_id=acc_a.account_id,
            to_account_id="ACC99999999",
            amount=100
        )