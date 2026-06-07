from datetime import timedelta

from django.db import models
from django.utils import timezone


class PizzaOrder(models.Model):
    """A pizza order placed by chat or by form."""

    NAMES = [('cheese', 'Cheese'), ('pepperoni', 'Pepperoni'), ('vegetarian', 'Vegetarian')]
    SIZES = [('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')]

    name = models.CharField(max_length=50, choices=NAMES)
    size = models.CharField(max_length=50, choices=SIZES)
    created_at = models.DateTimeField(auto_now_add=True)
    total_time = models.IntegerField(default=60)

    def add_extra_time(self, seconds: int) -> None:
        """Bump cooking time by `seconds`."""
        self.total_time += seconds

    @property
    def seconds_left(self) -> int:
        delta = self.created_at + timedelta(seconds=self.total_time) - timezone.now()
        return max(0, int(delta.total_seconds()))

    @property
    def is_finished(self) -> bool:
        return self.seconds_left == 0
