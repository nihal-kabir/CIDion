"""
Test the tool system.
"""
import pytest
from src.tools import create_tool_manager
from src.tools.calculator import CalculatorTool

@pytest.mark.asyncio
async def test_tool_manager_creation():
    """Test tool manager creation and registration."""
    manager = create_tool_manager()
    
    # Check that tools are registered
    assert len(manager.tools) > 0
    assert "calculate" in manager.tools
    assert "read_file" in manager.tools
    assert "web_search" in manager.tools

@pytest.mark.asyncio
async def test_calculator_tool():
    """Test the calculator tool."""
    calc = CalculatorTool()
    
    # Test basic calculation
    result = await calc.execute(expression="2 + 3")
    assert "2 + 3 = 5" in result
    
    # Test mathematical functions
    result = await calc.execute(expression="sqrt(16)")
    assert "sqrt(16) = 4" in result
    
    # Test error handling
    result = await calc.execute(expression="1 / 0")
    assert "Error: Division by zero" in result

@pytest.mark.asyncio
async def test_tool_execution():
    """Test tool execution through manager."""
    manager = create_tool_manager()
    
    # Test calculator execution
    result = await manager.execute_tool("calculate", {"expression": "10 * 5"})
    assert "10 * 5 = 50" in result
    
    # Test invalid tool
    with pytest.raises(ValueError):
        await manager.execute_tool("invalid_tool", {})
