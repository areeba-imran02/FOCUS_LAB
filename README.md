# FocusLab — Understand Your Focus. Take Back Your Attention.

A Streamlit educational productivity lab: manual intake, a short visual target-detection exercise, deterministic scoring, local lexical evidence retrieval, an optional Gemini Focus Coach, a focus timer, reflection, and JSON export. This is not a medical device or diagnostic test.

## Features

- Manual editable intake works without AI credentials.
- Six practice responses and randomized quiet / simulated-notification conditions. Each generated condition contains 24 trials: 12 blue-circle targets and 12 balanced non-targets.
- Pure scoring for hits, misses, false alarms, correct rejections, accuracy, and median reaction time for correctly detected targets. Missing reaction time is shown as unavailable.
- Local BM25-style lexical retrieval over `data/evidence.json`; evidence entries are marked unverified until source metadata is audited.
- Optional, consent-gated Gemini plan generation using the official `google-genai` SDK, bounded attempts, model discovery, schema validation, and a clearly labeled local fallback.
- Focus-session controls, reflection, and optional JSON history export.
- Dark/light appearance and Streamlit-native navigation.

## Architecture

`app.py` is the overview and global navigation. Pages live in `pages/`. Reusable logic is in `focuslab_core/`: experiment generation, scoring, analytics, evidence retrieval, Pydantic models, Gemini/model registry, fallback, coach orchestration, and local storage. No database, vector service, separate backend, or model-training pipeline is used.

## Prerequisites and local setup

Python 3.11+ is recommended. Create a virtual environment in your own development workflow if desired, then install dependencies there; this project does not install packages automatically.

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

The developer environment used to assemble this archive did **not** have Streamlit or `google-genai` installed, and no packages were installed during build. `pytest`, Pydantic, pandas, and Plotly were present. See `VERIFICATION.md` for exact checks.

## Gemini API configuration

The manual intake, experiment, scoring, local retrieval, fallback plan, focus session, reflection, and exports work without an API key. To use Gemini, the user must explicitly check the consent box on Focus Coach.

For local use, set environment variables in your shell or use Streamlit's local secrets file (never commit it):

```toml
# .streamlit/secrets.toml — local only; do not commit
GEMINI_API_KEY = "YOUR_KEY_HERE"
GEMINI_MODEL = "gemini-2.5-flash"
```

The app reads `st.secrets["GEMINI_API_KEY"]` server-side (with an environment-variable fallback for local testing). It never displays or exports the key. `GEMINI_MODEL` is optional. The model registry prefers the configured model, then tries compatible discovered model IDs, then a small fallback list. Discovery and exact identifiers are account/API-dependent and were **not live-verified during this build**. Accessibility does not mean a model is free; quotas and billing policies depend on the account. Authentication, quota, and safety errors stop retries; other failures are bounded. Account-wide quota exhaustion may affect every model.

## Streamlit Community Cloud deployment

1. Push the contents of this folder to a GitHub repository.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/) and create an app from that repository.
3. Select `app.py` as the entry point.
4. In the app's **Settings → Secrets**, enter your own values: `GEMINI_API_KEY = "YOUR_KEY_HERE"` and optionally `GEMINI_MODEL = "gemini-2.5-flash"`. Replace the placeholder with your own key inside Streamlit Secrets; never put a real key in GitHub.
5. Deploy and test manual mode first, then opt in to test Gemini.

No resources are created and no deployment is performed by this project. Free-tier capacity, app sleeping, API quotas, and ephemeral filesystem behavior can change. Cloud local JSON history may be lost on restart/redeployment; download the JSON export to keep it.

## Tests

```bash
python -m pytest -q
```

Tests use deterministic seeds and mocks; they do not require a Gemini key. `google-genai` is only imported inside the AI request path.

## Experiment and interpretation limitations

The stimulus is drawn in Streamlit and advances on button clicks. The intended 900 ms response window and 300–500 ms blank intervals cannot be enforced accurately by this implementation without a client-side event loop. Reaction times include browser, server, rerun, and user interaction latency; a missed response is manually marked. Streamlit cannot reliably detect tab visibility or focus loss here. Simulated notification cards are ordinary UI text and never request browser notifications or audio. Use Restart experiment to discard an incomplete round. Trial order is randomized, but practice, fatigue, device, chance, and order effects remain. Do not infer diagnosis, stable attention ability, or proven cognitive change.

## Evidence status

`data/evidence.json` contains 10 locally bundled entries. `verifiedAt` is null for all entries because source pages and metadata were not opened and verified during this offline build. Treat summaries as provisional source leads, not verified citations. One topic is duplicated and one entry explicitly requires a source audit. Audit each primary source, metadata, and claims before describing the collection as verified research. The app shows source links and limitations.

## Privacy

Intake and experiment calculations stay local unless the user explicitly consents to AI processing. With consent, intake, metrics, and retrieved evidence are sent to Google Gemini. Avoid sensitive or identifying information. There is no authentication or database. Local history is optional and stored in a JSON file on the runtime filesystem, which is not guaranteed to persist in Streamlit Cloud. Clear or export history from the history page.

## Troubleshooting

- **API configuration required:** add `GEMINI_API_KEY` to Streamlit Secrets; local fallback still works.
- **Gemini unavailable / quota:** verify the key, model access, API quota, and current provider policies. A second model may not fix account-wide quota limits.
- **Model ID retired:** set a currently supported `GEMINI_MODEL` or update `focuslab_core/model_registry.py` after checking Google's official model registry.
- **Import error:** install `requirements.txt` in the target environment; no package install was run on the build machine.
- **History missing after redeploy:** cloud filesystem persistence is not guaranteed; export JSON before leaving the session.
