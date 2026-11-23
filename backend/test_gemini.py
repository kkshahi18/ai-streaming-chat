"""Explicit live diagnostic; running this script uses Gemini API quota."""
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from diagnostics import log_failure

def main():
    load_dotenv(Path(__file__).resolve().with_name(".env"))
    key = os.getenv("GEMINI_API_KEY", "").strip()
    print("API key present:", bool(key))
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    print("Configured model:", model)
    if not key:
        return 1
    failed = False
    for streaming in (False, True):
        label = "Streaming" if streaming else "Normal"
        try:
            with genai.Client(api_key=key) as client:
                args = dict(model=model, contents="Say hello in one sentence.")
                chunks = (client.models.generate_content_stream(**args) if streaming
                          else [client.models.generate_content(**args)])
                if not any([bool(chunk.text) for chunk in chunks]):
                    raise RuntimeError("No text returned")
            print(label, "PASS (text received)")
        except Exception as exc:
            failed = True
            print(label, "FAIL")
            log_failure(exc)
    return int(failed)

if __name__ == "__main__":
    raise SystemExit(main())
