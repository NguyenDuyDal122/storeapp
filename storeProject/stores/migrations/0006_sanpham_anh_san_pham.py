# Generated by Django 5.1.4 on 2025-01-10 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0005_thongkebanhangcuahang_thongkedoanhthusanphamcuahang_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sanpham',
            name='anh_san_pham',
            field=models.ImageField(blank=True, null=True, upload_to='products/%Y/%m'),
        ),
    ]
