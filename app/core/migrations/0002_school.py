# Generated by Django 3.2.23 on 2023-12-03 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('subdomain', models.CharField(max_length=64, unique=True)),
                ('motto', models.CharField(blank=True, default='', max_length=255)),
                ('logo', models.CharField(blank=True, default='', max_length=64)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=64)),
                ('region', models.CharField(max_length=64)),
                ('phone', models.CharField(max_length=32)),
                ('email', models.CharField(blank=True, max_length=64, null=True, unique=True)),
            ],
        ),
    ]