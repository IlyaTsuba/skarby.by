# Generated by Django 4.2.7 on 2023-11-16 14:37

import accounts.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70, verbose_name='Імя/Назва')),
                ('description', models.TextField()),
                ('instagram', models.CharField(blank=True, max_length=50, null=True)),
                ('telegram', models.CharField(blank=True, max_length=50, null=True)),
                ('avatar', models.ImageField(upload_to=accounts.models.account_avatar_upload_to, verbose_name='Аватар')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Photos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to=accounts.models.account_photos_upload_to, verbose_name='Фота')),
                ('accounts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.account', verbose_name='Аккаўнт')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.category'),
        ),
    ]