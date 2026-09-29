"""Langfuse tracing. If Langfuse keys are missing in .env, everything still runs (tracing is simply off)."""
import os

import askit_core.config  # noqa: F401  (loads .env first)

ENABLED = bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))

if ENABLED:
    from langfuse import get_client, observe  # noqa: F401

    langfuse = get_client()
else:
    def observe(*args, **kwargs):
        """No-op stand-in for langfuse.observe (works as @observe and @observe(...))."""
        if args and callable(args[0]) and len(args) == 1 and not kwargs:
            return args[0]
        return lambda fn: fn

    class _Off:
        def __getattr__(self, name):
            return lambda *a, **k: None

    langfuse = _Off()
