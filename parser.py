from typing import Tuple, List, Optional
from tree import Node

class ExpressionTree:
    def __init__(self):
        self.operators = {
            '+': 1, '-': 1,
            '*': 2, '/': 2,
            '^': 3,
            'u-': 4
        }
        self.right_associative = {'^'}
    
    def get_priority(self, op: str) -> int:
        return self.operators.get(op, 0)
    
    def is_right_associative(self, op: str) -> bool:
        return op in self.right_associative
    
    def is_operator(self, char: str) -> bool:
        return char in '+-*/^'
    
    def is_digit(self, char: str) -> bool:
        return char.isdigit()
    
    def is_single_number(self, expr: str) -> bool:
        expr = expr.replace(' ', '')
        
        if not expr:
            return False
        
        if expr.isdigit():
            return True
        
        if len(expr) > 1 and expr[0] == '-' and expr[1:].isdigit():
            return True
        
        if len(expr) >= 3 and expr[0] == '(' and expr[-1] == ')':
            inner = expr[1:-1]
            if inner.isdigit():
                return True
            if len(inner) > 1 and inner[0] == '-' and inner[1:].isdigit():
                return True
        
        return False
    
    def has_operators(self, expr: str) -> bool:
        operators = '+-*/^'
        return any(op in expr for op in operators)
    
    def validate_parentheses(self, expr: str) -> Tuple[bool, str]:
        expr_no_spaces = expr.replace(' ', '')
        
        if '()' in expr_no_spaces:
            return False, "Пустые скобки () не допускаются"
        
        bracket_count = 0
        for char in expr_no_spaces:
            if char == '(':
                bracket_count += 1
            elif char == ')':
                bracket_count -= 1
                if bracket_count < 0:
                    return False, "Несогласованные скобки"
        
        if bracket_count > 0:
            return False, "Незакрытые скобки"
        
        for i in range(len(expr_no_spaces) - 1):
            if (expr_no_spaces[i].isdigit() or expr_no_spaces[i] == ')') and expr_no_spaces[i+1] == '(':
                return False, "Отсутствует оператор перед скобкой"
            
            if expr_no_spaces[i] == ')' and expr_no_spaces[i+1].isdigit():
                return False, "Отсутствует оператор после скобки"
        
        return True, "OK"
    
    def validate_expression(self, expr: str) -> Tuple[bool, str]:
        if self.is_single_number(expr):
            return False, "Введено только число. Пожалуйста, введите выражение с операторами (например: 2+3, 4*5, -2+3)"
        
        expr_no_spaces = expr.replace(' ', '')
        
        if not expr_no_spaces:
            return False, "Пустое выражение"
        
        if not self.has_operators(expr_no_spaces):
            has_multiple_numbers = False
            i = 0
            while i < len(expr_no_spaces):
                if expr_no_spaces[i].isdigit():
                    while i < len(expr_no_spaces) and expr_no_spaces[i].isdigit():
                        i += 1
                    j = i
                    while j < len(expr_no_spaces) and not expr_no_spaces[j].isdigit():
                        j += 1
                    if j < len(expr_no_spaces) and expr_no_spaces[j].isdigit():
                        has_multiple_numbers = True
                        break
                else:
                    i += 1
            
            if has_multiple_numbers:
                return False, "Не найдены операторы между числами. Пожалуйста, используйте операторы (+, -, *, /, ^)"
        
        allowed_chars = set('0123456789+-*/^() ')
        for char in expr:
            if char not in allowed_chars:
                return False, "Недопустимый символ в выражении"
        
        is_valid_parentheses, parent_error = self.validate_parentheses(expr)
        if not is_valid_parentheses:
            return False, parent_error
        
        for i in range(len(expr_no_spaces) - 1):
            if (self.is_operator(expr_no_spaces[i]) and self.is_operator(expr_no_spaces[i+1]) and 
                not (expr_no_spaces[i+1] == '-' and (i == 0 or expr_no_spaces[i] == '(' or self.is_operator(expr_no_spaces[i])))):
                return False, "Два оператора подряд"
        
        if self.is_operator(expr_no_spaces[-1]):
            return False, "Выражение не может заканчиваться оператором"
        
        if self.is_operator(expr_no_spaces[0]) and expr_no_spaces[0] != '-':
            return False, "Выражение не может начинаться с бинарного оператора"
        
        for i in range(len(expr_no_spaces) - 1):
            if self.is_operator(expr_no_spaces[i]) and expr_no_spaces[i+1] == ')':
                return False, "Закрывающая скобка после оператора"
        
        for i in range(len(expr_no_spaces) - 1):
            if expr_no_spaces[i] == '(' and self.is_operator(expr_no_spaces[i+1]) and expr_no_spaces[i+1] != '-':
                return False, "Бинарный оператор после открывающей скобки"
        
        return True, "OK"
    
    def tokenize(self, expr: str) -> List[str]:
        tokens = []
        i = 0
        expr = expr.replace(' ', '')
        n = len(expr)
        
        while i < n:
            if self.is_digit(expr[i]):
                num = ''
                while i < n and self.is_digit(expr[i]):
                    num += expr[i]
                    i += 1
                tokens.append(num)
                continue
            elif expr[i] == '-':
                if i == 0 or expr[i-1] == '(' or (i > 0 and self.is_operator(expr[i-1])):
                    tokens.append('u-')
                else:
                    tokens.append('-')
            else:
                tokens.append(expr[i])
            i += 1
        
        return tokens
    
    def build_tree(self, tokens: List[str]) -> Node:
        if not tokens:
            return None
        
        values = []
        ops = []
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if token.isdigit() or (token[0] == '-' and token[1:].isdigit()):
                values.append(Node('num', int(token)))
            
            elif token == '(':
                ops.append('(')
            
            elif token == ')':
                while ops and ops[-1] != '(':
                    self.apply_operator(ops, values)
                ops.pop()
            
            elif token in self.operators:
                current_priority = self.get_priority(token)
                current_is_right_assoc = self.is_right_associative(token)
                
                while (ops and ops[-1] != '('):
                    top_op = ops[-1]
                    top_priority = self.get_priority(top_op)
                    
                    if current_is_right_assoc:
                        if top_priority > current_priority:
                            self.apply_operator(ops, values)
                        else:
                            break
                    else:
                        if top_priority >= current_priority:
                            self.apply_operator(ops, values)
                        else:
                            break
                
                ops.append(token)
            
            i += 1
        
        while ops:
            self.apply_operator(ops, values)
        
        return values[0] if values else None
    
    def apply_operator(self, ops: List[str], values: List[Node]):
        if not ops:
            return
        
        op = ops.pop()
        
        if op == 'u-':
            if not values:
                raise ValueError("Недостаточно операндов для унарного минуса")
            operand = values.pop()
            node = Node('op', 'u-')
            node.right = operand
            values.append(node)
        else:
            if len(values) < 2:
                raise ValueError(f"Недостаточно операндов для оператора {op}")
            right = values.pop()
            left = values.pop()
            node = Node('op', op)
            node.left = left
            node.right = right
            values.append(node)
    
    def evaluate(self, node: Node) -> float:
        if node is None:
            return 0
        
        if node.type == 'num':
            return float(node.value)
        
        if node.value == 'u-':
            return -self.evaluate(node.right)
        
        left_val = self.evaluate(node.left)
        right_val = self.evaluate(node.right)
        
        if node.value == '+':
            return left_val + right_val
        elif node.value == '-':
            return left_val - right_val
        elif node.value == '*':
            return left_val * right_val
        elif node.value == '/':
            if right_val == 0:
                raise ZeroDivisionError("Деление на ноль")
            return left_val / right_val
        elif node.value == '^':
            return left_val ** right_val
        
        raise ValueError(f"Неизвестный оператор: {node.value}")
    
    def to_infix(self, node: Node, parent_op: str = None) -> str:
        if node is None:
            return ""
        
        if node.type == 'num':
            return str(node.value)
        
        if node.value == 'u-':
            return f"(-{self.to_infix(node.right)})"
        
        left_str = self.to_infix(node.left, node.value)
        right_str = self.to_infix(node.right, node.value)
        
        if node.value == '^':
            if (hasattr(node.right, 'value') and node.right.type == 'op' and 
                self.get_priority(node.right.value) >= self.get_priority(node.value)):
                right_str = f"({right_str})"
            
            if parent_op and self.get_priority(node.value) < self.get_priority(parent_op):
                return f"({left_str} {node.value} {right_str})"
        
        result = f"{left_str} {node.value} {right_str}"
        
        if (parent_op and node.value != '^' and 
            self.get_priority(node.value) < self.get_priority(parent_op)):
            result = f"({result})"
        
        return result
    
    def to_prefix(self, node: Node) -> str:
        if node is None:
            return ""
        
        if node.type == 'num':
            return str(node.value)
        
        if node.value == 'u-':
            return f"- {self.to_prefix(node.right)}"
        
        left_str = self.to_prefix(node.left)
        right_str = self.to_prefix(node.right)
        
        return f"{node.value} {left_str} {right_str}"
    
    def to_postfix(self, node: Node) -> str:
        if node is None:
            return ""
        
        if node.type == 'num':
            return str(node.value)
        
        if node.value == 'u-':
            return f"{self.to_postfix(node.right)} -"
        
        left_str = self.to_postfix(node.left)
        right_str = self.to_postfix(node.right)
        
        return f"{left_str} {right_str} {node.value}"