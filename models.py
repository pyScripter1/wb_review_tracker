from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class Review(Base):
    __tablename__ = "wb_reviews"
    __table_args__ = (UniqueConstraint('review_id', 'nm_id', name='unique_review_product'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    review_id = Column(String(36), nullable=False)
    nm_id = Column(Integer, nullable=False)  # артикул товара
    text = Column(Text, nullable=True)
    rating = Column(Integer, nullable=False)
    created_date = Column(DateTime, nullable=False)
    user_name = Column(String(255), nullable=True)
    matching_rating = Column(Boolean, default=False)  # соответствует ли критерию плохого отзыва
    archived = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Review(id={self.review_id}, rating={self.rating}, product={self.nm_id})>"

    @classmethod
    def from_wb_data(cls, data: dict, min_rating: int) -> 'Review':
        """Создает объект Review из данных Wildberries"""
        return cls(
            review_id=str(data.get('id', uuid.uuid4())),
            nm_id=data.get('nmId'),
            text=data.get('text'),
            rating=data.get('productValuation', 0),
            created_date=datetime.fromisoformat(data.get('createdDate').replace('Z', '+00:00')),
            user_name=data.get('wbUserDetails', {}).get('name'),
            matching_rating=data.get('productValuation', 0) < min_rating
        )