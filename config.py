import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///reviews.db")
    WB_API_BASE_URL: str = "https://feedbacks-api.wildberries.ru/api/v1/feedbacks"
    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 2

config = Config()