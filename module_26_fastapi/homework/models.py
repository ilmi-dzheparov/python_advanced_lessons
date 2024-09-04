"""
Модели для работы с базой данных, используя SQLAlchemy
"""

from sqlalchemy import Column, String, Integer, Table, ForeignKey, Float
from sqlalchemy.orm import relationship

from database import Base


# recipe_ingredients = Table('recipe_ingredients', Base.metadata,
#                            Column('recipe_id', Integer, ForeignKey('recipes.id'), primary_key=True),
#                            Column('ingredient_id', Integer, ForeignKey('ingredients.id'), primary_key=True),
#                            Column('quantity', Float, nullable=False),
#                            Column('unit', String(50)),
#                            # extend_existing=True
#                            )


class RecipeIngredient(Base):
    """
    Эта модель представляет собой промежуточную таблицу, которая связывает таблицы recipes и ingredients.
    Это необходимо для реализации отношения "многие ко многим" (many-to-many)
    """
    __tablename__ = 'recipe_ingredients'
    recipe_id = Column(Integer, ForeignKey('recipes.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), primary_key=True)
    quantity = Column(Float, nullable=False)  # Количество используемого ингредиента
    unit = Column(String(50))  # Единица измерения
    recipe = relationship('Recipe', back_populates='recipe_ingredients')
    ingredient = relationship('Ingredient', back_populates='recipe_ingredients')


class Recipe(Base):
    """
    Эта модель представляет таблицу рецептов recipes
    """
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    name = Column(String)  # Название рецепта
    cook_time = Column(Integer, nullable=False)  # Время приготовления
    description = Column(String)  # Описание рецепта
    # ingredients = relationship('Ingredient', secondary=recipe_ingredients, back_populates='recipes')
    views_number = Column(Integer, default=0)  # Количество просмотров
    recipe_ingredients = relationship('RecipeIngredient', back_populates='recipe')


class Ingredient(Base):
    """
    Эта модель представляет таблицу рецептов ingredients
    """
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(String)  # Название ингредиента
    # recipes = relationship('Recipe', secondary=recipe_ingredients, back_populates='ingredients')
    recipe_ingredients = relationship('RecipeIngredient', back_populates='ingredient')
