
from data_models.hecvat_model import HecvatFullDocument
from data_models.hecvat_risk_model import HecvatRiskSummary

SHOULD_BE_YES = {"COMP-01", "COMP-03", "COMP-04", "DOCU-04", "DOCU-05", "DOCU-06", "DOCU-07", "THRD-01", "THRD-02", 
                 "THRD-03", "THRD-04", "THRD-05", "CHNG-01", "CHNG-03", "CHNG-04", "CHNG-05", "CHNG-06", "CHNG-07", 
                 "CHNG-08", "CHNG-10", "CHNG-11", "CHNG-13", "CHNG-14", "CHNG-15", "CHNG-16", "PPPR-01", "PPPR-02", 
                 "PPPR-03", "PPPR-05", "PPPR-09", "PPPR-04", "PPPR-10", "PPPR-11", "PPPR-12", "PPPR-13", "PPPR-14", 
                 "PPPR-15", "AAAI-01", "AAAI-02", "AAAI-04", "AAAI-09", "AAAI-11", "AAAI-15", "AAAI-16", "AAAI-17", 
                 "AAAI-18", "DATA-01", "DATA-02", "DATA-03", "DATA-05", "DATA-06", "DATA-08", "DATA-09", "DATA-10", 
                 "DATA-11", "DATA-12", "DATA-14", "DATA-15", "DATA-17", "DATA-18", "DATA-19", "DATA-20", "DATA-21", 
                 "DATA-22", "DATA-23", "APPL-01", "APPL-02", "APPL-03", "APPL-05", "APPL-06", "APPL-07", "APPL-08", 
                 "APPL-09", "APPL-10", "APPL-11", "APPL-12", "APPL-14", "DCTR-02", "DCTR-03", "DCTR-04", "DCTR-06",
                 "DCTR-10", "DCTR-11", "DCTR-12", "DCTR-13", "DCTR-08", "DCTR-14", "DCTR-15", "DCTR-16", "FIDP-01",
                 "FIDP-02", "FIDP-03", "FIDP-04", "FIDP-05", "FIDP-06", "FIDP-07", "FIDP-08", "FIDP-09", "FIDP-11", 
                 "HFIH-01", "HFIH-02", "HFIH-03", "VULN-01", "VULN-03", "VULN-04", "VULN-05", "VULN-06", "CONS-02",
                 "CONS-03", "CONS-04", "HIPA-01", "HIPA-02", "HIPA-03", "HIPA-04", "HIPA-05", "HIPA-06", "HIPA-07",
                 "HIPA-08", "HIPA-09", "HIPA-10", "HIPA-11", "HIPA-12", "HIPA-13", "HIPA-15", "HIPA-16", "HIPA-17",
                 "HIPA-18", "HIPA-20", "HIPA-21", "HIPA-22", "HIPA-23", "HIPA-24", "HIPA-25", "HIPA-26", "HIPA-27",
                 "HIPA-28", "HIPA-29", "PCID-01", "PCID-02", "PCID-04", "PCID-05", "PCID-11", "OPEM-01", "OPEM-03",
                 "OPEM-05", "OPEM-06", "OPEM-07", "AIGN-01", "AIGN-03", "AIGN-05", "AIPL-01", "AIPL-02", "AIPL-03", 
                 "AIPL-04", "AISC-01", "AISC-03", "AISC-05", "AIML-01", "AIML-02", "AIML-07", "AIML-08", 
                 "AILM-01", "AILM-04", "AILM-05", "PDOC-03", "PTHP-01", "PTHP-02", "PDAT-05", "PDAT-07", "INTL-03",
                 "INTL-05", "PDAT-08", "PRPO-01", "PRPO-02", "PRPO-03", "PRPO-04", "PRPO-05", "DRPV-01", "DRPV-02", 
                 "DRPV-03", "DRPV-04", "DRPV-05", "DRPV-06", "DRPV-07", "DRPV-08", "DRPV-09", "DRPV-10","DRPV-11", 
                 "DRPV-12", "DRPV-14", "DRPV-15", "DPAI-03", "DPAI-05", "DPAI-07", "DPAI-08"}

