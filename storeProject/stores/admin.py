from django.contrib import admin
from .models import *
from django.utils.html import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.urls import path
from stores.dao import *
from django.shortcuts import render


class StoreAppAdminSite(admin.AdminSite):
    site_header = 'QUẢN TRỊ HỆ THỐNG SÀN THƯƠNG MẠI ĐIỆN TỬ'

    def get_urls(self):
        return [
            path('store-stats/', self.stats_view),
        ] + super().get_urls()

    def stats_view(self, request):
        cua_hang_list = CuaHang.objects.all()
        selected_store = request.GET.get('store')
        selected_month = request.GET.get('month')
        selected_quarter = request.GET.get('quarter')
        selected_year = request.GET.get('year')
        filter_type = request.GET.get('filter')

        # Kiểm tra nếu chưa chọn cửa hàng và gửi thông báo lỗi
        if not selected_store:
            error_message = "Vui lòng chọn cửa hàng xem thống kê."
            thong_ke_thang = thong_ke_quy = thong_ke_nam = []  # Không lấy dữ liệu thống kê nếu chưa chọn cửa hàng
            thong_ke_san_pham = []
        else:
            error_message = None

            # Lọc theo cửa hàng nếu có
            filter_conditions = {}
            if selected_store:
                filter_conditions['cua_hang__id'] = selected_store

            if selected_month:
                filter_conditions['ngay_dat_hang__month'] = int(selected_month.split('-')[1])
                filter_conditions['ngay_dat_hang__year'] = int(selected_month.split('-')[0])

            if selected_quarter:
                if selected_quarter == "1":
                    filter_conditions['ngay_dat_hang__month__in'] = [1, 2, 3]
                elif selected_quarter == "2":
                    filter_conditions['ngay_dat_hang__month__in'] = [4, 5, 6]
                elif selected_quarter == "3":
                    filter_conditions['ngay_dat_hang__month__in'] = [7, 8, 9]
                elif selected_quarter == "4":
                    filter_conditions['ngay_dat_hang__month__in'] = [10, 11, 12]

            if selected_year:
                filter_conditions['ngay_dat_hang__year'] = selected_year

            # Gọi hàm từ dao.py để lấy dữ liệu thống kê
            thong_ke_thang, thong_ke_quy, thong_ke_nam, thong_ke_san_pham = get_store_statistics(filter_conditions, filter_type)

        context = {
            'thong_ke_thang': thong_ke_thang,
            'thong_ke_quy': thong_ke_quy,
            'thong_ke_nam': thong_ke_nam,
            'thong_ke_san_pham': thong_ke_san_pham,
            'cua_hang_list': cua_hang_list,
            'selected_store': selected_store,
            'selected_month': selected_month,
            'selected_quarter': selected_quarter,
            'selected_year': selected_year,
            'error_message': error_message,
        }

        return render(request, 'admin/stats.html', context)


admin_site = StoreAppAdminSite(name='myapp')


class NguoiDungAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'vai_tro', 'da_xac_minh')  # Hiển thị các trường quan trọng
    list_filter = ('vai_tro', 'da_xac_minh')  # Lọc theo vai trò và trạng thái xác minh
    search_fields = ('username', 'email')  # Tìm kiếm theo tên người dùng hoặc email


class CuaHangAdmin(admin.ModelAdmin):
    list_display = ('ten', 'chu_so_huu', 'ngay_tao')
    search_fields = ('ten', 'chu_so_huu__username')  # Tìm kiếm theo tên cửa hàng hoặc chủ sở hữu
    date_hierarchy = 'ngay_tao'  # Lọc theo ngày tạo


class DanhMucAdmin(admin.ModelAdmin):
    list_display = ('ten',)
    search_fields = ('ten',)


class SanPhamAdmin(admin.ModelAdmin):
    list_display = ('ten', 'cua_hang', 'gia', 'so_luong_ton', 'ngay_tao')
    list_filter = ('cua_hang', 'danh_muc')  # Lọc theo cửa hàng và danh mục
    search_fields = ('ten', 'cua_hang__ten')  # Tìm kiếm theo tên sản phẩm hoặc cửa hàng
    readonly_fields = ['img']

    def img(self, pro):
        if pro:
            return mark_safe(
                '<img src="/static/{url}" width="120" />' \
                    .format(url=pro.anh_san_pham.name)
            )


class DanhGiaSanPhamAdmin(admin.ModelAdmin):
    list_display = ('san_pham', 'nguoi_dung', 'diem', 'ngay_tao')
    list_filter = ('diem',)
    search_fields = ('san_pham__ten', 'nguoi_dung__username')


class DanhGiaNguoiBanAdmin(admin.ModelAdmin):
    list_display = ('nguoi_ban', 'nguoi_dung', 'diem', 'ngay_tao')
    list_filter = ('diem',)
    search_fields = ('nguoi_ban__ten', 'nguoi_dung__username')


class DonHangAdmin(admin.ModelAdmin):
    list_display = ('id', 'nguoi_dung', 'phuong_thuc_thanh_toan', 'tong_tien', 'da_thanh_toan', 'ngay_tao')
    list_filter = ('phuong_thuc_thanh_toan', 'da_thanh_toan')
    search_fields = ('nguoi_dung__username',)
    date_hierarchy = 'ngay_tao'


class SanPhamDonHangAdmin(admin.ModelAdmin):
    list_display = ('don_hang', 'san_pham', 'so_luong', 'gia')


class TinNhanForm(forms.ModelForm):
    noi_dung = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = TinNhan
        fields = '__all__'


class TinNhanAdmin(admin.ModelAdmin):
    list_display = ('nguoi_gui', 'nguoi_nhan', 'noi_dung', 'thoi_gian')
    search_fields = ('nguoi_gui__username', 'nguoi_nhan__username')
    form = TinNhanForm


admin_site.register(NguoiDung, NguoiDungAdmin)
admin_site.register(CuaHang, CuaHangAdmin)
admin_site.register(DanhMuc, DanhMucAdmin)
admin_site.register(SanPham, SanPhamAdmin)
admin_site.register(GioHang)
admin_site.register(SanPhamGioHang)
admin_site.register(DanhGiaSanPham, DanhGiaSanPhamAdmin)
admin_site.register(DanhGiaNguoiBan, DanhGiaNguoiBanAdmin)
admin_site.register(DonHang, DonHangAdmin)
admin_site.register(SanPhamDonHang, SanPhamDonHangAdmin)
admin_site.register(TinNhan, TinNhanAdmin)
admin_site.register(ThongKeDonHangVaSanPhamCuaHang)
