"""Defines the tool for reading the contents of a PDF file in OneDrive 
    and returns the contents as a text string."""

import fitz, io
from .base import Tool
from graph.client import GraphClient

class OnedrivePdfReader(Tool):
    def __init__(self, graph_client : GraphClient) -> None:
        self.graph_client = graph_client

    @property
    def name(self) -> str:
        """The tool's unique identifier."""
        return "onedrive_pdf_reader"

    @property 
    def description(self) -> str:
        """A description of what the tool does."""
        return "Retrieves the content of a PDF file stored in OneDrive given its name, and returns the file name and content."
    
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
        byte_content = io.BytesIO(content)

        pdf_file = fitz.open(stream=byte_content, filetype="pdf")
        for page_num in range(len(pdf_file)):
            page = pdf_file[page_num]
            print(f"\n--- Page {page_num + 1} ---")

        # Extract text blocks — each block contains positional + text data
            blocks = page.get_text("blocks")
            for block in blocks:
                # block format: (x0, y0, x1, y1, text, block_no, block_type)
                text = block[4].strip()
                if text:  # Skip empty blocks
                    print(text)

        pdf_file.close()

        output = {
            "file_path" : file_name,
            "content" : "test"
        }
        return output