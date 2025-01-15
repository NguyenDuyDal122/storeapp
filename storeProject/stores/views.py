
from rest_framework.decorators import action
from rest_framework.response import Response
from stores.models import *
from rest_framework import viewsets, generics, status, parsers, permissions
from stores import serializers, paginators
from django.shortcuts import get_object_or_404


class NguoiDungViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = NguoiDung.objects.filter(is_active=True).all()
    serializer_class = serializers.NguoiDungSerializer
    parser_classes = [parsers.MultiPartParser]

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == 'create_store':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], url_name='current-user', detail=False)
    def current_user(self, request):
        return Response(serializers.NguoiDungSerializer(request.user).data)

class CuaHangViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = CuaHang.objects.filter(active=True).all()
    serializer_class = serializers.CuaHangSerializer

    @action(methods=['post'], detail=False, url_path='create-store')
    def create_store(self, request):
        user = request.user

        # Kiểm tra nếu người dùng có vai trò là người bán và đã được xác minh
        if user.vai_tro != 'seller' or not user.da_xac_minh:
            return Response({'detail': 'Bạn không có quyền tạo cửa hàng'}, status=status.HTTP_403_FORBIDDEN)

        # Kiểm tra xem người dùng đã có cửa hàng hay chưa
        if hasattr(user, 'cua_hang'):
            return Response({'detail': 'Bạn đã có cửa hàng'}, status=status.HTTP_400_BAD_REQUEST)

        # Lấy dữ liệu cửa hàng từ request
        store_data = request.data
        store_name = store_data.get('name')
        store_description = store_data.get('description')

        # Kiểm tra nếu tên và mô tả cửa hàng không có
        if not store_name or not store_description:
            return Response({'detail': 'Tên cửa hàng và mô tả là bắt buộc'}, status=status.HTTP_400_BAD_REQUEST)

        # Tạo cửa hàng mới cho người bán
        cua_hang = CuaHang.objects.create(
            chu_so_huu=user,
            ten=store_name,
            mo_ta=store_description
        )

        return Response(serializers.CuaHangSerializer(cua_hang).data, status=status.HTTP_201_CREATED)

class DanhMucViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = DanhMuc.objects.all()
    serializer_class = serializers.DanhMucSerializer

    @action(methods=['get'], detail=True)
    def sanpham(self, request, pk):
        sanpham = self.get_object().san_pham.all()

        return Response(serializers.SanPhamSerializer(sanpham, many = True, context={'request':request}).data, status=status.HTTP_200_OK)

class SanPhamViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.ListAPIView):
    queryset = SanPham.objects.filter(active=True).all()
    serializer_class = serializers.SanPhamSerializer
    pagination_class = paginators.SanPhamPaginator

    def create(self, request, *args, **kwargs):
        user = request.user

        # Kiểm tra xem người dùng có vai trò là người bán không
        if user.vai_tro != 'seller':
            return Response({'detail': 'Bạn không có quyền tạo sản phẩm'}, status=status.HTTP_403_FORBIDDEN)

        # Kiểm tra nếu người bán có cửa hàng không
        if not hasattr(user, 'cua_hang'):
            return Response({'detail': 'Bạn phải có cửa hàng để tạo sản phẩm'}, status=status.HTTP_400_BAD_REQUEST)

        # Lấy dữ liệu sản phẩm từ request
        product_data = request.data
        danh_muc_id = product_data.get('danh_muc')

        # Kiểm tra danh mục có hợp lệ không
        try:
            danh_muc = DanhMuc.objects.get(id=danh_muc_id)
        except DanhMuc.DoesNotExist:
            return Response({'detail': 'Danh mục không tồn tại'}, status=status.HTTP_400_BAD_REQUEST)

        # Tạo sản phẩm mới
        san_pham = SanPham.objects.create(
            cua_hang=user.cua_hang,
            danh_muc=danh_muc,
            ten=product_data.get('ten'),
            mo_ta=product_data.get('mo_ta'),
            gia=product_data.get('gia'),
            so_luong_ton=product_data.get('so_luong_ton', 0),
            anh_san_pham=product_data.get('anh_san_pham'),
        )

        return Response(serializers.SanPhamSerializer(san_pham).data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        user = request.user

        # Lấy sản phẩm cần sửa
        try:
            san_pham = SanPham.objects.get(id=kwargs['pk'])
        except SanPham.DoesNotExist:
            return Response({'detail': 'Sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        # Kiểm tra xem người bán có quyền sửa sản phẩm này không
        if san_pham.cua_hang.chu_so_huu != user:
            return Response({'detail': 'Bạn không có quyền sửa sản phẩm này'}, status=status.HTTP_403_FORBIDDEN)

        # Cập nhật dữ liệu sản phẩm từ request (chỉ những trường có trong request sẽ được cập nhật)
        product_data = request.data
        serializer = self.get_serializer(san_pham, data=product_data, partial=True)  # partial=True cho phép cập nhật một phần

        if serializer.is_valid():
            serializer.save()  # Chỉ lưu các trường được cung cấp trong request
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user = request.user

        # Lấy sản phẩm cần xóa
        try:
            san_pham = SanPham.objects.get(id=kwargs['pk'])
        except SanPham.DoesNotExist:
            return Response({'detail': 'Sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        # Kiểm tra xem người bán có quyền xóa sản phẩm này không
        if san_pham.cua_hang.chu_so_huu != user:
            return Response({'detail': 'Bạn không có quyền xóa sản phẩm này'}, status=status.HTTP_403_FORBIDDEN)

        # Xóa sản phẩm
        san_pham.delete()

        return Response({'detail': 'Sản phẩm đã được xóa thành công'}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset

        # Tìm kiếm theo tên sản phẩm
        ten = request.query_params.get('ten')
        if ten:
            queryset = queryset.filter(ten__icontains=ten)

        # Lọc theo khoảng giá
        gia_min = request.query_params.get('gia_min')
        gia_max = request.query_params.get('gia_max')
        if gia_min and gia_max:
            queryset = queryset.filter(gia__gte=gia_min, gia__lte=gia_max)
        elif gia_min:
            queryset = queryset.filter(gia__gte=gia_min)
        elif gia_max:
            queryset = queryset.filter(gia__lte=gia_max)

        # Tìm kiếm theo tên cửa hàng
        cua_hang_ten = request.query_params.get('cua_hang')
        if cua_hang_ten:
            queryset = queryset.filter(cua_hang__ten__icontains=cua_hang_ten)

        # Sắp xếp theo tên hoặc giá
        ordering = request.query_params.get('ordering')
        if ordering in ['ten', '-ten', 'gia', '-gia']:
            queryset = queryset.order_by(ordering)

        # Trả về kết quả không phân trang
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class GioHangViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = GioHang.objects.all()
    serializer_class = serializers.GioHangSerializer

    def create(self, request, *args, **kwargs):
        user = request.user

        # Kiểm tra xem người dùng đã có giỏ hàng chưa
        gio_hang, created = GioHang.objects.get_or_create(nguoi_dung=user)

        product_data = request.data.get('san_pham', [])  # Danh sách sản phẩm (danh sách dict)

        for item in product_data:
            san_pham_id = item.get('san_pham')  # ID sản phẩm
            so_luong = item.get('so_luong', 1)  # Số lượng sản phẩm

            try:
                san_pham = SanPham.objects.get(id=san_pham_id)
            except SanPham.DoesNotExist:
                return Response({'detail': f'Sản phẩm {san_pham_id} không tồn tại'}, status=status.HTTP_400_BAD_REQUEST)

            # Kiểm tra số lượng sản phẩm
            if san_pham.so_luong_ton < so_luong:
                return Response({'detail': f'Số lượng sản phẩm {san_pham.ten} không đủ'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Thêm sản phẩm vào giỏ hàng
            SanPhamGioHang.objects.create(gio_hang=gio_hang, san_pham=san_pham, so_luong=so_luong, gia=san_pham.gia)

        # Cập nhật tổng tiền giỏ hàng
        gio_hang.tinh_tong_tien()

        return Response(serializers.GioHangSerializer(gio_hang).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        user = request.user

        # Lấy sản phẩm trong giỏ hàng cần xóa
        try:
            san_pham_gio_hang = SanPhamGioHang.objects.get(id=kwargs['pk'])
        except SanPhamGioHang.DoesNotExist:
            return Response({'detail': 'Sản phẩm trong giỏ hàng không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        # Kiểm tra xem sản phẩm này có thuộc giỏ hàng của người dùng không
        if san_pham_gio_hang.gio_hang.nguoi_dung != user:
            return Response({'detail': 'Bạn không có quyền xóa sản phẩm này'}, status=status.HTTP_403_FORBIDDEN)

        # Xóa sản phẩm trong giỏ hàng
        san_pham_gio_hang.delete()

        # Cập nhật lại tổng tiền của giỏ hàng sau khi xóa sản phẩm
        san_pham_gio_hang.gio_hang.tinh_tong_tien()

        return Response({'detail': 'Sản phẩm đã được xóa khỏi giỏ hàng'}, status=status.HTTP_204_NO_CONTENT)

class SanPhamGioHangViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = SanPhamGioHang.objects.all()
    serializer_class = serializers.SanPhamGioHangSerializer

class DonHangViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = DonHang.objects.all()
    serializer_class = serializers.DonHangSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        product_data = request.data
        phuong_thuc_thanh_toan = product_data.get('phuong_thuc_thanh_toan')

        # Trường hợp thanh toán ngay cho sản phẩm trong giỏ hàng
        if 'san_pham' in product_data and 'so_luong' in product_data:
            san_pham_id = product_data.get('san_pham')
            so_luong = product_data.get('so_luong', 1)

            try:
                san_pham = SanPham.objects.get(id=san_pham_id)
            except SanPham.DoesNotExist:
                return Response({'detail': 'Sản phẩm không tồn tại'}, status=status.HTTP_400_BAD_REQUEST)

            # Kiểm tra số lượng sản phẩm
            if san_pham.so_luong_ton < so_luong:
                return Response({'detail': 'Số lượng sản phẩm không đủ'}, status=status.HTTP_400_BAD_REQUEST)

            # Tạo đơn hàng cho sản phẩm được chọn
            don_hang = DonHang.objects.create(
                nguoi_dung=user,
                phuong_thuc_thanh_toan=phuong_thuc_thanh_toan,
                tong_tien=san_pham.gia * so_luong
            )

            # Thêm sản phẩm vào đơn hàng
            SanPhamDonHang.objects.create(
                don_hang=don_hang,
                san_pham=san_pham,
                so_luong=so_luong,
                gia=san_pham.gia
            )

            # Cập nhật thống kê doanh thu
            ThongKeDoanhThu.objects.create(
                cua_hang=san_pham.cua_hang,  # Lấy cửa hàng của sản phẩm
                danh_muc=san_pham.danh_muc,  # Lấy danh mục của sản phẩm
                san_pham=san_pham,
                so_luong=so_luong,
                gia=san_pham.gia,
                ngay_thanh_toan=don_hang.ngay_tao,
                tong_doanh_thu=san_pham.gia * so_luong
            )

            # Cập nhật thống kê sản phẩm của đơn hàng
            ThongKeDonHangVaSanPhamCuaHang.objects.create(
                don_hang=don_hang,
                san_pham=san_pham,
                cua_hang=san_pham.cua_hang,
                so_luong=so_luong,
                gia=san_pham.gia,
                ngay_dat_hang=don_hang.ngay_tao
            )

            return Response(serializers.DonHangSerializer(don_hang).data, status=status.HTTP_201_CREATED)

        # Trường hợp thanh toán cho giỏ hàng
        try:
            gio_hang = GioHang.objects.get(nguoi_dung=user)
        except GioHang.DoesNotExist:
            return Response({'detail': 'Giỏ hàng không tồn tại'}, status=status.HTTP_400_BAD_REQUEST)

        # Lấy các sản phẩm trong giỏ hàng
        san_pham_gio_hang = gio_hang.san_pham.all()

        # Kiểm tra nếu giỏ hàng trống
        if not san_pham_gio_hang:
            return Response({'detail': 'Giỏ hàng của bạn không có sản phẩm'}, status=status.HTTP_400_BAD_REQUEST)

        # Tính tổng tiền của giỏ hàng
        tong_tien = gio_hang.tong_tien

        # Tạo đơn hàng cho toàn bộ giỏ hàng
        don_hang = DonHang.objects.create(
            nguoi_dung=user,
            phuong_thuc_thanh_toan=phuong_thuc_thanh_toan,
            tong_tien=tong_tien
        )

        # Thêm tất cả sản phẩm trong giỏ hàng vào đơn hàng và cập nhật thống kê
        for item in san_pham_gio_hang:
            # Thêm sản phẩm vào đơn hàng
            SanPhamDonHang.objects.create(
                don_hang=don_hang,
                san_pham=item.san_pham,
                so_luong=item.so_luong,
                gia=item.gia
            )

            # Cập nhật thống kê doanh thu
            ThongKeDoanhThu.objects.create(
                cua_hang=item.san_pham.cua_hang,
                danh_muc=item.san_pham.danh_muc,
                san_pham=item.san_pham,
                so_luong=item.so_luong,
                gia=item.gia,
                ngay_thanh_toan=don_hang.ngay_tao,
                tong_doanh_thu=item.gia * item.so_luong
            )

            # Cập nhật thống kê sản phẩm của đơn hàng
            ThongKeDonHangVaSanPhamCuaHang.objects.create(
                don_hang=don_hang,
                san_pham=item.san_pham,
                cua_hang=item.san_pham.cua_hang,
                so_luong=item.so_luong,
                gia=item.gia,
                ngay_dat_hang=don_hang.ngay_tao
            )

        # Đánh dấu giỏ hàng là đã thanh toán và xóa giỏ hàng
        gio_hang.delete()

        return Response(serializers.DonHangSerializer(don_hang).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        user = request.user

        # Lấy đơn hàng cần hủy theo id (pk) từ URL
        try:
            don_hang = DonHang.objects.get(id=kwargs['pk'])
        except DonHang.DoesNotExist:
            return Response({'detail': 'Đơn hàng không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        # Kiểm tra xem đơn hàng có thuộc về người dùng hiện tại không
        if don_hang.nguoi_dung != user:
            return Response({'detail': 'Bạn không có quyền hủy đơn hàng này'}, status=status.HTTP_403_FORBIDDEN)

        # Kiểm tra trạng thái thanh toán, nếu đã thanh toán thì không thể hủy
        if don_hang.da_thanh_toan:
            return Response({'detail': 'Không thể hủy đơn hàng đã thanh toán'}, status=status.HTTP_400_BAD_REQUEST)

        # Tiến hành hủy đơn hàng
        don_hang.delete()

        # Trả về thông báo thành công
        return Response({'detail': 'Đơn hàng đã được hủy'}, status=status.HTTP_204_NO_CONTENT)

class SanPhamDonHangViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = SanPhamDonHang.objects.all()
    serializer_class = serializers.SanPhamDonHangSerializer

# Danh gia san pham
class DanhGiaSanPhamViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = DanhGiaSanPham.objects.all()
    serializer_class = serializers.DanhGiaSanPhamSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def tao_danh_gia(self, serializer):
        san_pham_id = self.request.data.get('san_pham')
        san_pham = get_object_or_404(SanPham, id=san_pham_id)
        # Kiểm tra nếu người dùng đã mua sản phẩm mới được đánh giá
        serializer.save(nguoi_dung=self.request.user, san_pham=san_pham)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def cap_nhat_danh_gia(self, request, pk=None):
        danh_gia = get_object_or_404(DanhGiaSanPham, pk=pk, nguoi_dung=request.user)
        serializer = self.get_serializer(danh_gia, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def xoa_danh_gia(self, request, pk=None):
        danh_gia = get_object_or_404(DanhGiaSanPham, pk=pk, nguoi_dung=request.user)
        danh_gia.delete()
        return Response({'message': 'Đã xoá đánh giá'}, status=status.HTTP_204_NO_CONTENT)

# Danh gia nguoi ban
class DanhGiaNguoiBanViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = DanhGiaNguoiBan.objects.all()
    serializer_class = serializers.DanhGiaNguoiBanSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def tao_danh_gia(self, serializer):
        nguoi_ban_id = self.request.data.get('nguoi_ban')
        nguoi_ban = get_object_or_404(CuaHang, id=nguoi_ban_id)
        serializer.save(nguoi_dung=self.request.user, nguoi_ban=nguoi_ban)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def cap_nhat_danh_gia(self, request, pk=None):
        danh_gia = get_object_or_404(DanhGiaNguoiBan, pk=pk, nguoi_dung=request.user)
        serializer = self.get_serializer(danh_gia, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def xoa_danh_gia(self, request, pk=None):
        danh_gia = get_object_or_404(DanhGiaNguoiBan, pk=pk, nguoi_dung=request.user)
        danh_gia.delete()
        return Response({'message': 'Đã xoá đánh giá'}, status=status.HTTP_204_NO_CONTENT)

class TinNhanViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = TinNhan.objects.all()
    serializer_class = serializers.TinNhanSerializer

class ThongKeDoanhThuViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = ThongKeDoanhThu.objects.all()
    serializer_class = serializers.ThongKeDoanhThuSerializer

class ThongKeDonHangVaSanPhamViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = ThongKeDonHangVaSanPhamCuaHang.objects.all()
    serializer_class = serializers.ThongKeDonHangVaSanPhamSerializer