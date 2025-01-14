from stores.models import *
from rest_framework import serializers


class NguoiDungSerializer(serializers.ModelSerializer):

    class Meta:
        model  = NguoiDung
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'gioi_tinh', 'avatar', 'vai_tro']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()

        user = NguoiDung(**data)
        user.set_password(data['password'])
        user.save()

        return user

class CuaHangSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuaHang
        fields = '__all__'

class SanPhamSerializer(serializers.ModelSerializer):
    anh_san_pham = serializers.SerializerMethodField(source='anh_san_pham')

    def get_anh_san_pham(self, pro):

        if pro.anh_san_pham:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri('/static/%s' % pro.anh_san_pham.name)
            return '/static/%s' % pro.anh_san_pham.name

    class Meta:
        model = SanPham
        fields = '__all__'

class DonHangSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonHang
        fields = '__all__'

class GioHangSerializer(serializers.ModelSerializer):
    class Meta:
        model = GioHang
        fields = '__all__'

class SanPhamGioHangSerializer(serializers.ModelSerializer):
    class Meta:
        model = SanPhamGioHang
        fields = '__all__'

class DanhGiaSanPhamSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanhGiaSanPham
        fields = '__all__'

class DanhGiaNguoiBanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanhGiaNguoiBan
        fields = '__all__'

class SanPhamDonHangSerializer(serializers.ModelSerializer):
    class Meta:
        model = SanPhamDonHang
        fields = '__all__'

class DanhMucSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanhMuc
        fields = '__all__'

class TinNhanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TinNhan
        fields = '__all__'

class ThongKeDonHangVaSanPhamSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThongKeDonHangVaSanPhamCuaHang
        fields = '__all__'