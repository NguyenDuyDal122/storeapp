
from rest_framework.decorators import action
from rest_framework.response import Response
from stores.models import *
from rest_framework import viewsets, generics, status, parsers, permissions
from stores import serializers, paginators


class NguoiDungViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = NguoiDung.objects.filter(is_active=True).all()
    serializer_class = serializers.NguoiDungSerializer
    parser_classes = [parsers.MultiPartParser]

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action.__eq__('current_user'):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], url_name='current-user', detail=False)
    def current_user(self, request):
        return Response(serializers.NguoiDungSerializer(request.user).data)

class CuaHangViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = CuaHang.objects.filter(active=True).all()
    serializer_class = serializers.CuaHangSerializer

class SanPhamViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = SanPham.objects.filter(active=True).all()
    serializer_class = serializers.SanPhamSerializer
    pagination_class = paginators.SanPhamPaginator

class DonHangViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = DonHang.objects.all()
    serializer_class = serializers.DonHangSerializer

class GioHangViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = GioHang.objects.all()
    serializer_class = serializers.GioHangSerializer

class SanPhamGioHangViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = SanPhamGioHang.objects.all()
    serializer_class = serializers.SanPhamGioHangSerializer

class DanhGiaSanPhamViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = DanhGiaSanPham.objects.all()
    serializer_class = serializers.DanhGiaSanPhamSerializer

class DanhGiaNguoiBanViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = DanhGiaNguoiBan.objects.all()
    serializer_class = serializers.DanhGiaNguoiBanSerializer

class SanPhamDonHangViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = SanPhamDonHang.objects.all()
    serializer_class = serializers.SanPhamDonHangSerializer

class DanhMucViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = DanhMuc.objects.all()
    serializer_class = serializers.DanhMucSerializer

    @action(methods=['get'], detail=True)
    def sanpham(self, request, pk):
        sanpham = self.get_object().san_pham.all()

        return Response(serializers.SanPhamSerializer(sanpham, many = True, context={'request':request}).data, status=status.HTTP_200_OK)

class TinNhanViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = TinNhan.objects.all()
    serializer_class = serializers.TinNhanSerializer

class ThongKeDonHangVaSanPhamViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = ThongKeDonHangVaSanPhamCuaHang.objects.all()
    serializer_class = serializers.ThongKeDonHangVaSanPhamSerializer