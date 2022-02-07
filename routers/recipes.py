from typing import List
from uuid import UUID

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from pydantic import BaseModel
from sqlalchemy import and_
from sqlalchemy.orm import Session

from . import get_db
from . import router
from database.models import Recipe
from database.models import RecipeContent


class RecipeBase(BaseModel):
    title: str
    excerpt: str
    featured_image: str
    slug: str

    class Config:
        orm_mode = True


class RecipeContents(BaseModel):
    id: UUID
    prep_time: int
    cook_time: int
    total_time: int
    ingredients: List[str]
    notes: str
    directions: List[str]
    excerpt: str
    tags: List[str]

    class Config:
        orm_mode = True


class RecipeTag(BaseModel):
    title: str
    slug: str
    featured_image: str
    excerpt: str
    recipe_id: UUID

    class Config:
        orm_mode = True


@router.get(
    "/recipes/all", response_model=List[RecipeBase], status_code=status.HTTP_200_OK
)
def get_all_recipes(db: Session = Depends(get_db)):
    try:
        return db.query(Recipe).all()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not fetch all the recipes",
        )


@router.get(
    "/recipe/{slug}", response_model=RecipeContents, status_code=status.HTTP_200_OK
)
def get_Recipe_from_slug(slug: str, db: Session = Depends(get_db)):
    try:
        recipe = db.query(Recipe.excerpt, Recipe.id).filter(Recipe.slug == slug).first()

        contents = (
            db.query(RecipeContent.section, RecipeContent.content)
            .join(Recipe, Recipe.id == RecipeContent.recipe_id)
            .filter(Recipe.slug == slug)
            .all()
        )

        full_recipe = {content[0]: content[1] for content in contents}

        full_recipe["prep_time"] = int(full_recipe["prep_time"])
        full_recipe["cook_time"] = int(full_recipe["cook_time"])
        full_recipe["total_time"] = full_recipe["prep_time"] + full_recipe["cook_time"]
        full_recipe["ingredients"] = full_recipe["ingredients"].split(",")
        full_recipe["directions"] = full_recipe["directions"].split("|")
        full_recipe["tags"] = full_recipe["tags"].split(",")

        full_recipe["excerpt"] = recipe.excerpt
        full_recipe["id"] = recipe.id

        return full_recipe
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not fetch recipe",
        )


@router.get(
    "/recipe/tag/{tag}", response_model=List[RecipeTag], status_code=status.HTTP_200_OK
)
def get_recipes_from_tag(tag: str, db: Session = Depends(get_db)):
    try:
        return (
            db.query(
                Recipe.title,
                Recipe.slug,
                Recipe.featured_image,
                Recipe.excerpt,
                RecipeContent.recipe_id,
            )
            .join(RecipeContent, RecipeContent.recipe_id == Recipe.id)
            .filter(
                and_(
                    RecipeContent.section == "tags",
                    RecipeContent.content.ilike("%" + tag + "%"),
                )
            )
            .all()
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not fetch recipe from tag",
        )