NO_IS_GOOD = ["REQU-07", "AAAI-07", "AAAI-08", "DATA-17", "CONS-01", "CONS-06", "CONS-08", "CONS-09", "HIPA-14",
              "OPEM-04", "AISC-02", "PCOM-01", "PCOM-03", "PDAT-03", "PRPO-09", "PRPO-12", "INTL-01", "INTL-04", 
              "DRPV-13", "DPAI-02"]

NO_IS_OK = {"REQU-03", "DOCU-01", "DOCU-02", "DOCU-03", "CHNG-02", "CHNG-09", "CHNG-12", "DATA-04", "DATA-07", 
            "DATA-13", "DATA-16", "AAAI-03", "AAAI-06", "AAAI-12", "AAAI-13", "AAAI-14", "CONS-05", "CONS-07", 
            "HIPA-19", "PCID-03", "PCID-06", "PCID-07", "PCID-08", "OPEM-02", "OPEM-10", "AIGN-02", "AIQU-01", 
            "AIML-03", "AIML-04", "AIML-05", "AIML-06", "AILM-02", "AILM-03", "AILM-06", "PRGN-01", "AIQU-02", 
            "PRGN-02", "PRGN-03", "PRGN-04", "PCOM-04", "APPL-04", "APPL-13", "DCTR-05", "DCTR-06", "DCTR-07", 
            "DCTR-09", "HFIH-04", "VULN-02", "AIPL-05", "PDAT-01", "PDAT-02", "PDAT-04", "PDAT-06", "PDAT-07", 
            "PRPO-06", "PRPO-07", "PRPO-08", "PRPO-09", "PRPO-10", "PRPO-11", "PRPO-13", "PDOC-02", 
            "PCHG-01", "PCHG-02", "INTL-02", "DPAI-01", "DPAI-04", "DPAI-06"}

NONE_IS_OK = ["COMP-02", "COMP-05", "AAAI-10", "AIGN-04", "AISC-04", "PRGN-05", "PCOM-02", "PDOC-01", ]

REQU_SECTION_MAP = {
        "REQU-03": {"CONS"},
        "REQU-05": {"HIPA"},
        "REQU-06": {"PCID"},
        "REQU-07": {"OPEM", "DCTR"}
    }

def get_relevant_section_prefixes(document: HecvatFullDocument) -> set[str]:
    start_here = next(sheet for sheet in document.sheets if sheet.name == "START HERE")
    return {
        prefix
        for requ_id, prefixes in REQU_SECTION_MAP.items()
        if (question := start_here.get_question(requ_id)) is not None
        and question.answer == "Yes"
        for prefix in prefixes
    }

def no_answers(document: HecvatFullDocument, relevant_prefixes: set[str]) -> dict:
    return {
        key: value
        for sheet in document.sheets 
        for key, value in sheet.question_ids_by_answer(
            "No", 
            relevant_prefixes if sheet.name == "Case-Specific" else None
            ).items()
    }

def yes_answers(document: HecvatFullDocument, relevant_prefixes: set[str]) -> dict:
    return {
        key: value
        for sheet in document.sheets 
        for key, value in sheet.question_ids_by_answer(
            "Yes", 
            relevant_prefixes if sheet.name == "Case-Specific" else None
            ).items()
    }

def none_answers(document: HecvatFullDocument, relevant_prefixes: set[str]) -> dict:
    return {
        key: value
        for sheet in document.sheets
        for answer in ("N/A", None)
        for key, value in sheet.question_ids_by_answer(
            answer, 
            relevant_prefixes if sheet.name == "Case-Specific" else None
            ).items()
    }

def build_risk_summary(document: HecvatFullDocument, relevant_prefixes: set[str]) -> HecvatRiskSummary:
    should_be_yes_but_no = {
        key: value
        for answers in (no_answers(document, relevant_prefixes), none_answers(document, relevant_prefixes))
        for key, value in answers.items()
        if key in set(SHOULD_BE_YES)
    }
    
    should_be_no_but_yes = {
        key: value
        for key, value in yes_answers(document, relevant_prefixes).items()
        if key in NO_IS_GOOD
    }

    no_needs_review = {
        key: value
        for key, value in no_answers(document, relevant_prefixes).items()
        if key in set(NO_IS_OK)
    }
    
    return HecvatRiskSummary(
        should_be_yes=should_be_yes_but_no,
        should_be_no=should_be_no_but_yes,
        no_is_ok=no_needs_review,
    )
