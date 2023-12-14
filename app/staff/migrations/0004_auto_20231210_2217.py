# Generated by Django 3.2.23 on 2023-12-10 22:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_auto_20231209_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='staff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='promotions', to='staff.staff'),
        ),
        migrations.AlterField(
            model_name='qualification',
            name='staff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='qualifications', to='staff.staff'),
        ),
    ]
