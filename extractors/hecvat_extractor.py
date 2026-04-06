import re
from itertools import groupby
from pydantic import ValidationError
from data_models.hecvat_model import HecvatQuestion, HecvatSection, HecvatSheet, HecvatFullDocument

def is_row_question(row: tuple) -> bool:
    pattern = re.compile(r'^[A-Z]+-\d+$')
    if row[0] is None or type(row[0]) is int:
        return False
    elif row[0][:4] == "GNRL" or row[0][:4] == "REQU":
        return False 
    else:
        return bool(row[0] and pattern.match(str(row[0])))

def convert_questions_from_rows(sheet) -> list:
    questions = []
    for row in sheet.iter_rows(values_only=True):
        try:
            if is_row_question(row):
                questions.append(HecvatQuestion(
                    id=row[0], 
                    text=row[1], 
                    answer=row[2],
                    additional_info=row[3]))
        except ValidationError:
            print(f"Please ensure question {row[0]} in sheet {sheet} conforms to the data model.")
    return questions

def convert_sections_from_questions(questions: list) -> list[HecvatSection]:
    section = []
    prefix = lambda question: question.id[:4]
    try:
        for prefix, group in groupby(questions, key=prefix):
            section.append(HecvatSection(questions=list(group)))
    except ValidationError:
        print("There were no questions available to group into sections.")
    return section

def get_full_document(sheet, sheets: list[HecvatSheet]) -> HecvatFullDocument:
    date = None
    vendor_name = None
    solution_name = None
    version = None
    for row in sheet.iter_rows(values_only=True):
        if row[0] == "Date Completed":
            date = row[2]
        if row[0] == "GNRL-01":
            vendor_name = row[2]
        if row[0] == "GNRL-02":
            solution_name = row[2]
        if row[0] is not None and "Solution Provider Response" in row[0]:
            version = row[5]
    if date is None:
        raise ValueError("Could not find date (Date Completed) in the provided sheet.")
    elif vendor_name is None:
        raise ValueError("Could not find vendor name (GNRL-01) in the provided sheet.")
    elif solution_name is None:
        raise ValueError("Could not find solution name (GNRL-02) in the provided sheet.")
    elif version is None:
        raise ValueError("Could not find Hecvat version in the provided sheet.")
    document = HecvatFullDocument(
        vendor_name=vendor_name, 
        solution_name=solution_name,
        date=date,
        version=version, 
        sheets=sheets)
    return document