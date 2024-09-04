"""
Схемы данных с использованием Pydantic для работы с рецептами и ингредиентами
"""

from pydantic import BaseModel, Field
from typing import List


# Схема для ингредиента
class IngredientBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


# Схема для ингредиента с добавлением количества и единицы измерения
class IngredientIn(IngredientBase):
    quantity: float  # или int, если количество всегда целое число
    unit: str

    class Config:
        orm_mode = True


# Базовая схема для рецепта
class BaseRecipe(BaseModel):
    name: str = Field(..., title='Название рецепта')
    description: str = Field(..., title='Описание рецепта')
    cook_time: int = Field(..., title='Время приготовления')
    ingredients: List[IngredientIn]

    class Config:
        orm_mode = True


# Схема для создания рецепта
class RecipeIn(BaseRecipe):
    ...


# Схема для вывода рецепта
class RecipeOut(BaseRecipe):
    id: int


# Схема для вывода списка рецептов
class RecipeOutInList(BaseModel):
    name: str
    views_number: int
    cook_time: int
