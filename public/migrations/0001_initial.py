# Generated by Django 2.2.5 on 2019-09-15 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('titulo', models.TextField(max_length=50, primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField()),
                ('markup', models.TextField()),
            ],
        ),
    ]
