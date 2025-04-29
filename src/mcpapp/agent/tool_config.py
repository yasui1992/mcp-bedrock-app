from typing import TYPE_CHECKING

from mcp import Tool

if TYPE_CHECKING:
    from mypy_boto3_bedrock_runtime.type_defs import (
        ToolConfigurationTypeDef,
        ToolSpecificationTypeDef
    )


class ToolConfig:
    def __init__(self):
        self._tools: list[Tool] = []

    def set_tools(self, tools: list[Tool]):
        self._tools = tools

    def dump_to_converse_dict(self) -> "ToolConfigurationTypeDef":
        tool_specs: list["ToolSpecificationTypeDef"] = [
            {
                "name": tool.name,
                "description": tool.description or "",
                "inputSchema": {
                    "json": tool.inputSchema
                }
            }
            for tool in self._tools
        ]
        config: "ToolConfigurationTypeDef" = {
            "tools": [
                {"toolSpec": ts}
                for ts in tool_specs
            ]
        }

        return config
