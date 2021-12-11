from django.db import models

from django.db.models.signals import pre_save, post_save

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
    # chapter_link = models.URLField()
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, related_name="chapters")
    is_locked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "{} - {}".format(self.name, self.subject.name)

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


def document_pre_save(sender, instance, *args, **kwargs):
    chapter = instance.chapter
    no_of_docs = chapter.documents.count()
    if instance.rank is None:
        instance.rank = no_of_docs + 1

    else:
        if instance.rank <= no_of_docs:
            doc_list = chapter.documents.all()
            doc_list = [doc for doc in doc_list if doc.rank >= instance.rank]
            print(doc_list, instance.rank)
            for doc in doc_list:
                doc.rank += 1
                doc.save()
        else:
            instance.rank = no_of_docs + 1
            
pre_save.connect(document_pre_save, sender = ChapterDocument)
