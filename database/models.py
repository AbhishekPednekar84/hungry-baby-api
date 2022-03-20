import uuid
from datetime import date

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship

from database.db import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(250), nullable=False)
    excerpt = Column(String(500), nullable=False)
    featured_image = Column(String(250), nullable=False)
    slug = Column(String(300), nullable=False, index=True)
    author = Column(String(50))
    primary_tag = Column(String(50))
    date_created = Column(Date, default=date.today)
    date_updated = Column(Date)
    active_recipe = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"Recipe({self.title})"


class RecipeContent(Base):
    __tablename__ = "recipe_content"

    id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(UUID, ForeignKey("recipes.id"))
    prep_time = Column(Integer, nullable=False)
    cook_time = Column(Integer, nullable=False)
    ingredients = Column(String(5000), nullable=False, index=True)
    procedure = Column(String(10000), nullable=False, index=True)
    tags = Column(String(1000), nullable=False, index=True)
    notes = Column(String(1000))
    nutritional_value = Column(MutableList.as_mutable(JSONB))
    ingredients_token = Column(TSVECTOR)
    plugged_products = Column(String(50))

    recipe = relationship(Recipe)

    def __repr__(self) -> str:
        return f"RecipeContent({self.recipe_id})"


class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(UUID, ForeignKey("recipes.id"))
    question = Column(String(500), nullable=False)
    answer = Column(String(2000), nullable=False)

    recipe = relationship(Recipe)

    def __repr__(self) -> str:
        return f"FAQ({self.question})"


class ProductPlug(Base):
    __tablename__ = "productplugs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(100))
    product_name = Column(String(100))
    product_url = Column(String(500))
    product_image = Column(String(500))

    def __repr__(self) -> str:
        return f"ProductPlug({self.id}, {self.product_name})"
