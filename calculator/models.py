from django.contrib.auth.models import User
from django.db import models


class Calculation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calculation_expression = models.CharField(max_length=140)
    calculation_answer = models.CharField(max_length=140)
    has_errors = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.calculation_expression} by {self.user.get_full_name()}"
