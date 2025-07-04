"""
Calculator and mathematical tools.
"""
import ast
import operator
import math
from typing import Dict, Any
from src.tools.base import Tool

class CalculatorTool(Tool):
    """Tool for mathematical calculations."""
    
    # Safe operations for evaluation
    _operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.BitXor: operator.xor,
        ast.USub: operator.neg,
    }
    
    @property
    def name(self) -> str:
        return "calculate"
    
    @property
    def description(self) -> str:
        return "Perform mathematical calculations safely"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate (e.g., '2 + 3 * 4', 'sqrt(16)', 'sin(3.14159/2)')"
                }
            },
            "required": ["expression"]
        }
    
    def _safe_eval(self, node):
        """Safely evaluate a mathematical expression."""
        if isinstance(node, ast.Num):  # Numbers
            return node.n
        elif isinstance(node, ast.Constant):  # Constants (Python 3.8+)
            return node.value
        elif isinstance(node, ast.BinOp):  # Binary operations
            return self._operators[type(node.op)](
                self._safe_eval(node.left), 
                self._safe_eval(node.right)
            )
        elif isinstance(node, ast.UnaryOp):  # Unary operations
            return self._operators[type(node.op)](self._safe_eval(node.operand))
        elif isinstance(node, ast.Call):  # Function calls
            func_name = node.func.id
            args = [self._safe_eval(arg) for arg in node.args]
            
            # Math functions
            if func_name == 'sqrt':
                return math.sqrt(args[0])
            elif func_name == 'sin':
                return math.sin(args[0])
            elif func_name == 'cos':
                return math.cos(args[0])
            elif func_name == 'tan':
                return math.tan(args[0])
            elif func_name == 'log':
                return math.log(args[0])
            elif func_name == 'log10':
                return math.log10(args[0])
            elif func_name == 'exp':
                return math.exp(args[0])
            elif func_name == 'abs':
                return abs(args[0])
            elif func_name == 'round':
                return round(args[0], args[1] if len(args) > 1 else 0)
            elif func_name == 'min':
                return min(args)
            elif func_name == 'max':
                return max(args)
            else:
                raise ValueError(f"Function '{func_name}' not allowed")
        elif isinstance(node, ast.Name):  # Constants like pi, e
            if node.id == 'pi':
                return math.pi
            elif node.id == 'e':
                return math.e
            else:
                raise ValueError(f"Name '{node.id}' not allowed")
        else:
            raise ValueError(f"Operation {type(node)} not allowed")
    
    async def execute(self, expression: str) -> str:
        """Calculate the result of a mathematical expression."""
        try:
            # Clean the expression
            expression = expression.strip()
            
            # Parse the expression
            node = ast.parse(expression, mode='eval')
            
            # Evaluate safely
            result = self._safe_eval(node.body)
            
            return f"{expression} = {result}"
            
        except ZeroDivisionError:
            return "Error: Division by zero"
        except ValueError as e:
            return f"Error: {str(e)}"
        except Exception as e:
            return f"Error evaluating expression: {str(e)}"
