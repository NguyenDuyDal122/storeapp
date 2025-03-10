# Generated by Django 5.1.4 on 2025-01-10 10:42

import ckeditor.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0003_alter_tinnhan_noi_dung'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='thongkedoanhthu',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='thongkedoanhthu',
            name='danh_muc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='thong_ke_doanh_thu', to='stores.danhmuc'),
        ),
        migrations.AddField(
            model_name='thongkedoanhthu',
            name='san_pham',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='thong_ke_doanh_thu', to='stores.sanpham'),
        ),
        migrations.AlterField(
            model_name='cuahang',
            name='mo_ta',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='danhmuc',
            name='mo_ta',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sanpham',
            name='mo_ta',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='thongkedoanhthu',
            unique_together={('nguoi_ban', 'thang', 'nam', 'san_pham', 'danh_muc')},
        ),
        migrations.CreateModel(
            name='GioHang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ngay_tao', models.DateTimeField(auto_now_add=True)),
                ('tong_tien', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('nguoi_dung', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gio_hang', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SanPhamGioHang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('so_luong', models.PositiveIntegerField()),
                ('gia', models.DecimalField(decimal_places=2, max_digits=10)),
                ('gio_hang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='san_pham', to='stores.giohang')),
                ('san_pham', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.sanpham')),
            ],
            options={
                'unique_together': {('gio_hang', 'san_pham')},
            },
        ),
    ]
