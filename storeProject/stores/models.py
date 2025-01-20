from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField

# Vai tro nguoi dung
class NguoiDung(AbstractUser):
    VAI_TRO = [
        ('user', 'Nguoi dung thuong'),
        ('seller', 'Nguoi ban'),
        ('admin', 'Quan tri vien'),
        ('staff', 'Nhan vien he thong'),
    ]
    GIOI_TINH = [
        ('male', 'Nam'),
        ('female', 'Nu'),
        ('other', 'Khac'),
    ]

    vai_tro = models.CharField(max_length=20, choices=VAI_TRO, default='user')  # Vai tro
    avatar = models.ImageField(upload_to='avatar/%Y/%m', blank=True, null=True)
    gioi_tinh = models.CharField(max_length=10, choices=GIOI_TINH, blank=True, null=True)  # Gioi tinh
    da_xac_minh = models.BooleanField(default=False)  # Trang thai xac minh (cho nguoi ban)

    def __str__(self):
        return f"{self.username} ({self.get_vai_tro_display()})"


# Cua hang
class CuaHang(models.Model):
    chu_so_huu = models.OneToOneField(NguoiDung, on_delete=models.CASCADE, related_name='cua_hang')  # Chu so huu
    ten = models.CharField(max_length=100)  # Ten cua hang
    mo_ta = RichTextField(blank=True, null=True)  # Mo ta cua hang
    ngay_tao = models.DateTimeField(auto_now_add=True)  # Thoi gian tao
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.ten

    class Meta:
        unique_together = ('chu_so_huu',)


# Danh muc san pham
class DanhMuc(models.Model):
    ten = models.CharField(max_length=100)  # Ten danh muc
    mo_ta = RichTextField(blank=True, null=True)  # Mo ta danh muc

    def __str__(self):
        return self.ten


# San pham
class SanPham(models.Model):
    cua_hang = models.ForeignKey(CuaHang, on_delete=models.CASCADE, related_name='san_pham')  # Cửa hàng
    danh_muc = models.ForeignKey(DanhMuc, on_delete=models.SET_NULL, null=True, related_name='san_pham')  # Danh mục
    ten = models.CharField(max_length=100)  # Tên sản phẩm
    mo_ta = RichTextField(blank=True, null=True)  # Mô tả sản phẩm
    gia = models.DecimalField(max_digits=10, decimal_places=2)  # Giá sản phẩm
    so_luong_ton = models.PositiveIntegerField(default=0)  # Số lượng tồn
    ngay_tao = models.DateTimeField(auto_now_add=True)  # Ngày tạo
    ngay_cap_nhat = models.DateTimeField(auto_now=True)  # Ngày cập nhật
    anh_san_pham = models.ImageField(upload_to='products/%Y/%m', blank=True, null=True)  # Ảnh sản phẩm
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.ten

    class Meta:
        unique_together = ('ten', 'cua_hang')


# Giỏ hàng
class GioHang(models.Model):
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE, related_name='gio_hang')  # Người dùng
    ngay_tao = models.DateTimeField(auto_now_add=True)  # Ngày tạo
    tong_tien = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Tổng tiền

    def tinh_tong_tien(self):
        total = sum([sp.gia * sp.so_luong for sp in self.san_pham.all()])
        self.tong_tien = total
        self.save()

    def __str__(self):
        return f"Gio hang của {self.nguoi_dung.username}"

# Sản phẩm trong giỏ hàng
class SanPhamGioHang(models.Model):
    gio_hang = models.ForeignKey(GioHang, on_delete=models.CASCADE, related_name='san_pham')  # Giỏ hàng
    san_pham = models.ForeignKey(SanPham, on_delete=models.CASCADE)  # Sản phẩm
    so_luong = models.PositiveIntegerField()  # Số lượng
    gia = models.DecimalField(max_digits=10, decimal_places=2)  # Giá

    def __str__(self):
        return f"{self.so_luong} x {self.san_pham.ten} trong giỏ hàng của {self.gio_hang.nguoi_dung.username}"

    class Meta:
        unique_together = ('gio_hang', 'san_pham')


# Don hang
class DonHang(models.Model):
    PHUONG_THUC_THANH_TOAN = [
        ('cod', 'Thanh toan khi nhan hang'),
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
        ('zalo', 'Zalo Pay'),
        ('momo', 'MoMo'),
    ]
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE, related_name='don_hang')  # Nguoi dung
    ngay_tao = models.DateTimeField(auto_now_add=True)  # Ngay tao
    phuong_thuc_thanh_toan = models.CharField(max_length=20, choices=PHUONG_THUC_THANH_TOAN)  # Phuong thuc thanh toan
    tong_tien = models.DecimalField(max_digits=10, decimal_places=2)  # Tong tien
    da_thanh_toan = models.BooleanField(default=False)  # Trang thai thanh toan

    def __str__(self):
        return f"Don hang #{self.id} boi {self.nguoi_dung.username}"


