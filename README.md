# SYNTRA GPT

This repository powers the SYNTRA language experiments. API keys were
previously stored in `config.json`, but this file is now only a template.

## Configuration

1. Set the following environment variables before running the tools:
   - `OPENAI_API_KEY`
   - `ELEVENLABS_API_KEY`

   You can export them in your shell or store them in a local file.

2. Alternatively create a `config.local.json`
   (ignored by git) with the same structure as `config.json`. The loader
   checks `config.local.json` first, falling back to the repository's
   `config.json` if no override file exists. Values from environment
   variables override those in the file.
3. If no override files exist, `load_config` reads the default `config.json`
   in the repository root.
4. Set `telemetry_csv_path` to the location of your telemetry log CSV if you
   want the bridge to monitor a custom file.
5. To enable Apple's local LLM, define `apple_llm_api_base` and optionally
   `apple_llm_api_key` in your configuration or environment variables.

Example `config.local.json`:
```json
{
  "openai_api_key": "sk-...",
  "openai_api_base": "http://localhost:1234/v1",
  "openai_model": "phi-3-mini-4k-instruct",
  "elevenlabs_api_key": "elevenlabs-...",
  "use_mistral_for_valon": true,
  "preferred_voice": "auto",
  "drift_ratio": { "valon": 0.7, "modi": 0.3 },
  "memory_mode": "flat",
  "telemetry_csv_path": "C:\\HWiNFO_logs\\syntra_runtime.csv",
  "apple_llm_api_base": "http://localhost:8080/v1",
  "apple_llm_api_key": "apple-...",
  "use_apple_llm": false
}
```

With this setup, the code will automatically read from environment variables or
`config.local.json` if present. The checked-in
`config.json` only provides defaults and should not contain real credentials.

## Directory layout

- `ingest/` – scripts for loading data. `pdf_ingestor.py` processes PDFs from
  `source_pdfs/` and writes summaries into `memory_vault/`.
- `utils/` – helper modules including the language engine, telemetry bridge and
  logging helpers.
- `memory_vault/` – persistent JSON archives for the Modi and Valon memory
  nodes. When `memory_mode` is set to `hybrid`, a `hybrid_store/` subdirectory
  stores graph nodes and edge maps.
- `source_pdfs/` – raw PDF documents waiting to be ingested.
- `entropy_logs/` – logs for failures and drift information.

## Key scripts

### `run_SYNTRA_loop.py`
A minimal interactive loop. It waits for user input, calls the language engine
and optionally speaks the result using ElevenLabs.

### `main.py`
Starts the interactive loop while running the telemetry bridge in a background
thread. Use this script for a quick demo that ingests PDF updates.

### `Deep_Cognition_Run.py`
A larger orchestration script that watches for new PDFs, processes them and
runs a deep cognition cycle across the memory vault. It also starts the
telemetry bridge in a background thread.

### `ingest/pdf_ingestor.py`
Standalone utility that extracts text from PDFs with `PyPDF2`, summarizes the
content using Mistral or a local LM Studio server and stores the result in the
vault.

### `syntra_interactive.py`
Opens an interactive console that prints the VALON, MODI, DRIFT and DREAM
segments for each prompt. Start it with:

```bash
python syntra_interactive.py
```
Type `exit` or `quit` to close the console.

## Dependencies

The core modules rely on several Python packages. The easiest way to install
everything is to run:

```bash
pip install -r Requirements.txt
```

Key packages include:

- `openai` – required for compatibility with LM Studio's local server.
- `elevenlabs` – speech synthesis.
- `PyPDF2` – PDF text extraction.
- `pandas` – used in `telemetry_bridge.py` to parse telemetry logs.
- `spacy` – for linguistic analysis in the language engine.
- `nltk` – provides WordNet lookups.
- `requests` – needed by the Apple LLM and Phi‑3 bridges for HTTP calls.

Install them with `pip install openai tiktoken python-dotenv numpy fuzzywuzzy nltk`
and any optional packages like `elevenlabs` or `spacy` as needed. Some modules
may require model downloads (e.g. `python -m spacy download en_core_web_sm`).

The project previously listed `sounddevice`, `pyttsx3` and `python-Levenshtein`
in `Requirements.txt`, but these dependencies are no longer used.

## Swift components

The repository includes a Swift Package named `SyntraSwift` providing `Valon`,
`Modi`, `Drift`, and `MemoryEngine` modules. A CLI target under `swift/` exposes
the `reflect_valon`, `reflect_modi`, `drift_average`, and
`processThroughBrains` commands. The Python layer invokes this CLI through
`utils.reasoning_engine._run_swift`, which runs:

```bash
swift run --package-path . SyntraSwiftCLI <command> <args>
```

If `use_apple_llm` is enabled in `config.local.json` or via the
`USE_APPLE_LLM` environment variable, the `processThroughBrains` CLI will
also send the raw user input to `queryAppleLLM`. This helper calls an
Apple-provided local LLM using `apple_llm_api_base` and optionally
`apple_llm_api_key`.

### Using Xcode

1. Open the Swift package in Xcode:

   ```bash
   open Package.swift
   ```
2. Select the **SyntraSwiftCLI** scheme.
3. Build the project and run the tests with **Product → Test**.

### Testing

Run the Python test suite with:

```bash
python -m pytest
```

Run the Swift package tests with:

```bash
swift test
```

## API keys

Configuration overrides can be placed in `config.local.json` using the same
structure as `config.json`. The loader checks this file before falling back to
the repository's defaults. Environment variables `OPENAI_API_KEY` and
`ELEVENLABS_API_KEY` override any values from the file. You may also specify
`openai_api_base` and `openai_model` here to point at a local LM Studio server.

## Citations

SYNTRA stores metadata about document references in `memory_vault/citations.json`.
Each entry maps an identifier to a source fragment so VALON and MODI can attach
contextual citations.
## License

This repository is licensed under a custom Source View License.

🔎 You may inspect the source code for learning, research, and transparency.
🚫 You may not reuse, distribute, or modify it without written permission.

See [LICENSE](./LICENSE) for full terms.
