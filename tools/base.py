"""
Abstract base class for all broker tools.
"""

from abc import ABC, abstractmethod
from data_models.hecvat_model import HecvatFullDocument


class Tool(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        """
        The tool's unique identifier.

        This is the string the LLM returns when it wants to invoke this tool.
        The broker uses it as the registry key, so it must be unique across
        all registered tools.
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """
        A plain-language description of what this tool does.

        This is included in the schema sent to the LLM so it can decide
        whether to call this tool. Write it for the model, not the developer
        — be specific about what the tool returns, not just what it does.
        """
        pass

    @property
    @abstractmethod
    def parameters(self) -> dict:
        """
        JSON Schema definition of the arguments this tool accepts.

        Returned as a dict rather than a JSON string so the adapter layer
        can embed it in a provider-specific payload without an extra
        parse/serialize round-trip.

        Example structure:
        {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file in OneDrive."
                }
            },
            "required": ["file_path"]
        }
        """
        pass

    @abstractmethod
    async def execute(self, arguments: dict) -> HecvatFullDocument | None:
        """
        Performs the tool's work and returns a structured result.

        Arguments are passed as a dict matching the shape declared in
        `parameters`. The broker is responsible for validating the arguments
        before calling execute() — this method can assume they are present
        and correctly typed.

        Returns a dict rather than a plain string so the broker can inspect,
        route, or sanitize individual fields before passing content to the LLM.
        Concrete tools should document the keys their result dict contains.
        """
        pass