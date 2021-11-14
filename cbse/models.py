from django.db import models

class Board(models.Model):
    name = models.CharField(max_length=15, blank=False, null=False)

    def __str__(self) -> str:
        return self.name

class Standard(models.Model):
    name = models.CharField(max_length=15, blank=False, null=False)
    is_locked = models.BooleanField(default=False)
    boards = models.ManyToManyField(to=Board)

    def __str__(self) -> str:
        return "{} -  {}".format(self.name, self.is_locked)

