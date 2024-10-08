# Generated by Django 5.0.6 on 2024-09-02 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0011_remove_project_description_ca_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('photo', models.ImageField(upload_to='cards-img/')),
                ('url_to_jatos', models.URLField(default='')),
                ('is_active', models.BooleanField(default=False)),
                ('is_recommended', models.BooleanField(default=False)),
            ],
        ),
    ]
