"""Defines the pydantic data models used to build the hecvat_data_structure using the hecvat_extractor."""

import datetime
from pydantic import BaseModel, computed_field, model_validator
from typing import Literal, ClassVar

class HecvatQuestion(BaseModel):
    """A single question row in a given sheet/section of the hecvat."""
    id: str
    text: str
    answer: Literal["Yes", "No", "N/A"] | None
    additional_info: str | None

class HecvatSection(BaseModel):
    """A list of all of the questions for each section in a given sheet of the hecvat."""
    section_map: ClassVar[dict] = {
        "GNRL":"General Information",
        "COMP":"Company Information",
        "REQU":"Required Questions",
        "DOCU":"Documentation",
        "THRD":"Assessment of Third Parties",
        "CHNG":"Change Management",
        "PPPR":"Policies, Processes, and Procedures",
        "AAAI":"Authentication, Authorization, and Account Management",
        "DATA":"Data",
        "APPL":"Application/Service Security",
        "DCTR":"Datacenter",
        "FIDP":"Firewalls, IDS, IPS, and Networking",
        "HFIH":"Incident Handling",
        "VULN":"Vulnerability Management",
        "ITAC":"IT Accessibility",
        "CONS":"Consulting Services",
        "HIPA":"HIPAA Compliance",
        "PCID":"Payment Card Industry Data Security Standard (PCI DSS)",
        "OPEM":"On-Premises Data Solutions",
        "AIQU":"AI Qualifying Questions",
        "AIGN":"General AI Questions",
        "AIPL":"AI Policy",
        "AISC":"AI Data Security",
        "AIML":"AI Machine Learning",
        "AILM":"AI Large Language Model (LLM)",
        "PRGN":"General Privacy",
        "PCOM":"Privacy-Specific Company Details",
        "PDOC":"Privacy-Specific Documentation",
        "PTHP":"Privacy of Third Parties",
        "PCHG":"Privacy Change Management",
        "PDAT":"Privacy of Sensitive Data",
        "PRPO":"Privacy Policies and Procedures",
        "INTL":"International Privacy",
        "DRPV":"Data Privacy",
        "DPAI":"Privacy and AI"
    }
    @computed_field
    @property
    def name(self) -> str:
        try:
            return self.section_map.get(self.questions[0].id[:4], "Unknown Section")
        except IndexError:
            return "This section has no questions."
    questions: list[HecvatQuestion]
    
class HecvatSheet(BaseModel):
    """A list of all of the sections on a given hecvat sheet and their names."""
    name: str
    sections: list[HecvatSection]

    def get_question(self, question_id: str) -> HecvatQuestion | None:
        for section in self.sections:
            for question in section.questions:
                if question.id == question_id:
                    return question
        return None

    def question_ids_by_answer(self, answer: Literal["Yes", "No", "N/A"] | None, relevant_prefixes: set[str] | None) -> dict:
        sorted_questions = {}
        for section in self.sections:
            if relevant_prefixes is None or section.questions[0].id[:4] in relevant_prefixes:
                for question in section.questions:
                    if question.answer == answer:
                        sorted_questions[question.id] = question
        return sorted_questions

class HecvatFullDocument(BaseModel):
    """The full hecvat document including relavent metadata."""
    vendor_name: str
    solution_name: str
    date: datetime.date
    version: str
    sheets: list[HecvatSheet]

    @model_validator(mode="after")
    def check_duplicate_sheet_names(self):
        sheet_names = [sheet.name for sheet in self.sheets]
        if len(sheet_names) != len(set(sheet_names)):
            raise ValueError("Duplicate sheet names are not allowed.")
        return self