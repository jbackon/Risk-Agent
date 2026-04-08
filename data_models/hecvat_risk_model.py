from pydantic import BaseModel, model_validator

class HecvatRiskSummary(BaseModel):
    no_answers: list[str]
    unanswered: list[str]
    should_be_yes: list[str]
    no_is_good: list[str]
    no_is_ok: list[str]
    none_is_ok: list[str]

    @model_validator(mode="after")
    def duplicate_category_check(self):
        all_categories = {
            "should_be_yes": self.should_be_yes,
            "no_is_good": self.no_is_good,
            "no_is_ok": self.no_is_ok,
            "none_is_ok": self.none_is_ok
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