# Generated by Django 5.1.4 on 2024-12-29 05:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("questions", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="explanationstep",
            options={},
        ),
        migrations.AlterModelOptions(
            name="option",
            options={"ordering": ("-updated_at",)},
        ),
        migrations.AlterModelOptions(
            name="question",
            options={"ordering": ("-updated_at",)},
        ),
        migrations.AlterModelOptions(
            name="tag",
            options={"ordering": ("-updated_at",)},
        ),
        migrations.RemoveField(
            model_name="explanationstep",
            name="step_number",
        ),
    ]