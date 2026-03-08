"""
传统开发方式示例 - 对比 SDD
=====================================

注意：这是"传统方式"的代码，存在以下问题：
1. 业务规则散落在代码中，没有统一文档
2. 错误处理不完整
3. 边界情况考虑不足
4. AI 辅助时上下文不完整
"""

from datetime import datetime
from typing import Optional
import uuid


class AccountOld:
    """传统方式：账户类"""
    
    def __init__(self, name: str, initial: float = 0):
        self.id = f"ACC{str(uuid.uuid4().int)[:8]}"
        self.name = name
        self.balance = initial
        self.status = "ACTIVE"  # 没有枚举，直接字符串
        self.created = datetime.now()


def transfer_old(from_acc: AccountOld, to_acc: AccountOld, amount: float) -> dict:
    """
    传统方式：转账函数
    
    问题：
    1. 没有明确的业务规则文档
    2. 错误信息不统一
    3. 缺少必要的校验（如单笔限额、日限额）
    4. 返回值不规范
    """
    # 基本的校验
    if from_acc.balance < amount:
        return {"success": False, "error": "余额不足"}
    
    if amount <= 0:
        return {"success": False, "error": "金额错误"}
    
    if from_acc.id == to_acc.id:
        return {"success": False, "error": "不能转给自己"}
    
    # 执行转账
    from_acc.balance -= amount
    to_acc.balance += amount
    
    return {
        "success": True,
        "txn_id": f"TXN{str(uuid.uuid4().int)[:12]}",
        "from": from_acc.id,
        "to": to_acc.id,
        "amount": amount
    }


# ==================== SDD 方式的优势 ====================
#
# 1. SPEC.md 是单一事实源
#    - 所有业务规则明确列出
#    - 错误码统一规范
#    - 验收标准清晰
#
# 2. 测试驱动开发
#    - 每个 AC 对应一个测试用例
#    - 全面覆盖边界情况
#
# 3. AI 友好
#    - 给 AI 完整的 Spec，它能生成正确代码
#    - 不需要来回补充"遗漏的规则"
#
# 4. 可追溯
#    - 所有变更基于 Spec
#    - 便于审计和 review
#


if __name__ == "__main__":
    # 简单演示
    acc1 = AccountOld("张三", 1000)
    acc2 = AccountOld("李四", 0)
    
    result = transfer_old(acc1, acc2, 500)
    print(f"转账结果: {result}")
    print(f"张三余额: {acc1.balance}")
    print(f"李四余额: {acc2.balance}")