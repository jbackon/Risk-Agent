"""The class that defines the tool for reading the contents of a OneDrive file 
    and returns the contents as a text string."""

from .base import Tool
from graph.client import GraphClient

class OnedriveReader(Tool):
    def __init__(self, graph_client : GraphClient) -> None:
        self.graph_client = graph_client

    @property
    def name(self) -> str:
        """The tool's unique identifier."""
        return "onedrive_reader"

    @property 
    def description(self) -> str:
        """A description of what the tool does."""
        return "Retrieves the text content of a file stored in OneDrive given its path, and returns the file path and content."
    
    @property
    def parameters(self) -> dict:
        """A JSON schema of the allowed parameters for the tool returned as a dictionary."""
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file in OneDrive."
                }
            },
            "required": ["file_path"]
        }
    
    async def execute(self, arguments: dict) -> dict:
        """The main function that performs the work of the tool and returns a file_path and content."""
        file_path = arguments["file_path"]
        path = f"/me/drive/root:/{file_path}:/content"
        if file_path is None:
            raise RuntimeError(f"{file_path} has a value of 'None'.")
        content = await self.graph_client.get(path)
        output = {
            "file_path" : file_path,
            "content" : content
        }
        return output