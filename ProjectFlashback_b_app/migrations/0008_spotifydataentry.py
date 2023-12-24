# Generated by Django 5.0 on 2023-12-20 00:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectFlashback_b_app', '0007_rename_about_wikipediadataentry_summary'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpotifyDataEntry',
            fields=[
                ('entryId', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('date', models.IntegerField(blank=True, null=True)),
                ('year', models.IntegerField()),
                ('url', models.URLField()),
                ('title', models.CharField(max_length=250)),
                ('entryType', models.CharField(choices=[('RE', 'Reddit'), ('NW', 'News'), ('ME', 'Meme'), ('WK', 'Wikipedia'), ('MV', 'Movie'), ('TV', 'TV Show'), ('SO', 'Song'), ('GA', 'Game')], max_length=2)),
                ('scoreValue', models.DecimalField(decimal_places=2, max_digits=6)),
                ('dataset', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ProjectFlashback_b_app.dataset')),
            ],
            options={
                'db_table': 'SpotifyDataEntry',
            },
        ),
    ]
