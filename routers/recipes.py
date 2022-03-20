import random
from typing import List
from uuid import UUID

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import get_db
from . import router
from database.models import FAQ
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
    procedure: List[str]
    excerpt: str
    tags: List[str]
    slug: str
    featured_image: str

    class Config:
        orm_mode = True


class RecipeTag(BaseModel):
    title: str
    slug: str
    featured_image: str
    excerpt: str
    recipe_id: UUID
    tags: str

    class Config:
        orm_mode = True


def all_recipes(db: Session = Depends(get_db)):
    return (
        db.query(Recipe)
        .filter(Recipe.active_recipe == True)
        .order_by(Recipe.date_created.desc())
        .all()
    )


def clear_search(meal_type: str, db: Session = Depends(get_db)):

    return (
        db.query(
            Recipe.title,
            Recipe.slug,
            Recipe.featured_image,
            Recipe.excerpt,
            RecipeContent.recipe_id,
            RecipeContent.tags,
        )
        .join(RecipeContent, RecipeContent.recipe_id == Recipe.id)
        .filter(
            RecipeContent.tags.ilike(f"%{meal_type}%"), Recipe.active_recipe == True
        )
        .all()
    )


def clear_search_for_primary_tag(primary_tag: str, db: Session = Depends(get_db)):
    return (
        db.query(
            Recipe.title,
            Recipe.slug,
            Recipe.featured_image,
            Recipe.excerpt,
            RecipeContent.recipe_id,
            RecipeContent.tags,
        )
        .join(RecipeContent, RecipeContent.recipe_id == Recipe.id)
        .filter(Recipe.primary_tag == primary_tag, Recipe.active_recipe == True)
        .all()
    )


@router.get(
    "/recipes/all", response_model=List[RecipeBase], status_code=status.HTTP_200_OK
)
def get_all_recipes(db: Session = Depends(get_db)):
    try:
        return all_recipes(db)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not fetch all the recipes",
        )


@router.get("/recipe/random", response_model=RecipeBase, status_code=status.HTTP_200_OK)
def get_random_recipe(db: Session = Depends(get_db)):
    try:
        recipes = all_recipes(db)

        total_recipes = len(recipes)

        random_recipe = random.randint(0, total_recipes - 1)

        return recipes[random_recipe]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not fetch all the recipes",
        )


@router.get("/recipe/{slug}", status_code=status.HTTP_200_OK)
def get_Recipe_from_slug(slug: str, db: Session = Depends(get_db)):
    try:
        full_recipe = {}

        recipe = (
            db.query(
                Recipe.id,
                Recipe.title,
                Recipe.excerpt,
                Recipe.id,
                Recipe.featured_image,
                Recipe.date_created,
                Recipe.author,
                Recipe.primary_tag,
            )
            .filter(Recipe.slug == slug, Recipe.active_recipe == True)
            .first()
        )

        if not recipe:
            return {}

        faqs = db.query(FAQ).filter(FAQ.recipe_id == str(recipe.id)).all()

        faq_list = [{"question": faq.question, "answer": faq.answer} for faq in faqs]

        contents = (
            db.query(RecipeContent)
            .join(Recipe, Recipe.id == RecipeContent.recipe_id)
            .filter(Recipe.slug == slug)
            .all()
        )

        for content in contents:
            full_recipe["prep_time"] = content.prep_time
            full_recipe["cook_time"] = content.cook_time
            full_recipe["total_time"] = content.prep_time + content.cook_time
            full_recipe["ingredients"] = content.ingredients.split(",")
            full_recipe["procedure"] = content.procedure.split("|")
            full_recipe["notes"] = content.notes.split("|")
            full_recipe["tags"] = content.tags.split(",")
            full_recipe["nutritional_value"] = content.nutritional_value
            full_recipe["faqs"] = faq_list

            full_recipe["title"] = recipe.title
            full_recipe["excerpt"] = recipe.excerpt
            full_recipe["id"] = recipe.id
            full_recipe["primary_tag"] = recipe.primary_tag.title()
            full_recipe["slug"] = slug
            full_recipe["featured_image"] = recipe.featured_image
            full_recipe["date_published"] = recipe.date_created
            full_recipe["author"] = recipe.author

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
        tag = "%" if tag == "all" else f"%{tag}%"

        return (
            db.query(
                Recipe.title,
                Recipe.slug,
                Recipe.featured_image,
                Recipe.excerpt,
                RecipeContent.recipe_id,
                RecipeContent.tags,
            )
            .join(RecipeContent, RecipeContent.recipe_id == Recipe.id)
            .filter(RecipeContent.tags.ilike(tag), Recipe.active_recipe == True)
            .order_by(Recipe.date_created.desc())
            .all()
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not fetch recipe from tag",
        )


