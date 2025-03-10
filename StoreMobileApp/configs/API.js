import axios from "axios";

const HOST = 'https://duydal.pythonanywhere.com';  // Địa chỉ IP máy tính của bạn

export const endpoints = {
    'cua-hang': '/cua-hang/',
    'danh-muc': '/danh-muc/',
    'danhgia-nguoiban': '/danhgia-nguoiban/',
    'danhgia-sanpham': '/danhgia-sanpham/',
    'don-hang': '/don-hang/',
    'gio-hang': '/gio-hang/',
    'nguoi-dung': '/nguoi-dung/',
    'san-pham': '/san-pham/',
    'sanpham-donhang': '/sanpham-donhang/',
    'sanpham-giohang': '/sanpham-giohang/',
    'tin-nhan': '/tin-nhan/',
    'login': '/o/token/'
}

export const authApi = () => {
    return axios.create({
        baseURL: HOST,
        headers: {
            'Authorization': `Bearer ...`
        }
    })
}

export default axios.create({
    baseURL: HOST
})
