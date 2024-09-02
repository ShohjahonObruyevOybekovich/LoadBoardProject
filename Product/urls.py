from django.urls import path
from .views import (
    UserMonthView, UserYearView, DeleteUserYearProductView, ProductListView,
    UploadExcelAPIView, ProductUpdateView, DownloadExcelAllAPIView,
    DownloadExcelFilteredAPIView
)

urlpatterns = [
    path('user_month/<uuid:uuid>/', UserMonthView.as_view(), name='user-month'),
    path('user_year/<uuid:uuid>/', UserYearView.as_view(), name='user-year'),
    path('users/<uuid:uuid>/delete_year_item/<int:product_id>/', DeleteUserYearProductView.as_view(), name='delete-year-product'),

    path('product-list/',ProductListView.as_view(), name='product-list'),
    path('product-update/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
    # path('product-delete/,ProductDeleteView.as_view()',  name='product-delete'),

    path('upload-excel/', UploadExcelAPIView.as_view(), name='upload-excel'),
    path('download-excel-all-info/<uuid:uuid>/', DownloadExcelAllAPIView.as_view(), name='download-excel'),
    path("download-excel-filter/<uuid:uuid>/", DownloadExcelFilteredAPIView.as_view(), name="download-excel-filter"),
]
