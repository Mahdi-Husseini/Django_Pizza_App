# Generated by Django 4.1 on 2022-09-28 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzaapp', '0003_customermodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=10)),
                ('ordereditems', models.CharField(max_length=10)),
            ],
        ),
    ]