# San pham trong don hang
class SanPhamDonHang(models.Model):
    don_hang = models.ForeignKey(DonHang, on_delete=models.CASCADE, related_name='san_pham')  # Don hang
    san_pham = models.ForeignKey(SanPham, on_delete=models.SET_NULL, null=True)  # San pham
    so_luong = models.PositiveIntegerField()  # So luong
    gia = models.DecimalField(max_digits=10, decimal_places=2)  # Gia

    def __str__(self):
        return f"{self.so_luong} x {self.san_pham.ten} (Don hang #{self.don_hang.id})"

    class Meta:
        unique_together = ('don_hang', 'san_pham')


# Danh gia san pham
class DanhGiaSanPham(models.Model):
    san_pham = models.ForeignKey(SanPham, on_delete=models.CASCADE, related_name='danh_gia')  # San pham
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE, related_name='danh_gia_san_pham')  # Nguoi dung
    diem = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  # Diem danh gia
    binh_luan = models.TextField(blank=True, null=True)  # Binh luan
    ngay_tao = models.DateTimeField(auto_now_add=True)  # Ngay tao

    def __str__(self):
        return f"Danh gia cho {self.san_pham.ten} boi {self.nguoi_dung.username}"

    class Meta:
        unique_together = ('san_pham', 'nguoi_dung')


# Danh gia nguoi ban
class DanhGiaNguoiBan(models.Model):
    nguoi_ban = models.ForeignKey(CuaHang, on_delete=models.CASCADE, related_name='danh_gia_nguoi_ban')  # Nguoi ban
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE, related_name='danh_gia_nguoi_ban')  # Nguoi dung
    diem = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  # Diem danh gia
    binh_luan = models.TextField(blank=True, null=True)  # Binh luan
    ngay_tao = models.DateTimeField(auto_now_add=True)  # Ngay tao

    def __str__(self):
        return f"Danh gia cho {self.nguoi_ban.ten} boi {self.nguoi_dung.username}"

    class Meta:
        unique_together = ('nguoi_ban', 'nguoi_dung')


# Tin nhan chat (tich hop Firebase)
class TinNhan(models.Model):
    nguoi_gui = models.ForeignKey(NguoiDung, on_delete=models.CASCADE, related_name='tin_nhan_gui')  # Nguoi gui
    nguoi_nhan = models.ForeignKey(NguoiDung, on_delete=models.CASCADE, related_name='tin_nhan_nhan')  # Nguoi nhan
    noi_dung = RichTextField()  # Noi dung tin nhan
    thoi_gian = models.DateTimeField(auto_now_add=True)  # Thoi gian gui

    def __str__(self):
        return f"Tin nhan tu {self.nguoi_gui.username} den {self.nguoi_nhan.username}"


class ThongKeDoanhThu(models.Model):
    cua_hang = models.ForeignKey(CuaHang, on_delete=models.CASCADE, related_name='thong_ke_doanh_thu')
    danh_muc = models.ForeignKey(DanhMuc, on_delete=models.CASCADE, related_name='thong_ke_doanh_thu')
    san_pham = models.ForeignKey(SanPham, on_delete=models.CASCADE, related_name='thong_ke_doanh_thu')
    so_luong = models.PositiveIntegerField(default=0)
    gia = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ngay_thanh_toan = models.DateTimeField()
    tong_doanh_thu = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"Doanh thu từ {self.san_pham.ten} - {self.cua_hang.ten} vào {self.ngay_thanh_toan.strftime('%d/%m/%Y')}"


class ThongKeDonHangVaSanPhamCuaHang(models.Model):
    don_hang = models.ForeignKey(DonHang, on_delete=models.CASCADE)  # Đơn hàng
    san_pham = models.ForeignKey(SanPham, on_delete=models.CASCADE)  # Sản phẩm
    cua_hang = models.ForeignKey(CuaHang, on_delete=models.CASCADE)  # Cửa hàng
    so_luong = models.PositiveIntegerField()  # Số lượng sản phẩm đã bán
    gia = models.DecimalField(max_digits=10, decimal_places=2)  # Giá của sản phẩm
    ngay_dat_hang = models.DateTimeField()  # Ngày đặt hàng

    def __str__(self):
        return f"Thống kê cho {self.san_pham.ten} trong đơn hàng #{self.don_hang.id}"


