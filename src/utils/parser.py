"""
Parser for momentum twistor expressions.
Module handles parsing, tokenization, and manipulation of momentum twistor expressions.
"""
import re
from enum import Enum
from typing import List, Dict, Union, Tuple, Optional

class TokenType(Enum):
    """
    Types of tokens in momentum twistor expressions.
    """
    TWISTOR = "TWISTOR"
    DUAL_TWISTOR = "DUAL_TWISTOR"
    OPERATOR = "OPERATOR"
    NUMBER = "NUMBER"
    BRACKET_OPEN = "BRACKET_OPEN"
    BRACKET_CLOSE = "BRACKET_CLOSE"
    DOT = "DOT"
    INFINITY_TWISTOR = "INFINITY_TWISTOR"

class Token:
    """
    Represents a token in a momentum twistor expression.
    """
    def __init__(self, type : TokenType, value :str, indices :Optional[List[int]] = None):
        self.type = type
        self.value = value
        self.indices = indices or []
    
    def __repr__(self):
        if self.indices:
            return f"{self.type.value}({self.value}{self.indices})"
        return f"{self.type.value}({self.value})"
    
class ExpressionNode:
    """
    Base class for nodes in the expression tree.
    """
    def to_prefix_notation(self) -> List[str]:
        """
        Converts the node to prefix notation.
        """
        raise NotImplementedError("Subvlasses must implement to_prefix_notation")
    
    def to_string(self) -> str:
        """
        Convert to string representation.
        """
        raise NotImplementedError("Subclasses must implement to_string")

class OperatorNode(ExpressionNode):
    """
    Node representing an operator in the expression tree.
    """
    def __init__(self, op_type: str, operands: List[ExpressionNode]):
        self.op_type = op_type
        self.operands = operands
    
    def to_prefix_notation(self) -> List[str]:
        """
        Convert to prefix notation.
        """
        result = [self.op_type]
        for operand in self.operands:
            result.extend(operand.to_prefix_notation())
        return result
    
    def to_string(self) -> str:
        """
        Convert to string representation.
        """
        if self.op_type == 'add':
            return '(' + ' + '.join([operand.to_string() for operand in self.operands]) +')'
        elif self.op_type == 'sub':
            return f"({self.operands[0].to_string()} - {self.operands[1].to_string()})"
        elif self.op_type == 'mul':
            return ' * '.join([operand.to_string() for operand in self.operands])
        elif self.op_type == 'div':
            return f"({self.operands[0].to_string()} / {self.operands[1].to_string()})"
        elif self.op_type == 'pow':
            return f"({self.operands[0].to_string()}^{self.operands[1].to_string()})"
        else:
            return f"{self.op_type}({', '.join([operand.to_string() for operand in self.operands])})"