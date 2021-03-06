# Generated by Django 3.0.7 on 2020-06-21 01:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200621_0033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='store',
        ),
        migrations.AddField(
            model_name='store',
            name='products',
            field=models.ManyToManyField(blank=django.db.models.deletion.PROTECT, related_name='store', to='core.Product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Name'),
        ),
    ]
