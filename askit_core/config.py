"""Settings loaded from your .env file."""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

DATA_DIR = ROOT / "askit_data"
REGION = os.getenv("AWS_REGION", "us-east-1")
SMALL_MODEL = os.getenv("BEDROCK_SMALL_MODEL_ID", "")
LARGE_MODEL = os.getenv("BEDROCK_LARGE_MODEL_ID", "")


def require_models():
    """Stop with a clear message if model IDs are missing in .env."""
    missing = [n for n, v in (("BEDROCK_SMALL_MODEL_ID", SMALL_MODEL), ("BEDROCK_LARGE_MODEL_ID", LARGE_MODEL))
               if not v or v == "REPLACE_ME"]
    if missing:
        raise SystemExit(f"Set {', '.join(missing)} in .env (trainer shares the values).")
