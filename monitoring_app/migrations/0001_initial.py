# Generated by Django 3.2 on 2024-07-30 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instance_id', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField()),
                ('average', models.FloatField()),
            ],
        ),
    ]
