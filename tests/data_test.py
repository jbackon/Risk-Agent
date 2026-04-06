from tools.onedrive_xlsx_reader import HecvatQuestion

test = HecvatQuestion(id="DOCU-01", text="test text", answer="Yes", additional_info=None)
# print(type(test.id))
print(test.id[:4])