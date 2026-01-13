from functools import lru_cache
from pathlib import Path
import yaml

# from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# 项目根目录（假设结构是 root/app/setting.py）
BASE_DIR = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    # ----------------
    # ENV
    # ----------------
    ENV: str = "dev"
    DEBUG: bool = False

    # ----------------
    # OpenAI
    # ----------------
    OPENAI_API_KEY: str
    OPENAI_MODEL: str
    SUMMARY_MAX_CHARS: int

    # ----------------
    # BigQuery
    # ----------------
    GCP_PROJECT_ID: str
    BIGQUERY_DATASET: str
    UK_TABLE_ID: str
    BIGQUERY_KEY_PATH: Path

    # ----------------
    # News
    # ----------------
    UK_NEWS_TOP_N: int

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


def load_yaml_config() -> dict:
    with open(BASE_DIR / "app/config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@lru_cache()
def get_settings() -> Settings:
    yaml_cfg = load_yaml_config()

    return Settings(
        ENV=yaml_cfg["env"],
        DEBUG=yaml_cfg["debug"],

        OPENAI_MODEL=yaml_cfg["openai"]["model"],
        SUMMARY_MAX_CHARS=yaml_cfg["openai"]["summary_max_chars"],

        GCP_PROJECT_ID=yaml_cfg["gcp"]["project_id"],
        BIGQUERY_DATASET=yaml_cfg["gcp"]["bigquery"]["dataset_id"],
        UK_TABLE_ID=yaml_cfg["gcp"]["bigquery"]["uk_table_id"],
        BIGQUERY_KEY_PATH= BASE_DIR / "app/bigquery_key" /yaml_cfg["gcp"]["bigquery_key_path"],

        UK_NEWS_TOP_N=yaml_cfg["news"]["uk_top_n"],
        )
