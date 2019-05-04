# Generated by Django 2.2 on 2019-04-21 18:27

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20190421_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('image', '730x390', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropping'),
        ),
    ]
