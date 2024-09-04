"""
Базовое API с использованием FastAPI и SQLAlchemy для работы с объектами Recipe и Ingredient
"""

from typing import List
from fastapi import FastAPI, Path, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

import models
import schemas
from database import engine, session

app = FastAPI()

"""
Обработчики событий при запуске и завершении приложения
"""


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


@app.post('/recipes', response_model=schemas.RecipeOut)
async def recipe(recipe: schemas.RecipeIn) -> models.Recipe:
    """
    Обработчик POST-запроса для добавления рецепта
    """
    new_recipe = models.Recipe(
        name=recipe.name,
        description=recipe.description,
        cook_time=recipe.cook_time
    )
    # Добавляем рецепт в сессию и сохраняем его в базе данных
    async with session.begin():  # Открываем одну транзакцию для всех операций

        session.add(new_recipe)
        await session.flush()  # Обновляем сессию, чтобы получить ID нового рецепта

        # Добавление ингредиентов из рецепта в таблицу ингредиентов (после проверки наличия ингредиента в таблице)
        ingredients = []
        for ingredient_data in recipe.ingredients:
            result = await session.execute(
                select(models.Ingredient).where(models.Ingredient.name == ingredient_data.name)
            )
            ingredient = result.scalar_one_or_none()

            if ingredient is None:
                ingredient = models.Ingredient(name=ingredient_data.name)
                session.add(ingredient)
                await session.flush()

            # Добавляем записи в промежуточную таблицу recipe_ingredients
            new_recipe_ingredient = models.RecipeIngredient(
                recipe_id=new_recipe.id,
                ingredient_id=ingredient.id,
                quantity=ingredient_data.quantity,
                unit=ingredient_data.unit
            )
            session.add(new_recipe_ingredient)

            # Создание списка ингредиентов, используемого для вывода информации о добавленном рецепте
            ingredients.append({
                "name": ingredient.name,
                "quantity": ingredient_data.quantity,
                "unit": ingredient_data.unit
            })

    # Добавленный рецепт согласно схеме вывода
    recipe_out = schemas.RecipeOut(
        id=new_recipe.id,
        name=new_recipe.name,
        description=new_recipe.description,
        cook_time=new_recipe.cook_time,
        ingredients=ingredients
    )

    return recipe_out


@app.get('/recipes', response_model=List[schemas.RecipeOutInList])
async def get_recipes() -> List[models.Recipe]:
    """
    Обработчик GET-запроса для вывода списка рецептов с сортировкой по количеству просмотров и времени приготовления
    """
    res = await session.execute(select(models.Recipe).order_by(
        models.Recipe.views_number.desc(),  # сортировка по убыванию по views_number
        models.Recipe.cook_time.asc()  # сортировка по возрастанию по cook_time
    ))
    return res.scalars().all()


@app.get('/recipes/{idx}', response_model=schemas.RecipeOut)
async def get_recipes_by_id(
        idx: int = Path(
            ...,
            title='Id of the recipe to view'
        )
) -> models.Recipe:
    """
    Обработчик GET-запроса для вывода рецепта по его ID
    """
    stmt = (
        select(models.Recipe)
        .options(selectinload(models.Recipe.recipe_ingredients).selectinload(models.RecipeIngredient.ingredient))
        .where(models.Recipe.id == idx)
    )
    res = await session.execute(stmt)

    # Извлекаем объект модели из результата запроса
    recipe = res.scalar_one_or_none()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Формирование списка ингредиентов для запрашиваемого рецепта
    ingredients = [
        schemas.IngredientIn(
            name=assoc.ingredient.name,
            quantity=assoc.quantity,
            unit=assoc.unit
        )
        for assoc in recipe.recipe_ingredients
    ]

    # Формирование рецепта согласно схеме вывода
    recipe_out = schemas.RecipeOut(
        id=recipe.id,
        name=recipe.name,
        description=recipe.description,
        cook_time=recipe.cook_time,
        ingredients=ingredients
    )

    return recipe_out
