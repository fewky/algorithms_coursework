from typing import Optional

class NodeType:
    NUMBER = 'num'
    UNARY_OPERATOR = 'op'
    BINARY_OPERATOR = 'op'

class Node:
    def __init__(self, node_type: str, value: Optional[str] = None):
        self.type = node_type  # 'num' для числа, 'op' для оператора
        self.value = value    # само число или оператор
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None