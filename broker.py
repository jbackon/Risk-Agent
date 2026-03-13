import logging
from tools.base import Tool

class Broker:
    """A class to perform various tool calls depending on agent use case."""
    def __init__(self) -> None:
        self.registry = {}

    def register_tool(self, name: str, tool: Tool) -> None:
        """Adds an instance of a given tool to the registry to be called when needed."""
        if name not in self.registry:
            self.registry[name] = tool
        else:
            logging.info(f"Tool {name} already exists in the registry")

    async def dispatch(self, name: str, arguments: dict) -> dict:
        """Runs the 'named' tool and returns its output."""
        if name not in self.registry:
            raise KeyError("The requested tool does not exist in the registry.")
        else:
            active_tool = self.registry[name]
        output = await active_tool.execute(arguments)
        return output
        
        