# ClarifyRec

**README prose word count: 482 words (excluding code blocks and headings; whitespace-count estimate).**

ClarifyRec is a local, interactive prototype for investigating how a conversational recommender handles ambiguous and revised natural-language preferences. It uses a movie-recommendation scenario to study when immediate preference updates may be less appropriate than asking a clarification question.

## Project status

- **Implemented:** Streamlit chat interface; local rule-based phrase extraction; immediate-update baseline; recency-weighted baseline; ambiguity-aware ClarifyRec strategy; clarification pending/resolution state; explicit preference polarity updates; transparent content-based ranking; 20-item illustrative movie catalogue; unit tests; deterministic comparison smoke script.
- **Simulated:** The comparison script uses three fixed dialogue scenarios and automatically chooses the first clarification option to make runs repeatable. This is a software smoke test, not a human-subject evaluation.
- **Not yet implemented:** MovieLens dataset ingestion, general-purpose semantic NLP, learned confidence calibration, persistent user accounts, real-user study, statistical significance testing and production deployment.

## Technology stack

- Python 3.10+ for application and recommendation logic.
- Streamlit for the interactive local interface.
- Standard-library regular expressions and data structures for transparent local preference extraction and state management.
- A small hand-curated illustrative catalogue in `clarifyrec/catalog.py`; no external API, paid model or network request is required.
- `unittest` for automated tests; CSV output for the deterministic comparison smoke script.

The rule-based NLP was chosen to keep the prototype inspectable, reproducible and offline. It is deliberately limited and should not be described as a general language model.

## Run the application

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit. Select each strategy in the sidebar and replay the same example conversations. The sidebar displays the current preference profile.

## Run tests and comparison

```bash
python -m unittest discover -s tests -v
python experiments/run_comparison.py
```

The comparison output is written to `experiments/comparison_smoke_results.csv`. It measures prompt/resolution counts in fixed scenarios only; it does not establish recommendation quality or user satisfaction.

## Inspect the work

- Architecture source: `docs/architecture.mmd` (Mermaid diagram source).
- Interaction walkthroughs: `docs/storyboards.md`.
- Assignment 2 report draft: `report/assignment2_report.md`.
- Test code: `tests/test_core.py`.
- Experimental smoke script: `experiments/run_comparison.py`.

## Development record

1. Defined a narrow film-domain task and an illustrative catalogue so the complete interaction can run offline.
2. Added a transparent immediate-update baseline.
3. Added a recency-weighted baseline to compare a simple feedback-weighting policy.
4. Added ambiguity detection and a pending clarification state; clear constraints bypass clarification.
5. Added profile inspection, strategy selection, deterministic scenarios and automated tests.

This is a generated initial project snapshot. Record meaningful changes and test outcomes in subsequent commits; do not invent historical commits.

## AI assistance and authorship

ChatGPT was used to help scaffold the project structure, draft Python modules, tests, architecture documentation and report text. The student should inspect, run and adapt the code, verify all claims and references, and record any corrections made before submission. Do not submit this declaration unchanged unless it accurately describes the assistance used.

## Additional files

No external dataset or API key is required for the current prototype. The catalogue is included in `clarifyrec/catalog.py`. Do not commit API keys or personal data if future extensions introduce external services.
