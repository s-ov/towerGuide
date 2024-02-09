# Generated by Django 4.2.9 on 2024-01-29 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='level',
            field=models.CharField(choices=[('4.8', 'Level 4.8m'), ('8.0', 'Level 8.0m'), ('11.2', 'Level 11.2m'), ('15.4', 'Level 15.4m'), ('21.0', 'Level 21.0m'), ('25.0', 'Level 25.0m')], default=4.8, max_length=25),
            preserve_default=False,
        ),
    ]