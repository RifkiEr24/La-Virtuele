# Generated by Django 3.1.7 on 2021-05-04 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_auto_20210410_0812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.CharField(editable=False, max_length=255, null=True, unique=True),
        ),
    ]