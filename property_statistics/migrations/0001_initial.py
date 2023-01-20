# Generated by Django 4.1.5 on 2023-01-20 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('dept_code', models.IntegerField()),
                ('city', models.CharField(max_length=100)),
                ('zip_code', models.IntegerField()),
            ],
        ),
    ]
