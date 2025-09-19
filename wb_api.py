import httpx
import asyncio
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from loguru import logger
from config import config


class WildberriesAPI:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or config.WB_API_BASE_URL
        self.client = None

    async def __aenter__(self):
        self.client = httpx.AsyncClient(timeout=config.REQUEST_TIMEOUT)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()

    async def get_feedbacks(self, nm_id: int, date_from: Optional[datetime] = None) -> List[Dict]:
        """
        Получение отзывов для товара с артикулом nm_id
        """
        if date_from is None:
            date_from = datetime.now() - timedelta(days=3)

        params = {
            'nmId': nm_id,
            'take': 5000,  # максимальное количество отзывов
            'skip': 0,
            'dateFrom': date_from.isoformat() + 'Z'
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }

        try:
            response = await self.client.get(
                self.base_url,
                params=params,
                headers=headers
            )
            response.raise_for_status()

            data = response.json()
            return data.get('data', {}).get('feedbacks', [])

        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching feedbacks for nm_id {nm_id}: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching feedbacks: {e}")
            return []