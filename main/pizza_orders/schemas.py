from typing import Literal

from pydantic import BaseModel


class PizzaOrderIn(BaseModel):
    name: Literal['cheese', 'pepperoni', 'vegetarian']
    size: Literal['small', 'medium', 'large']
