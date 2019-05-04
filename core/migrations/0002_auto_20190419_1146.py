# Generated by Django 2.2 on 2019-04-19 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='userprofil',
            options={'verbose_name_plural': 'User Profiles'},
        ),
        migrations.AlterModelOptions(
            name='writerprofil',
            options={'verbose_name_plural': 'Writer Profiles'},
        ),
        migrations.RemoveField(
            model_name='post',
            name='posted',
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Category'),
        ),
    ]