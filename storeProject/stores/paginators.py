from rest_framework.pagination import PageNumberPagination


class SanPhamPaginator(PageNumberPagination):
    page_size = 20