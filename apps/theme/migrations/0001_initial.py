# Generated by Django 3.0 on 2019-12-21 23:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Theme',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(max_length=600)),
                ('meta', models.TextField(null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                (
                    'updated',
                    models.DateTimeField(
                        default=django.utils.timezone.now
                    )
                ),
            ],
        ),
    ]
