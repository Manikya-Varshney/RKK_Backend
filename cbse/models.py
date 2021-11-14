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

class Subject(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    standards = models.ManyToManyField(to= Standard)

    def __str__(self) -> str:
        return self.name

class Chapter(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    chapter_link = models.URLField()
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "{} - {} - {}".format(self.name, self.subject.name, self.chapter_link)
