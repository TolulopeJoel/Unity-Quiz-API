from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework import serializers

from .models import ExplanationStep, Option, Question


class StepSerializer(serializers.ModelSerializer):
    Title = serializers.CharField(source='title')
    Result = serializers.CharField(source='result')
    ImageUrl = serializers.URLField(
        source='image_url',
        required=False
    )

    class Meta:
        model = ExplanationStep
        fields = ['Title', 'Result', 'ImageUrl']


class OptionSerializer(serializers.ModelSerializer):
    Text = serializers.CharField(source='text')
    IsCorrect = serializers.BooleanField(
        source='is_correct',
        write_only=True,
        default=False
    )

    class Meta:
        model = Option
        fields = ['Text', 'IsCorrect']


class QuestionSerializer(serializers.ModelSerializer):
    Question = serializers.CharField(source='text')
    Solution = serializers.CharField(source='solution')
    CorrectAnswer = serializers.SerializerMethodField(read_only=True)
    Steps = StepSerializer(
        many=True,
        source='steps',
        allow_empty=False
    )
    Options = OptionSerializer(
        many=True,
        min_length=2,
        source='options',
        allow_empty=False
    )
    ImageUrl = serializers.URLField(
        required=False,
        source='image_url',
    )

    class Meta:
        model = Question
        fields = [
            'id',
            'Question',
            'Solution',
            'CorrectAnswer',
            'Steps',
            'Options',
            'ImageUrl',
        ]

    def get_CorrectAnswer(self, obj):
        options = obj.options.all()
        # might need to adjust to accept multiple answers
        return options.get(is_correct=True).text

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['Options'] = list(instance.options.values_list('text', flat=True))
        return data

    def create(self, validated_data):
        steps = validated_data.pop('steps', [])
        options = validated_data.pop('options', [])

        with transaction.atomic():
            # Create question
            try:
                question = Question.objects.create(**validated_data)
            except IntegrityError:
                raise serializers.ValidationError('Question already exists')

            # Bulk create steps and options
            ExplanationStep.objects.bulk_create([
                ExplanationStep(
                    question=question,
                    **step
                ) for step in steps
            ])

            Option.objects.bulk_create([
                Option(
                    question=question,
                    **option
                ) for option in options
            ])

            return question
