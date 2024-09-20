# Generated by Django 5.1.1 on 2024-09-04 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('marche', models.FloatField(default=0)),
                ('jogging', models.FloatField(default=0)),
                ('velo', models.FloatField(default=0)),
                ('total', models.FloatField(default=0)),
                ('calories', models.FloatField(default=0)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('duration', models.DurationField()),
            ],
        ),
    ]
