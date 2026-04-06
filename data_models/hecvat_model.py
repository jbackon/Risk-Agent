import datetime
from pydantic import BaseModel, computed_field, model_validator
from typing import Literal, ClassVar

class HecvatQuestion(BaseModel):
    id: str
    text: str
    answer: Literal["Yes", "No", "N/A"] | None
    additional_info: str | None

class HecvatSection(BaseModel):
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
    name: str
    sections: list[HecvatSection]

    def get_no_response(self) -> list[HecvatQuestion]:
        no_answers = []
        for section in self.sections:
            for question in section.questions:
                if question.answer == "No":
                    no_answers.append(question)
        return no_answers

class HecvatFullDocument(BaseModel):
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