# Generated by Django 5.0.6 on 2024-06-20 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_project_url_to_jatos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('photo', models.ImageField(upload_to='cards-img/')),
                ('url_to_jatos', models.URLField(default='')),
                ('is_active', models.BooleanField(default=False)),
                ('recommended', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='recommended',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='cards-img/'),
        ),
    ]
