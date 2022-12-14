# Generated by Django 3.2 on 2022-10-25 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatalogImg',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='products_catalogimg', serialize=False, to='cms.cmsplugin')),
                ('image', models.ImageField(upload_to='catalog/')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
