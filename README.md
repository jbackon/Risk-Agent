# Risk Agent

An AI agent that automates third-party risk assessments of higher-education vendors.

Risk Agent reads a vendor's completed [HECVAT](https://www.educause.edu/hecvat) (Higher Education Community Vendor Assessment Toolkit) from OneDrive, applies a set of explicit review rules to decide which answers deserve scrutiny, and asks an LLM to turn the flagged answers into a short executive summary of the vendor's most significant risk themes.

The rules decide **what** gets reviewed. The LLM only decides how to **summarize** it.

## Why this exists

A HECVAT can contain hundreds of questions across dozens of sections. Reviewing one by hand is slow, and the answers that matter are easy to miss: a "No" to a control that should be a "Yes", a "Yes" to something that should be a "No", or a question left blank with no explanation. Risk Agent does the first pass so an analyst can start from the risk themes instead of the raw spreadsheet.

## How it works

```
 OneDrive (HECVAT .xlsx)
        │  Microsoft Graph API (app-only auth via MSAL)
        ▼
   Broker ──► OneDrive reader tool ──► Extractor ──► Pydantic data models
                                                          │
                                                          ▼
                                        Transformer (deterministic rules)
                                        should_be_yes / should_be_no / no_is_ok
                                                          │
                                                          ▼
                                       Prompt builder ──► LLM (Anthropic API)
                                                          │
                                                          ▼
                                    Response contract (parse + validate JSON)
                                                          │
                                                          ▼
                                          Executive risk summary (JSON)
```

1. **Retrieve.** The broker dispatches a registered tool that finds the file in the user's OneDrive by name and downloads it through the Microsoft Graph API.
2. **Extract.** The extractor walks each worksheet, turns question rows into structured records (ID, text, answer, additional info), groups them into sections, and pulls vendor name, solution name, date, and HECVAT version from the "START HERE" sheet.
3. **Transform.** Deterministic rules sort the flagged answers into three buckets:
   - `should_be_yes`: controls the vendor should have, answered "No", "N/A", or left blank
   - `should_be_no`: answers that are a red flag when "Yes"
   - `no_is_ok`: "No" answers that are sometimes acceptable and need a judgment call
4. **Summarize.** The flagged questions are sent to the LLM with a prompt that sets the role (senior information security risk analyst for a small college), asks for 3 to 5 risk themes with cited question IDs, and defines what counts as a credible compensating control.
5. **Validate.** The response must be valid JSON matching the response contract and must contain a non-empty summary, or the run fails.

### Scoping rules

The transformer avoids flagging questions that don't apply:

- **Case-specific sections** (consulting, HIPAA, PCI DSS, on-premises) are only reviewed when the vendor's answers to the required questions (REQU) on the START HERE sheet say they apply.
- **Datacenter questions** are skipped when the vendor hosts on AWS, Azure, or GCP.
- **AI questions** are skipped when the vendor answers "No" to REQU-04.

## Project layout

| Path | Purpose |
|---|---|
| `main.py` | Command-line entry point and orchestration |
| `broker.py` | Tool registry and dispatcher |
| `tools/` | Tools the broker can call. `base.py` defines the interface, and the OneDrive readers fetch files via Graph |
| `graph/` | Microsoft Graph client and authentication strategy |
| `extractors/` | Converts raw worksheet rows into structured HECVAT data |
| `data_models/` | Pydantic models for the HECVAT document and the risk summary |
| `transformers/` | Rule sets that classify answers into risk buckets |
| `prompt.py` | LLM prompt template |
| `llm/` | LLM client |
| `response_contract.py` | Parses and validates the LLM response |
| `hecvat_data_structure.json` | Example of the structured HECVAT format |
| `tests/` | Unit tests |

## Getting started

### Requirements

- Python 3.10 or newer
- A Microsoft Entra app registration with permission to read files from the target OneDrive
- An Anthropic API key (or a compatible gateway)

### Install

```bash
git clone https://github.com/jbackon/Risk-Agent.git
cd Risk-Agent
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .
pip install anthropic httpx msal openpyxl pydantic python-dotenv python-docx pymupdf pytest
```

### Configure

Create a `.env` file in the project root. It is listed in `.gitignore`; never commit it.

```
BASE_URL=                 # Microsoft Graph base URL
GRAPH_AUTHORITY=          # Authority URL prefix; the tenant ID is appended to it
GRAPH_TENANT_ID=
GRAPH_CLIENT_ID=
GRAPH_CLIENT_SECRET=
GRAPH_SCOPE=              # Graph scope for the client-credentials flow
ANTHROPIC_API_KEY=
ANTHROPIC_BASE_URL=       # Optional: gateway or proxy URL
```

The model ID is set in `llm/client.py`. Change it to match the model your endpoint exposes.

### Run

```bash
python main.py "<hecvat_file_name>.xlsx" "<user@example.edu>"
```

- `file_name`: the name of the file in the root of the user's OneDrive
- `upn`: the user principal name of the account that owns the file

The result is printed as JSON:

```json
{
  "summary": "There are several indicators of vendor risk that the college should be aware of..."
}
```

### Test

```bash
pytest
```

## Security considerations

This tool handles vendor security questionnaires and sends their contents to an LLM, so a few design points matter.

- **Secrets stay in the environment.** Credentials are read from environment variables, and `.env` is git-ignored.
- **Scope the Graph permission.** The client-credentials flow acts as the application, not a signed-in user. Grant the narrowest file-read permission that works and, where possible, restrict the app to the specific site or drive that holds HECVATs.
- **Know where the data goes.** Question text and vendor free-text answers are sent to the configured LLM endpoint. Confirm that endpoint's data-handling and retention terms are acceptable for the vendor data you process.
- **Vendor text is untrusted input.** The `additional_info` field is vendor-written and is included in the prompt. Treat the output as a recommendation for an analyst to review, not as an automated decision.
- **Output is validated.** The response must parse into a defined schema, and an empty summary fails the run instead of passing silently.

## Known limitations

- Analysis currently supports HECVAT workbooks in Excel (`.xlsx`) format. The `.docx` and `.pdf` readers retrieve file text but are not yet part of the analysis pipeline.
- The question classification rules are written for a specific HECVAT layout and version, and may need updates when the HECVAT changes.
- Each run assesses a single vendor document and returns a narrative summary only.
- Dependencies are not yet declared in `pyproject.toml`.
- The test suite covers the broker and is small.

## Status

Version 0.1.0. The core pipeline from retrieval to executive summary is complete.
