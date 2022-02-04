import uuid
from datetime import date

from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.db import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(250), nullable=False)
    excerpt = Column(String(500), nullable=False)
    featured_image = Column(String(250), nullable=False)
    slug = Column(String(300), nullable=False)
    date_created = Column(Date, default=date.today)

    def __repr__(self) -> str:
        return f"Recipe({self.title})"


class RecipeContent(Base):
    __tablename__ = "recipe_content"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recipe_id = Column(UUID, ForeignKey("recipes.id"))
    section = Column(String(100), nullable=False)
    content = Column(String(2000))

    recipe = relationship(Recipe)

    def __repr__(self) -> str:
        return f"RecipeContent({self.recipe_id})"
