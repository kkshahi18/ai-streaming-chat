"""Safe diagnostics: traceback locations plus allowlisted error descriptions.

Never log raw provider messages, headers, source lines, or local variables.
"""
import logging
import traceback

MESSAGES = {
    400: "Gemini rejected the request (400). Check request and model configuration.",
    401: "Gemini authentication failed (401). Check the backend API key.",
    403: "Gemini access denied (403). Check API permissions.",
    404: "Gemini model or resource not found (404). Check the configured model.",
    429: "Gemini quota or rate limit reached (429). Try later or check quota.",
    500: "Gemini internal error (500). Try again later.",
    503: "Gemini temporarily unavailable (503). Try again later.",
}

def public_error(exc):
    code = getattr(exc, "code", None)
    if not isinstance(code, int):
        code = None
    return {"code": code, "message": MESSAGES.get(code,
        "AI generation failed. Check backend diagnostics for connection or SDK errors.")}

def log_failure(exc):
    info = public_error(exc)
    frames = "\n".join(
        f"  {frame.filename}:{frame.lineno} in {frame.name}"
        for frame in traceback.extract_tb(exc.__traceback__)
    )
    logging.getLogger("uvicorn.error").error(
        "Gemini exception %s, status=%s: %s\nTraceback (locations only):\n%s",
        type(exc).__name__, info["code"], info["message"], frames,
    )
