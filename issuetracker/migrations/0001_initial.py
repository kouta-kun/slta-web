# Generated by Django 2.2.5 on 2019-11-09 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('name', models.TextField(primary_key=True, serialize=False)),
                ('pin', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('description', models.TextField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('P', 'Progreso'), ('R', 'Reparado')], default='R', max_length=1)),
                ('report_time', models.DateField(auto_now_add=True)),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='issuetracker.User')),
            ],
        ),
    ]
