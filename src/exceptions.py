"""
SDD Banking Kata - 异常定义
对应 SPEC.md 3.3 节
"""

from typing import Optional


class BankingException(Exception):
    """银行系统基础异常"""
    def __init__(self, error_code: str, message: str):
        self.error_code = error_code
        self.message = message
        super().__init__(f"[{error_code}] {message}")


# 对应 SPEC.md 3.3 节的错误码定义
ERROR_MESSAGES = {
    "E001": "账户不存在",
    "E002": "账户已冻结",
    "E003": "余额不足",
    "E004": "金额无效",
    "E005": "超出单笔限额",
    "E006": "超出日限额",
    "E007": "不能转账给自己",
}


class AccountNotFoundError(BankingException):
    """E001: 账户不存在"""
    def __init__(self, account_id: str):
        super().__init__("E001", f"账户 {account_id} 不存在")


class AccountFrozenError(BankingException):
    """E002: 账户已冻结"""
    def __init__(self, account_id: str):
        super().__init__("E002", f"账户 {account_id} 已冻结")


class InsufficientBalanceError(BankingException):
    """E003: 余额不足"""
    def __init__(self, account_id: str, available: float, required: float):
        super().__init__(
            "E003", 
            f"账户 {account_id} 余额不足 (可用: {available}, 需要: {required})"
        )


class InvalidAmountError(BankingException):
    """E004: 金额无效"""
    def __init__(self, message: str = "金额必须大于0且精确到分"):
        super().__init__("E004", message)


class SingleTransferLimitError(BankingException):
    """E005: 超出单笔限额"""
    def __init__(self, amount: float, limit: float = 50000):
        super().__init__(
            "E005", 
            f"单笔转账金额 {amount} 超出限额 {limit}"
        )


class DailyLimitError(BankingException):
    """E006: 超出日限额"""
    def __init__(self, today_total: float, amount: float, limit: float = 100000):
        super().__init__(
            "E006",
            f"今日累计转账 {today_total + amount} 超出日限额 {limit}"
        )


class SelfTransferError(BankingException):
    """E007: 不能转账给自己"""
    def __init__(self):
        super().__init__("E007", "不能转账到自己账户")


def get_error_message(error_code: str) -> str:
    """根据错误码获取错误信息"""
    return ERROR_MESSAGES.get(error_code, "未知错误")