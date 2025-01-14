from django.db.models import Sum, Count, F
from django.db.models.functions import TruncMonth, TruncQuarter, TruncYear
from .models import ThongKeDonHangVaSanPhamCuaHang

def get_store_statistics(filter_conditions, filter_type):
    thong_ke_thang = thong_ke_quy = thong_ke_nam = thong_ke_san_pham = []

    if filter_type == 'month':
        thong_ke_thang = ThongKeDonHangVaSanPhamCuaHang.objects.filter(**filter_conditions).annotate(
            thang=TruncMonth('ngay_dat_hang')
        ).values('cua_hang', 'thang').annotate(
            tong_so_don_hang=Count('don_hang'),
            tong_doanh_thu=Sum(F('gia') * F('so_luong'))
        ).order_by('thang')

    elif filter_type == 'quarter':
        thong_ke_quy = ThongKeDonHangVaSanPhamCuaHang.objects.filter(**filter_conditions).annotate(
            quy=TruncQuarter('ngay_dat_hang')
        ).values('cua_hang', 'quy').annotate(
            tong_so_don_hang=Count('don_hang'),
            tong_doanh_thu=Sum(F('gia') * F('so_luong'))
        ).order_by('quy')

    elif filter_type == 'year':
        thong_ke_nam = ThongKeDonHangVaSanPhamCuaHang.objects.filter(**filter_conditions).annotate(
            nam=TruncYear('ngay_dat_hang')
        ).values('cua_hang', 'nam').annotate(
            tong_so_don_hang=Count('don_hang'),
            tong_doanh_thu=Sum(F('gia') * F('so_luong'))
        ).order_by('nam')

    # Thay đổi ở đây, sử dụng Sum('so_luong') để tính tổng số lượng sản phẩm bán ra
    thong_ke_san_pham = ThongKeDonHangVaSanPhamCuaHang.objects.filter(**filter_conditions).values('san_pham').annotate(
        tong_so_san_pham=Sum('so_luong')  # Sử dụng Sum để tính tổng số lượng sản phẩm bán ra
    )

    return thong_ke_thang, thong_ke_quy, thong_ke_nam, thong_ke_san_pham

