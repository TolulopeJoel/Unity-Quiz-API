from django.core.validators import MinValueValidator
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Question(TimeStampedModel):
    text = models.TextField(unique=True)
    solution = models.TextField()
    tags = models.ManyToManyField("Tag", related_name="questions")
    image_url = models.URLField(null=True, blank=True)


class ExplanationStep(TimeStampedModel):
    question = models.ForeignKey(
        "Question", on_delete=models.CASCADE, related_name="steps"
    )
    step_number = models.IntegerField(validators=[MinValueValidator(1)])

    title = models.CharField(max_length=255)
    result = models.TextField()
    image_url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ("step_number",)
        unique_together = ("question", "title", "result")


class Option(TimeStampedModel):
    question = models.ForeignKey(
        "Question", on_delete=models.CASCADE, related_name="options"
    )
    text = models.TextField()
    is_correct = models.BooleanField(default=False)


class Tag(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
