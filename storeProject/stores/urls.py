from stores import views
from django.urls import path, include
from rest_framework import routers


routers = routers.DefaultRouter()
routers.register('nguoi-dung', views.NguoiDungViewSet, basename='nguoidung')
routers.register('cua-hang', views.CuaHangViewSet, basename='cuahang')
routers.register('san-pham', views.SanPhamViewSet, basename='sanpham')
routers.register('don-hang', views.DonHangViewSet, basename='donhang')
routers.register('gio-hang', views.GioHangViewSet, basename='giohang')
routers.register('sanpham-giohang', views.SanPhamGioHangViewSet, basename='sanphamgiohang')
routers.register('danhgia-sanpham', views.DanhGiaSanPhamViewSet, basename='danhgiasanpham')
routers.register('danhgia-nguoiban', views.DanhGiaNguoiBanViewSet, basename='danhgianguoiban')
routers.register('sanpham-donhang', views.SanPhamDonHangViewSet, basename='sanphamdonhang')
routers.register('danh-muc', views.DanhMucViewSet, basename='danhmuc')
routers.register('tin-nhan', views.TinNhanViewSet, basename='tinnhan')
routers.register('thongke-donhangsanpham', views.ThongKeDonHangVaSanPhamViewSet, basename='thongkedonhangsanpham')

urlpatterns = [
    path('',include(routers.urls))
]