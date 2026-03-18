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
    
    ## I need to to extract file_id from the file in Onedrive/Sharepoint for this code to work as written
    async def execute(self, arguments: dict) -> dict:
        """The main function that performs the work of the tool and returns a file_path and content."""
        file_name = arguments["file_name"]
        upn = arguments["upn"]
        if file_name is None:
            raise RuntimeError(f"'file_name' has a value of 'None'.")
        elif upn is None:
            raise RuntimeError(f"'upn' has a value of 'None'.")
        id = await self.graph_client.file_id(upn, file_name)
        content_path = f"/users/{upn}/drive/items/{id}/content"
        content = await self.graph_client.get(content_path)
        output = {
            "file_path" : file_name,
            "content" : content
        }
        return output