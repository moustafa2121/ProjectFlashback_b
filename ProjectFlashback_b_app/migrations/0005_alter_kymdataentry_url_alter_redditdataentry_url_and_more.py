# Generated by Django 5.0 on 2023-12-19 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectFlashback_b_app', '0004_wikipediadataentry_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kymdataentry',
            name='url',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='redditdataentry',
            name='url',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='twitterdataentry',
            name='url',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='wikipediadataentry',
            name='url',
            field=models.URLField(),
        ),
    ]
