# Generated by Django 4.2.6 on 2023-11-02 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='encuesta',
            name='browser',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='encuesta',
            name='operative_sistem',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
