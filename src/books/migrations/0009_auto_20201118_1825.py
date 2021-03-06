# Generated by Django 3.1.3 on 2020-11-18 11:25

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_auto_20201117_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='liked_posts',
            field=models.ManyToManyField(related_name='users', to='books.Post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
