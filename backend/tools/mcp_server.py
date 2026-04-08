from typing import Dict, Any, List
import json


class MCPToolServer:
    """
    Implements Model Context Protocol for tool integration
    Manages calendar, tasks, notes, and other external tools
    """
    
    def __init__(self):
        self.tools = {}
        self.tool_schemas = {}
    
    def register_tool(self, name: str, tool_class, schema: Dict[str, Any]):
        """Register MCP tool"""
        self.tools[name] = tool_class()
        self.tool_schemas[name] = schema
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Return list of available tools in MCP format"""
        return [
            {
                "name": name,
                "description": schema.get("description"),
                "inputSchema": schema.get("inputSchema")
            }
            for name, schema in self.tool_schemas.items()
        ]
    
    async def execute_tool(self, tool_name: str, input_params: Dict[str, Any]) -> Any:
        """Execute tool with given parameters"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found")
        
        tool = self.tools[tool_name]
        
        # Call appropriate method based on tool type
        method_name = input_params.pop("method", "execute")
        method = getattr(tool, method_name, None)
        
        if not method:
            raise ValueError(f"Method {method_name} not found in {tool_name}")
        
        return await method(**input_params)
    
    def get_tool_schema(self, tool_name: str) -> Dict[str, Any]:
        """Get tool schema for agent context"""
        return self.tool_schemas.get(tool_name, {})
