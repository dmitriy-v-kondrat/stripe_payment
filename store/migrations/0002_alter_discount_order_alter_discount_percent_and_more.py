# Generated by Django 4.2.8 on 2023-12-07 06:54

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.order'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='percent',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(99)], verbose_name='Discount %'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Price without discount'),
        ),
        migrations.AlterField(
            model_name='tax',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.order'),
        ),
    ]
