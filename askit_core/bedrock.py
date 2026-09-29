"""Bedrock client with safe retries (handles throttling when the whole class runs at once)."""
import boto3
from botocore.config import Config

from askit_core.config import REGION


def client():
    return boto3.client(
        "bedrock-runtime",
        region_name=REGION,
        config=Config(retries={"max_attempts": 8, "mode": "adaptive"}, read_timeout=120, connect_timeout=10),
    )
