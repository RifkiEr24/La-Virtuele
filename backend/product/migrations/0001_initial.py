# Generated by Django 3.1.7 on 2021-03-20 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=255, verbose_name='Product Name')),
                ('slug', models.CharField(editable=False, max_length=255, null=True)),
                ('price', models.FloatField()),
                ('size', models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')], max_length=1)),
                ('category', models.ManyToManyField(to='product.Category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveSmallIntegerField(verbose_name='Quantity')),
                ('total', models.PositiveIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=255)),
                ('checked_out', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('total', models.PositiveIntegerField()),
                ('items', models.ManyToManyField(to='product.ProductCart')),
            ],
        ),
    ]