
from data_models.hecvat_model import HecvatFullDocument
from data_models.hecvat_risk_model import HecvatRiskSummary

def no_answers(document: HecvatFullDocument) -> list[str]:
    all_no_answers = []
    for sheet in document.sheets:
        all_no_answers.extend(sheet.question_ids_by_answer("No"))
    return all_no_answers

def none_answers(document: HecvatFullDocument) -> list[str]:
    all_none_answers = []
    for sheet in document.sheets:
        all_none_answers.extend(sheet.question_ids_by_answer(None))
    return all_none_answers

SHOULD_BE_YES = ["DOCU-03", "DOCU-04", "DOCU-06", "THRD-01", "THRD-02", "CHNG-01", "CHNG-04", "CHNG-07", 
                 "CHNG-16", "PPPR-01", "PPPR-02", "PPPR-09", "PPPR-04", "PPPR-10", "AAAI-01", 
                 "AAAI-09", "AAAI-15", "AAAI-18", "DATA-01", "DATA-02", "DATA-03", "DATA-09", 
                 "DATA-14", "DATA-17", "DATA-19", "DATA-23", "APPL-03", "APPL-05", "APPL-10", "APPL-12", 
                 "DCTR-14", "DCTR-15", "DCTR-16", "FIDP-02", "FIDP-05", "FIDP-11", "HFIH-01", "HFIH-03", 
                 "VULN-01", "VULN-04", "VULN-05", "AIQU-01", "AIQU-02", "AIGN-05", "AIPL-02", "AIPL-03", 
                 "AISC-01", "AISC-03", "AISC-05", "AIML-01", "AIML-02", "AILM-01", "PTHP-01", "PDAT-07", 
                 "PDAT-08", "PRPO-02", "PRPO-03", "PRPO-04", "DRPV-02", "DRPV-04", "DRPV-07", "DRPV-08", 
                 "DRPV-11", "DRPV-12", "DPAI-05", "DPAI-07", "DPAI-08"]

NO_IS_GOOD = ["AAAI-07", "AAAI-08", "AISC-02", "PCOM-01", "PCOM-03", "PDAT-03", "PRPO-09", "PRPO-12", 
              "INTL-04", "DRPV-13", "DPAI-02"]

NO_IS_OK = ["DATA-04", "DATA-13", "APPL-04", "APPL-13", "DCTR-04", "DCTR-05", "DCTR-06", "DCTR-09", 
            "DCTR-10", "DCTR-11", "DCTR-12", "DCTR-13", "VULN-02", "VULN-06", "AIPL-05", "PDAT-02", 
            "PRPO-10", "INTL-01", "DRPV-01", "DRPV-15"]

NONE_IS_OK = ["AAAI-10", "AIGN-04", "AISC-04", "PRGN-05", "PCOM-02"]

def build_risk_summary(document: HecvatFullDocument) -> HecvatRiskSummary:
    return HecvatRiskSummary(
        no_answers=no_answers(document),
        unanswered=none_answers(document),
        should_be_yes=SHOULD_BE_YES,
        no_is_good=NO_IS_GOOD,
        no_is_ok=NO_IS_OK,
        none_is_ok=NONE_IS_OK
    )
