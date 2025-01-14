# Generated by Django 5.1.4 on 2025-01-14 10:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0008_product_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='types',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='product', to='market.type'),
        ),
    ]
