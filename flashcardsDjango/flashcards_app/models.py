from django.db import models


class Collection(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Flashcard(models.Model):
    question = models.TextField(max_length=300)
    answer = models.TextField(max_length=300)
    collectionId = models.ForeignKey(Collection, on_delete=models.CASCADE)

    def __str__(self):
        return self.question
