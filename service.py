from typing import List, Optional
from datetime import datetime, timedelta
from loguru import logger
from sqlalchemy.exc import IntegrityError
from models import Review
from database import db_manager
from wb_api import WildberriesAPI


class ReviewService:
    def __init__(self):
        self.db_manager = db_manager

    async def fetch_and_save_bad_reviews(
            self,
            nm_id: int,
            min_rating: int = 3,
            days_back: int = 3
    ) -> int:
        """
        Основной метод: получает и сохраняет плохие отзывы
        Возвращает количество сохраненных отзывов
        """
        date_from = datetime.now() - timedelta(days=days_back)
        saved_count = 0

        async with WildberriesAPI() as wb_api:
            feedbacks = await wb_api.get_feedbacks(nm_id, date_from)

            if not feedbacks:
                logger.warning(f"No feedbacks found for nm_id {nm_id}")
                return 0

            bad_reviews = [
                feedback for feedback in feedbacks
                if feedback.get('productValuation', 5) < min_rating
            ]

            logger.info(f"Found {len(bad_reviews)} bad reviews out of {len(feedbacks)} total")

            for feedback_data in bad_reviews:
                if await self._save_review(feedback_data, min_rating):
                    saved_count += 1

        return saved_count

    async def _save_review(self, feedback_data: dict, min_rating: int) -> bool:
        """Сохранение отзыва в базу данных с проверкой на дубликаты"""
        try:
            review = Review.from_wb_data(feedback_data, min_rating)

            with self.db_manager.get_session() as session:
                # Проверяем, существует ли уже такой отзыв
                existing = session.query(Review).filter(
                    Review.review_id == review.review_id,
                    Review.nm_id == review.nm_id
                ).first()

                if not existing:
                    session.add(review)
                    logger.info(f"Saved review {review.review_id} for product {review.nm_id}")
                    return True
                else:
                    logger.debug(f"Review {review.review_id} already exists")
                    return False

        except IntegrityError as e:
            logger.warning(f"Integrity error (likely duplicate): {e}")
            return False
        except Exception as e:
            logger.error(f"Error saving review: {e}")
            return False

    async def get_bad_reviews(self, nm_id: Optional[int] = None) -> List[Review]:
        """Получение сохраненных плохих отзывов"""
        try:
            with self.db_manager.get_session() as session:
                query = session.query(Review).filter(Review.matching_rating == True)

                if nm_id:
                    query = query.filter(Review.nm_id == nm_id)

                return query.all()

        except Exception as e:
            logger.error(f"Error fetching reviews: {e}")
            return []