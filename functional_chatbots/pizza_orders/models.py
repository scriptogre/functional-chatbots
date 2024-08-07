from datetime import timedelta

from django.db import models
from django.utils import timezone

"""
This is a Django model for a pizza order. It has fields for the name, size, created_at, and total_time of the order.
"""


class PizzaOrder(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, choices=[("cheese", "Cheese"), ("pepperoni", "Pepperoni"), ("vegetarian", "Vegetarian")])
    size = models.CharField(max_length=50, choices=[("small", "Small"), ("medium", "Medium"), ("large", "Large")])
    created_at = models.DateTimeField(auto_now_add=True)
    total_time = models.IntegerField(default=60)

    def add_extra_time(self, seconds: int) -> None:
        """Add extra time to the total cooking time of the pizza order."""
        self.total_time += seconds

    @property
    def seconds_left(self) -> int:
        """Calculate the seconds left until the pizza order is finished."""
        delta = self.created_at + timedelta(seconds=self.total_time) - timezone.now()
        return max(0, int(delta.total_seconds()))

    @property
    def is_finished(self) -> bool:
        """Check if the pizza order is finished."""
        return self.seconds_left == 0