@router.get("/verify/tag/{tag}", status_code=status.HTTP_200_OK)
def verify_tag(tag: str, db: Session = Depends(get_db)):
    try:
        return db.query(Recipe.id).filter(Recipe.primary_tag == tag).count()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not verify tag",
        )


@router.get(
    "/recipe/primary_tag/{primary_tag}",
    response_model=List[RecipeTag],
    status_code=status.HTTP_200_OK,
)
def get_recipes_from_primary_tag(primary_tag: str, db: Session = Depends(get_db)):
    try:
        return (
            db.query(
                Recipe.title,
                Recipe.slug,
                Recipe.featured_image,
                Recipe.excerpt,
                RecipeContent.recipe_id,
                RecipeContent.tags,
            )
            .join(RecipeContent, RecipeContent.recipe_id == Recipe.id)
            .filter(
                Recipe.primary_tag == primary_tag.lower(), Recipe.active_recipe == True
            )
            .order_by(Recipe.date_created.desc())
            .all()
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not fetch recipe from the primary tag",
        )


@router.get(
    "/recipe/search/{search_text}/{meal_type}",
    response_model=List[RecipeTag],
    status_code=status.HTTP_200_OK,
)
def search_recipes(search_text: str, meal_type: str, db: Session = Depends(get_db)):
    try:
        # search_text = "%" if not search_text else "%" + search_text + "%"

        if search_text == "%":
            return clear_search(meal_type, db)

        return (
            db.query(
                Recipe.title,
                Recipe.slug,
                Recipe.featured_image,
                Recipe.excerpt,
                RecipeContent.recipe_id,
                RecipeContent.tags,
            )
            .join(RecipeContent, RecipeContent.recipe_id == Recipe.id)
            .filter(
                RecipeContent.tags.ilike(f"%{meal_type}%"),
                RecipeContent.ingredients_token.match(f"{search_text}:*"),
                Recipe.active_recipe == True,
            )
            .order_by(Recipe.date_created.desc())
            .all()
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not fetch recipe from tag",
        )


@router.get(
    "/recipe/search/primary/{search_text}/{primary_tag}",
    response_model=List[RecipeTag],
    status_code=status.HTTP_200_OK,
)
def search_recipes_from_primary_tag(
    search_text: str, primary_tag: str, db: Session = Depends(get_db)
):
    try:
        # search_text = "%" if not search_text else "%" + search_text + "%"

        if search_text == "%":
            return clear_search_for_primary_tag(primary_tag, db)

        return (
            db.query(
                Recipe.title,
                Recipe.slug,
                Recipe.featured_image,
                Recipe.excerpt,
                RecipeContent.recipe_id,
                RecipeContent.tags,
            )
            .join(RecipeContent, RecipeContent.recipe_id == Recipe.id)
            .filter(
                RecipeContent.ingredients_token.match(f"{search_text}:*"),
                Recipe.active_recipe == True,
            )
            .order_by(Recipe.date_created.desc())
            .all()
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not fetch recipe from tag",
        )
