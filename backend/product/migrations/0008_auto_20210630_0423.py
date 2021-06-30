# Generated by Django 3.1.7 on 2021-06-30 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_review_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, related_name='product', to='product.Category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_featured',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]