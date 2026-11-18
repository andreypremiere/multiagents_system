import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

WORKSPACE_PATH = Path(
    os.getenv("WORKSPACE_PATH", "./workspace")
).resolve()

POSTGRES_DB = os.getenv("POSTGRES_DB")
USER_AGENT = os.getenv("USER_AGENT")
AGENT_PASSWORD = os.getenv("AGENT_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5442")

required_db_vars = {
    "POSTGRES_DB": POSTGRES_DB,
    "USER_AGENT": USER_AGENT,
    "AGENT_PASSWORD": AGENT_PASSWORD,
}
missing_vars = [name for name, val in required_db_vars.items() if not val]

if missing_vars:
    raise RuntimeError(f"В .env не указаны обязательные переменные БД: {', '.join(missing_vars)}")

encoded_password = quote_plus(AGENT_PASSWORD)
DATABASE_URL = f"postgresql://{USER_AGENT}:{encoded_password}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

AGENT_MAX_ITERATIONS = int(
    os.getenv("AGENT_MAX_ITERATIONS", "10")
)

AGENT_TEMPERATURE = float(
    os.getenv("AGENT_TEMPERATURE", "0.0")
)

WORKSPACE_PATH.mkdir(parents=True, exist_ok=True)