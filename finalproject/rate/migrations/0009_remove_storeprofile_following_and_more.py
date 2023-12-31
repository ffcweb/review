# Generated by Django 4.2.7 on 2023-12-21 05:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0008_store_followers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storeprofile',
            name='following',
        ),
        migrations.RemoveField(
            model_name='storeprofile',
            name='store',
        ),
        migrations.RemoveField(
            model_name='storefollowers',
            name='count',
        ),
        migrations.AlterField(
            model_name='store',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='following_stores', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='storefollowers',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rate.store'),
        ),
        migrations.DeleteModel(
            name='Follow',
        ),
        migrations.DeleteModel(
            name='StoreProfile',
        ),
    ]
