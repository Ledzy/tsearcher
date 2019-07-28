# Generated by Django 2.2.3 on 2019-07-28 09:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import random


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextension',
            name='id',
            field=models.AutoField(auto_created=True, default=random.randint(5000,10000), primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userextension',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, related_name='extension', to=settings.AUTH_USER_MODEL),
        ),
    ]
