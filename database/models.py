import uuid
from datetime import date

from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.db import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(250), nullable=False)
    excerpt = Column(String(500), nullable=False)
    featured_image = Column(String(250), nullable=False)
    slug = Column(String(300), nullable=False, index=True)
    date_created = Column(Date, default=date.today)

    def __repr__(self) -> str:
        return f"Recipe({self.title})"


class RecipeContent(Base):
    __tablename__ = "recipe_content"

    id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(UUID, ForeignKey("recipes.id"))
    section = Column(String(100), nullable=False, index=True)
    content = Column(String(10000), index=True)

    recipe = relationship(Recipe)

    def __repr__(self) -> str:
        return f"RecipeContent({self.recipe_id})"
