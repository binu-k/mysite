# Generated by Django 4.1.1 on 2022-10-20 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_product_description_alter_product_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='images', upload_to=''),
        ),
    ]