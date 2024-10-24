# Generated by Django 5.1.2 on 2024-10-23 00:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChefResponsibility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'label',
                    models.CharField(
                        choices=[
                            ('executive_chef', 'Executive Chef'),
                            ('chef', 'Chef'),
                            ('sous_chef', 'Sous Chef'),
                            ('baker', 'Baker'),
                            ('pastry_chef', 'Pastry Chef'),
                            ('other', 'Other'),
                        ],
                        max_length=15,
                        unique=True,
                        verbose_name='Label of the Chef Type',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Chef Responsibility',
                'verbose_name_plural': 'Chef Responsibilities',
            },
        ),
        migrations.CreateModel(
            name='Chef',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                (
                    'bio',
                    models.TextField(
                        blank=True, help_text='A brief description of the chef.', null=True, verbose_name='Biography'
                    ),
                ),
                (
                    'user',
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
                (
                    'responsibilities',
                    models.ManyToManyField(
                        blank=True,
                        help_text='The responsibilities of the chef.',
                        to='user.chefresponsibility',
                        verbose_name='Responsibilities',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Chef',
                'verbose_name_plural': 'Chefs',
            },
        ),
    ]
