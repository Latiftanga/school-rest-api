# Generated by Django 3.2.23 on 2023-12-30 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0005_auto_20231229_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='email',
            field=models.EmailField(blank=True, max_length=128, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='has_account',
            field=models.BooleanField(default=False),
        ),
    ]
