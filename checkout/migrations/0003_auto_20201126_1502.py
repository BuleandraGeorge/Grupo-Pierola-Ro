# Generated by Django 3.1.3 on 2020-11-26 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_auto_20201125_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='original_bag',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='order',
            name='stripe_id',
            field=models.CharField(default='', max_length=254),
        ),
    ]
