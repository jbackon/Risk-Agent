from pydantic import BaseModel, model_validator

class HecvatRiskSummary(BaseModel):
    should_be_yes: dict
    should_be_no: dict
    no_is_ok: dict

    @model_validator(mode="after")
    def duplicate_category_check(self):
        all_categories = {
            "should_be_yes": self.should_be_yes,
            "no_is_ok": self.no_is_ok,
            "should_be_no": self.should_be_no
        }
        seen = {}
        for category_name, question_ids in all_categories.items():
            for question_id in question_ids:
                if question_id in seen:
                    raise ValueError(
                        f"{question_id} appears in both '{seen[question_id]}' and '{category_name}'."
                        "Each ID may only belong in one category."
                    )
                seen[question_id] = category_name
        return self