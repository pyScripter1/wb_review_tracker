import asyncio
import argparse
from loguru import logger
from database import db_manager
from service import ReviewService


def setup_logging():
    """Настройка логирования"""
    logger.add(
        "wb_reviews.log",
        rotation="10 MB",
        retention="10 days",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )


def parse_arguments():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(description="Wildberries Bad Reviews Tracker")
    parser.add_argument("nm_id", type=int, help="Артикул товара Wildberries")
    parser.add_argument("--min-rating", type=int, default=3,
                        help="Минимальный рейтинг для плохого отзыва (по умолчанию 3)")
    parser.add_argument("--days-back", type=int, default=3,
                        help="Количество дней для поиска отзывов (по умолчанию 3)")
    return parser.parse_args()


async def main():
    """Основная функция"""
    setup_logging()

    # Парсим аргументы
    args = parse_arguments()

    # Инициализируем базу данных
    try:
        db_manager.connect()
        db_manager.create_tables()
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return

    # Создаем сервис
    service = ReviewService()

    logger.info(f"Starting review collection for nm_id {args.nm_id}")
    logger.info(f"Parameters: min_rating={args.min_rating}, days_back={args.days_back}")

    try:
        # Получаем и сохраняем отзывы
        saved_count = await service.fetch_and_save_bad_reviews(
            nm_id=args.nm_id,
            min_rating=args.min_rating,
            days_back=args.days_back
        )

        logger.info(f"Successfully saved {saved_count} bad reviews")

        # Показываем сохраненные отзывы
        reviews = await service.get_bad_reviews(args.nm_id)
        if reviews:
            logger.info("\nSaved bad reviews:")
            for review in reviews:
                logger.info(f"  - Rating: {review.rating}, Date: {review.created_date}, User: {review.user_name}")

    except Exception as e:
        logger.error(f"Error during review collection: {e}")
    finally:
        db_manager.close()


if __name__ == "__main__":
    asyncio.run(main())