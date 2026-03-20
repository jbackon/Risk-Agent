"""The class that defines the tool for reading the contents of a OneDrive .docx file 
    and returns the contents as a text string."""

from .base import Tool
from graph.client import GraphClient
from docx import Document
from io import BytesIO

class OnedriveDocxReader(Tool):
    def __init__(self, graph_client : GraphClient) -> None:
        self.graph_client = graph_client

    @property
    def name(self) -> str:
        """The tool's unique identifier."""
        return "onedrive_reader"

    @property 
    def description(self) -> str:
        """A description of what the tool does."""
        return "Retrieves the content of a .docx file stored in OneDrive given its name, and returns the file name and content."
    
    @property
    def parameters(self) -> dict:
        """A JSON schema of the allowed parameters for the tool returned as a dictionary."""
        return {
            "type": "object",
            "properties": {
                "file_name": {
                    "type": "string",
                    "description": "The name of the file in OneDrive."
                }
            },
            "required": ["file_name"]
        }
    
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
        doc = Document(BytesIO(content))
        for paragraph in doc.paragraphs:
            print(paragraph.text) 

        output = {
            "file_name" : file_name,
            "content" : "test"
        }
        return output