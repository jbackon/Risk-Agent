import json
from data_models.hecvat_risk_model import HecvatRiskSummary

PROMPT_TEMPLATE = """
<role>
You are a senior information security risk analyst for a small college.
</role>
<task>
Review the flagged questions below and identify the 3 to 5 most significant risk themes they represent.
For each theme:
- Describe the risk it poses to the college in plain language.
- Cite 1 to 3 specific question IDs and brief additional_info excerpts as evidence.
- Note whether the vendor provided any compensating controls and whether they are credible.
A genuine compensating control must name a specific alternative mechanism, apply to the same threat, and be
verifiable by an auditor. Assertions that risk is "managed" without specifics are not compensating controls.
Unanswered questions with no additional_info are always a risk — a vendor leaving a question blank with no
explanation is not acceptable.
Write the result as a concise 2 to 3 paragraph executive summary. Do not enumerate every question — focus on
the patterns and themes that matter most to the college's risk posture.
The response must strictly adhere to the json output format below.
</task>
<questions>
{questions}
</questions>
<output_format>
{{
    "summary": "There are several indicators of vendor risk that the college should be aware of..."
}}
</output_format>
"""

def build_prompt(risk_summary: HecvatRiskSummary) -> str:
    questions = json.dumps(risk_summary.model_dump(mode="json"), indent=2)
    return PROMPT_TEMPLATE.format(questions=questions)
