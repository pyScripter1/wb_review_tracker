from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from loguru import logger
from models import Base
from config import config


class DatabaseManager:
    def __init__(self, database_url: str = None):
        self.database_url = database_url or config.DATABASE_URL
        self.engine = None
        self.session_factory = None

    def connect(self):
        """Установка соединения с базой данных"""
        try:
            self.engine = create_engine(
                self.database_url,
                echo=False,
                pool_size=10,
                max_overflow=20,
                pool_timeout=30,
                pool_recycle=1800
            )
            self.session_factory = scoped_session(
                sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
            )
            logger.info(f"Connected to database: {self.database_url}")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise

    def create_tables(self):
        """Создание таблиц в базе данных"""
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Database tables created successfully")
        except SQLAlchemyError as e:
            logger.error(f"Failed to create tables: {e}")
            raise

    @contextmanager
    def get_session(self):
        """Контекстный менеджер для работы с сессией"""
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Session rollback due to error: {e}")
            raise
        finally:
            session.close()

    def close(self):
        """Закрытие соединения с базой данных"""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")


# Глобальный экземпляр менеджера БД
db_manager = DatabaseManager()