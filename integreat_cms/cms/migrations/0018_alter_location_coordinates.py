# Generated by Django 3.2.13 on 2022-04-30 15:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Make the coordination fields of POIs/locations optional and move validation into the POI form.
    Coordinates are still required if the location should be shown on the map.
    Also, add validation to make sure the values are in the allowed range.
    """

    dependencies = [
        ("cms", "0017_region_timezone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="poi",
            name="latitude",
            field=models.FloatField(
                blank=True,
                help_text="The latitude coordinate",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(-90.0),
                    django.core.validators.MaxValueValidator(90.0),
                ],
                verbose_name="latitude",
            ),
        ),
        migrations.AlterField(
            model_name="poi",
            name="longitude",
            field=models.FloatField(
                blank=True,
                help_text="The longitude coordinate",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(-180.0),
                    django.core.validators.MaxValueValidator(180.0),
                ],
                verbose_name="longitude",
            ),
        ),
    ]
