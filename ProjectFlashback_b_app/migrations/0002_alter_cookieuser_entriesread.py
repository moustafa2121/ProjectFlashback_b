# Generated by Django 5.0 on 2023-12-15 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectFlashback_b_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cookieuser',
            name='entriesRead',
            field=models.ManyToManyField(to='ProjectFlashback_b_app.userentryread'),
        ),
    ]
