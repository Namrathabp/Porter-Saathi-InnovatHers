[README.md](https://github.com/user-attachments/files/22310652/README.md)
# Porter Saathi — README

**Voice‑first assistant for drivers (Porter Saathi)**

This repository contains a small voice‑first assistant prototype that uses an LLM (via OpenRouter) + local TTS/STT for simple Hindi/Hinglish conversations. The assistant supports two modes: synchronous (non‑streaming) and streaming (token‑by‑token) with real‑time speech playback.

---

## Table of contents
- Project overview
- Prerequisites
- Installation (step‑by‑step)
- Configuration (`.env`)
- Project structure
- How to run
- Streaming vs non‑streaming behavior
- Troubleshooting (common errors & fixes)
- Security & best practices
- Contributing
- License

---

## Project overview
`Porter Saathi` is a small CLI prototype that:
- Sends user queries to an LLM through **OpenRouter**.
- Streams partial replies and uses a local TTS (`pyttsx3`) to speak responses as they arrive.
- Falls back to a small rule‑based reply engine if the LLM call fails.

This README walks you through getting the project running on Windows (the examples use PowerShell/CMD); they should work on macOS/Linux with small changes.

---

## Prerequisites
- Python 3.8+ (3.11 used in some examples)
- Internet connection for OpenRouter
- A valid **OpenRouter API key**

Required Python packages (we show commands in the Installation section):
- `openai` (used to call OpenRouter via `OpenAI(base_url=...)`)
- `python-dotenv` (optional, for loading `.env`)
- `pyttsx3` (text-to-speech)
- `SpeechRecognition` (speech-to-text)
- `pyaudio` (microphone input, on Windows you may need a wheel)
- `requests` (optional)

---

## Installation (step‑by‑step)
1. Clone or copy the project folder to your machine.

2. Create and activate a virtual environment (recommended):

**PowerShell**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**CMD**
```cmd
python -m venv .venv
.\.venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install openai python-dotenv pyttsx3 SpeechRecognition requests
```

4. Install PyAudio (Windows notes):
- If `pip install pyaudio` fails on Windows, download the correct `.whl` from Christoph Gohlke: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
- Example (after downloading the correct wheel for your Python):
```bash
pip install PyAudio-0.2.11-cp311-cp311-win_amd64.whl
```

5. (Optional) If you plan to edit or test more, install developer helpers (linters, etc.).

---

## Configuration (`.env`)
Create a `.env` file in the project root (DO NOT commit this file):

```
OPENROUTER_API_KEY=sk-or-v1-xxxx-your-key-here
```

Alternatively set environment variables in your shell:

**PowerShell (session only)**
```powershell
$env:OPENROUTER_API_KEY="sk-or-v1-xxxx"
```

**CMD**
```cmd
set OPENROUTER_API_KEY=sk-or-v1-xxxx
```

**Important:** Never expose or commit API keys to version control. Rotate keys immediately if leaked.

---

## Project structure (important files)
```
Porter Saathi/
├── main.py            # CLI launcher (reads input, calls ai_engine.ask_ai)
├── ai_engine.py       # Handles OpenRouter client, streaming and fallback
├── voice_client.py    # speak(text) and listen() helper functions
├── rule_based.py      # simple fallback rule-based replies
├── .env               # your OpenRouter API key (ignored by git)
└── README.md
```

**Where to put files:** all Python files must be in the same project root folder so imports like `from voice_client import speak` work.

---

## How to run (basic)
1. Ensure your virtualenv is activated and `.env` is present.
2. From the project root run:

```bash
python main.py
```

3. The CLI will prompt:
```
👉 Enter query (or 'exit'):
```
Type a query (for example `Aaj kitna kamaya?`) and press Enter. The assistant will print and speak the reply.

**Using speech input:**
If your environment supports microphone input and PyAudio is installed, you can use `listen()` if you extend `main.py` to call `listen()` instead of `input()`.

---

## Streaming vs Non‑streaming behavior
- **Non‑streaming (`ask_ai`)**: waits for the full reply from the model, then returns it. Useful if you must display the whole response before speaking.
- **Streaming (`ask_ai_stream`)**: receives tokens as they are generated and calls `speak()` on sentence chunks. This creates a near real‑time conversational feel.

To switch model or behavior, change `model=` in `ai_engine.py` (e.g., `"openai/gpt-4o-mini"`) or toggle `stream=True/False`.

---

## Troubleshooting — common errors & fixes
**Error: `RuntimeError` from `pyttsx3` (engine.runAndWait)**
- Cause: engine reinitialized repeatedly or multiple overlapping calls.
- Fix: ensure `voice_client.py` initializes the engine once at top-level, uses a `threading.Lock()`, calls `engine.stop()` before `engine.say()`, and declares `global engine` at top of `speak()` if you reassign it.

**Error: `OPENROUTER_API_KEY not set`**
- Cause: `.env` not created or environment variable not set.
- Fix: create `.env` or export the env var before running.

**Error: `ModuleNotFoundError: No module named 'rule_based'`**
- Cause: missing `rule_based.py` file.
- Fix: create `rule_based.py` in the project root with the fallback function.

**SyntaxError: name 'engine' is used prior to global declaration**
- Cause: `global engine` used after you already referenced `engine` in the function.
- Fix: put `global engine` at the top of `speak()` before any usage.

**NameError: name 'lock' is not defined**
- Cause: `lock` was removed or not defined in the module scope.
- Fix: ensure `lock = threading.Lock()` is set at the top of `voice_client.py`.

**PyAudio install problems on Windows**
- Use the prebuilt `.whl` from Gohlke and install with `pip install <wheelfile>`.

---

## Security & best practices
- Never hardcode API keys. Use `.env` or a secrets manager.
- Add `.env` to `.gitignore`.
- Rate‑limit user inputs and handle API errors gracefully.
- If you shared the key in a chat or committed it, rotate it immediately.

---

## Contributing
- Fork the repo, create a branch, make changes, and open a PR.
- Keep changes small and focused; add tests for the core logic if adding features.

---

## License
Add your chosen license here (e.g., MIT). If you haven’t chosen one, add a `LICENSE` file.

---

If you want, I can:
- generate a `requirements.txt` for the exact packages used, or
- update `main.py` to add an optional voice input flow (press `v` to speak), or
- convert the streaming TTS to smaller word‑level chunks for even earlier playback.

Tell me which of those you want next.
