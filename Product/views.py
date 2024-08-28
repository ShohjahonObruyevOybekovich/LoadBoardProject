from symtable import Class

import pandas as pd
from django.utils import timezone
from django.views.generic import DeleteView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404, UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .Djangofilters import ProductFilter
from .models import CustomUser, Product
from .serializers import ProductSerializer


class UserMonthView(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        user = get_object_or_404(CustomUser, uuid=self.kwargs['uuid'])
        return user.products.filter(date__month=timezone.now().month)


class UserYearView(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        user = get_object_or_404(CustomUser, uuid=self.kwargs['uuid'])
        return user.products.filter(date__year=timezone.now().year)



class DeleteUserYearProductView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def delete(self, request, uuid, product_id):
        user = get_object_or_404(CustomUser, uuid=uuid)
        product = get_object_or_404(Product, id=product_id, user=user)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class ProductCreateAPIView(CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()


class ProductListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication,]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class ProductUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

# class ProductDeleteView(DeleteView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()
#

from django.http import HttpResponse, HttpResponseBadRequest
import io


class UploadExcelAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if not request.FILES.get('file'):
            return HttpResponseBadRequest("No file uploaded")

        file = request.FILES['file']
        try:
            df = pd.read_excel(file)

            # Validate required columns
            required_columns = {
                'title', 'places', 'view', 'cube', 'kg', 'cube_kg', 'price',
                'payment', 'debt', 'where_from', 'date', 'transport',
                'current_place', 'status', 'user_id'
            }
            if not required_columns.issubset(df.columns):
                return HttpResponseBadRequest("Invalid file format. Required columns are missing.")

            # Process data and create/update products
            for _, row in df.iterrows():
                user_id = row.get('user_id')
                try:
                    user = CustomUser.objects.get(id=user_id)
                except CustomUser.DoesNotExist:
                    continue  # Skip rows with invalid user_id

                Product.objects.update_or_create(
                    title=row.get('title'),
                    user=user,
                    defaults={
                        'places': row.get('places'),
                        'view': row.get('view'),
                        'cube': row.get('cube'),
                        'kg': row.get('kg'),
                        'cube_kg': row.get('cube_kg'),
                        'price': row.get('price'),
                        'payment': row.get('payment'),
                        'debt': row.get('debt'),
                        'where_from': row.get('where_from'),
                        'date': row.get('date'),
                        'transport': row.get('transport'),
                        'current_place': row.get('current_place'),
                        'status': row.get('status'),
                    }
                )
            return Response({"status": "success", "message": "File processed successfully"})
        except Exception as e:
            return HttpResponseBadRequest(f"Error processing file: {str(e)}")


class DownloadExcelAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Fetch products from the database
        products = Product.objects.all().values(
            'title', 'places', 'view', 'cube', 'kg', 'cube_kg', 'price',
            'payment', 'debt', 'where_from', 'date', 'transport',
            'current_place', 'status', 'user_id'
        )
        df = pd.DataFrame(products)

        # Create an Excel file
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Products')

        buffer.seek(0)
        response = HttpResponse(
            buffer,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={'Content-Disposition': 'attachment; filename="products.xlsx"'}
        )
        return response