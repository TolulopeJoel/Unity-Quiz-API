from django.db import transaction
from rest_framework import serializers

from .models import ExplanationStep, Option
from .models import Question as QuestionModel
from .models import Tag


class OptionSerializer(serializers.ListSerializer):
    child = serializers.CharField()


class TagSerializer(serializers.ListSerializer):
    child = serializers.CharField()


class StepSerializer(serializers.ModelSerializer):
    """
    Serializer for explanation steps in a question.
    Maps internal model field names to external API representation.
    """
    Title = serializers.CharField(source='title', trim_whitespace=False)
    Result = serializers.CharField(source='result', trim_whitespace=False)
    ImageUrl = serializers.URLField(
        source='image_url',
        required=False
    )

    class Meta:
        model = ExplanationStep
        fields = ['Title', 'Result', 'ImageUrl']


class QuestionSerializer(serializers.ModelSerializer):
    # Field mappings from external API names to internal model fields
    Question = serializers.CharField(trim_whitespace=False, source='text')
    Solution = serializers.CharField(trim_whitespace=False, source='solution')
    CorrectAnswer = serializers.CharField(write_only=True)  # Only used during creation

    # Nested serializers for related models
    Options = OptionSerializer(min_length=2, source='options')
    Steps = StepSerializer(many=True, allow_empty=False, source='steps')
    Tags = TagSerializer(required=False, source='tags')

    Difficulty = serializers.ChoiceField(
        required=False, choices=QuestionModel.DIFFICULTY_CHOICES, source='difficulty'
    )
    ImageUrl = serializers.URLField(required=False, source='image_url')

    class Meta:
        model = QuestionModel
        fields = [
            'id', 'Question', 'Solution', 'CorrectAnswer',
            'Steps', 'Options', 'ImageUrl', 'Difficulty', 'Tags',
        ]

    def validate_Question(self, obj):
        # Ensure questions are unique by checking if the text already exists.
        if QuestionModel.objects.filter(text=obj).exists():
            raise serializers.ValidationError("Question already exists")
        return obj

    def validate_CorrectAnswer(self, obj):
        # Validate that the correct answer is one of the provided options.
        if obj not in self.initial_data.get('Options', []):
            raise serializers.ValidationError("Answer must be in the options")
        return obj

    def create(self, validated_data):
        steps = validated_data.pop('steps', [])
        tags = validated_data.pop('tags', [])
        options = validated_data.pop('options', [])
        correct_answer = validated_data.pop('CorrectAnswer')

        with transaction.atomic():
            # Create main question object
            question = QuestionModel.objects.create(**validated_data)

            # Bulk create related steps
            ExplanationStep.objects.bulk_create([
                ExplanationStep(
                    question=question,
                    **step
                ) for step in steps
            ])

            # Bulk create options, marking the correct one
            Option.objects.bulk_create([
                Option(
                    question=question,
                    text=option,
                    is_correct=(option == correct_answer)
                ) for option in options
            ])

            # Create or get tags and associate with question
            for tag in tags:
                tag_obj, _ = Tag.objects.get_or_create(name=tag.lower())
                question.tags.add(tag_obj)

            return question
    
    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data['CorrectAnswer'] = instance.options.all().get(is_correct=True).text
        return data
