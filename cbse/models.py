from django.db import models

class Board(models.Model):
    name = models.CharField(max_length=15, blank=False, null=False)

    def __str__(self) -> str:
        return self.name

class Standard(models.Model):
    name = models.CharField(max_length=15, blank=False, null=False)
    is_locked = models.BooleanField(default=False)
    # boards = models.ManyToManyField(to=Board)
    board = models.ForeignKey(to=Board, on_delete=models.CASCADE, related_name="standards")

    def __str__(self) -> str:
        return "{} -  {}".format(self.name, self.is_locked)

class Subject(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    # standards = models.ManyToManyField(to= Standard)
    standard = models.ForeignKey(to = Standard, on_delete=models.CASCADE, related_name="subjects")

    def __str__(self) -> str:
        return "{} - {} - {}".format(self.name, self.standard.board.name, self.standard.name)

class Chapter(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    chapter_link = models.URLField()
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, related_name="chapters")
    is_locked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "{} - {} - {}".format(self.name, self.subject.name, self.chapter_link)

class ChapterDocument(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    chapter = models.ForeignKey(to = Chapter, on_delete=models.CASCADE, related_name="documents")
    pdf_link = models.URLField()
    rank = models.IntegerField(default = None, null = True, blank = True)
    is_locked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "{} - {} - {} - {}".format(str(self.rank), self.name, self.chapter.name, self.pdf_link)

class Language(models.Model):
    name = models.CharField(max_length=15)
    # boards = models.ManyToManyField(to=Board)
    board = models.ForeignKey(to = Board, on_delete=models.CASCADE, related_name="languages")

    def __str__(self) -> str:
        return "{} - {}".format(self.name, self.board.name)
