"""Defines the tool for reading the contents of an Excel file in OneDrive 
    and returns the contents as a text string."""

import openpyxl, io
from .base import Tool
from graph.client import GraphClient
from extractors.hecvat_extractor import convert_questions_from_rows, convert_sections_from_questions, get_full_document
from data_models.hecvat_model import HecvatSheet, HecvatFullDocument

class OnedriveXlsxReader(Tool):
    def __init__(self, graph_client : GraphClient) -> None:
        self.graph_client = graph_client

    @property
    def name(self) -> str:
        """The tool's unique identifier."""
        return "onedrive_xlsx_reader"

    @property 
    def description(self) -> str:
        """A description of what the tool does."""
        return "Retrieves the content of an Excel file stored in OneDrive given its name, and returns the file name and content."
    
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
    
    async def execute(self, arguments: dict) -> HecvatFullDocument:
        """The main function that performs the work of the tool and returns a file_name and content."""
        file_name = arguments["file_name"]
        upn = arguments["upn"]
        if file_name is None:
            raise RuntimeError(f"'file_name' has a value of 'None'.")
        elif upn is None:
            raise RuntimeError(f"'upn' has a value of 'None'.")
        id = await self.graph_client.file_id(upn, file_name)
        content_path = f"/users/{upn}/drive/items/{id}/content"
        content = await self.graph_client.get(content_path)
        
        excel_data = io.BytesIO(content)
        workbook = openpyxl.load_workbook(excel_data, data_only=True)

        sheets = []
        for sheet_name in workbook.sheetnames:
            sheet = workbook[sheet_name]
            if sheet_name == "Institution Evaluation":
                break
            questions = convert_questions_from_rows(sheet)
            sections = convert_sections_from_questions(questions)
            sheets.append(HecvatSheet(name=sheet_name, sections=sections))
        
        full_document = get_full_document(sheet=workbook["START HERE"], sheets=sheets)
        
        return full_document